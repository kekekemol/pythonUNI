# HeartSense authentication, migration fix, and palette redesign

## Critical fixes

1. `predictor/migrations/0002_patient_user.py` is included and the bundled `db.sqlite3` has been migrated.
2. `STATICFILES_DIRS = [BASE_DIR / 'static']` was added to `heart_project/settings.py` so the project-level stylesheet is actually discovered and served by Django during development.
3. `RUN_PROJECT.cmd` now runs `manage.py check`, then `manage.py migrate --noinput`, then starts the server. This prevents the `no such column: predictor_patient.user_id` error when starting through the script.
4. Time zone is set to `Asia/Kuala_Lumpur` for local timestamps.

## Authentication retained

- Sign up, login and logout using Django authentication.
- Prediction pages require authentication.
- New prediction records are linked to the signed-in account.
- Normal users only see/download their own records.
- Staff accounts may access all patient prediction records.

## New design palette

The supplied palette was used directly:

- Navy: `#012C4B`
- Blue: `#005395`
- Magenta: `#C711A4`
- Mauve: `#8A3D7B`
- Plum: `#5D0247`

## Design improvements

- Dark branded navigation bar with icon-based navigation and user chip.
- More substantial dashboard hero area with layered palette accents.
- Three redesigned statistic cards.
- Improved prediction-result panel with circular confidence visualization.
- Clinical form split into three visually distinct sections.
- Icons/symbols added to patient details, measurements, diagnostics, history, PDF and account actions.
- Redesigned side information cards.
- History page now has a strong banner, legend, refined table and PDF controls.
- Login and sign-up pages use split visual/form layouts and password show/hide buttons.
- Responsive styling for tablet and mobile screens.
- Footer and application branding redesigned to match the palette.

## If updating an existing copy

Keep your existing `venv` and `db.sqlite3` if you want to preserve installed packages, accounts and previous records. Copy the new source files over the old project, then run:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Or double-click `RUN_PROJECT.cmd`, which performs the migration automatically before starting the server.
