from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_LIMIT = 5


def get_published_posts():
    """Возвращает queryset опубликованных постов.

    Условия публикации:
    - флаг is_published равен True;
    - категория поста существует и опубликована (is_published=True);
    - дата публикации pub_date не позже текущего времени (timezone.now()).
    Использует select_related для оптимизации запросов к связанным моделям.
    """
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    """Главная страница сайта.

    Отображает пять последних опубликованных постов.
    """
    post_list = get_published_posts()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    """Страница отдельной публикации.

    Возвращает пост по первичному ключу.
    Если пост не опубликован, снята с публикации его категория,
    дата публикации в будущем или пост не найден — возвращает 404.
    """
    post = get_object_or_404(
        get_published_posts(),
        pk=id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница публикаций выбранной категории.

    Возвращает только опубликованные посты выбранной категории.
    Если категория снята с публикации или не существует — возвращает 404.
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list,
        }
    )
