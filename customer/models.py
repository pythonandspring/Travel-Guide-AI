from django.db import models
from datetime import date, timedelta
from django.db import models


# Role Class Model
class Role(models.Model):
    role_id = models.IntegerField()  
    role_title = models.CharField(max_length=100)  
    role_description = models.CharField(max_length=255)  

    def __str__(self):
        return self.role_title


class User(models.Model):
    
    user_id = models.IntegerField()  
    user_role_id = models.ForeignKey(Role, on_delete=models.CASCADE) 
    user_name = models.CharField(max_length=100)  
    user_email = models.EmailField(unique=True)  
    user_dob = models.DateField()  
    user_address = models.CharField(max_length=255) 
    
    def __str__(self):
        return f"{self.user_id} - {self.user_name}"
    
