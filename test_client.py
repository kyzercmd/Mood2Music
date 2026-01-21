import requests

url = "http://localhost:8000/analyze"

# We use a tuple: (filename, file_object, content_type)
# This forces the server to see it as an image, preventing the 400 Error.
files = {
    'file': ('test_image.jpg', open('test_image.PNG', 'rb'), 'image/jpeg')
}

try:
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        print("✅ Success!")
        print(response.json())
    else:
        print(f"❌ Error {response.status_code}:")
        print(response.text)

except Exception as e:
    print(f"Connection failed: {e}")