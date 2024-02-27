import requests
from datetime import datetime
from django.shortcuts import HttpResponse , redirect
from .models import Price
from django.db.utils import IntegrityError
from django.shortcuts import render
from datetime import date, timedelta

import environ
env = environ.Env()
environ.Env.read_env()

def fetch_and_store_data(request):
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
            modal_price = result.get('modal_price', 0)
            arrival_date_str = result.get('arrival_date', '')
            arrival_date = datetime.strptime(arrival_date_str, '%d/%m/%Y').date()

            Price.objects.create(
                commodity=commodity,
                market=market,
                district=district,
                state=state,
                min_price=min_price,
                max_price=max_price,
                model_price=modal_price,
                arrival_date=arrival_date
            )
        except IntegrityError:
            pass

    return HttpResponse("Data fetched and stored successfully.")


def index(request):
    if 'HTTP_USER_AGENT' in request.META:
        user_agent = request.META['HTTP_USER_AGENT']
        if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
            return mobile_view(request)
    return desktop_view(request)


def desktop_view(request):
    if request.method == 'POST':
        selected_commodity = request.POST.get('commodity')
        selected_district = request.POST.get('district')
        selected_market = request.POST.get('market')
        selected_date = request.POST.get('date')

        prices = Price.objects.all()
        commodities = Price.objects.values_list('commodity', flat=True).distinct()
        markets = Price.objects.values_list('market', flat=True).distinct()
        districts = Price.objects.values_list('district', flat=True).distinct()
        dates = Price.objects.values_list('arrival_date', flat=True).distinct()

        if selected_commodity:
            prices = prices.filter(commodity=selected_commodity)
            commodities = Price.objects.filter(commodity=selected_commodity).values_list('commodity', flat=True).distinct()
            markets = Price.objects.filter(commodity=selected_commodity).values_list('market', flat=True).distinct()
            districts = Price.objects.filter(commodity=selected_commodity).values_list('district', flat=True).distinct()
            dates = Price.objects.filter(commodity=selected_commodity).values_list('arrival_date', flat=True).distinct()
        if selected_district:
            commodities = Price.objects.filter(district=selected_district).values_list('commodity', flat=True).distinct()
            prices = prices.filter(district=selected_district)
            markets = Price.objects.filter(district=selected_district).values_list('market', flat=True).distinct()
            dates = Price.objects.filter(district=selected_district).values_list('arrival_date', flat=True).distinct()
        if selected_market:
            commodities = Price.objects.filter(market=selected_market).values_list('commodity', flat=True).distinct()
            prices = prices.filter(market=selected_market)
            districts = Price.objects.filter(market=selected_market).values_list('district', flat=True).distinct()
            dates = Price.objects.filter(market=selected_market).values_list('arrival_date', flat=True).distinct()
        if selected_date:
            prices = prices.filter(arrival_date=selected_date)

        context = {
            'prices': prices,
            'commodities': commodities,
            'markets': markets,
            'districts': districts,
            'dates': dates
        }

    else:
            today = date.today()
            today_prices = Price.objects.filter(arrival_date=today)
            previous_date = None
            previous_prices = None
            for i in range(1, 8):  # Check the last 7 days
                previous_date = today - timedelta(days=i)
                previous_prices = Price.objects.filter(arrival_date=previous_date)
                if previous_prices.exists():
                    break  # Stop if prices are found for the previous date

            all_prices = list(today_prices) + list(previous_prices)
            
    
            context = {
                'today': today,
                'prices': all_prices,
                'commodities': Price.objects.values_list('commodity', flat=True).distinct(),
                'markets': Price.objects.values_list('market', flat=True).distinct(),
                'districts': Price.objects.values_list('district', flat=True).distinct(),
                'dates': Price.objects.values_list('arrival_date', flat=True).distinct()
                
        }
    return render(request, 'desktop/index.html', context)


def mobile_view(request, district=None, market=None):
    if district is None:
        districts = Price.objects.values_list('district', flat=True).distinct()
        context = {'districts': districts}
    elif market is None:
        markets = Price.objects.filter(district=district).values_list('market', flat=True).distinct()
        context = {'district': district, 'markets': markets}
    else:
        commodities = Price.objects.filter(market=market)
        context = {'district': district, 'market': market, 'commodities': commodities}

    return render(request, 'mobile/index.html', context)
