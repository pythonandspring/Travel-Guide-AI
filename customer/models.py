from django.db import models
from datetime import date, timedelta
from django.db import models


class Customer(models.Model):
    
    user_id = models.IntegerField(primary_key=True)  
    user_role_id = models.IntegerField() 
    user_name = models.CharField(max_length=100)  
    user_email = models.EmailField(unique=True)  
    user_dob = models.DateField()  
    user_address = models.CharField(max_length=255) 
    
    def __str__(self):
        return f"{self.user_id} - {self.user_name}"

