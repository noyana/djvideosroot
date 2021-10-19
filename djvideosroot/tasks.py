# core/tasks.py
from celery import shared_task
from  videos.models import Folder, Video, Artist, Tag


@shared_task
def add(x, y):
    return x + y


@shared_task
def folder_add_videos(folder_id):
    f = Folder.objects


@shared_task
def add_new_videos():
    pass


