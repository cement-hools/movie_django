from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Movie, Category, Actor, Genre


class GenreYear:
    """Жанры и года выхода"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).order_by('year')  # БЕРЕМ ТОЛЬКО ПОЛЕ YEAR


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    queryset = Movie.objects.filter(draft=False)


class MoviesDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = get_object_or_404(Movie, id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent'):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolut_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'  # поле по которому ищем актера


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    def get_queryset(self):
        years = self.request.GET.getlist('year')
        genres = self.request.GET.getlist('genre')
        queryset = Movie.objects.filter(
            Q(year__in=years) |
            Q(genres__in=genres)
        )
        return queryset
