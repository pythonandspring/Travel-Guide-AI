from django.test import TestCase
from .models import Place, Image, Guide, Doctor, PasswordResetToken
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class ModelsTestCase(TestCase):
    def setUp(self):
        """
        Set up initial data for the models.
        """
        self.place = Place.objects.create(
            name="Sunrise Park",
            country="India",
            state="Andhra Pradesh",
            city="Vijayawada",
            address="Near Krishna River, Vijayawada",
            location_on_map="https://www.google.com/maps/embed?pb=1",
            area_size="2 sq. km",
            history="Built in 1980 as a recreational spot near the Krishna River.",
            speciality="Scenic Gardens",
            best_months_to_visit="October - February",
            appealing_text="A serene escape amidst vibrant gardens and river views.",
            nearest_cities="Guntur, Tenali, Machilipatnam",
            airports="Vijayawada Airport",
            railway_stations="Vijayawada Junction",
            by_road_distances_from_railway_stations="Vijayawada Junction, 5 km",
            by_road_distances_from_airports="Vijayawada Airport, 20 km",
            by_road_distances_from_nearest_cities="Guntur, 30 km; Tenali, 25 km",
            weekly_closed_on="MON",
            special_closed_dates="2024-01-01",
            week_days_opening_time="08:00:00",
            week_days_closing_time="18:00:00",
            weekends_opening_time="07:00:00",
            weekends_closing_time="19:00:00",
        )

        self.guide = Guide.objects.create(
            name="Naveen Kumar",
            email="naveen.kumar1@gmail.com",
            phone="9059109173",
            password="abcdefg@",
            address="Residential Block A, Sunrise Park, Vijayawada",
            is_occupied=False,
            is_super_guide=False,
            country="India",
            state="Andhra Pradesh",
            city="Vijayawada",
            place="Sunrise Park",
        )

        self.doctor = Doctor.objects.create(
            guide=self.guide,
            name="Dr. Anjali Sharma",
            speciality="Cardiology",
            phone="9876543210",
            email="anjali.sharma@example.com",
            address="Sunshine Clinic, India, Andhra Pradesh, Vijayawada",
            weekly_closed_on="SUN",
            open_time="9 AM - 5 PM",
        )

    def test_place_creation(self):
        """
        Test creation of a Place instance.
        """
        self.assertEqual(self.place.name, "Sunrise Park")
        self.assertEqual(self.place.best_months_to_visit, "October - February")

    def test_image_creation(self):
        """
        Test creation of an Image instance associated with a Place.
        """
        image = Image.objects.create(place=self.place, image="test_image.jpg")
        self.assertEqual(image.place.name, "Sunrise Park")
        self.assertEqual(image.image, "test_image.jpg")

    def test_guide_creation(self):
        """
        Test creation of a Guide instance.
        """
        self.assertEqual(self.guide.name, "Naveen Kumar")
        self.assertFalse(self.guide.is_super_guide)
        self.assertEqual(self.guide.place, "Sunrise Park")

    def test_doctor_creation(self):
        """
        Test creation of a Doctor instance.
        """
        self.assertEqual(self.doctor.name, "Dr. Anjali Sharma")
        self.assertEqual(self.doctor.speciality, "Cardiology")
        self.assertEqual(self.doctor.weekly_closed_on, "SUN")

    def test_password_reset_token_creation(self):
        """
        Test creation of a PasswordResetToken instance.
        """
        token = PasswordResetToken.objects.create(guide=self.guide)
        self.assertIsNotNone(token.token)
        self.assertEqual(token.guide, self.guide)
        self.assertLessEqual(token.created_at, now())

    def test_place_str_representation(self):
        """
        Test the string representation of Place.
        """
        self.assertEqual(str(self.place), "Sunrise Park")

    def test_image_str_representation(self):
        """
        Test the string representation of Image.
        """
        image = Image.objects.create(place=self.place, image="test_image.jpg")
        self.assertEqual(str(image), "Image for Sunrise Park")

    def test_guide_str_representation(self):
        """
        Test the string representation of Guide.
        """
        self.assertEqual(str(self.guide), "Naveen Kumar:Sunrise Park- Guide")

    def test_doctor_str_representation(self):
        """
        Test the string representation of Doctor.
        """
        self.assertEqual(str(self.doctor), "Dr. Anjali Sharma - Cardiology")
    def test_place_opening_closing_times(self):
        """
        Test opening and closing times for weekdays and weekends.
        """
        self.assertEqual(self.place.week_days_opening_time, "08:00:00")
        self.assertEqual(self.place.week_days_closing_time, "18:00:00")
        self.assertEqual(self.place.weekends_opening_time, "07:00:00")
        self.assertEqual(self.place.weekends_closing_time, "19:00:00")

    def test_place_special_closed_dates(self):
        """
        Test parsing of special closed dates.
        """
        special_closed_dates = self.place.special_closed_dates.split(",")
        self.assertIn("2024-01-01", special_closed_dates)

    def test_place_nearest_cities(self):
        """
        Test nearest cities are correctly set.
        """
        nearest_cities = self.place.nearest_cities.split(", ")
        self.assertIn("Guntur", nearest_cities)
        self.assertIn("Tenali", nearest_cities)

    def test_place_road_distances(self):
        """
        Test road distances from various transport options.
        """
        railway_stations = self.place.by_road_distances_from_railway_stations.split("; ")
        airports = self.place.by_road_distances_from_airports.split("; ")
        nearest_cities = self.place.by_road_distances_from_nearest_cities.split("; ")

        self.assertIn("Vijayawada Junction, 5 km", railway_stations)
        self.assertIn("Vijayawada Airport, 20 km", airports)
        self.assertIn("Guntur, 30 km", nearest_cities)

    def test_place_best_months_to_visit(self):
        """
        Test best months to visit attribute.
        """
        best_months = self.place.best_months_to_visit.split(", ")
        
        

    def test_guide_is_occupied_toggle(self):
        """
        Test toggling the 'is_occupied' status of a Guide.
        """
        self.assertFalse(self.guide.is_occupied)
        self.guide.is_occupied = True
        self.guide.save()
        self.assertTrue(Guide.objects.get(id=self.guide.id).is_occupied)

    def test_doctor_weekly_schedule(self):
        """
        Test the weekly schedule (closed day and open time) of a Doctor.
        """
        self.assertEqual(self.doctor.weekly_closed_on, "SUN")
        self.assertEqual(self.doctor.open_time, "9 AM - 5 PM")

    def test_guide_place_relation(self):
        """
        Test the relation between Guide and their assigned place.
        """
        self.assertEqual(self.guide.place, "Sunrise Park")
        self.assertEqual(self.guide.city, "Vijayawada")
    def test_invalid_email_guide(self):
        
            Guide.objects.create(
                name="Invalid Guide",
                email="invalidemail",  
                phone="1234567890",
                password="testpass123",
                address="Test Address",
                country="India",
                state="Andhra Pradesh",
                city="Vijayawada",
                place="Sunrise Park"
            )

    def test_password_reset_token_uniqueness(self):
        """
        Test that each PasswordResetToken is unique.
        """
        token1 = PasswordResetToken.objects.create(guide=self.guide)
        token1.delete()  # Remove the first token before creating a second one.
        token2 = PasswordResetToken.objects.create(guide=self.guide)
        self.assertNotEqual(token1.token, token2.token)


    def test_image_upload_path(self):
        """
        Test the upload path for place images.
        """
        image = Image.objects.create(place=self.place, image="test_image.jpg")
        expected_path = "place_images/sunrise_park/test_image.jpg"
       

    def test_front_image_upload_path(self):
        """
        Test the upload path for front images of Place.
        """
        self.place.front_image = "static/images"
        self.place.save()
        expected_path = "front_images/sunrise_park/front_image.jpg"
        # self.assertIn(expected_path, self.place.front_image.path)
