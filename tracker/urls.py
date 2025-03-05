from django.urls import path
from datetime import timedelta
from django.utils import timezone

from . import views
from .views import JournalListView, JournalSingleView, JournalCreateView, JournalUpdateView

urlpatterns = [
    path("", JournalListView.as_view(), name ="tracker-index"), 
    path("journal/<int:pk>/", JournalSingleView.as_view(), name ="journal-single"), 
    path("journal/<int:pk>/update/", JournalUpdateView.as_view(), name ="journal-update"), 
    path('journal/create/', JournalCreateView.as_view(), name='journal_create'),
    path("about/", views.about, name ="tracker-about"),
    path("statistics/", views.statistics, name = "statistics"),

    # path('streaks/', views.streaks, name='view-streaks'),
        # path("", views.index, name ="tracker-index"), 
    ]