from django.db import models
from treebeard.mp_tree import MP_Node
from common.models import BaseImageModel


class Category(BaseImageModel,MP_Node):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    alt_text = models.TextField(max_length=126, blank=True, null=True, help_text='Alt text field for images in categories')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ['name']

    pass

    def activate_descendants(self):
        """
        Activate all descendants of this category.
        """
        descendants = self.get_descendants()
        for descendant in descendants:
            descendant.is_active = True
            descendant.save()

    def deactivate_descendants(self):
        """
        Deactivate all descendants of this category.
        """
        descendants = self.get_descendants()
        for descendant in descendants:
            descendant.is_active = False
            descendant.save()

    def save(self, *args, **kwargs):
        if not self.is_active:  # Check if the category is being deactivated
            self.deactivate_descendants()  # Deactivate all descendants
        elif self.is_active:  # Check if the category is being activated
            self.activate_descendants()  # Activate all descendants
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        level_indicator = '→' * self.depth  # Use arrows (→) for indentation
        return '%s %s' % (level_indicator, self.name)