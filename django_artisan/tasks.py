import logging

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

def db_backup(self) -> None:
    # clear existing backups first - dbbackup --clean doesn't work with
    # dropbox.
    try:
        dbx = dropbox.Dropbox(
            confg.settings.DBBACKUP_STORAGE_OPTIONS['oauth2_access_token'])
    except dropbox.exceptions.AuthError as e:
        logger.error("Dropbox Auth Issue : {0}".format(e))
    except dropbox.exceptions.HttpError as e:
        logger.error("Dropbox HttpError : {0}".format(e))
    for entry in dbx.files_list_folder('', recursive=True).entries:
        dbx.files_delete(entry.path_display)
    management.call_command("dbbackup --traceback")
    management.call_command("mediabackup")
    logger.info("succesfully backed up database and media files")