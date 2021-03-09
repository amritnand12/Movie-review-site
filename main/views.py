from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    allmovies = Movie.objects.all()
    
    context = {
        "movies": allmovies,
    }

    return render(request,'main/index.html', context)
    
def detail(request, id):
    movie = Movie.objects.get(id=id) #select * from movie where id = id

    context = {
        "movie": movie,
    }

    return render(request,'main/details.html', context)

def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit = False)
            data.save()
            return redirect("main:main-home")

    else:
        form = MovieForm()
    return render(request, 'main/addmovies.html', {"form":form, "controller": "Add Movie"})

def edit_movies(request, id):
    movie = Movie.objects.get(id = id)

    if request.method == "POST":
        form = MovieForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit = False)
            data.save()
            return redirect("main:details",id)
    
    else:
        form = MovieForm(instance= movie)
    return render(request, 'main/addmovies.html',{"form":form, "controller": "Edit Movie"})

def delete_movies(request, id):
    movie = Movie.objects.get(id = id)

    movie.delete()
    return redirect("main:main-home")