from django import forms
from mytube.models import Genre, Movie
from django.contrib.auth.models import User
#from mytube.models import UserProfile
from datetime import datetime

class GenreForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the genre name.")
    class Meta:
        model = Genre

class MovieForm(forms.ModelForm):

    title = forms.CharField(max_length=128, help_text="Please enter the title of the movie.")
    #year = forms.DateTimeField(datetime.year, help_text="Please enter the year of the movie.")
    pg = forms.IntegerField(help_text="Please enter pg level of the movie.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the youtube page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Movie
        # fields = ('title', 'year', 'pg', 'url', 'views', 'likes')
        fields = ('title', 'pg', 'url', 'views', 'likes')

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     url = cleaned_data.get('url')
    #
    #     if url and not url.startswith('http://') and not url.startswith('https://'):
    #         url = 'http://' + url
    #         cleaned_data['url'] = url
    #
    #     return cleaned_data

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

