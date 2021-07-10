from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категории', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режисеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Актеры и режисеры'
        verbose_name_plural = 'Актеры и режисеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Категории', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Год выхода', default=2020)
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Режисер',
                                       related_name='films_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры',
                                    related_name='films_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры',
                                    related_name='films')
    world_premiere = models.DateField('Примьера в мире', default=date.today)
    budget = models.PositiveIntegerField(
        'Бюджет', default=0, help_text='указывать сумму в долларах'
    )
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text='указывать сумму в долларах'
    )
    fees_in_world = models.PositiveIntegerField(
        'Сборы в мире', default=0, help_text='указывать сумму в долларах'
    )
    category = models.ForeignKey(Category, related_name='movies',
                                 verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True)

    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, related_name='shots',
                              verbose_name='Фильм',
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ('-value',)


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, models.CASCADE, 'ratings',
                             verbose_name='Звезда')
    movie = models.ForeignKey(Movie, models.CASCADE, 'ratings',
                              verbose_name='Фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Обзор', max_length=5000)
    parent = models.ForeignKey(
        'self', models.CASCADE,
        related_name='comment',
        verbose_name='Родитель',
        blank=True, null=True
    )
    movie = models.ForeignKey(Movie, models.CASCADE, related_name='reviews',
                              verbose_name='Фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
