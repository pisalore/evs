from django.urls import path
from users.api.views import ContactUsAPIView, CurrentUserAPIView, UserProfileAPIView, ProfileImageUpdateView

urlpatterns = [
    path("profile-image/", ProfileImageUpdateView.as_view(), name="profile-image"),
    path("user/", CurrentUserAPIView.as_view(), name="current-user"),
    path("user/<str:username>/", UserProfileAPIView.as_view(), name="user-profile"),
    path("contactus/", ContactUsAPIView.as_view(), name="contact-us")
]
