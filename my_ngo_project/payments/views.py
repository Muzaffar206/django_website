import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ngo_app.models import Donor, Donation
from django.db.models import Q
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def create_razorpay_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(float(data.get('amount', 0)) * 100)  # Convert rupees to paise
            
            donor_data = {
                'surname': data.get('surname', ''),
                'first_name': data.get('firstName', ''),  # Make sure this matches the form field name
                'middle_name': data.get('middleName', ''),  # Make sure this matches the form field name
                'pan_no': data.get('panNo', ''),  # Make sure this matches the form field name
                'email': data.get('email', ''),
                'mobile': data.get('mobile', ''),
                'dofficial': data.get('dofficial', ''),
                'address': data.get('address', ''),
                'city': data.get('city', ''),
                'country': data.get('country', ''),
                'state': data.get('state', ''),
                'pincode': data.get('pincode', ''),
            }
            
            print("Donor data received:", donor_data)  # Add this line for debugging
            
            donor = Donor.objects.filter(
                Q(email=donor_data['email']) | Q(mobile=donor_data['mobile'])
            ).first()

            if donor:
                for key, value in donor_data.items():
                    setattr(donor, key, value)  # Update all fields, even if empty
                donor.save()
            else:
                donor = Donor.objects.create(**donor_data)

            print("Donor after save:", donor.__dict__)  # Add this line for debugging

            if request.user.is_authenticated and not donor.user:
                donor.user = request.user
                donor.save()

            razorpay_order = razorpay_client.order.create(dict(
                amount=amount,
                currency='INR',
                payment_capture='0'
            ))

            donation, created = Donation.objects.get_or_create(
                razorpay_order_id=razorpay_order['id'],
                defaults={
                    'donor': donor,
                    'amount': amount / 100,
                    'purpose': data.get('purpose', ''),
                    'is_zakat': data.get('is_zakat') == 'yes',
                    'notes': data.get('notes', ''),
                }
            )

            if not created:
                donation.amount = amount / 100
                donation.purpose = data.get('purpose', '')
                donation.is_zakat = data.get('is_zakat') == 'yes'
                donation.notes = data.get('notes', '')
                donation.save()
                
            return JsonResponse({
                'order_id': razorpay_order['id'],
                'amount': amount,
                'currency': 'INR',
            })
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({'error': f'Razorpay BadRequestError: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Error in create_razorpay_order: {str(e)}")  # Add this line for debugging
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def razorpay_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            params_dict = {
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_signature': data.get('razorpay_signature')
            }
            try:
                donation = Donation.objects.get(razorpay_order_id=params_dict['razorpay_order_id'])
            except Donation.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': "Donation does not exist"})
            except Donation.MultipleObjectsReturned:
                # Log this error and handle it gracefully
                logger.error(f"Multiple donations found for order_id: {params_dict['razorpay_order_id']}")
                return JsonResponse({'status': 'error', 'message': "Multiple donations found for this order"})
            
            try:
                result = razorpay_client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'status': 'error', 'message': 'Invalid payment signature'})

            if result:
                amount = int(donation.amount * 100)  # Convert to paise
                try:
                    razorpay_client.payment.capture(params_dict['razorpay_payment_id'], amount)
                    donation.razorpay_payment_id = params_dict['razorpay_payment_id']
                    donation.paid = True
                    donation.save()
                    return JsonResponse({'status': 'success', 'message': 'Payment successful'})
                except razorpay.errors.BadRequestError as e:
                    return JsonResponse({'status': 'error', 'message': f'Payment capture failed: {str(e)}'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid payment signature'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON in request body'})
        except Exception as e:
            logger.error(f"Unexpected error in razorpay_callback: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Error processing payment: {str(e)}'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})