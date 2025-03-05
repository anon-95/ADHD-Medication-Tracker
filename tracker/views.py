from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.db.models import Count
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
from django.http import HttpResponse
from .models import Journal
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# def index(request) :

#     context = {
#         'journals': Journal.objects.filter(author_id=request.user.id)
#     }
#     return render(request, "tracker/home.html", context)
class JournalListView(LoginRequiredMixin, ListView):
    model = Journal
    template_name = "tracker/home.html"
    context_object_name = 'journals'

    login_url = '/login/'  # Optional: Set a custom login URL (if not using the default)
    redirect_field_name = 'next'  # Optional: The query parameter to store the redirect URL
    paginate_by = 10
    def get_queryset(self):

        journals = Journal.objects.filter(author_id=self.request.user.id).order_by('-date_posted')
        for journal in journals:
            journal.update_day_number()  # Update the day_number of each journal
        
        return journals

class JournalSingleView(DetailView):
    model = Journal
    template_name = "tracker/single_journal.html"

    def get_queryset(self):
        user = self.request.user  # Get the currently logged-in users
        return Journal.objects.filter(author_id=user.id)

def about(request) :
    return render(request, "tracker/about.html")

class JournalCreateView(LoginRequiredMixin, CreateView):
    today = timezone.now().date()
    
    model = Journal
    template_name = "tracker/create_journal.html"
    fields = ['title', 'remembered', 'notes', 'mood']
    widgets = {
            'mood': forms.Select(choices=Journal.condition_choices)  # Render mood as a dropdown
        }
    remembered = forms.BooleanField(
        required=False,  # Optional checkbox (so it's not mandatory)
        widget=forms.CheckboxInput(attrs={'class': 'large-checkbox'})  # Add custom class
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        # Get current local time
        local_time = timezone.localtime(timezone.now())
        today = local_time.date()  # Get today's date in the user's local time zone
        user = request.user
        # Check if the user has already posted today
        existing_journal = Journal.objects.filter(author_id=user.id, date_posted__date=today).first()
        check_journal = Journal.objects.filter(author_id=user.id).first()

        if existing_journal:
            messages.info(request, 'You have filled out your daily check-in for today.')
            return redirect('tracker-index') 
        # Otherwise, continue with normal CreateView behavior
        return super().get(request, *args, **kwargs)

class JournalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):    
    model = Journal
    template_name = "tracker/create_journal.html"
    fields = ['title', 'remembered', 'notes', 'mood']
    widgets = {
            'mood': forms.Select(choices=Journal.condition_choices)  # Render mood as a dropdown
        }
    remembered = forms.BooleanField(
        required=False,  # Optional checkbox (so it's not mandatory)
        widget=forms.CheckboxInput(attrs={'class': 'large-checkbox'})  # Add custom class
    )
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        journal = self.get_object()
        if self.request.user.id == journal.author_id:
            return True
        return False
def about(request) :
    return render(request, "tracker/about.html")
@login_required
def statistics(request):
    user = request.user

    # Count remembered and non-remembered journals
    total_journals = Journal.objects.filter(author_id=user.id).count()
    remembered_journals = Journal.objects.filter(author_id=user.id, remembered=True).count()

    percent_remembered = (remembered_journals / total_journals) * 100 if total_journals > 0 else 0
    
 # Create Pie chart for percentage of days remembered to take medication
    medication_fig = go.Figure(data=[go.Pie(labels=['Remembered', 'Not Remembered'],
                                            values=[remembered_journals, total_journals - remembered_journals],
                                            hole=0.3
    )])
    
    # 2. Frequency of Journal Entries (How often the user remembered to journal)
    journal_entries = Journal.objects.filter(author=user).annotate(day=TruncDay('date_posted')).values('day').annotate(count=Count('id'))
    journaled_days = [entry['day'] for entry in journal_entries]
    first_journal_date = last_journal_date = None
    
    if journaled_days:
        first_journal_date = min(journaled_days)
        last_journal_date = max(journaled_days)
    else:
        last_journal_date = first_journal_date = 0
    # Get all days between the first and last journal entries
    all_days = [first_journal_date + timedelta(days=i) for i in range((last_journal_date - first_journal_date).days + 1)] if first_journal_date else []

    # Count days journaled and days not journaled
    days_journaled = len(journaled_days)
    days_not_journaled = len(all_days) - days_journaled

    # Create Bar chart for journal frequency
    frequency_fig = go.Figure(data=[go.Bar(
        x=['Days Journaled', 'Days Not Journaled'],
        y=[days_journaled, days_not_journaled],
        marker=dict(color=['green', 'red'])
    )])
    frequency_fig.update_layout(title=None, xaxis_title='Category', yaxis_title='Number of Days')
    # 3. Mood Distribution (How often each mood was recorded)
    mood_counts = Journal.objects.filter(author_id=user.id).values('mood').annotate(count=Count('mood'))
    mood_data = {'Improving': 0, 'Stable': 0, 'Worsening': 0}
    for mood_count in mood_counts:
        mood_data[mood_count['mood']] = mood_count['count']
    # Create Pie chart for mood distribution
    mood_fig = go.Figure(data=[go.Pie(
        labels=list(mood_data.keys()),
        values=list(mood_data.values()),
        hole=0.3
    )])    
     # 4. Mood Progression Over Time
    # Get the journals and map moods to numerical values
    mood_mapping = {'Improving': 3, 'Stable': 2, 'Worsening': 1}
    mood_progression = Journal.objects.filter(author_id=user.id).order_by('date_posted').values('date_posted', 'mood')
    dates = [entry['date_posted'].strftime('%Y-%m-%d') for entry in mood_progression]
    mood_values = [mood_mapping[entry['mood']] for entry in mood_progression]
    # Create a line chart for mood progression over time
    progression_fig = go.Figure(data=[go.Scatter(
                                                x=dates,
                                                y=mood_values,
                                                mode='lines+markers',
                                                line=dict(color='purple'),
                                                marker=dict(size=8)
    )])
    progression_fig.update_layout(
        title=None,
        xaxis_title='Date',
        yaxis_title='Mood',
        yaxis=dict(tickvals=[1, 2, 3], ticktext=['Worsening', 'Stable', 'Improving']),
        showlegend=False
    )
    # Convert the charts to JSON format
    medication_chart_json = json.dumps(medication_fig, cls=plotly.utils.PlotlyJSONEncoder)
    frequency_chart_json = json.dumps(frequency_fig, cls=plotly.utils.PlotlyJSONEncoder)
    mood_chart_json = json.dumps(mood_fig, cls=plotly.utils.PlotlyJSONEncoder)
    progression_chart_json = json.dumps(progression_fig, cls=plotly.utils.PlotlyJSONEncoder)
    # Pass the chart data to the template
    context = {
    'medication_chart_json': medication_chart_json,
    'frequency_chart_json': frequency_chart_json,
    'mood_chart_json': mood_chart_json,
    'progression_chart_json': progression_chart_json,
    }

    return render(request, 'tracker/statistics.html', context)
