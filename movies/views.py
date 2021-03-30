from django.shortcuts import render, get_object_or_404
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


class MoviesDetailView(View):
    """Полное описание фильма"""

    def get(self, request, slug):
        print('qwrqwr', slug)
        movie = get_object_or_404(Movie, url=slug)
        context = {
            'movie': movie,
        }
        return render(request, 'movies/movie_detail.html', context)
