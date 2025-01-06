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

from accommodation.models import Hotel, HotelImage  # Import your models from the 'accommodation' app

# Debugging: Ensure MEDIA_ROOT is correct
print(f"MEDIA_ROOT is: {settings.BASE_DIR}")

# Define the image folder path
image_folder = os.path.join(settings.BASE_DIR, 'dummy_data/hotel_images')

# Debugging: Ensure the image folder exists
if not os.path.exists(image_folder):
    print(f"Image folder does not exist: {image_folder}")
else:
    print(f"Image folder found: {image_folder}")

# Iterate through all hotels in the database and associate images
for hotel in Hotel.objects.all():
    folder_name = hotel.hotel_name.lower().replace(" ", "_")
    hotel_folder = os.path.join(image_folder, folder_name)

    # Check if the folder exists for the hotel
    if os.path.exists(hotel_folder) and os.path.isdir(hotel_folder):
        for file_name in os.listdir(hotel_folder):
            image_path = os.path.join(hotel_folder, file_name)
            if os.path.isfile(image_path):
                with open(image_path, 'rb') as img_file:
                    # Create an image instance and associate it with the hotel
                    image_instance = HotelImage(
                        hotel=hotel,
                        name=file_name  # Storing the file name as 'name'
                    )
                    # Save the image to the database
                    image_instance.image.save(file_name, img_file)
                print(f"Added image {file_name} for Hotel: {hotel.hotel_name}")
    else:
        print(f"No folder found for Hotel: {hotel.hotel_name}")

