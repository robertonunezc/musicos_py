from django.urls import include, path
from django.contrib import admin
from contratar_musicos.main import views
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/password/', auth_views.PasswordResetView.as_view(
        template_name='registration/reset.html',
        email_template_name='registration/reset_email.html',
        subject_template_name='registration/reset_subject.txt',
        success_url='/main/success/'
    )
         , name='reset'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('success/', views.success, name='success'),
    path('contacto/', views.contacto, name='contacto'),
    path('success/reset/', views.success_reset, name='success_reset'),
    path('confirmacion/email/<token>', views.confirmar_registro, name='confirmar_registro')
]
