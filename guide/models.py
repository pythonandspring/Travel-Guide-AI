from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.TextField()
    speciality = models.TextField()
    attraction_info = models.TextField()
    location_url = models.URLField()
    nearest_cities = models.TextField()  
    airports = models.TextField()  
    railway_stations = models.TextField()  
    by_road_distances = models.TextField()  
    images = models.ImageField(upload_to='place_images/')

    # super_guide = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supervised_places')
    # related_guides = models.ManyToManyField(User, related_name='accessible_places')

    def __str__(self):
        return self.name
    

class Guide(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    is_super_guide = models.BooleanField(default=False)
    state = models.CharField(max_length=50, choices=[])
    city = models.CharField(max_length=50, choices=[])
    place = models.CharField(max_length=50, choices=[])

    def __str__(self):
        return f"{self.name} - {'Super Guide' if self.is_super_guide else 'Guide'}"
    
class Doctor(models.Model):
    guide = models.ForeignKey("app.Model", verbose_name=(""), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    availability = models.CharField(max_length=100, help_text="E.g., Mon-Fri, 9 AM - 5 PM")
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="doctors")

    def __str__(self):
        return f"{self.name} - {self.specialty}"