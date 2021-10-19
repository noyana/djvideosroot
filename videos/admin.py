from django.contrib import admin
from .models import Artist, Video, Tag, Category, Folder

# Register your models here.
admin.site.register(Video)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Folder)

@admin.action(description='Change category to Raw')
def make_raw(modeladmin, request, queryset):
    queryset.update(category=1)

@admin.action(description='Change category to LGBT')
def make_lgbt(modeladmin, request, queryset):
    queryset.update(category=3)

@admin.action(description='Change category to Popular')
def make_popular(modeladmin, request, queryset):
    queryset.update(category=6)

@admin.action(description='Change category to Unpopular')
def make_unpopular(modeladmin, request, queryset):
    queryset.update(category=7)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'video_count']
    ordering = ['-video_count', 'name']
    actions = [make_raw, make_lgbt, make_popular, make_unpopular]

admin.site.register(Artist, ArtistAdmin)
