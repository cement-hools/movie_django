from django.shortcuts import render
from django.views.generic.base import View

from .models import Movie


class MoviesView(View):
    """Список фильмов"""
    def get(self, request):
        movies = Movie.objects.all()
        context = {
            'movie_list': movies,
        }
        return render(request, 'movies/movies.html', context)
