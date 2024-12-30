# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import GuideRequest, Guide
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_request(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    user = request.user  # Current logged-in user

    # Check if the guide is available (not occupied)
    if guide.is_occupied:
        messages.error(
            request, "This guide is currently occupied. Please try later.")
        # Assuming 'get_guides' is the page with the list of guides
        return redirect('get_guides')

    # Create a new GuideRequest
    new_request = GuideRequest(
        user=user,
        guide=guide,
        status='pending',
        created_at=timezone.now(),
        # Set expiration time (3 minutes)
        expires_at=timezone.now() + timedelta(minutes=3)
    )
    new_request.save()

    # Notify guide about the request via WebSocket (real-time)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"guide_{guide.id}",  # Group name for the guide
        {
            "type": "guide.request",
            "message": {
                "request_id": new_request.id,
                "user_name": user.username,
                "status": new_request.status,
                "expires_at": new_request.expires_at.isoformat()
            }
        }
    )

    messages.success(request, "Your request has been sent to the guide!")
    # Redirect to the waiting page
    return redirect('waiting_page', request_id=new_request.id)


def waiting_page(request, request_id):
    user_request = get_object_or_404(GuideRequest, id=request_id)
    return render(request, 'chat/waiting_page.html', {'user_request': user_request})


def chat_page(request, request_id):
    # Fetch the GuideRequest based on the provided request_id
    guide_request = get_object_or_404(GuideRequest, id=request_id)

    # Add any other context variables you need for the chat page
    return render(request, 'chat/chat_page.html', {'guide_request': guide_request})


def guide_requests(request):
    if request.session.get('super_guide_id') or request.session.get('guide_id'):
        try:
            guide_id = request.session.get('super_guide_id')
            guide = Guide.objects.get(id=guide_id)
        except Guide.DoesNotExist:
            guide_id = request.session.get('guide_id')
            guide = Guide.objects.get(id=guide_id)
        finally:
            guide_requests = GuideRequest.objects.filter(
                guide=guide)  # Adjust based on your model structure
            return render(request, 'chat/guide_requests.html', {'guide_requests': guide_requests})
    else:
        return redirect('guide_login')
    