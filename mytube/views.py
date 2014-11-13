#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from mytube.models import Genre
from mytube.models import Movie, UserProfile
from mytube.forms import GenreForm, MovieForm
from mytube.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from mytube.bing_search import run_query
from django.contrib.auth.models import User
from django.shortcuts import redirect

def index(request):
    context = RequestContext(request)
    genre_list = Genre.objects.order_by('-likes')[:5]
    movie_list = Movie.objects.order_by('-views')[:5]

    genre_list = get_genre_list()
    context_dict = {'genres': genre_list, 'movies': movie_list}
    context_dict['genre_list'] = genre_list

    for genre in genre_list:
        genre.url = encode_url(genre.name)

    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visit'] = 1

    return render_to_response('mytube/index.html', context_dict, context)

    # response = render_to_response('mytube/index.html', context_dict, context)

    # visits = int(request.COOKIES.get('visits', '0'))

    # if 'last_visit' in request.COOKIES:
    #     last_visit = request.COOKIES['last_visit']
    #     last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    #
    #     if (datetime.now() - last_visit_time).seconds > 5:
    #         response.set_cookie('visits', visits + 1)
    #         response.set_cookie('last_visit', datetime.now())
    # else:
    #     response.set_cookie('visits', 1)
    #     response.set_cookie('last_visit', datetime.now())
    #
    # return response

def genre(request, genre_name_url):

    context = RequestContext(request)
    genre_name = decode_url(genre_name_url)
    context_dict = {'genre_name': genre_name,
                    'genre_name_url': genre_name_url}
    genre_list = get_genre_list()
    context_dict['genre_list'] = genre_list

    try:
        genre = Genre.objects.get(name=genre_name)
        movies = Movie.objects.filter(genre=genre).order_by('-views')
        context_dict['movies'] = movies
        context_dict['genre'] = genre
    except Genre.DoesNotExist:
        pass
        # return HttpResponse("This genre doesn't exist")

    # if request.method == 'POST':
    #
    #     query = request.POST['query'].strip()
    #     if query:
    #         result_list = run_query(query)
    #         context_dict['result_list'] = result_list
    return render_to_response('mytube/genre.html', context_dict, context)

def about(request):
    context = RequestContext(request)

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict = {'italicmsg': "about movie", 'visits': count}
    genre_list = get_genre_list()
    context_dict['genre_list'] = genre_list
    return render_to_response('mytube/about.html', context_dict, context)

def add_genre(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = GenreForm

    genre_list = get_genre_list()
    context_dict = {'genre_list': genre_list, 'form': form}

    return render_to_response('mytube/add_genre.html', context_dict, context)

def add_movie(request, genre_name_url):
    context = RequestContext(request)
    genre_name = decode_url(genre_name_url)

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)

            try:
                current_genre = Genre.objects.get(name=genre_name)
                movie.genre = current_genre
            except Genre.DoesNotExist:
                return render_to_response('mytube/add_genre.html', {}, context)

            movie.views = 0
            movie.likes = 0
            movie.save()

            return genre(request, genre_name_url)
        else:
            print(form.errors)
    else:
        form = MovieForm()

    genre_list = get_genre_list()
    context_dict = {'genre_name_url': genre_name_url,
         'genre_name': genre_name, 'form': form, 'genre_list': genre_list}
    return render_to_response('mytube/add_movie.html',context_dict, context)

def decode_url(genre_name_url):
    genre_name = genre_name_url.replace('_', ' ')
    return genre_name

def encode_url(genre_name):
    genre_name_url = genre_name.replace(' ', '_')
    return genre_name_url

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    genre_list = get_genre_list()
    context_dict = {'user_form': user_form,
                    'registered': registered, 'genre_list': genre_list}

    return render_to_response('mytube/register.html', context_dict,context)

def user_login(request):
    context = RequestContext(request)
    genre_list = get_genre_list()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        bad_details = False
        disabled_account = False
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/mytube/')
            else:
                disabled_account = True
                return render_to_response('mytube/login.html',
                                          {'disabled_account': disabled_account,'genre_list': genre_list}, context)
        else:
            bad_details = True
            return render_to_response('mytube/login.html', {'bad_details': bad_details,'genre_list': genre_list}, context)
    else:
        return render_to_response('mytube/login.html', {'genre_list': genre_list}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/mytube/')

@login_required
def profile(request):
    context = RequestContext(request)
    genre_list = get_genre_list()
    context_dict = {'genre_list': genre_list}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('mytube/profile.html', context_dict, context)

@login_required
def like_genre(request):
    context = RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['genre_id']

    likes = 0
    if cat_id:
        genre = Genre.objects.get(id=int(cat_id))
        if genre:
            likes = genre.likes + 1
            genre.likes =  likes
            genre.save()

    return HttpResponse(likes)

def search(request):
    context = RequestContext(request)
    genre_list = get_genre_list()
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render_to_response('mytube/search.html', {'result_list': result_list, 'genre_list': genre_list}, context)

def get_genre_list():
    genre_list = Genre.objects.all()

    for genre in genre_list:
        genre.url = encode_url(genre.name)

    return genre_list

def track_url(request):
    context = RequestContext(request)
    movie_id = None
    url = '/mytube/'
    if request.method == 'GET':
        if 'movie_id' in request.GET:
            movie_id = request.GET['movie_id']
            try:
                movie = Movie.objects.get(id=movie_id)
                movie.views = movie.views + 1
                movie.save()
                url = movie.url
            except:
                pass

    return redirect(url)

def get_genre_list(max_results=0, starts_with=''):
    genre_list = []
    if starts_with:
        genre_list = Genre.objects.filter(name__istartswith=starts_with)
    else:
        genre_list = Genre.objects.all()

    if max_results > 0:
        if len(genre_list) > max_results:
            genre_list = genre_list[:max_results]

    for genre in genre_list:
        genre.url = encode_url(genre.name)

    return genre_list

def suggest_genre(request):
    context = RequestContext(request)
    genre_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    genre_list = get_genre_list(8, starts_with)

    return render_to_response('mytube/genre_list.html', {'genre_list': genre_list }, context)