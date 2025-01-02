from django.contrib import admin
from .models import Place, Guide, Doctor,Image

admin.site.register(Place)
admin.site.register(Image)
admin.site.register(Guide)
admin.site.register(Doctor)

