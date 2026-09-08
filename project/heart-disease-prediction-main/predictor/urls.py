from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("history/", views.history, name="history"),
    path("api/hospitals/nearby/", views.nearby_hospitals, name="nearby_hospitals"),
    path("download/<int:patient_id>/", views.download_pdf, name="download_pdf"),
]
