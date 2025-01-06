from django.core.cache import cache
from django.db.models import Q, Count
from django.shortcuts import render

from .models import Category, Product, Tag

# Cache timeout duration
CACHE_TIMEOUT = 3600  # 1 hour 

def index(request):
    # Get filters from URL parameters
    query = request.GET.get('query', '')
    category = request.GET.get('category', 0)
    tags = request.GET.getlist('tag', [])

    # Get all products
    products = Product.objects.all()

    # Initialize filters
    filters = Q()

    if query:
        filters &= Q(description__icontains=query)
    if category:
        filters &= Q(category__id=category)
    if tags:
        products = Product.objects.filter(tags__id__in=tags) \
            .annotate(matched_tags=Count('tags', filter=Q(tags__id__in=tags))) \
            .filter(matched_tags=len(tags))

    products = products.filter(filters)

    # Cache all categories and tags
    all_categories = cache.get('all_categories')
    if not all_categories:
        all_categories = Category.objects.all()
        cache.set('all_categories', all_categories, timeout=CACHE_TIMEOUT)  

    all_tags = cache.get('all_tags')
    if not all_tags:
        all_tags = Tag.objects.all()
        cache.set('all_tags', all_tags, timeout=CACHE_TIMEOUT) 

    context = {
        'products': products,
        'categories': all_categories,
        'tags': all_tags,
        'query': query,
        'selected_category': category,
        'selected_tags': tags,
    }

    return render(request, 'remarcableapp/index.html', context)