# # chat/models.py

# from django.db import models
# from django.contrib.auth.models import User
# from guide.models import Guide
# from datetime import timedelta
# from django.utils import timezone


# class GuideRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Assuming you have a Guide model
#     guide = models.ForeignKey('guide.Guide', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('pending', 'Pending'), (
#         'accepted', 'Accepted'), ('rejected', 'Rejected'), ('time_out', 'Timed Out')], default='pending')
#     created_at = models.DateTimeField(default=timezone.now)
#     expires_at = models.DateTimeField(default=timezone.now(
#     ) + timedelta(minutes=3))  # Default 3 minutes expiration

#     def __str__(self):
#         return f"Request from {self.user.username} to {self.guide.name}"


# class ChatMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     guide_request = models.ForeignKey(GuideRequest, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.user.username} at {self.timestamp}"
