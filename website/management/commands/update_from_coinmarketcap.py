from django.core.management.base import BaseCommand, CommandError
from website.models import Cryptocurrency
import requests
import datetime
import decimal

class Command(BaseCommand):
    help = 'Reorders'

    def handle(self, *args, **options):

        r = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
        for coin in r.json():
            try:
                obj, created = Cryptocurrency.objects.update_or_create(
                    slug=coin['id'],
                    defaults={
                        'name': coin['name'],
                        'symbol': coin['symbol'],
                        'rank': coin['rank'],
                        'price_usd': coin['price_usd'],
                        'price_btc': coin['price_btc'],
                        'volume_usd_24h': coin['24h_volume_usd'] or 0,
                        'market_cap_usd': decimal.Decimal(coin['market_cap_usd'] or 0).normalize(),
                        'available_supply': coin['available_supply'] or 0,
                        'total_supply': coin['total_supply'] or 0,
                        'max_supply': coin['max_supply'] or 0,
                        'percent_change_1h': coin['percent_change_1h'] or 0,
                        'percent_change_24h': coin['percent_change_24h'] or 0,
                        'percent_change_7d': coin['percent_change_7d'] or 0,
                        'last_updated': datetime.datetime.fromtimestamp(float(coin['last_updated'])) 
                        },
                )
                print obj,created
            except Exception as error:
                print coin, error, decimal.Decimal(coin['market_cap_usd']).normalize()
