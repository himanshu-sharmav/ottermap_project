from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
from .forms import ShopForm
from django.views.generic import ListView
from .models import Shop
from .serializers import ShopSerializer
from .utils import haversine
from rest_framework.views import APIView

def home(request):
    """
    Renders the home page for the application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page template.
    """
    return render(request, 'shops/home.html')

# View for registering a shop
def register_shop(request):
    """
    Handles the registration of a new shop.

    This view accepts a POST request with shop details and creates a new shop entry.
    On successful registration, it redirects the user to the shop list view.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponse: Redirects to the shop list view if form is valid,
        otherwise renders the registration form.
    """
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')  # Ensure 'shop_list' is correctly defined in urls.py
    else:
        form = ShopForm()
    return render(request, 'shops/register.html', {'form': form})

# View for searching shops based on user's location
def search_shops(request):
    """
    Searches for nearby shops based on the user's location.

    This view handles a POST request containing the user's latitude and longitude
    and searches for shops that are nearby. The results are sorted by proximity.

    Args:
        request (HttpRequest): The HTTP request object containing latitude and longitude.

    Returns:
        HttpResponse: Renders the search results page with a list of shops sorted by distance.
    """
    if request.method == 'POST':
        try:
            user_lat = float(request.POST.get('latitude'))
            user_lon = float(request.POST.get('longitude'))
        except (TypeError, ValueError):
            return render(request, 'shops/search.html', {'error': 'Invalid latitude or longitude'})

        shops = Shop.objects.all()
        shop_distances = []

        for shop in shops:
            distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
            shop_distances.append((shop, distance))

        shop_distances.sort(key=lambda x: x[1])

        return render(request, 'shops/search_results.html', {'shop_distances': shop_distances})

    return render(request, 'shops/search.html')

# API view for registering a shop (POST request)

@api_view(['POST'])
def register_shop_api(request):
    """
    API view for registering a new shop.

    This view accepts a POST request with shop data in JSON format and creates a new shop entry.
    It returns the created shop's data or validation errors.

    Args:
        request (HttpRequest): The HTTP request object containing the shop data.

    Returns:
        Response: A JSON response containing the created shop data or errors.
    """
    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# API view for searching shops (GET request)
@api_view(['GET'])
def search_shops_api(request):
    """
    API view for searching shops near a given location.

    This view accepts a GET request with latitude and longitude as query parameters
    and returns a list of shops sorted by proximity to the given location.

    Args:
        request (HttpRequest): The HTTP request object containing query parameters.

    Returns:
        Response: A JSON response containing the list of shops or an error message.
    """
    try:
        user_lat = float(request.GET.get('latitude'))
        user_lon = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return Response({'error': 'Invalid latitude or longitude'}, status=400)

    shops = Shop.objects.all()
    shop_distances = []

    for shop in shops:
        distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
        shop_distances.append((shop, distance))

    shop_distances.sort(key=lambda x: x[1])
    sorted_shops = [shop for shop, _ in shop_distances]

    serializer = ShopSerializer(sorted_shops, many=True)
    return Response(serializer.data)

# Class-based view for listing shops
class ShopListView(APIView):
    """A view to list shops.
    
    This view retrieves a list of shops from the database and renders them using the specified template.

    Attributes:
        model (Shop): The model to be used for this view.
        template_name (str): The template to be rendered.
        context_object_name (str): The context variable used in the template.
    
    Note:
        If you also document these attributes in another place, consider using `:no-index:` 
        to avoid duplication warnings.
    """
    model = Shop
    template_name = 'shops/shop_list.html'
    context_object_name = 'shops'
