# daily_prices/management/commands/fetch_data.py
from django.core.management.base import BaseCommand
from daily_prices.models import Price
import requests
from django.db import IntegrityError
from datetime import datetime
import environ

env = environ.Env()

class Command(BaseCommand):
    help = 'Fetches and stores data'

    def handle(self, *args, **kwargs):
        endpoint = 'https://api.data.gov.in/catalog/6141ea17-a69d-4713-b600-0a43c8fd9a6c'
        api_key = env('DATA_API')

        params = {
            'api-key': api_key,
            'format': 'json',
            'filters[state]': 'Gujarat',
            'limit': '1000'
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        for result in data['records']:
            try:
                commodity = result.get('commodity', '')
                market = result.get('market', '')
                district = result.get('district', '')
                state = result.get('state', '')
                min_price = result.get('min_price', 0)
                max_price = result.get('max_price', 0)
                model_price = result.get('model_price', 0)
                arrival_date_str = result.get('arrival_date', '')
                arrival_date = datetime.strptime(arrival_date_str, '%d/%m/%Y').date()

                Price.objects.create(
                    commodity=commodity,
                    market=market,
                    district=district,
                    state=state,
                    min_price=min_price,
                    max_price=max_price,
                    model_price=model_price,
                    arrival_date=arrival_date
                )
            except IntegrityError:
                pass

        self.stdout.write(self.style.SUCCESS('Data fetched and stored successfully.'))
