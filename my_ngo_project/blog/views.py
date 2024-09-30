from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import BlogPost, Category
from django.utils import timezone
from taggit.models import Tag
from django.contrib import messages
from django.db.models import Q

def blog_list(request):
    now = timezone.now()
    posts = BlogPost.objects.filter(is_published=True, created_at__lte=now).order_by('-created_at')
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    
    # Add absolute URLs to each post
    for post in page_obj:
        post.absolute_url = request.build_absolute_uri(post.get_absolute_url())
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_page': 'Blog',
        'page_title': 'Our Blog',
    }
    
    return render(request, 'blog/blog_list.html', context)

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    categories = Category.objects.all()
    related_posts = BlogPost.objects.filter(categories__in=post.categories.all(), is_published=True).exclude(id=post.id).distinct()[:5]

    context = {
        'post': post,
        'categories': categories,
        'related_posts': related_posts,
    }
    return render(request, 'blog/blog_post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(categories=category, is_published=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_posts.html', {'category': category, 'page_obj': page_obj})

def tagged_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag, is_published=True)
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'current_page': f'Posts tagged with "{tag.name}"',
        'page_title': f'Posts tagged with "{tag.name}"',
    }
    
    return render(request, 'blog/tagged_posts.html', context)

# Remove the add_comment view

def blog_search(request):
    query = request.GET.get('q')
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        results = BlogPost.objects.none()
    
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search_results.html', context)