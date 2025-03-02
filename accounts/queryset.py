from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone


class UserQuerySet(QuerySet):
    def annotate_live_blog_count(self):
        current_datetime = timezone.now()
        return self.annotate(
            blog_count=models.Count(
                expression='user_blogs',
                 filter=Q(
                user_blogs__published_on__lte=current_datetime,
                user_blogs__unpublished_on__gte=current_datetime,
                user_blogs__is_published=True,
                user_blogs__is_draft=False,
            ) | Q(
                user_blogs__published_on__lte=current_datetime,
                user_blogs__unpublished_on__isnull=True,
                user_blogs__is_published=True,
                user_blogs__is_draft=False,
            )
        )
    )
        