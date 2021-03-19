from celery.schedules import crontab


CELERY_SCHEDULE = {
    'delete_anonymous_cart': {
        'task': 'shop.tasks.delete_cart_for_anonymous_user',
        'schedule': crontab(hour=0, minute=1),
    }
}
