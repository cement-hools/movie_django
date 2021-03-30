from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    queryset = Movie.objects.filter(draft=False)


class MoviesDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'
