from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Category, Genre, Movie, MovieShots, Actor, Rating,
                     RatingStar, Review)
from .utils import case_of_entries


class MovieAdminForm(forms.ModelForm):
    """Форма для описания фильма."""
    description = forms.CharField(
        label='Описание',
        widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


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


class MovieShotsInline(admin.TabularInline):
    """Кадры из фильма на странице фильмы."""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вывести миниатюру
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы."""
    list_display = ('title', 'category', 'url', 'draft',)
    list_filter = ('category', 'year',)
    search_fields = ('title', 'category__name',)
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True  # кнопки сохранения сверху
    save_as = True
    list_editable = ('draft',)  # редактируемое поле
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline',),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image',),)
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

    def get_image(self, obj):  # вывести миниатюру
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации."""
        row_update = queryset.update(draft=True)
        messege_bit = case_of_entries(row_update)
        self.message_user(request, f'{messege_bit}')

    def publish(self, request, queryset):
        """Опубликовать."""
        row_update = queryset.update(draft=False)
        messege_bit = case_of_entries(row_update)
        self.message_user(request, f'{messege_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


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

    def get_image(self, obj):  # вывести миниатюру
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг."""
    list_display = ('star', 'movie', 'ip',)


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
