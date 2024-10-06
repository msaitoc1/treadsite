from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import coffeeShop, Event, stat, GlobalInvertedIndex, coffeeShopSearchDoc
from django.contrib.postgres.search import SearchVector
import math

#gets coffeeshop list for the home page of the site
def home(request):
    items = coffeeShop.objects.all()
    return render(request, 'home.html', {'coffeeShops': items})

#gets a coffeeshop's information for a coffeeshop's detail site.
def coffeeShop_detail(request, pk):
    coffee_shop = get_object_or_404(coffeeShop, pk=pk)
    events=  Event.objects.filter(coffee_shop_id=pk)
    coffeeStats = stat.objects.all()
    favorited = request.user.is_authenticated and request.user in coffee_shop.favorited_by.all()
    return render(request, 'coffeeShop_detail.html', {'coffeeShop': coffee_shop, 
                                                      'events': events, 
                                                      'coffeestats': coffeeStats,
                                                      'favorited': favorited})

#gets favorited shops for a user's favorites page
def favorites(request): 
    favorited_shops = request.user.favorite_coffee_shops.all()
    return render(request, 'favorites.html', {'coffeeShops': favorited_shops})

def calculate_idf(term):
    """
    Calculates the Inverse Document Frequency for a given term
    """
    total_shops = coffeeShop.objects.count()
    containing_shops = GlobalInvertedIndex.objects.filter(term=term).count()
    if containing_shops == 0:
        return 0
    else:
        return math.log(float(total_shops) / containing_shops)
def search_coffee_shops(query):
    """
    search coffee shops using search query based on TF-IDF
    """
    words = query.split()
    matches = {}
    for word in words:
        cleaned_word = coffeeShop.clean_word(None, word)
        try:
            index_entry = GlobalInvertedIndex.objects.get(term=cleaned_word)
        except GlobalInvertedIndex.DoesNotExist:
            continue
        coffee_shop_ids = index_entry.coffee_shop_ids
        coffee_shop_docs = coffeeShopSearchDoc.objects.filter(coffee_shop_id__in = coffee_shop_ids)
        for shop_doc in coffee_shop_docs:
            tf = shop_doc.term_frequency(cleaned_word)
            idf = calculate_idf(cleaned_word)
            score = tf*idf
            if shop_doc.coffee_shop_id not in matches:
                matches[shop_doc.coffee_shop_id] = 0.0
            matches[shop_doc.coffee_shop_id] += score
    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    return[coffeeShop.objects.get(id=shop_id) for shop_id, score in sorted_matches]    
    
    
def search(request):
    """
    Handles the search query from the search bar and returns matching coffee Shops.
    """
    query = request.GET.get('query', '')
    coffee_shops = search_coffee_shops(query)

    return render(request, 'search_results.html', {'coffee_shops': coffee_shops})
    

# Toggles favorite status based on primary key(pk)
def toggleFavorite(request, pk):
    coffee_shop = coffeeShop.objects.get(pk=pk)

    if coffee_shop.favorited_by.filter(id=request.user.id).exists():
        coffee_shop.favorited_by.remove(request.user)
        favorited = False
    else:
        coffee_shop.favorited_by.add(request.user)
        favorited = True
    return JsonResponse({'favorited': favorited})

