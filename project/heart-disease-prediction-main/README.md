# Heart Disease Prediction Using Machine Learning

## Nearby hospital finder (Google Places API)

The dashboard includes a location-based hospital finder. It searches up to six
hospitals within 5, 10, or 25 km, ranked by distance, with addresses, ratings,
and Google Maps links. It works independently of the prediction result.

### Enable live searches

1. In Google Cloud, select a project, enable billing and **Places API (New)**,
   then create an API key. Restrict it to Places API (New); for deployment, use
   appropriate server IP restrictions. Configure quotas in Google Cloud.
2. In PowerShell, from this project directory, set the key and start Django:

   ```powershell
   $env:GOOGLE_PLACES_API_KEY = "YOUR_KEY_HERE"
   .\.venv\Scripts\python.exe manage.py runserver
   ```

   The environment variable must exist in the process starting Django. Setting
   it in a terminal does not configure a separately double-clicked launcher.
   Alternatively, run `.\RUN_PROJECT.cmd` from that same PowerShell window.
   Restart an existing server after setting the key. `.env` is not loaded
   automatically. Never commit a real key or place one in JavaScript/templates.
3. Sign in at `http://127.0.0.1:8000/`, click **Find nearby hospitals**, and allow
   browser location access. Geolocation needs localhost or HTTPS.

Without a key, the dashboard offers a direct Google Maps search link. There are
no simulated hospitals or results. A Maps link is also available if location is
denied, there are no results, or Google is unavailable.

### How the code works

- `predictor/places.py`: calls Google's Nearby Search (New) endpoint with a
  10-second timeout and an explicit field mask. Ratings use the Enterprise
  billing tier; check current pricing before enabling live use.
- `predictor/views.py`, `nearby_hospitals`: authenticated, CSRF-protected JSON
  POST endpoint at `/api/hospitals/nearby/`; validates coordinates and radius.
- `predictor/templates/hospital_finder.html`: dashboard search controls.
- `static/js/hospitals.js`: requests permission, submits coordinates, renders
  returned text safely, and handles loading, denied permission, and failures.
- The key stays on the server. Search requests contain coordinates and radius,
  not medical predictions or patient contact information. Neither locations nor
  Google results are written to the database. Responses disable caching.
- A 10-second cooldown per user limits repeated calls. Django's default cache
  is per process; use a shared cache and provider quotas for a multiworker site.
- Google Maps attribution and returned third-party attributions are displayed.
  Before public deployment, publish Terms of Use and a Privacy Policy as
  required by Google Maps Platform, describing location sharing.

Tests use mocked Google responses and require no key or billable API calls:

```powershell
.\.venv\Scripts\python.exe manage.py test predictor
```

References: [Nearby Search documentation](https://developers.google.com/maps/documentation/places/web-service/nearby-search),
[Places API policies](https://developers.google.com/maps/documentation/places/web-service/policies).

## 📌 Project Overview

Heart Disease Prediction is a Machine Learning based web application that predicts whether a person is likely to have heart disease based on medical parameters.

The Machine Learning model is integrated with a Django web application, allowing users to enter their health-related information and receive a prediction.

## 🚀 Features

- Heart disease prediction using Machine Learning
- Django-based web application
- User-friendly prediction form
- Prediction history stored using SQLite
- Trained ML model saved using Joblib
- PDF report generation
- Separate preprocessing/scaling using a saved scaler

## 🛠️ Technologies Used

- Python
- Django
- Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib
- SQLite
- HTML
- CSS
- JavaScript

## 🤖 Machine Learning

The project uses a trained Machine Learning model to predict the possibility of heart disease from medical input parameters.

The trained model and scaler are saved as:

- `heart_model.pkl`
- `scaler.pkl`

## 📊 Dataset

The project uses a heart disease dataset containing medical attributes such as:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- ST Depression
- Slope
- Number of Major Vessels
- Thalassemia

## 🌐 Django Integration

Django is used to build the web application and connect the Machine Learning model with the user interface.

The application accepts user input, preprocesses the data, sends it to the trained model, and displays the prediction result.

## 🗄️ Database

SQLite is used to store prediction history.

## 📄 PDF Report

The application also provides functionality to generate a PDF report containing prediction-related information.

## 💻 How to Run the Project
Follow the steps below to run the Heart Disease Prediction web application locally.


### 1. Clone the Repository

```bash
git clone https://github.com/Nikitavaitkar/heart-disease-prediction.git
```

### 2. Navigate to the Project Folder

```bash
cd heart-disease-prediction
```

## ⚙️ Installation

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

```bash
.venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements-minimal.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Django Development Server

```bash
python manage.py runserver
```

You can also double-click `RUN_PROJECT.cmd`. It uses this project's `.venv` automatically.

### 6. Open the Application

Open your browser and visit:

http://127.0.0.1:8000/

## 🔐 Authentication Update

This version includes Django account authentication. Users must create an account or log in before running predictions. New prediction records are linked to the signed-in user, and normal users can only view/download their own records. Staff users retain access to all records.

After updating the project, run:

```bash
python manage.py migrate
python manage.py runserver
```
