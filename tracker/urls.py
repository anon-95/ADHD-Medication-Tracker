from django.urls import path

from . import views
from .views import JournalListView, JournalSingleView

urlpatterns = [
    path("", JournalListView.as_view(), name ="tracker-index"), 
    path("journal/<int:pk>/", JournalSingleView.as_view(), name ="journal-single"), 
    # path("", views.index, name ="tracker-index"), 
    path("about/", views.about, name ="tracker-about"),
    ]