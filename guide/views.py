from django.shortcuts import render, get_object_or_404, redirect
from .models import Place, Guide
from django.contrib.auth.decorators import login_required

@login_required
def add_place(request):
    if request.method == "POST":
        # Collect data from POST request
        name = request.POST['name']
        area = request.POST['area']
        city = request.POST['city']
        address = request.POST['address']
        speciality = request.POST['speciality']
        attractions = request.POST['attractions']
        location_url = request.POST['location_url']
        nearest_cities = request.POST['nearest_cities']
        state = request.POST['state']
        airports = request.POST['airports']
        railway_stations = request.POST['railway_stations']
        road_distance = request.POST['road_distance']
        
        # Create the Place
        place = Place.objects.create(
            name=name,
            area=area,
            city=city,
            address=address,
            speciality=speciality,
            attractions=attractions,
            location_url=location_url,
            nearest_cities=nearest_cities,
            state=state,
            airports=airports,
            railway_stations=railway_stations,
            road_distance=road_distance,
        )
        # Assign current guide as Super Guide
        guide = Guide.objects.get(user=request.user)
        place.super_guide = guide
        place.save()

        return redirect('gallery')
    return render(request, 'add_place.html')

def gallery(request):
    places = Place.objects.all()
    return render(request, 'gallery.html', {'places': places})
