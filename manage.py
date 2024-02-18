#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import schedule
import threading
import time


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SearchAgrigate.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def parallel_scraper_func():
    """responsible for the parallel process of scraping news and writing it to the database"""
    from app import scrapers
    scrapers.update_db()


def start_schedule():
    schedule.every(10).minutes.do(parallel_scraper_func)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    thread = threading.Thread(target=start_schedule)
    thread.start()
    main()
