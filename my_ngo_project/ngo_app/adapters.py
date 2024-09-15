from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if not email.endswith('@example.com'):  # Replace with your actual email validation logic
            super().send_mail(template_prefix, email, context)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            user = User.objects.get(email=user.email)
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass

    def is_auto_signup_allowed(self, request, sociallogin):
        email = sociallogin.email_addresses[0].email if sociallogin.email_addresses else None
        if email:
            try:
                user = User.objects.get(email=email)
                if user.socialaccount_set.exists():
                    return True
                else:
                    return False  # User exists but registered manually
            except User.DoesNotExist:
                return True  # New user, allow auto signup
        return False
