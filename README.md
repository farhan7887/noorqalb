# NoorQalb — Quran Mood Website 🌙
**ICT Project** | Built with Flask + HTML/CSS

---

## Features
- 8 moods: Happy, Sad, Anxious, Grateful, Lonely, Hopeful, Angry, Lost
- Relevant Quranic Ayah for each mood (with Arabic + English)
- Durood Pak splash screen on startup
- User Signup / Login / Logout
- Contact Us form
- Beautiful animated UI

---

## Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
```
Open http://localhost:5000 in your browser.

---

## Deploy on GitHub + Railway

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - NoorQalb"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/noorqalb.git
git push -u origin main
```

### Step 2 — Deploy on Railway
1. Go to https://railway.app and login (GitHub se)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Apni repo select karein: `noorqalb`
4. Railway automatically detect karega Flask app
5. **Environment Variables** mein yeh add karein:
   - `SECRET_KEY` = `koi-bhi-random-string-likhein`
6. Click **Deploy** — done! ✅

Railway aapko ek live URL dega jaise:
`https://noorqalb-production.up.railway.app`

---

## Project Structure
```
quran-mood/
├── app.py              ← Flask backend
├── requirements.txt    ← Python packages
├── Procfile            ← Railway/Heroku start command
├── railway.toml        ← Railway config
├── .gitignore
├── templates/
│   ├── base.html       ← Navbar + Footer + Splash
│   ├── index.html      ← Home (mood selector)
│   ├── login.html
│   ├── signup.html
│   └── contact.html
└── static/
    └── style.css       ← All styles + animations
```

---

Contact: mubashir@khan.com
