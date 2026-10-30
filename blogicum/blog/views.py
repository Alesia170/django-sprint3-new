from django.shortcuts import render, get_object_or_404

from django.utils import timezone

from .models import Category, Post

LIMIT_POSTS = 5


def index(request):
    template = 'blog/index.html'
    posts = get_published_posts()[:LIMIT_POSTS]
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(get_published_posts(), pk=pk)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True,
        )
    )
    posts = get_published_posts().filter(
        category=category,
    )
    context = {'category': category, 'posts': posts}
    return render(request, template, context)


def get_published_posts():
    return Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
