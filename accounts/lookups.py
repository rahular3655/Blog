from ajax_select import register, LookupChannel
from .models import User
from django.db.models import Q


@register('users')
class TagsLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(Q(email__icontains=q) | Q(username__icontains=q), is_active=True, is_author=True, is_deleted=False).order_by(
            'email')[:50]

    def format_item_display(self, item):
        return "<text class='user text-primary'>%s</text>" % item.username
