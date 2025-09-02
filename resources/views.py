from rest_framework import viewsets
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import qrcode
import io
from .models import ResourceLink, ResourceSet
from .serializers import ResourceLinkSerializer, ResourceSetSerializer, ResourceSetDetailSerializer

class ResourceLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows resource links to be viewed.
    """
    queryset = ResourceLink.objects.all()
    serializer_class = ResourceLinkSerializer

class ResourceSetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows resource sets to be viewed.
    Uses different serializers for list and detail views.
    """
    queryset = ResourceSet.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ResourceSetDetailSerializer
        return ResourceSetSerializer

def generate_qr_code(request, pk):
    """
    Generates a QR code for a given ResourceLink's URL.
    """
    link = get_object_or_404(ResourceLink, pk=pk)
    url = link.get_url()

    # Fallback to construct an absolute URL if a relative one is returned.
    # In a correctly configured cloud storage setup, get_url() should be absolute.
    if url.startswith('/'):
        bucket_name = 'your-bucket-name' # Replace with your bucket name or pull from settings
        url = f"https://storage.googleapis.com/{bucket_name}{url}"

    img = qrcode.make(url)
    
    # Create an in-memory binary stream for the image
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # Create the HTTP response with the image
    response = HttpResponse(buf, content_type='image/png')
    
    # Sanitize the title to create a safe filename
    safe_title = "".join([c for c in link.title if c.isalpha() or c.isdigit() or c.isspace()]).rstrip()
    filename = f"{safe_title.replace(' ', '_')}_qr.png"
    
    # Set the Content-Disposition header to make the browser download the file
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
