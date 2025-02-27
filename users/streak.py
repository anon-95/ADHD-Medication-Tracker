# your_app/utils.py
from datetime import timedelta
from tracker.models import Journal

def calculate_streak(user_id):
    user = user_id
    journals = Journal.objects.filter(author_id=user).order_by('date_posted')

    streak = 0
    current_streak = 0
    previous_date = None

    for journal in journals:
        post_date = journal.date_posted.date()  # Get only the date (without time)

        if previous_date is None:
            current_streak = 1
        elif post_date == previous_date + timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1

        streak = max(streak, current_streak)
        previous_date = post_date

    return streak
