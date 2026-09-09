# Heart Disease Prediction Using Machine Learning

## Nearby hospital finder (free OpenStreetMap / Overpass API)

The dashboard includes a location-based hospital finder. It searches up to six
hospitals within 5, 10, or 25 km, ranked by approximate straight-line distance,
with available addresses and OpenStreetMap links. It works independently of the
prediction result. **No signup, API key, billing account, or prepayment is needed.**
The former Google Places integration and key setting have been removed.

### Enable live searches

1. In PowerShell, from this project directory, start Django:

   ```powershell
   .\.venv\Scripts\python.exe manage.py runserver
   ```

   Alternatively, double-click `RUN_PROJECT.cmd`. No key configuration is needed.
2. Sign in at `http://127.0.0.1:8000/`, click **Find nearby hospitals**, and allow
   browser location access. Geolocation needs localhost or HTTPS.

An internet connection is required. OpenStreetMap is community-maintained, so
coverage and address details can be incomplete. Google ratings are no longer
shown. Distances are calculated to mapped points or area centers, not driving
routes; only hospitals whose representative point is within the radius appear.
The OpenStreetMap link opens the map website for manual browsing if location
permission is denied or the API is busy. Results are real API data, not simulated.

### How the code works

- `predictor/places.py`: sends a bounded Overpass QL query to
  `https://overpass-api.de/api/interpreter` for nodes, ways, and relations tagged
  `amenity=hospital` or `healthcare=hospital`. Calculates great-circle distances,
  removes duplicate OSM IDs, sorts results, and returns the nearest six.
  The query has a 20-second execution limit and HTTP has a 30-second timeout.
  Overpass partial results with runtime errors are treated as service failures.
- `predictor/views.py`, `nearby_hospitals`: authenticated, CSRF-protected JSON
  POST endpoint at `/api/hospitals/nearby/`; validates coordinates and radius.
- `predictor/templates/hospital_finder.html`: dashboard search controls.
- `static/js/hospitals.js`: requests permission, submits coordinates, renders
  returned text safely, and handles loading, denied permission, and failures.
- Search requests contain coordinates and radius,
  not medical predictions or patient contact information. Neither locations nor
  hospital results are written to the database. Responses disable caching.
- A 10-second cooldown per user limits repeated calls. Django's default cache
  is per process. Requests happen only on a user's click, with no automatic
  retries, background polling, or autocomplete. No new dependencies or migrations.
- OpenStreetMap contributor attribution and an ODbL copyright link are displayed.
- The public Overpass instance is shared and may throttle or time out. This
  setup is intended for a small local coursework demonstration. Its operator
  discourages production apps relying on the shared public backend; for wider
  deployment, arrange a dedicated provider or self-hosted instance. The published
  broad fair-use guideline is below 10,000 requests and 1 GB downloaded per day;
  these are not guaranteed capacity or a service-level agreement.

Tests use mocked Overpass responses and do not contact an external API:

```powershell
.\.venv\Scripts\python.exe manage.py test predictor
```

References: [Overpass public-service guidance](https://dev.overpass-api.de/overpass-doc/en/preface/commons.html),
[Overpass QL](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL),
[OpenStreetMap attribution](https://www.openstreetmap.org/copyright).

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
