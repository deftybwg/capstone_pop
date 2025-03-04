from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import WorkoutLog, WorkoutEntry, WorkoutWeek
from functools import wraps

import json, re

@login_required
def profile_redirect(request):
    return redirect("profile")


def login_required_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")  # Redirects to login page if not logged in
        return func(request, *args, **kwargs)
    return wrapper

@login_required
def profile_view(request):
    user = request.user
    weeks = WorkoutWeek.objects.filter(user=user).order_by("-number")
    formatted_weeks = []

    for week in weeks:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        week_data = {
            "number": week.number,
            "days": days,
            "entries": {day: "" for day in days},  # Default empty values
        }

        # Calculate total hours for this week
        total_hours = 0
        for entry in WorkoutEntry.objects.filter(week=week):
            week_data["entries"][entry.day] = entry.value  # Store log entry

            # Extract numerical values from "xh" formatted strings
            matches = re.findall(r"(\d+(\.\d+)?)h", entry.value)
            total_hours += sum(float(match[0]) for match in matches)

        # Ensure "Total" is added correctly and does not duplicate
        week_data["entries"]["Total"] = f"{round(total_hours, 1)}h" if total_hours > 0 else "0h"

        formatted_weeks.append(week_data)

    return render(request, "profile.html", {"weeks": formatted_weeks, "user_profile": user})




@login_required
def create_week(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user

            # Get the latest week number for this user
            last_week = WorkoutWeek.objects.filter(user=user).order_by("-number").first()
            next_week_number = (last_week.number + 1) if last_week else 1

            # Ensure we are not creating a duplicate week
            if WorkoutWeek.objects.filter(user=user, number=next_week_number).exists():
                return JsonResponse({"status": "error", "message": "Week already exists"})

            # Create new week
            WorkoutWeek.objects.create(user=user, number=next_week_number)

            return JsonResponse({"status": "success", "week_number": next_week_number})

        except Exception as e:
            print("Error creating week:", e)  # Debugging
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@login_required
def update_entry(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            week_number = data.get("week_number")
            day = data.get("day")
            value = data.get("value")

            # Get the correct week
            week = WorkoutWeek.objects.get(user=request.user, number=week_number)

            # Update or create the entry for this day
            entry, created = WorkoutEntry.objects.update_or_create(
                week=week,
                day=day,
                column=0,  # Always use column 0 since there's only one editable column
                defaults={"value": value}
            )

            return JsonResponse({"status": "success", "updated": not created})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")  # Redirect to login page after success
        else:
            for error in form.errors.values():
                messages.error(request, error)  # Capture form errors (like weak password)

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})



def index_view(request):
    return render(request, "index.html")