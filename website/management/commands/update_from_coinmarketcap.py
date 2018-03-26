from django.core.management.base import BaseCommand, CommandError
from website.models import Cryptocurrency
import requests
import datetime
import decimal
from django.core.mail import send_mail
import os
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import *

ROLLBAR = {
    'access_token': os.environ.get('ROLLBAR_ACCESS_TOKEN', '11111111111111111'),
    'environment': 'development' if settings.DEBUG else 'production',
    'root': settings.BASE_DIR
}
import rollbar
rollbar.init(**ROLLBAR)

class Command(BaseCommand):

    def handle(self, *args, **options):

        new_coin_list = ""

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
                        'last_updated': datetime.datetime.fromtimestamp(float(coin['last_updated'] or 0)) 
                        },
                )
                if created:
                    new_coin_list += "<a href='https://coinmarketcap.com/currencies/"+obj.slug+"/'>" + obj.name + "</a> ("+str(Decimal(obj.price_usd))+")<br>"

                chart_list = obj.chart_24h.split(",")
                if len(chart_list) == 24:
                    chart_list.pop(0)

                if Decimal(obj.price_usd) > 1:
                    chart_list.append("{0:.2f}".format(Decimal(obj.price_usd)))
                else:
                    chart_list.append(Decimal(obj.price_usd).normalize())

                obj.chart_24h = ','.join(map(str, chart_list)).lstrip(',')
                obj.save()

                print (obj, obj.chart_24h, created)
            except Exception as error:
                print (coin, error)

        if new_coin_list:

            send_mail(
                subject = 'Spurri Cryptocurrency Report',
                html_message = "New coins added to CoinMarketCap:<br>" + new_coin_list,
                from_email = 'info@spurri.com',
                recipient_list = [os.environ.get('EMAIL_TO', 'info@spurri.com'),],
                fail_silently=False,
            )