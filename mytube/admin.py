from django.contrib import admin
from mytube.models import Genre, Movie, UserProfile
from embed_video.admin import AdminVideoMixin


class MovieAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'genre', 'video')

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserProfile)
