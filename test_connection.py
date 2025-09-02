#!/usr/bin/env python3
"""
Test script to verify Firebase Storage connection
Run this in your Django project root directory
"""

import os
from pathlib import Path
from google.cloud import storage

# Update this path to match your project structure
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'google-cloud-credentials.json')
BUCKET_NAME = 'customer-support-resources.firebasestorage.app'

def test_connection():
    try:
        print("1. Testing credentials file...")
        if not os.path.exists(CREDENTIALS_PATH):
            print(f"❌ Credentials file not found at: {CREDENTIALS_PATH}")
            return False
        print(f"✅ Credentials file found at: {CREDENTIALS_PATH}")
        
        print("\n2. Testing Google Cloud Storage connection...")
        # Set the credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH
        
        # Initialize client
        client = storage.Client()
        print("✅ Google Cloud Storage client initialized")
        
        print("\n3. Testing bucket access...")
        bucket = client.bucket(BUCKET_NAME)
        
        # Try to get bucket info
        bucket.reload()
        print(f"✅ Successfully connected to bucket: {bucket.name}")
        print(f"   Bucket location: {bucket.location}")
        print(f"   Bucket storage class: {bucket.storage_class}")
        
        print("\n4. Testing file upload...")
        # Create a test blob
        blob = bucket.blob('test-connection.txt')
        test_content = "This is a test file from Django"
        
        blob.upload_from_string(test_content, content_type='text/plain')
        blob.make_public()
        
        print(f"✅ Test file uploaded successfully!")
        print(f"   Public URL: {blob.public_url}")
        
        # Clean up test file
        blob.delete()
        print("✅ Test file deleted successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("Testing Firebase Storage Connection...")
    print("=" * 50)
    
    success = test_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Your Firebase Storage is configured correctly.")
    else:
        print("❌ Tests failed. Check the errors above.")
        print("\nCommon solutions:")
        print("- Verify your google-cloud-credentials.json file exists and is valid")
        print("- Check that your service account has 'Storage Object Admin' permissions")
        print("- Ensure your bucket name is correct")
        print("- Make sure you've enabled the Cloud Storage API in Google Cloud Console")