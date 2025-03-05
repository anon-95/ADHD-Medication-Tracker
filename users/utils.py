from datetime import timedelta
from django.utils import timezone
from tracker.models import Journal
from datetime import timedelta
from django.utils import timezone
from tracker.models import Journal

def calculate_streak(user_id, current_streak):
    user = user_id
    journals = Journal.objects.filter(author_id=user).order_by('-date_posted')  # Get journals in reverse order
    # Get today's date (midnight)
    today = timezone.now().date()
    # Get yesterday's date
    yesterday = today - timedelta(days=1)

    # Query for journals from today
    journals_today = Journal.objects.filter(author_id=user, date_posted__date=today)
    # Query for journals from yesterday
    journals_yesterday = Journal.objects.filter(author_id=user, date_posted__date=yesterday)
    print(current_streak)
    journals_today = Journal.objects.filter(author_id=user, date_posted__date=today)
    print(journals_yesterday.exists())
    print(journals_today.exists())
    if not journals_yesterday.exists():
        print("streak is reset")
        current_streak = 0
    if journals_today.exists():  # Checks if the queryset is empty
        current_streak +=1
        print("added to streak")
    return current_streak