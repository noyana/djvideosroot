from django.db import models
from django.db.models import F, Subquery, OuterRef
import os
import ffmpeg
import re
import fnmatch
from datetime import datetime, timedelta
from django.utils import timezone
from djvideosroot.settings import BASE_DIR, UNPOPULAR_COUNT

# Create your models here.


class Category(models.Model):
    """"
    Category for all models
    """

    RAW = 'R'
    ALL = 'A'
    POP = 'P'
    UNP = 'U'
    BIS = 'B'
    MOV = 'M'
    HJB = 'H'
    CATEGORIES = [
        (ALL, 'All'),
        (BIS, 'LGBT'),
        (MOV, 'Movie'),
        (HJB, 'Hijab'),
        (POP, 'Popular'),
        (RAW, 'Raw'),
        (UNP, 'Unpopular'),
    ]
    name = models.CharField(max_length=1, unique=True, blank=False, choices=CATEGORIES, default=RAW)
    full_name = models.CharField(max_length=50, unique=True, blank=False)

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.full_name


class Video(models.Model):
    """ Video record """

    full_path = models.FilePathField(unique=True, allow_files=True, allow_folders=False)
    name = models.CharField(unique=True, max_length=100)
    file_size = models.PositiveBigIntegerField(null=False, default=0)
    file_date = models.DateTimeField()
    duration = models.DurationField(null=False)
    file_count = models.PositiveIntegerField(null=True)
    is_movie = models.BooleanField(default=False)
    width = models.IntegerField(default=840, null=False)
    height = models.IntegerField(default=480, null=False)
    frame_rate = models.FloatField(default=23.96)
    video_bitrate = models.FloatField(default=768)
    audio_bitrate = models.FloatField(default=128)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_DEFAULT, default=2)  # default is Ordinary
    tags = models.ManyToManyField('Tag', blank=True)
    artists = models.ManyToManyField('Artist', blank=True)

    class Meta:
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_movie', 'name']),
            models.Index(fields=['file_size'])
        ]

    @property
    def url_path(self):
        cat = self.category.full_name
        return "%s/%s" % (cat, self.name)

    def __str__(self):
        return self.name + " " + str(self.file_count)

    def get_extension(self):
        """ get file extension from file name """
        name, ext = os.path.splitext(self.full_path)
        return ext

    def get_if_movie(self):
        """ return if file is a movie"""
        name = os.path.splitext(os.path.split(self.full_path)[1])[0]
        return '_' == name[0]

    def if_deleted(self):
        """ return if folder exists but file deleted """
        if not os.path.exists(self.full_path):
            if not os.path.isdir(os.path.split(self.full_path)[0]):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def add_videos_from_folder(folder):
        for video_name in fnmatch.filter(os.listdir(folder.name), '*.mp4'):
            v = Video()
            people = v.read_from_file(file_name="{folder}\{v_name}".format(folder=folder.name, v_name=video_name), folder_id= folder.id)
            v.save()
            folder.videos.add(v)
            folder.save()
            if people:
                for pers in people:
                    try:
                        art = Artist.objects.get(name=pers)
                    except Artist.DoesNotExist:
                        art = None
                    if not art:
                        new_person = Artist(name=pers)
                        new_person.save()
                        new_person.videos.add(v)
                        new_person.video_count += 1
                        new_person.save()
                    else:
                        try:
                            prev = art.videos_set.first()
                        except Video.DoesNotExist:
                            prev = None
                        if not prev:
                            art.videos.add(v)
                            art.video_count += 1
                        art.save()

    def read_from_file(self, file_name, folder_id):
        people = []
        if os.path.isfile(file_name):
            self.full_path = file_name
            base_name = os.path.split(file_name)[1]
            self.name = base_name
            self.file_size = os.path.getsize(file_name)
            self.file_date = timezone.make_aware(datetime.fromtimestamp(os.path.getmtime(file_name)))
            # print("{} : {}".format(self.file_date, file_name))
            # base_with_path = os.path.splitext(file_name)[0]
            movies = re.compile(r'_(.+)_(,\s*([SsCcDd]{2})(.+)\s*)*.mp4')
            movie_search = movies.match(base_name)
            if movie_search:
                self.is_movie = True
                if movie_search.group(2):
                    self.name = movie_search.group(1) + movie_search.group(2)
                else:
                    self.name = movie_search.group(1)
                if movie_search.group(4):
                    self.file_count = int(movie_search.group(4))
                else:
                    self.file_count = 1
            else:
                self.is_movie = False
                c_reg = re.compile(r'.*\((\d+)\)\s*\.mp4')
                c = c_reg.search(base_name)
                if c:
                    self.file_count = int(c.group(1))
                else:
                    self.file_count = 1
                c_rep = re.compile(r'\s*(\(\s*\d+\s*\))*\.mp4')
                base_name_no_count = c_rep.sub("", base_name)
                p = re.compile(r'\s*,\s*')
                people = p.split(base_name_no_count)
        try:
            vid = Video.objects.get(file_size=self.file_size)
        except Video.DoesNotExist:
            vid = None
        if not vid:
            try:
                probe = ffmpeg.probe(file_name)
                video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                self.width = int(video_stream['width'])
                self.height = int(video_stream['height'])
                self.duration = timedelta(seconds=float(video_stream['duration']))
                self.frame_rate = float(eval(video_stream['r_frame_rate']))
            except ffmpeg.Error:
                self.width = 0
                self.height = 0
                self.duration = 0
                self.frame_rate = 0
                self.name = "DELETE {}".format(self.name)
        else:
            self = vid

        self.save()
        return people

GENDERS = [
    ('F', 'Female'),
    ('T', 'Trans'),
    ('M', 'Male'),
    ('B', 'Bi')
]


class Artist(models.Model):
    """ Artists acted on movie"""

    name = models.CharField(max_length=255, null=False)
    gender = models.CharField(max_length=1, choices=GENDERS, default='F')
    video_count = models.IntegerField(default=0, null=False)
    videos = models.ManyToManyField('Video', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default= 2)

    class Meta:
        ordering = ['-video_count', 'name']

    def __str__(self):
        if int(self.video_count) > 1:
            return "{name} ({gender}) - {count}".format(name=self.name, gender=self.gender, count=self.videos.count())
        else:
            return "{name} ({gender}) - new!".format(name=self.name, gender=self.gender)

    def correct_video_count(self):
        self.video_count = 0
        for v in self.videos.all():
            if v.if_deleted():
                self.videos.remove(v)
            else:
                self.video_count += 1
        self.save()

    def save_model(self, request, obj, form, change):
        if change:
            if self.video_count <= UNPOPULAR_COUNT:
                self.category = Category(full_name="Unpopular")
            super(Artist, self).save_model(request, obj, form, change)


class Tag(models.Model):
    """ Tags of videos """

    TAGGER = '#'
    name = models.CharField(max_length=50, null=False, unique=True)
    text = models.CharField(max_length=4, default='new', null=False, unique=True)
    video_count = models.IntegerField(default=0)
    videos = models.ManyToManyField(Video, blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.SET_DEFAULT, default=2)  # default is Ordinary

    def __str__(self):
        return self.name + "(#" + self.text + ")"


class Folder(models.Model):
    """ Folders for files """

    name = models.CharField(max_length=400, unique=True)
    video_count = models.IntegerField(default=0)
    videos = models.ManyToManyField(Video, blank=True )
    category = models.ForeignKey(Category, blank=False, on_delete=models.SET_DEFAULT, default=1)  # default is RAW

    def __str__(self):
        return f"{self.name} - {self.category.full_name}: ({self.video_count} videos)"

    def search_file(self, filename):
        return os.path.isfile(self.name + os.pathsep + filename)

    def update_count(self):
        self.video_count = len(fnmatch.filter(os.listdir(self.name), '*.mp4'))
        self.save()
        return self.video_count

    def add_videos(self):
        if self.category.full_name != 'Raw':
            Video.add_videos_from_folder(self)
