import os
import sys
import django
from django.conf import settings

# Add the parent directory to the Python path (path to your project folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Travel-Guide-AI')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelling.settings')

# Setup Django
django.setup()

from guide.models import Place, Image  # Import your models from the 'guide' app

# Debugging: Ensure MEDIA_ROOT is correct
print(f"MEDIA_ROOT is: {settings.BASE_DIR}")

# Define the image folder path
image_folder = os.path.join(settings.BASE_DIR, 'dummy_data/place_images')

# Debugging: Ensure the image folder exists
if not os.path.exists(image_folder):
    print(f"Image folder does not exist: {image_folder}")
else:
    print(f"Image folder found: {image_folder}")

for place in Place.objects.all():
    folder_name = place.name.lower().replace(" ", "_")
    place_folder = os.path.join(image_folder, folder_name)

    # Check if folder exists for the place
    if os.path.exists(place_folder) and os.path.isdir(place_folder):
        for file_name in os.listdir(place_folder):
            image_path = os.path.join(place_folder, file_name)
            if os.path.isfile(image_path):
                with open(image_path, 'rb') as img_file:
                    # Create an image instance and associate it with the place
                    image_instance = Image(
                        place=place,
                    )
                    # Save the image to the database
                    image_instance.image.save(file_name, img_file)
                print(f"Added image {file_name} for Place: {place.name}")
    else:
        print(f"No folder found for Place: {place.name}")
