
from django.contrib import admin
from django.urls import path
from daily_prices.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('desktop/', desktop_view, name='desktop_view'),
    path('fetch/', fetch_and_store_data, name='fetch_data'),
    # path('search/', search_prices, name='search_prices'),
    path('mobile/', mobile_view, name='mobile_view'),
    path('graph/', graph, name='graph'),
    # path('mobile/<str:district>/', mobile_view, name='mobile_view_district'),
    # path('mobile/<str:district>/<str:market>/', mobile_view, name='mobile_view_market'),

]
