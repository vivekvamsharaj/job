# WorkNear — Daily Wage Worker Job Portal

WorkNear connects daily-wage workers with local employers. The interface includes English, Telugu (తెలుగు), and Hindi (हिन्दी), job posting, applications, distance-based search, and map directions.

## Features
- Worker and owner accounts
- Passwords stored as hashes
- Job posting with daily wage, date, skills, worksite address and coordinates
- Nearby job search within a selected radius (10 km by default)
- Browser GPS permission or manual coordinates
- Leaflet / OpenStreetMap map markers
- Google Maps directions link
- Owner can review applications and accept/reject workers
- English, Telugu and Hindi interface labels

## Technology
- Python + Flask
- MongoDB + Flask-PyMongo
- Bootstrap 5, HTML, CSS, JavaScript
- Leaflet + OpenStreetMap

## Run locally (Windows / VS Code)

1. Install Python 3.10+ and MongoDB Community Server, and start the MongoDB service.
2. Extract this project and open the `WorkNear` folder in VS Code.
3. Open a terminal in that folder and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and use `.\.venv\Scripts\python.exe app.py` for the following steps instead.

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

MongoDB defaults to `mongodb://localhost:27017/worknear`. To use another database, set `MONGO_URI` before starting the app.

## Test the portal
1. Register one account as **Job Owner**.
2. Post a job with a worksite address and valid latitude/longitude.
3. Register a second account as **Worker**.
4. Open Nearby Jobs and use **Use browser location**, or leave the default Hyderabad search coordinates / enter coordinates through the query parameters.
5. Apply for a job. The owner can review applications in the owner dashboard.
6. When the owner accepts an application, the worker dashboard shows directions to the worksite.

Example Hyderabad coordinates for testing:
- Latitude: `17.3850`
- Longitude: `78.4867`

Use a location near the example coordinates when testing the 10 km filter. Coordinates must be valid decimal latitude/longitude.

## Push to GitHub

Create an empty GitHub repository, then run these commands from this folder:

```powershell
git init
git add .
git commit -m "Initial WorkNear daily wage job portal"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your repository URL. Do not upload passwords, secret keys, database credentials, or real user information.

## Before deployment
- Set a strong `SECRET_KEY` environment variable.
- Set `MONGO_URI` to your hosted MongoDB connection string.
- Set `FLASK_DEBUG=false`.
- Deploy behind HTTPS; browser geolocation generally requires a secure context.
- Add phone OTP verification, CSRF protection, rate limiting, owner/worker identity checks and a privacy policy before public use.
- For real users, review privacy and consent before exposing a precise worksite address. This is a college project starter and is not production-hardened.
