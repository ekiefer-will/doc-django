# resources/models.py
from django.db import models
from markdownx.models import MarkdownxField

# ... (ProductCategory and Tag models remain the same) ...
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Product categories"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class ResourceSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, blank=True)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class ResourceLink(models.Model):
    # ... (Most fields remain the same) ...
    LINK_TYPE_CHOICES = [('EXTERNAL', 'External URL'), ('UPLOAD', 'File Upload'),]
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link_type = models.CharField(max_length=10, choices=LINK_TYPE_CHOICES, default='EXTERNAL')
    url = models.URLField(max_length=500, blank=True, help_text="Use this for an External URL.")
    file = models.FileField(upload_to='resources/', blank=True, help_text="Use this for a File Upload.")
    
    # NEW: Add a relationship to the ResourceSet through our new model
    sets = models.ManyToManyField(ResourceSet, through='ResourceSetMembership')

    def get_url(self):
        if self.link_type == 'UPLOAD' and self.file:
            return self.file.url
        return self.url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class ResourceSetMembership(models.Model):
    resource_set = models.ForeignKey(ResourceSet, on_delete=models.CASCADE)
    resource_link = models.ForeignKey(ResourceLink, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('resource_set', 'resource_link')