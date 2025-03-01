import time

from django.contrib.auth import get_user_model

from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count(i=0):
    """A pointless Celery task to demonstrate usage."""
    time.sleep(10)
    print(i)
    return User.objects.count()
