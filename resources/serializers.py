# resources/serializers.py
from rest_framework import serializers
from .models import ResourceLink, ResourceSet, ResourceSetMembership
import os

# UPDATED: The serializer for a link within a set now includes the order
class ContainedLinkSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(source='resourcesetmembership_set.first.order', read_only=True)
    class Meta:
        model = ResourceLink
        fields = ['id', 'title', 'order']

# ... (NavLinkSerializer remains the same) ...

class NavLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLink
        fields = ['id', 'title']

class ResourceLinkSerializer(serializers.ModelSerializer):
    # ... (existing fields)
    tags = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField()
    url = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    set_id = serializers.SerializerMethodField()
    # NEW: Add set_title
    set_title = serializers.SerializerMethodField()
    next_resource = serializers.SerializerMethodField()
    previous_resource = serializers.SerializerMethodField()
    
    class Meta:
        model = ResourceLink
        fields = [
            'id', 'title', 'description', 'category', 'url', 'tags', 'created_at', 
            'link_type', 'file_type', 'set_id', 'set_title', 'next_resource', 'previous_resource'
        ]

    def get_url(self, obj): return obj.get_url()
    def get_file_type(self, obj): # ... (same as before) ...
        if obj.link_type == 'UPLOAD' and obj.file:
            name, extension = os.path.splitext(obj.file.name); extension = extension.lower()
            if extension in ['.jpg', '.jpeg', '.png', '.gif', '.svg']: return 'image'
            if extension == '.pdf': return 'pdf'
        return None
        
    def get_set_membership(self, obj):
        # Helper to get the first membership (assuming one resource is in one set max)
        return obj.resourcesetmembership_set.first()

    def get_set_id(self, obj):
        membership = self.get_set_membership(obj)
        return membership.resource_set.id if membership else None
        
    def get_set_title(self, obj):
        membership = self.get_set_membership(obj)
        return membership.resource_set.title if membership else None

    def _get_adjacent_resource(self, obj, next=True):
        membership = self.get_set_membership(obj)
        if not membership: return None
        resource_set = membership.resource_set; current_order = membership.order
        if next: adjacent_membership = ResourceSetMembership.objects.filter(resource_set=resource_set, order__gt=current_order).order_by('order').first()
        else: adjacent_membership = ResourceSetMembership.objects.filter(resource_set=resource_set, order__lt=current_order).order_by('-order').first()
        if adjacent_membership: return NavLinkSerializer(adjacent_membership.resource_link).data
        return None
    def get_next_resource(self, obj): return self._get_adjacent_resource(obj, next=True)
    def get_previous_resource(self, obj): return self._get_adjacent_resource(obj, next=False)


# ... (ResourceSetSerializer for the list view remains the same) ...
class ResourceSetSerializer(serializers.ModelSerializer):
    first_resource_id = serializers.SerializerMethodField()
    class Meta:
        model = ResourceSet
        fields = ['id', 'title', 'description', 'version', 'published_date', 'first_resource_id']
    def get_first_resource_id(self, obj):
        first_membership = obj.resourcesetmembership_set.order_by('order').first()
        return first_membership.resource_link.id if first_membership else None

# UPDATED: The detailed serializer for a single set now returns more data
class ResourceSetDetailSerializer(serializers.ModelSerializer):
    resources = serializers.SerializerMethodField()

    class Meta:
        model = ResourceSet
        fields = ['id', 'title', 'description', 'version', 'published_date', 'resources']

    def get_resources(self, obj):
        # This custom method retrieves all memberships, gets the related resource_link for each,
        # and serializes it along with the order.
        memberships = obj.resourcesetmembership_set.order_by('order')
        
        # Manually construct the data to include the order
        resource_data = []
        for membership in memberships:
            resource_data.append({
                'id': membership.resource_link.id,
                'title': membership.resource_link.title,
                'order': membership.order
            })
        return resource_data
