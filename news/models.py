from django.db import models
from django.conf import settings


def generate_images_upload_path(instance, photo):
    return f'files/images/{photo}'


def generate_video_upload_path(instance, video):
    return f'files/images/{video}'


class News(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    photo = models.ImageField(upload_to=generate_images_upload_path)
    video = models.FileField(upload_to=generate_video_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(verbose_name='', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes_of_news')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislikes_of_news')

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
