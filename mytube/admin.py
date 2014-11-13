from django.contrib import admin
from mytube.models import Genre, Movie, UserProfile


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'url')

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserProfile)