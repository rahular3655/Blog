from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone


class TagQuerySet(QuerySet):
    def annotate_live_blog_count(self):
        current_datetime = timezone.now()
        return self.annotate(
            blog_count=models.Count(
                expression='blogs',
                filter=Q(blogs__published_on__lte=current_datetime) & (
                            Q(blogs__unpublished_on__gte=current_datetime) | Q(blogs__unpublished_on__isnull=True)),
                blogs__is_published=True
            )
        )
