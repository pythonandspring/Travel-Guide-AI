from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import EditProfileForm

# @login_required  
# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile') 
#     else:
#         form = EditProfileForm(instance=request.user)

#     return render(request, 'edit_profile.html', {'form': form})
