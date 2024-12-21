from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .utils import filter_posts

from .models import Post, Category


def index(request):
    posts = filter_posts(Post.objects.select_related(
        'author', 'category', 'location'
    ))[:5]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    dt_now = timezone.now()
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        pk=post_id,
        pub_date__lte=dt_now,
        is_published=True,
        category__is_published=True
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = filter_posts(category.posts.select_related(
        'author', 'category', 'location'
    ))
    return render(
        request,
        'blog/category.html',
        {
            'post_list': posts,
            'category': category
        }
    )
