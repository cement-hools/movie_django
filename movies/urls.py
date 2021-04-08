from django.urls import path

from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('<str:slug>', views.MoviesDetailView.as_view(), name='movie_detail'),
    path('actor/<str:slug>', views.ActorView.as_view(), name='actor_detail'),
    path('review/<int:pk>', views.AddReview.as_view(), name='add_review'),


]
