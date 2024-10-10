from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/list/', views.ShopListView.as_view(), name='shop_list'),  # Shop list view
    path('register/', views.register_shop, name='register_shop'),   # Shop registration view
    path('search/', views.search_shops, name='search_shops'),       # Shop search view
]
