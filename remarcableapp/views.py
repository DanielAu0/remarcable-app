from django.core.cache import cache
from django.db.models import Q, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Category, Product, Tag

# Cache timeout duration
CACHE_TIMEOUT: int = 3600  # 1 hour 

def index(request: HttpRequest) -> HttpResponse:
    # Get filters from URL parameters
    query: str = request.GET.get('query', '')
    category: int = int(request.GET.get('category', 0))
    tags: list[str] = request.GET.getlist('tag', [])

    # Get all products
    products = Product.objects.all()

    # Initialize filters
    filters: Q = Q()

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
    all_categories: list[Category] = cache.get('all_categories')
    if not all_categories:
        all_categories = Category.objects.all()
        cache.set('all_categories', all_categories, timeout=CACHE_TIMEOUT)  

    all_tags: list[Tag] = cache.get('all_tags')
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