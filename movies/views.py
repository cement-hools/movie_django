from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm, RatingForm
from .models import Movie, Category, Actor, Genre, Rating


class GenreYear:
    """Жанры и года выхода"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).order_by(
            'year')  # БЕРЕМ ТОЛЬКО ПОЛЕ YEAR


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    queryset = Movie.objects.filter(draft=False)


class MoviesDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


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


class AddStarRating(View):
    """Добавление рейтинга к фильму."""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        return HttpResponse(status=400)
