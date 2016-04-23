from django.core.management.base import BaseCommand, CommandError
import core.models as models
from grabber.grabber import GoodsMatrixSpider
import logging

class Command(BaseCommand):
    args = 'thread_number'
    help = 'Run grabber'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        if len(args) == 1:
            thread_number = int(args[0])
        else:
            thread_number = settings.GRAB_THREAD_NUMBER
        bot = GoodsMatrixSpider(thread_number=thread_number)
        bot.run()
