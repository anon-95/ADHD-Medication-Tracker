from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.http import HttpResponse
from .models import Journal
from django.views.generic import ListView, DetailView
# def index(request) :

#     context = {
#         'journals': Journal.objects.filter(author_id=request.user.id)
#     }
#     return render(request, "tracker/home.html", context)

class JournalListView(ListView):
    model = Journal
    template_name = "tracker/home.html"
    context_object_name = 'journals'

    def get_queryset(self):
        return Journal.objects.filter(author=self.request.user).order_by('-date_posted')

class JournalSingleView(DetailView):
    model = Journal
    template_name = "tracker/single_journal.html"
    def get_queryset(self):
        user = self.request.user  # Get the currently logged-in user
        return Journal.objects.filter(author_id=user.id)
def about(request) :
    return render(request, "tracker/about.html")
