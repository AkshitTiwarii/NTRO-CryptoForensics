# Celery Application Configuration
from celery import Celery
from celery.schedules import crontab

app = Celery(
    'ntro_crypto',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks']
)

# Celery Configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Celery Beat Schedule - Autonomous Scraping
app.conf.beat_schedule = {
    'autonomous-scraping-hourly': {
        'task': 'tasks.autonomous_scrape',
        'schedule': crontab(minute=0),  # Every hour on the hour
    },
    'enrichment-every-30min': {
        'task': 'tasks.enrich_pending_addresses',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    'check-watchlists-every-15min': {
        'task': 'tasks.check_watchlist_alerts',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'cleanup-old-jobs-daily': {
        'task': 'tasks.cleanup_old_jobs',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

if __name__ == '__main__':
    app.start()
