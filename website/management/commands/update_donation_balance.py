from django.core.management.base import BaseCommand, CommandError
from website.models import Cryptocurrency
import requests
import datetime
import decimal

class Command(BaseCommand):
    help = 'Reorders'

    def handle(self, *args, **options):
        donation_enabled_coins = Cryptocurrency.objects.exclude(donation_wallet__isnull=True).exclude(donation_wallet__exact='')
        for coin in donation_enabled_coins:


            r = requests.get(coin.block_explorer + 'ext/getaddress/' + coin.donation_wallet)
            result = r.json()

            coin.donation_count = result['received']
            coin.donation_total = result['balance']
            coin.save()








