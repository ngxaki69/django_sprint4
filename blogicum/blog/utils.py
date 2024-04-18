from django.db.models import Count
from django.utils import timezone


def filter_search_comment(entity):
    return entity.select_related(
        'author', 'category', 'location'
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def filter_search(entity):
    time = timezone.now()
    return entity.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=time
    )
