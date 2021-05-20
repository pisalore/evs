from django.contrib import admin
from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView
from core.views import IndexTemplateView


from users.forms import EvUserForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/register/",
         RegistrationView.as_view(
             form_class=EvUserForm,
             success_url="/"
         ), name='django_registration_register'),

    path("accounts/", include('django_registration.backends.one_step.urls')),
    path("accounts/", include('django.contrib.auth.urls')),

    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")
]
