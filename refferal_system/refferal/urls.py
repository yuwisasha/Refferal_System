from django.urls import path

from .views import EntryAuthView, AuthView, UserProfileView

urlpatterns = [
    path("login/", EntryAuthView.as_view(), name="sign-in"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
