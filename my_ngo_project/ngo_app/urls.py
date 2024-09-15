from django.urls import path
from . import views
from allauth.account.views import ConfirmEmailView
from ngo_app.views import CustomPasswordResetView, CustomConfirmEmailView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about/mesco-at-glance/', views.about_glance, name='about_glance'),
    path('about/managing-committee/', views.managing_committee, name='managing_committee'),
    path('about/good-governance/', views.good_governance, name='good_governance'),
    path('about/mesco-education-society/', views.mesco_education_society, name='mesco_education_society'),
    path('about/angels-paradise-nursery/', views.angels_paradise_nursery, name='angels_paradise_nursery'),
    path('about/vocational-training/', views.vocational_training, name='vocational_training'),
    path('about/ecce/', views.ecce, name='ecce'),

    path('our-work/', views.our_work, name='our_work'),
    path('our-work/educational-support/', views.educational_support, name='educational_support'),
    path('our-work/medical-aid/', views.medical_aid, name='medical_aid'),
    path('our-work/clinics-dispensaries/', views.clinics_dispensaries, name='clinics_dispensaries'),
    path('our-work/school-adoption/', views.school_adoption, name='school_adoption'),
    path('our-work/newspaper-units/', views.newspaper_units, name='newspaper_units'),

    path('media/', views.media, name='media'),
    path('media/in-media/', views.in_media, name='in_media'),
    path('media/image-gallery/', views.image_gallery, name='image_gallery'),
    path('media/video-gallery/', views.video_gallery, name='video_gallery'),
    path('media/newsletters/', views.newsletters, name='newsletters'),
    path('media/annual-reports/', views.annual_reports, name='annual_reports'),
    path('media/success-stories/', views.success_stories, name='success_stories'),
    path('media/donor-testimonials/', views.donor_testimonials, name='donor_testimonials'),
    path('blog/', views.blog, name='blog'),

    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('donate/', views.donate, name='donate'),

    path('accounts/login/', views.login, name='account_login'),
    path('accounts/signup/', views.custom_signup_view, name='account_signup'),
    path('accounts/logout/', views.custom_logout, name='account_logout'),
    path('accounts/confirm-email/', CustomConfirmEmailView.as_view(), name='account_email_verification_sent'),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
  
]
