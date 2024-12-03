from django.db import models
class Place(models.Model):
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.TextField()
    speciality = models.TextField()
    attractions = models.TextField()
    location_url = models.URLField()
    nearest_cities = models.TextField()
    state = models.CharField(max_length=100)
    airports = models.TextField()
    railway_stations = models.TextField()
    road_distance = models.TextField()
    images = models.ImageField(upload_to='place_images/', null=True, blank=True)

    def __str__(self):
        return self.name

