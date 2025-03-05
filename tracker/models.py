from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date published")
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default = 0)
    def __str__(self):
        return self.choice_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
def get_current_local_time():
    return timezone.localtime(timezone.now())
class Journal(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=get_current_local_time)
    day_number = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    remembered = models.BooleanField(default=False)
    notes = models.TextField()
    
    condition_choices = [
        ('Improving', 'Improving'),
        ('Stable', 'Stable'),
        ('Worsening', 'Worsening'),
    ]
    mood = models.CharField(max_length=50, choices=condition_choices, default="Stable")  # Mood with choices
    def update_day_number(self):
        profile = self.author.profile
        start_date = profile.start_date
        date_posted = self.date_posted
        start_datetime = datetime.combine(start_date, datetime.min.time())
        if date_posted.tzinfo is not None:
            date_posted = date_posted.replace(tzinfo=None)  # Make it naive
        delta = date_posted - start_datetime
        self.day_number = delta.days
        self.save()
    def get_absolute_url(self):
        return reverse('journal-single', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
