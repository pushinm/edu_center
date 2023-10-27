from django.urls import path
from .views import NewsListApiView, NewsDetailApiView, like_news, dislike_news

urlpatterns = [
    path('news/', NewsListApiView.as_view(), name='news-list-api'),
    path('news/<int:pk>/', NewsDetailApiView.as_view(), name='detail_news'),
    path('news/<int:pk>/like/', like_news, name='like'),
    path('news/<int:pk>/dislike/', dislike_news, name='dislike'),
]
