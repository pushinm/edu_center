from django.urls import path
from .views import RegisterAPIView, CustomAuthToken, Logout, ActivateView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('logout/', Logout.as_view()),
    path('activate/<uidb64>/<token>',
         ActivateView.as_view(),
         name='activate'),
]