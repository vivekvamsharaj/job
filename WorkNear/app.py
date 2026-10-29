from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-before-deploying")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/worknear")
mongo = PyMongo(app)

LANGUAGES = {
    "en": {"brand":"WorkNear", "tagline":"Find daily work close to home", "home":"Home", "jobs":"Nearby Jobs", "login":"Login", "register":"Register", "logout":"Logout", "worker":"Worker", "owner":"Job Owner", "name":"Full name", "phone":"Phone number", "password":"Password", "language":"Language", "skills":"Skills", "location":"Your location", "latitude":"Latitude", "longitude":"Longitude", "find":"Find jobs within 10 km", "post":"Post a job", "title":"Job title", "description":"Description", "wage":"Daily wage (₹)", "date":"Work date", "workers":"Workers needed", "address":"Worksite address", "apply":"Apply", "applied":"Application submitted", "distance":"Distance", "open":"Open", "nojobs":"No jobs found within 10 km.", "dashboard":"Dashboard", "applications":"Applications", "status":"Status", "save":"Save job", "welcome":"Welcome", "nearby":"Jobs near you", "required":"Please fill in all required fields.", "badlogin":"Invalid phone number or password.", "exists":"That phone number is already registered.", "posted":"Job posted successfully.", "appliedmsg":"Your application has been submitted.", "selectloc":"Use browser location", "manual":"Or enter coordinates manually", "accept":"Accept", "reject":"Reject", "pending":"Pending", "accepted":"Accepted", "rejected":"Rejected", "noapps":"No applications yet.", "owneronly":"Only job owners can post jobs.", "workeronly":"Only workers can apply."},
    "te": {"brand":"వర్క్‌నియర్", "tagline":"మీ ఇంటికి దగ్గరలో రోజువారీ పని కనుగొనండి", "home":"హోమ్", "jobs":"దగ్గరలో పనులు", "login":"లాగిన్", "register":"నమోదు", "logout":"లాగ్ అవుట్", "worker":"కార్మికుడు", "owner":"పని యజమాని", "name":"పూర్తి పేరు", "phone":"ఫోన్ నంబర్", "password":"పాస్‌వర్డ్", "language":"భాష", "skills":"నైపుణ్యాలు", "location":"మీ స్థానం", "latitude":"అక్షాంశం", "longitude":"రేఖాంశం", "find":"10 కి.మీ లోపు పనులు కనుగొనండి", "post":"పని ప్రకటించండి", "title":"పని పేరు", "description":"వివరణ", "wage":"రోజువారీ కూలి (₹)", "date":"పని తేదీ", "workers":"కావలసిన కార్మికులు", "address":"పని చిరునామా", "apply":"దరఖాస్తు", "applied":"దరఖాస్తు పంపబడింది", "distance":"దూరం", "open":"తెరవండి", "nojobs":"10 కి.మీ లోపు పనులు లేవు.", "dashboard":"డాష్‌బోర్డ్", "applications":"దరఖాస్తులు", "status":"స్థితి", "save":"పనిని సేవ్ చేయండి", "welcome":"స్వాగతం", "nearby":"మీ దగ్గరలో పనులు", "required":"అవసరమైన వివరాలను నమోదు చేయండి.", "badlogin":"ఫోన్ నంబర్ లేదా పాస్‌వర్డ్ తప్పు.", "exists":"ఈ ఫోన్ నంబర్ ఇప్పటికే నమోదైంది.", "posted":"పని విజయవంతంగా ప్రకటించబడింది.", "appliedmsg":"మీ దరఖాస్తు పంపబడింది.", "selectloc":"బ్రౌజర్ ద్వారా స్థానం పొందండి", "manual":"లేదా కోఆర్డినేట్లు నమోదు చేయండి", "accept":"అంగీకరించండి", "reject":"తిరస్కరించండి", "pending":"పెండింగ్", "accepted":"అంగీకరించబడింది", "rejected":"తిరస్కరించబడింది", "noapps":"ఇంకా దరఖాస్తులు లేవు.", "owneronly":"పని యజమానులు మాత్రమే పనులు ప్రకటించగలరు.", "workeronly":"కార్మికులు మాత్రమే దరఖాస్తు చేయగలరు."},
    "hi": {"brand":"वर्कनियर", "tagline":"घर के पास रोज़गार खोजें", "home":"होम", "jobs":"पास के काम", "login":"लॉगिन", "register":"रजिस्टर", "logout":"लॉगआउट", "worker":"मज़दूर", "owner":"काम के मालिक", "name":"पूरा नाम", "phone":"फ़ोन नंबर", "password":"पासवर्ड", "language":"भाषा", "skills":"कौशल", "location":"आपकी लोकेशन", "latitude":"अक्षांश", "longitude":"देशांतर", "find":"10 किमी के अंदर काम खोजें", "post":"काम पोस्ट करें", "title":"काम का नाम", "description":"विवरण", "wage":"दैनिक मज़दूरी (₹)", "date":"काम की तारीख", "workers":"ज़रूरी मज़दूर", "address":"काम की जगह", "apply":"आवेदन करें", "applied":"आवेदन भेज दिया गया", "distance":"दूरी", "open":"खोलें", "nojobs":"10 किमी के अंदर कोई काम नहीं मिला।", "dashboard":"डैशबोर्ड", "applications":"आवेदन", "status":"स्थिति", "save":"काम सेव करें", "welcome":"स्वागत है", "nearby":"आपके पास काम", "required":"कृपया सभी ज़रूरी जानकारी भरें।", "badlogin":"फ़ोन नंबर या पासवर्ड गलत है।", "exists":"यह फ़ोन नंबर पहले से रजिस्टर है।", "posted":"काम सफलतापूर्वक पोस्ट हो गया।", "appliedmsg":"आपका आवेदन भेज दिया गया है।", "selectloc":"ब्राउज़र लोकेशन इस्तेमाल करें", "manual":"या निर्देशांक दर्ज करें", "accept":"स्वीकार करें", "reject":"अस्वीकार करें", "pending":"लंबित", "accepted":"स्वीकृत", "rejected":"अस्वीकृत", "noapps":"अभी कोई आवेदन नहीं है।", "owneronly":"केवल मालिक काम पोस्ट कर सकते हैं।", "workeronly":"केवल मज़दूर आवेदन कर सकते हैं।"}
}

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    try:
        return mongo.db.users.find_one({"_id": ObjectId(uid)})
    except Exception:
        session.clear()
        return None

@app.context_processor
def inject_globals():
    user = current_user()
    lang = (user or {}).get("language") or session.get("language", "en")
    return {"user": user, "lang": lang, "t": LANGUAGES.get(lang, LANGUAGES["en"])}

def haversine(lat1, lon1, lat2, lon2):
    radius = 6371
    dlat, dlon = radians(lat2-lat1), radians(lon2-lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2 * radius * atan2(sqrt(a), sqrt(1-a))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/language", methods=["POST"])
def set_language():
    language = request.form.get("language", "en")
    if language not in LANGUAGES:
        language = "en"
    session["language"] = language
    user = current_user()
    if user:
        mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"language": language}})
    return redirect(request.referrer or url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "worker")
        language = request.form.get("language", "en")
        skills = request.form.get("skills", "").strip()
        if not name or not phone or len(password) < 6 or role not in ("worker", "owner"):
            flash("Please enter valid details. Password must be at least 6 characters.", "error")
            return render_template("register.html")
        if mongo.db.users.find_one({"phone": phone}):
            flash(LANGUAGES.get(language, LANGUAGES["en"])["exists"], "error")
            return render_template("register.html")
        doc = {"name": name, "phone": phone, "password_hash": generate_password_hash(password), "role": role, "language": language, "skills": skills, "created_at": datetime.utcnow()}
        result = mongo.db.users.insert_one(doc)
        session["user_id"] = str(result.inserted_id)
        session["language"] = language
        flash("Account created successfully.", "success")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        person = mongo.db.users.find_one({"phone": phone})
        if person and check_password_hash(person.get("password_hash", ""), password):
            session["user_id"] = str(person["_id"])
            session["language"] = person.get("language", "en")
            return redirect(url_for("dashboard"))
        flash(LANGUAGES.get(session.get("language", "en"), LANGUAGES["en"])["badlogin"], "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    person = current_user()
    if not person:
        return redirect(url_for("login"))
    if person["role"] == "owner":
        jobs = list(mongo.db.jobs.find({"owner_id": str(person["_id"])}).sort("created_at", -1))
        for job in jobs:
            job["id"] = str(job["_id"])
            job["application_count"] = mongo.db.applications.count_documents({"job_id": job["id"]})
        return render_template("owner_dashboard.html", jobs=jobs)
    applications = list(mongo.db.applications.find({"worker_id": str(person["_id"])}).sort("created_at", -1))
    for item in applications:
        item["job"] = mongo.db.jobs.find_one({"_id": ObjectId(item["job_id"])}) if ObjectId.is_valid(item["job_id"]) else None
    return render_template("worker_dashboard.html", applications=applications)

@app.route("/jobs")
def jobs():
    try:
        lat = float(request.args.get("lat", "17.3850"))
        lon = float(request.args.get("lon", "78.4867"))
        radius = min(max(float(request.args.get("radius", "10")), 1), 50)
    except ValueError:
        lat, lon, radius = 17.3850, 78.4867, 10
    skill = request.args.get("skill", "").strip().lower()
    all_jobs = list(mongo.db.jobs.find({"status": "open"}).sort("created_at", -1))
    found = []
    for job in all_jobs:
        try:
            distance = haversine(lat, lon, float(job["lat"]), float(job["lon"]))
        except (KeyError, TypeError, ValueError):
            continue
        if distance <= radius and (not skill or skill in job.get("title", "").lower() or skill in job.get("skills", "").lower()):
            job["id"] = str(job["_id"])
            job["distance"] = round(distance, 1)
            found.append(job)
    found.sort(key=lambda x: x["distance"])
    return render_template("jobs.html", jobs=found, lat=lat, lon=lon, radius=radius, skill=skill)

@app.route("/jobs/new", methods=["GET", "POST"])
def new_job():
    person = current_user()
    if not person:
        return redirect(url_for("login"))
    if person["role"] != "owner":
        flash("Only job owners can post jobs.", "error")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        try:
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            address = request.form.get("address", "").strip()
            wage = float(request.form.get("wage", "0"))
            lat = float(request.form.get("lat", ""))
            lon = float(request.form.get("lon", ""))
            workers_needed = int(request.form.get("workers_needed", "1"))
            date = request.form.get("date", "")
            if not title or not address or wage <= 0 or workers_needed < 1 or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError()
        except ValueError:
            flash("Enter a title, address, valid coordinates, positive wage and worker count.", "error")
            return render_template("new_job.html")
        mongo.db.jobs.insert_one({"title": title, "description": description, "address": address, "wage": wage, "lat": lat, "lon": lon, "workers_needed": workers_needed, "date": date, "owner_id": str(person["_id"]), "owner_name": person["name"], "owner_phone": person["phone"], "status": "open", "skills": request.form.get("skills", "").strip(), "created_at": datetime.utcnow()})
        flash("Job posted successfully.", "success")
        return redirect(url_for("dashboard"))
    return render_template("new_job.html")

@app.route("/jobs/<job_id>/apply", methods=["POST"])
def apply_job(job_id):
    person = current_user()
    if not person:
        return redirect(url_for("login"))
    if person["role"] != "worker":
        flash("Only workers can apply for jobs.", "error")
        return redirect(url_for("jobs"))
    if not ObjectId.is_valid(job_id):
        flash("Job not found.", "error")
        return redirect(url_for("jobs"))
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id), "status": "open"})
    if not job:
        flash("This job is no longer available.", "error")
        return redirect(url_for("jobs"))
    worker_id = str(person["_id"])
    if mongo.db.applications.find_one({"job_id": job_id, "worker_id": worker_id}):
        flash("You have already applied for this job.", "error")
    else:
        mongo.db.applications.insert_one({"job_id": job_id, "worker_id": worker_id, "worker_name": person["name"], "worker_phone": person["phone"], "skills": person.get("skills", ""), "status": "pending", "created_at": datetime.utcnow()})
        flash("Application submitted.", "success")
    return redirect(url_for("jobs"))

@app.route("/jobs/<job_id>/applications")
def job_applications(job_id):
    person = current_user()
    if not person or person["role"] != "owner":
        return redirect(url_for("login"))
    job = mongo.db.jobs.find_one({"_id": ObjectId(job_id)}) if ObjectId.is_valid(job_id) else None
    if not job or str(job["owner_id"]) != str(person["_id"]):
        flash("Job not found or access denied.", "error")
        return redirect(url_for("dashboard"))
    applicants = list(mongo.db.applications.find({"job_id": job_id}).sort("created_at", -1))
    return render_template("applications.html", job=job, applicants=applicants)

@app.route("/applications/<application_id>/<decision>", methods=["POST"])
def update_application(application_id, decision):
    person = current_user()
    if not person or person["role"] != "owner" or decision not in ("accepted", "rejected"):
        return redirect(url_for("login"))
    appdoc = mongo.db.applications.find_one({"_id": ObjectId(application_id)}) if ObjectId.is_valid(application_id) else None
    if appdoc:
        job = mongo.db.jobs.find_one({"_id": ObjectId(appdoc["job_id"])}) if ObjectId.is_valid(appdoc["job_id"]) else None
        if job and str(job["owner_id"]) == str(person["_id"]):
            mongo.db.applications.update_one({"_id": appdoc["_id"]}, {"$set": {"status": decision}})
            if decision == "accepted":
                # Reveal full worksite address only after the owner accepts the worker.
                pass
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/health")
def health():
    try:
        mongo.db.command("ping")
        return jsonify({"status": "ok", "database": "connected"})
    except Exception:
        return jsonify({"status": "error", "database": "unavailable"}), 503

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "true").lower() == "true")
