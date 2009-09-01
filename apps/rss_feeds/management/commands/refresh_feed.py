from django.core.management.base import BaseCommand
from django.core.handlers.wsgi import WSGIHandler
from apps.rss_feeds.models import Feed, Story
from django.core.cache import cache
from apps.reader.models import UserSubscription, UserSubscriptionFolders, UserStory
from optparse import OptionParser, make_option
from utils.management_functions import daemonize
import os
import logging
import errno

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-f", "--feed", dest="feed", default=None),
        make_option("-d", "--daemon", dest="daemonize", action="store_true"),
    )

    def handle(self, *args, **options):
        if options['daemonize']:
            daemonize()
            
        feed = Feed.objects.get(id=options['feed'])
        self._refresh_feeds([feed])
        
    def _refresh_feeds(self, feeds):
        for feed in feeds:
            feed.update(True)
            usersubs = UserSubscription.objects.filter(
                feed=feed.id
            )
            for us in usersubs:
                us.count_unread()
                cache.delete('usersub:%s' % us.user_id)