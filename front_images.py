import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Travel-Guide-AI')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelling.settings')
django.setup()

from guide.models import Place
from django.conf import settings

# Define the folder where images are stored
image_folder = os.path.join(settings.BASE_DIR, 'dummy_data/front_images')

# Ensure the folder exists
if not os.path.exists(image_folder):
    print(f"Image folder does not exist: {image_folder}")
else:
    print(f"Image folder found: {image_folder}")

# Iterate through all Place objects and update their front_image
for place in Place.objects.all():
    # Generate the expected file name based on the place's name
    folder_name =place.name.lower().replace(' ', '_')
    folder_name =place.name.lower().replace(' ', '_')
    file_name = f"FI_{place.name.lower().replace(' ', '_')}.jpg"
    image_path = os.path.join(image_folder, folder_name ,file_name)

    # Check if the image file exists
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            # Save the image file to the front_image field
            place.front_image.save(file_name, img_file)
        print(f"Updated front_image for Place: {place.name}")
    else:
        print(f"Image not found for Place: {place.name}")
