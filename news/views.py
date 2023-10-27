from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import News
from .serializers import NewsSerializer, NewsDetailSerializer
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


# Create your views here.


class NewsPagination(PageNumberPagination):
    page_size = 10


class NewsListApiView(ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_active=True).order_by('-published_at')
    pagination_class = NewsPagination


class NewsDetailApiView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer


@api_view(['POST'])
def like_news(request, pk):
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        token_string = auth_header.split(' ')[1]
    else:
        return Response({"detail": "Authorization header not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = Token.objects.get(key=token_string)
        request.user = token.user
    except Token.DoesNotExist:
        return Response({"detail": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    news = get_object_or_404(News, pk=pk)
    print(news)

    if request.user in news.dislikes.all():
        news.dislikes.remove(request.user)

    news.likes.add(request.user)
    news.save()

    return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def dislike_news(request, pk):
    auth_header = request.headers.get('Authorization')

    if auth_header is not None:
        token_string = auth_header.split(' ')[1]
    else:
        return Response({"detail": "Authorization header not provided"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token = Token.objects.get(key=token_string)
        request.user = token.user
    except Token.DoesNotExist:
        return Response({"detail": "Token is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    news = get_object_or_404(News, pk=pk)
    if request.user in news.likes.all():
        news.likes.remove(request.user)
    news.dislikes.add(request.user)
    news.save()
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
