from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}, you can now login.")
            return redirect("login")
    else: 
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form} )

@login_required
def streaks(request):
    profile = Profile.objects.get(user=request.user)
    profile.update_streak()
    context = {
            'streak': profile.streak,
        }

    return render(request, "users/streaks.html", context)
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    profile.update_streak()
    if request.method == "POST": #when user submits the form
        u_form = UserUpdateForm(request.POST, instance=request.user) #pass in post data
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) #also passes in file for pfp
        if u_form.is_valid() and p_form.is_valid():  # Make sure the forms are valid before saving
            u_form.save() 
            p_form.save()  
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
            "u_form": u_form,
            "p_form": p_form,
            'profile': profile,
        }
    # Render the profile template with the context

    return render(request, "users/profile.html", context)