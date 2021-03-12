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
    movie = Movie.objects.get(id=id) 
    review = Review.objects.filter(movie = id).order_by("-comment")

    context = {
        "movie": movie,
        "reviews": review
    }

    return render(request,'main/details.html', context)

def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit = False)
                    data.save()
                    return redirect("main:main-home")

            else:
                form = MovieForm()
            return render(request, 'main/addmovies.html', {"form":form, "controller": "Add Movie"})
        else:
            return redirect("main:main-home")
    return redirect("accounts:login")

def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
        else:
            return redirect("accounts:login")
    return redirect("accounts:login")

def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id = id)

            movie.delete()
            return redirect("main:main-home")
        else:
            return redirect("main:main-home")
    return redirect("accounts:login")

def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id = id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid:
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:details", id)
        else:
            form = ReviewForm()
        return render(request, "main:details.html",{"form": form})
    else:
        return redirect("accounts:login")

def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id = movie_id)
        review = Review.objects.get(movie = movie, id = review_id)

        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance = review)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:details",movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html',{"form":form})
        else:
            return redirect("main:details",movie_id)
    else:
        return redirect("accounts:login")