from django.urls import path
from . import views

urlpatterns = [
    path("polls/", views.poll_view, name="polls"),
    path("results/", views.results_view, name="results"),
]
