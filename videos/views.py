# from django.shortcuts import render
from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin
# from django.views.generic import UpdateView
# from django.views.generic import CreateView
# from django.core.paginator import Paginator
from djvideosroot.settings import global_filter
from .models import Artist, Video, Tag, Category, Folder
import celery
import django_celery_progressbar



# Create your views here.

class ArtistListView(ListView):
    """ Artists list paginated page """
    paginate_by = 4
    model = Artist

    def get_queryset(self):
        queryset = super(ArtistListView, self).get_queryset()
        if global_filter != "":
            if global_filter.lower() == "movie":
                queryset = queryset.filter(video__is_movie=True)
            else:
                queryset = Artist.objects.filter(Q(name__icontains=global_filter) |
                                                 Q(category__full_name__icontains=global_filter))
        return queryset


class ArtistDetailView(DetailView, MultipleObjectMixin):
    model = Artist
    paginate_by = 4

    def get_queryset(self):
        queryset = super(ArtistDetailView, self).get_queryset()
        if global_filter != "":
            if global_filter.lower() == "movie":
                queryset = queryset.filter(video__is_movie=True)
            else:
                queryset = Artist.objects.filter(Q(name__icontains=global_filter) |
                                                 Q(category__full_name__icontains=global_filter))
        return queryset

    def get_context_data(self, **kwargs):
        object_list = Video.objects.filter(artist=self.get_object()).order_by('-file_date')
        context = super(ArtistDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class FolderListView(ListView):
    """ Folders list paginated page """
    paginate_by = 3
    model = Folder

    def get_queryset(self):
        queryset = super(FolderListView, self).get_queryset()
        if global_filter != "":
            if global_filter.lower() == "movie":
                queryset = queryset.filter(video__is_movie=True)
            else:
                queryset = Folder.objects.filter(Q(name__icontains=global_filter) |
                                             Q(category__full_name__icontains=global_filter))
        return queryset


class FolderDetailView(DetailView, MultipleObjectMixin):
    model = Folder
    paginate_by = 3

    def get_queryset(self):
        queryset = super(FolderDetailView, self).get_queryset()
        if global_filter != "":
            if global_filter.lower() == "movie":
                queryset = queryset.filter(video__is_movie=True)
            else:
                queryset = Folder.objects.filter(Q(name__icontains=global_filter) |
                                                  Q(category__full_name__icontains=global_filter))
        return queryset

    def get_context_data(self, **kwargs):
        object_list = Video.objects.filter(artist=self.get_object()).order_by('-file_date')
        context = super(ArtistDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context



class ProcessAll(RedirectView):
    pass


class IndexView(TemplateView):
    """Home page view """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if global_filter:
            context['video'] = Video.objects.filter(Q(name__icontains=global_filter) |
                                                    Q(full_path__icontains=global_filter |
                                                                           Q(category__full_name__icontains=global_filter))).count()
            context['artist'] = Artist.objects.filter(Q(name__icontains=global_filter) |
                                                      Q(category__full_name__icontains=global_filter)).count()
            context['folder'] = Folder.objects.filter(Q(name__icontains=global_filter) |
                                                      Q(category__full_name__icontains=global_filter)).count()
            context['tag'] = Tag.objects.filter(Q(name__icontains=global_filter) |
                                                Q(category__full_name__icontains=global_filter)).count()
            context['category'] = Category.objects.filter(Q(name__icontains=global_filter) |
                                                          Q(category__full_name__icontains=global_filter)).count()
            if global_filter.lower() == "movie":
                self.queryset = self.queryset.filter(video__is_movie=True)
                context['category'] = Category.objects.filter(Q(name__icontains=global_filter) |
                                                              Q(category__full_name__icontains=global_filter)).count()
        else:
            context['video'] = Video.objects.all().count()
            context['artist'] = Artist.objects.all().count()
            context['folder'] = Folder.objects.all().count()
            context['tag'] = Tag.objects.all().count()
            context['category'] = Category.objects.all().count()
        return context
