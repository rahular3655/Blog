from django.db import models
from django.db.models import Case, When
from django.db.models import QuerySet, Q
from django.utils import timezone


class BlogQuerySet(QuerySet):

    def published(self):
        current_datetime = timezone.now()
        return self.filter(
            Q(published_on__lte=current_datetime) & (Q(unpublished_on__gte=current_datetime) | Q(unpublished_on__isnull=True)),
            is_published=True, is_draft=False, user__is_deleted=False
        )

    def annotate_is_live(self):
        current_datetime = timezone.now()
        return self.annotate(
            is_live=Case(
                When(
                    condition=Q(published_on__lte=current_datetime) & (Q(unpublished_on__gte=current_datetime) | Q(unpublished_on__isnull=True)),
                    is_published=True, is_draft=False, user__is_deleted=False,
                    then=True
                ),
                default=False,
                output_field=models.BooleanField()
            )
        )
