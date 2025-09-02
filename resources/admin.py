# resources/admin.py
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import ResourceLink, Tag, ProductCategory, ResourceSet, ResourceSetMembership

# ... (ResourceLinkAdmin, Tag, ProductCategory admins remain the same) ...
class ResourceLinkAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category', 'link_type', 'created_at')
    list_filter = ('category', 'tags', 'link_type')
    search_fields = ('title', 'description')
    fieldsets = ( (None, {'fields': ('title', 'description', 'category', 'tags')}), ('Link Configuration', {'fields': ('link_type', 'url', 'file'),}),)
    class Media: js = ('admin/js/resource_link_admin.js',)

class ResourceSetMembershipInline(admin.TabularInline):
    model = ResourceSetMembership
    extra = 1 # Show one extra empty slot

@admin.register(ResourceSet)
class ResourceSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'published_date')
    inlines = (ResourceSetMembershipInline,)

admin.site.register(ResourceLink, ResourceLinkAdmin)
admin.site.register(Tag)
admin.site.register(ProductCategory)