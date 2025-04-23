from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('newspapers/', views.NewspaperListView.as_view(), name='newspaper_list'),

    # Newspaper URLs
    path("newspapers/", views.NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", views.NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", views.NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", views.NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", views.NewspaperDeleteView.as_view(), name="newspaper-delete"),

    # Topic URLs
    path("topics/", views.TopicListView.as_view(), name="topic-list"),
    path("topics/create/", views.TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/update/", views.TopicUpdateView.as_view(), name="topic-update"),
    path("topics/<int:pk>/delete/", views.TopicDeleteView.as_view(), name="topic-delete"),

    # Redactor URLs
    path("redactors/", views.RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", views.RedactorDetailView.as_view(), name="redactor-detail"),
    path("redactors/create/", views.RedactorCreateView.as_view(), name="redactor-create"),
    path("redactors/<int:pk>/update/", views.RedactorUpdateView.as_view(), name="redactor-update"),
    path("redactors/<int:pk>/delete/", views.RedactorDeleteView.as_view(), name="redactor-delete"),
]

app_name = "newspaper"

