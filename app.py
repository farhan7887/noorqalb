from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'quran-ict-project-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/quran.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- Models ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    message = db.Column(db.Text)

# ---------- Quran Ayaat by Mood ----------
MOOD_AYAAT = {
    "happy": [
        {"arabic": "وَإِذْ تَأَذَّنَ رَبُّكُمْ لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ", "translation": "And when your Lord proclaimed: If you are grateful, I will surely increase you in favor.", "surah": "Surah Ibrahim (14:7)"},
        {"arabic": "فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ", "translation": "Then which of the favors of your Lord would you deny?", "surah": "Surah Ar-Rahman (55:13)"},
        {"arabic": "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ", "translation": "Verily, in the remembrance of Allah do hearts find rest.", "surah": "Surah Ar-Ra'd (13:28)"},
    ],
    "sad": [
        {"arabic": "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "translation": "Verily, with hardship comes ease.", "surah": "Surah Ash-Sharh (94:6)"},
        {"arabic": "وَلَا تَيْأَسُوا مِن رَّوْحِ اللَّهِ ۖ إِنَّهُ لَا يَيْأَسُ مِن رَّوْحِ اللَّهِ إِلَّا الْقَوْمُ الْكَافِرُونَ", "translation": "Do not despair of the mercy of Allah. Indeed, no one despairs of Allah's mercy except the disbelieving people.", "surah": "Surah Yusuf (12:87)"},
        {"arabic": "وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ", "translation": "And it may be that you dislike a thing which is good for you.", "surah": "Surah Al-Baqarah (2:216)"},
    ],
    "anxious": [
        {"arabic": "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ", "translation": "Allah is sufficient for us, and He is the best disposer of affairs.", "surah": "Surah Al-Imran (3:173)"},
        {"arabic": "وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ", "translation": "And whoever relies upon Allah — then He is sufficient for him.", "surah": "Surah At-Talaq (65:3)"},
        {"arabic": "لَا تَخَفْ وَلَا تَحْزَنْ", "translation": "Do not fear and do not grieve.", "surah": "Surah Fussilat (41:30)"},
    ],
    "grateful": [
        {"arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "translation": "All praise is due to Allah, Lord of all the worlds.", "surah": "Surah Al-Fatiha (1:2)"},
        {"arabic": "وَمَا بِكُم مِّن نِّعْمَةٍ فَمِنَ اللَّهِ", "translation": "And whatever you have of favor — it is from Allah.", "surah": "Surah An-Nahl (16:53)"},
        {"arabic": "لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ", "translation": "If you are grateful, I will surely increase you in favor.", "surah": "Surah Ibrahim (14:7)"},
    ],
    "lonely": [
        {"arabic": "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "translation": "And He is with you wherever you are.", "surah": "Surah Al-Hadid (57:4)"},
        {"arabic": "نَحْنُ أَقْرَبُ إِلَيْهِ مِنْ حَبْلِ الْوَرِيدِ", "translation": "We are closer to him than his jugular vein.", "surah": "Surah Qaf (50:16)"},
        {"arabic": "وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ", "translation": "And when My servants ask about Me — indeed I am near.", "surah": "Surah Al-Baqarah (2:186)"},
    ],
    "hopeful": [
        {"arabic": "إِنَّ اللَّهَ لَا يُغَيِّرُ مَا بِقَوْمٍ حَتَّىٰ يُغَيِّرُوا مَا بِأَنفُسِهِمْ", "translation": "Indeed, Allah will not change the condition of a people until they change what is in themselves.", "surah": "Surah Ar-Ra'd (13:11)"},
        {"arabic": "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "translation": "So verily, with hardship comes ease.", "surah": "Surah Ash-Sharh (94:5)"},
        {"arabic": "وَبَشِّرِ الصَّابِرِينَ", "translation": "And give good tidings to the patient.", "surah": "Surah Al-Baqarah (2:155)"},
    ],
    "angry": [
        {"arabic": "وَالْكَاظِمِينَ الْغَيْظَ وَالْعَافِينَ عَنِ النَّاسِ", "translation": "Those who restrain anger and pardon people — Allah loves the doers of good.", "surah": "Surah Al-Imran (3:134)"},
        {"arabic": "ادْفَعْ بِالَّتِي هِيَ أَحْسَنُ", "translation": "Repel evil by that which is better.", "surah": "Surah Fussilat (41:34)"},
        {"arabic": "وَإِن تَعْفُوا وَتَصْفَحُوا وَتَغْفِرُوا فَإِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ", "translation": "But if you pardon and overlook and forgive — then indeed, Allah is Forgiving and Merciful.", "surah": "Surah At-Taghabun (64:14)"},
    ],
    "lost": [
        {"arabic": "وَهُوَ يَهْدِي السَّبِيلَ", "translation": "And He guides to the right way.", "surah": "Surah Al-Ahzab (33:4)"},
        {"arabic": "إِنَّ اللَّهَ يَهْدِي مَن يَشَاءُ إِلَىٰ صِرَاطٍ مُّسْتَقِيمٍ", "translation": "Indeed, Allah guides whom He wills to a straight path.", "surah": "Surah Al-Baqarah (2:142)"},
        {"arabic": "وَمَن يَعْتَصِم بِاللَّهِ فَقَدْ هُدِيَ إِلَىٰ صِرَاطٍ مُّسْتَقِيمٍ", "translation": "Whoever holds firmly to Allah has been guided to the straight path.", "surah": "Surah Al-Imran (3:101)"},
    ],
}

import random

# ---------- Routes ----------
@app.route('/')
def index():
    user = session.get('user_name')
    return render_template('index.html', user=user)

@app.route('/get_ayah', methods=['POST'])
def get_ayah():
    data = request.get_json()
    mood = data.get('mood', 'happy').lower()
    ayaat = MOOD_AYAAT.get(mood, MOOD_AYAAT['happy'])
    ayah = random.choice(ayaat)
    return jsonify(ayah)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Email already registered.')
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        session['user_name'] = name
        session['user_email'] = email
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_name'] = user.name
            session['user_email'] = user.email
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(msg)
        db.session.commit()
        success = True
    return render_template('contact.html', success=success)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
