from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Genre, Movie, MovieShots, Actor, Rating,
                     RatingStar, Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории."""
    list_display = ('id', 'name', 'url',)
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильмы."""
    model = Review
    extra = 1
    readonly_fields = ('name', 'email',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы."""
    list_display = ('title', 'category', 'url', 'draft',)
    list_filter = ('category', 'year',)
    search_fields = ('title', 'category__name',)
    inlines = [ReviewInline]
    save_on_top = True  # кнопки сохранения сверху
    save_as = True
    list_editable = ('draft',)  # редактируемое поле
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline',),)
        }),
        (None, {
            'fields': (('description', 'poster',),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country',),)
        }),
        ('Actors', {
            'classes': ('collapse',),  # показать/скрыть панель
            'fields': (('actors', 'directors', 'genres', 'category',),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world',),)
        }),
        ('Options', {
            'fields': (('url', 'draft',),)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы."""
    list_display = ('name', 'email', 'parent', 'movie', 'id',)
    readonly_fields = ('name', 'email',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры."""
    list_display = ('name', 'url',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры."""
    list_display = ('name', 'age', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj): # вывести миниатюру
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг."""
    list_display = ('star', 'ip',)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма."""
    list_display = ('title', 'movie', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вывести миниатюру
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Фильмы'
admin.site.site_header = 'Django Фильмы'