from models import Place
cities = Place.objects.filter().values('city')
print(cities)

