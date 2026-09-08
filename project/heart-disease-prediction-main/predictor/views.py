from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
import joblib
import os
import json
import math

from .forms import LoginForm, SignUpForm
from .models import Patient
from .pdf import generate_pdf
from .places import PlacesUnavailable, search_hospitals


# Load the trained ML model and the scaler once when Django starts.
model_path = os.path.join(os.path.dirname(__file__), "heart_model.pkl")
model = joblib.load(model_path)

scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")
scaler = joblib.load(scaler_path)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.first_name or user.username}.")
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect("home")

    return render(request, "registration/login.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully. You are now signed in.")
        return redirect("home")

    return render(request, "registration/signup.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("login")


@login_required
def home(request):
    result = None
    confidence = None

    if request.method == "POST":
        try:
            # Patient details
            name = request.POST["name"].strip()
            email = request.POST["email"].strip()
            phone = request.POST["phone"].strip()

            # Medical inputs
            age = float(request.POST["age"])
            sex = int(request.POST["sex"])
            cp = int(request.POST["cp"])
            trestbps = float(request.POST["trestbps"])
            chol = float(request.POST["chol"])
            fbs = int(request.POST["fbs"])
            restecg = int(request.POST["restecg"])
            thalach = float(request.POST["thalach"])
            exang = int(request.POST["exang"])
            oldpeak = float(request.POST["oldpeak"])
            slope = int(request.POST["slope"])
            ca = int(request.POST["ca"])
            thal = int(request.POST["thal"])

            data = [[
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal,
            ]]

            scaled_data = scaler.transform(data)
            prediction = model.predict(scaled_data)[0]
            probability = model.predict_proba(scaled_data)
            confidence = round(max(probability[0]) * 100, 2)
            result = "Heart Disease Detected" if prediction == 1 else "No Heart Disease Detected"
            gender = "Male" if sex == 1 else "Female"

            Patient.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                age=int(age),
                gender=gender,
                prediction=result,
                confidence=confidence,
            )
            messages.success(request, "Prediction completed and saved to your history.")
        except (KeyError, TypeError, ValueError):
            messages.error(request, "Please check the form values and try again.")
        except Exception:
            messages.error(request, "The prediction could not be completed. Please try again.")

    user_predictions = Patient.objects.filter(user=request.user)
    stats = {
        "total": user_predictions.count(),
        "positive": user_predictions.filter(prediction="Heart Disease Detected").count(),
        "negative": user_predictions.filter(prediction="No Heart Disease Detected").count(),
    }

    full_name = request.user.get_full_name().strip()
    return render(
        request,
        "index.html",
        {
            "result": result,
            "confidence": confidence,
            "stats": stats,
            "default_name": full_name or request.user.username,
            "default_email": request.user.email,
            "hospital_search_enabled": bool(settings.GOOGLE_PLACES_API_KEY),
        },
    )


@never_cache
@require_POST
def nearby_hospitals(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Please sign in again to find hospitals."}, status=401)
    if not settings.GOOGLE_PLACES_API_KEY:
        return JsonResponse({"error": "Hospital search is not available yet."}, status=503)
    try:
        if len(request.body) > 1024:
            raise ValueError
        data = json.loads(request.body)
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        radius = float(data.get("radius", 10000))
        if any(isinstance(data.get(key), bool) for key in ("latitude", "longitude", "radius")):
            raise ValueError
        if not all(math.isfinite(value) for value in (latitude, longitude, radius)):
            raise ValueError
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError
        if radius not in (5000, 10000, 25000):
            raise ValueError
    except (ValueError, TypeError, KeyError, UnicodeDecodeError):
        return JsonResponse({"error": "Provide a valid location and search radius."}, status=400)
    # Only a short user cooldown is cached, never coordinates or Google results.
    if not cache.add(f"hospital-search:{request.user.pk}", True, timeout=10):
        response = JsonResponse({"error": "Please wait 10 seconds before searching again."}, status=429)
        response["Retry-After"] = "10"
        return response
    try:
        hospitals = search_hospitals(latitude, longitude, radius, settings.GOOGLE_PLACES_API_KEY)
    except PlacesUnavailable:
        return JsonResponse({"error": "Hospital search is temporarily unavailable. Please try again later."}, status=502)
    return JsonResponse({"hospitals": hospitals})


@login_required
def history(request):
    if request.user.is_staff:
        patients = Patient.objects.all().order_by("-created_at")
    else:
        patients = Patient.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "history.html", {"patients": patients})


@login_required
def download_pdf(request, patient_id):
    if request.user.is_staff:
        patient = get_object_or_404(Patient, id=patient_id)
    else:
        patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    pdf = generate_pdf(patient)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Patient_{patient.id}.pdf"'
    return response
