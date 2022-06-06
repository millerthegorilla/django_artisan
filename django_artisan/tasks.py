import logging

from django import core
from django.contrib import sitemaps

logger = logging.getLogger('django_artisan')

"""
    pings_google to recrawl site when user opts to list on about page
    or to display personal page
    You must be registered with google search console for this to work
    #         ... https://search.google.com/search-console/welcome
"""
def ping_google_func() -> None:
    try:
        sitemaps.ping_google()
        logger.info("Pinged Google!")
    except Exception as e:
        logger.error("unable to ping_google : {0}".format(e))

def db_backup() -> None:
    # clear existing backups first - dbbackup --clean doesn't work with
    # dropbox.
    core.management.call_command("dbbackup", "-e", "--clean")
    core.management.call_command("mediabackup", "-e", "--clean")
    logger.info("succesfully backed up database and media files")

def db_backup_hook(task) -> None:
    if task.success:
        logger.info("db and media backedup succesfully!")
    else:
        logger.warning("db and media backup failed!")
        core.mail.mail_admins(has_attr(core.settings, "django site"),
                              "db and media backup failed at {}".format(task.started), 
                              fail_silently=False, 
                              connection=None, 
                              html_message=None)