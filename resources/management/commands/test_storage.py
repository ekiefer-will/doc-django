# resources/management/commands/test_storage.py
# Create the directories: resources/management/commands/ (with __init__.py files in each)

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from resources.models import ResourceLink
import tempfile
import os

class Command(BaseCommand):
    help = 'Test Django file storage with Firebase'

    def handle(self, *args, **options):
        self.stdout.write("Testing Django Storage Configuration...")
        self.stdout.write("=" * 50)
        
        try:
            # Test 1: Check storage backend
            self.stdout.write("1. Checking storage backend...")
            self.stdout.write(f"   Storage class: {default_storage.__class__}")
            self.stdout.write(f"   Storage module: {default_storage.__class__.__module__}")
            
            # Test 2: Test direct storage save
            self.stdout.write("\n2. Testing direct file save...")
            test_content = "This is a test file from Django storage"
            test_file = ContentFile(test_content.encode(), name='django-test.txt')
            
            saved_path = default_storage.save('test-uploads/django-test.txt', test_file)
            self.stdout.write(f"   ✅ File saved to: {saved_path}")
            
            # Test 3: Get URL
            file_url = default_storage.url(saved_path)
            self.stdout.write(f"   ✅ File URL: {file_url}")
            
            # Test 4: Test with model
            self.stdout.write("\n3. Testing with ResourceLink model...")
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
                tmp_file.write("Test content for model upload")
                tmp_file_path = tmp_file.name
            
            try:
                # Create ResourceLink with file
                with open(tmp_file_path, 'rb') as f:
                    resource = ResourceLink.objects.create(
                        title="Test Resource",
                        description="Test upload via management command",
                        link_type='UPLOAD'
                    )
                    
                    # Save file to the model
                    from django.core.files import File
                    resource.file.save(
                        'test-model-upload.txt',
                        File(f),
                        save=True
                    )
                
                self.stdout.write(f"   ✅ ResourceLink created with ID: {resource.id}")
                self.stdout.write(f"   ✅ File URL from model: {resource.get_url()}")
                
                # Clean up
                resource.delete()
                self.stdout.write("   ✅ Test resource deleted")
                
            finally:
                # Clean up temp file
                os.unlink(tmp_file_path)
            
            # Clean up storage test file
            default_storage.delete(saved_path)
            self.stdout.write("   ✅ Test storage file deleted")
            
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(self.style.SUCCESS("✅ All Django storage tests passed!"))
            
        except Exception as e:
            self.stdout.write(f"\n❌ Error: {e}")
            self.stdout.write(f"   Error type: {type(e).__name__}")
            
            import traceback
            self.stdout.write("\nFull traceback:")
            self.stdout.write(traceback.format_exc())
            
            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(self.style.ERROR("❌ Django storage tests failed!"))