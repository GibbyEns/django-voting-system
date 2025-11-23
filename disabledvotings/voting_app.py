
import os, sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.core.wsgi import get_wsgi_application

# ================================
# Django Settings
# ================================
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='django-insecure-key',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        MIDDLEWARE=['django.middleware.common.CommonMiddleware'],
        INSTALLED_APPS=['django.contrib.staticfiles'],
        TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates'}],
        STATIC_URL='/static/',
    )

# ================================
# Data
# ================================
CANDIDATES = {
    1: 'Accessible Transport',
    2: 'Inclusive Education',
    3: 'Assistive Technology',
    4: 'Healthcare Accessibility',
    5: 'Digital Inclusion'
}
VOTE_COUNT = {cid: 0 for cid in CANDIDATES}
VOTERS = {cid: [] for cid in CANDIDATES}  # Store usernames per candidate
SURVEY_RESPONSES = []
CURRENT_USER = None  # Track logged-in user

SURVEY_QUESTIONS = [
    "Are schools accessible for students with disabilities?",
    "Do workplaces provide reasonable accommodations?",
    "Is public transport disability-friendly?",
    "Do you have access to assistive technology?",
    "Are healthcare facilities inclusive?",
    "Do you feel represented in policy-making?",
    "Are emergency services accessible?",
    "Do you have access to digital accessibility tools?",
    "Is voting easy for people with disabilities?",
    "Would you recommend improvements in accessibility laws?"
]

OPTIONS = ["Yes", "No", "Partially"]

# ================================
# HTML Template
# ================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Accessible Voting System</title>
<style>
body { font-family: Arial; background:#f0f9ff; margin:0; color:#1e293b; }
header { background:#0ea5e9; color:white; padding:1rem; text-align:center; font-size:1.8rem; }
.container { max-width:1000px; margin:auto; padding:1rem; }
footer { text-align:center; padding:1rem; font-size:0.9rem; color:#555; margin-top:20px; }
.btn { padding:0.75rem 1.5rem; background:#0ea5e9; color:white; border:none; border-radius:6px; font-size:1rem; margin:0.5rem; display:inline-block; transition:all 0.3s ease; }
.btn:hover { background:#0284c7; transform:scale(1.1); }
.card { background:white; border-radius:8px; padding:1rem; margin:1rem; box-shadow:0 4px 8px rgba(0,0,0,0.1); width:250px; text-align:center; transition:transform 0.3s; }
.card:hover { transform:scale(1.05); background:#e0f2fe; }
.alert { padding:1rem; margin:1rem 0; border-radius:6px; font-weight:bold; }
.alert-success { background:#dcfce7; color:#166534; }
.accessibility-toolbar { background:#1e293b; color:white; padding:1rem; text-align:center; }
.accessibility-toolbar button { margin:0.5rem; padding:0.5rem 1rem; border:none; border-radius:4px; background:#0ea5e9; color:white; font-size:1rem; }
.accessibility-toolbar button:hover { background:#0284c7; transform:scale(1.1); }
.high-contrast { background:black !important; color:white !important; }
.progress-bar { background:#e5e7eb; border-radius:10px; overflow:hidden; margin:0.5rem 0; }
.progress-fill { background:#0ea5e9; height:20px; transition:width 0.5s; }
.bar-chart { margin-top:20px; }
.bar { background:#0ea5e9; height:20px; margin:5px 0; color:white; text-align:right; padding-right:5px; border-radius:4px; }
.pie-container { width:300px; height:300px; border-radius:50%; margin:auto; background:conic-gradient(var(--colors)); }
</style>
<script>
let audioEnabled=false;
function toggleAudio(){
    audioEnabled=!audioEnabled;
    alert(audioEnabled?'Audio ON':'Audio OFF');
    if(audioEnabled && 'speechSynthesis' in window){
        let text=document.querySelector('.container').innerText;
        speechSynthesis.cancel();
        let u=new SpeechSynthesisUtterance(text);
        u.rate=0.9;
        speechSynthesis.speak(u);
    }
}
function speak(text){
    if(audioEnabled && 'speechSynthesis' in window){
        speechSynthesis.cancel();
        let u=new SpeechSynthesisUtterance(text);
        u.rate=0.9;
        speechSynthesis.speak(u);
    }
}
function toggleContrast(){document.body.classList.toggle('high-contrast');}
function increaseFont(){document.body.style.fontSize='larger';}
function decreaseFont(){document.body.style.fontSize='smaller';}
function updateProgress(){
    let answered=document.querySelectorAll('input[type=radio]:checked').length;
    let total=document.querySelectorAll('input[type=radio]').length/3;
    let percent=(answered/total)*100;
    document.getElementById('progressFill').style.width=percent+'%';
}
</script>
</head>
<body>
<div class="accessibility-toolbar">
<button onclick="toggleContrast()">Contrast</button>
<button onclick="increaseFont()">A+</button>
<button onclick="decreaseFont()">A-</button>
<button onclick="toggleAudio()">🔊 Audio</button>
</div>
<header><h1>Accessible Voting & Survey System</h1></header>
<div class="container">
{{ content }}
</div>
<footer>Created by Xolewe, Nongcebo, Wendy, Asemahle | GirlCode Project</footer>
</body>
</html>
"""

# ================================
# Views
# ================================
def welcome(request):
    content = """
    <img src='https://thumbs.dreamstime.com/x/disability-employment-disabled-people-work-landing-page-template-set-handicapped-businessman-characters-wheelchair-214613649.jpg' alt='Welcome Image' style='width:100%;max-height:300px;object-fit:cover;border-radius:8px;'>
    <h2>Welcome!</h2>
    <p>This system helps check if voting meets accessibility requirements for people with disabilities.</p>
    <a href='/login/'><button class='btn'>Login</button></a>
    """
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', content))

@csrf_exempt
def login(request):
    global CURRENT_USER
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        # Validate format: username = 4 letters, password = 2 letters + 2 numbers
        if len(u) == 4 and u.isalpha() and len(p) == 4 and p[:2].isalpha() and p[2:].isdigit():
            CURRENT_USER = u
            return menu(request)
        return HttpResponse(HTML_TEMPLATE.replace('{{ content }}',
            '<div class="alert alert-danger">Invalid credentials. Username must be 4 letters, password must be 2 letters + 2 numbers.</div><a href="/login/"><button class="btn">⬅ Back</button></a>'
        ))
    content = """
    <h2>Login</h2>
    <form method="post">
        <input name="username" placeholder="Username (4 letters)" required><br><br>
        <input name="password" type="password" placeholder="Password (2 letters + 2 numbers)" required><br>
        <small style="color:#555;">Password must be 2 letters followed by 2 numbers (e.g., ab12)</small><br><br>
        <button type="submit" class="btn">Login</button>
    </form>
    """
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', content))

def menu(request):
    content = """
    <h2>Main Menu</h2>
    <a href='/vote/'><button class='btn'>Vote Now</button></a>
    <a href='/survey/'><button class='btn'>Take Survey</button></a>
    <a href='/results/'><button class='btn'>View Results</button></a>
    """
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', content))

def vote_page(request):
    html = "<h2>Vote for Accessibility Priorities</h2><div style='display:flex;flex-wrap:wrap;'>"
    for cid, name in CANDIDATES.items():
        html += f"<div class='card'><h3>{name}</h3><a href='/cast_vote/{cid}/'><button class='btn'>Vote</button></a></div>"
    html += "</div><a href='/menu/'><button class='btn'>⬅ Back</button></a>"
    html += f"<script>window.onload=function(){{if(audioEnabled){{speak('Candidates are: {','.join(CANDIDATES.values())}');}}}}</script>"
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', html))

def cast_vote(request, cid):
    global CURRENT_USER
    VOTE_COUNT[cid] += 1
    if CURRENT_USER:
        VOTERS[cid].append(CURRENT_USER)
    html = f"<div class='alert alert-success'>Vote submitted for {CANDIDATES[cid]}!</div>"
    html += "<script>speak('Thank you! Your vote has been recorded.');</script>"
    html += "<a href='/vote/'><button class='btn'>⬅ Back</button></a>"
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', html))

@csrf_exempt
def survey(request):
    if request.method == 'POST':
        answers = [request.POST.get(f'q{i}', '') for i in range(len(SURVEY_QUESTIONS))]
        SURVEY_RESPONSES.append(answers)
        html = "<div class='alert alert-success'>Survey submitted! Thank you for your feedback.</div>"
        html += "<script>speak('Thank you! Your survey has been submitted.');</script>"
        html += "<a href='/menu/'><button class='btn'>⬅ Back</button></a>"
        return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', html))
    html = "<h2>Accessibility Survey</h2><form method='post' oninput='updateProgress()'>"
    html += "<div class='progress-bar'><div id='progressFill' class='progress-fill' style='width:0%;'></div></div>"
    for i, q in enumerate(SURVEY_QUESTIONS):
        html += f"<div><p onmouseover='speak(\"{q}\")'>{q}</p>"
        for opt in OPTIONS:
            html += f"<label><input type='radio' name='q{i}' value='{opt}' required> {opt}</label> "
        html += "</div><hr>"
    html += "<button class='btn'>Submit Survey</button></form><a href='/menu/'><button class='btn'>⬅ Back</button></a>"
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', html))

def results(request):
    total_votes = sum(VOTE_COUNT.values()) or 1
    percentages = [(VOTE_COUNT[cid] / total_votes) * 100 for cid in CANDIDATES]
    html = "<h2>Voting Results</h2><div class='pie-container' style='--colors:"
    colors = ["#0ea5e9", "#0284c7", "#38bdf8", "#7dd3fc", "#bae6fd"]
    start = 0
    for i, pct in enumerate(percentages):
        end = start + pct
        html += f"{colors[i]} {start}% {end}%,"
        start = end
    html = html.rstrip(',') + ";'></div><ul>"
    for i, name in enumerate(CANDIDATES.values()):
        html += f"<li>{name}: {percentages[i]:.1f}% ({VOTE_COUNT[i+1]} votes) - Voters: {', '.join(VOTERS[i+1]) if VOTERS[i+1] else 'None'}</li>"
    html += "</ul><h2>Survey Responses</h2><div class='bar-chart'>"
    if SURVEY_RESPONSES:
        counts = {"Yes": 0, "No": 0, "Partially": 0}
        for resp in SURVEY_RESPONSES:
            for ans in resp:
                if ans in counts:
                    counts[ans] += 1
        total_answers = sum(counts.values())
        for opt, count in counts.items():
            pct = (count / total_answers) * 100 if total_answers else 0
            html += f"<div class='bar' style='width:{pct}%'>{opt}: {pct:.1f}%</div>"
    else:
        html += "<p>No survey responses yet.</p>"
    html += "</div><a href='/menu/'><button class='btn'>⬅ Back</button></a>"
    return HttpResponse(HTML_TEMPLATE.replace('{{ content }}', html))

# ================================
# URLs
# ================================
urlpatterns = [
    path('', welcome),
    path('login/', login),
    path('menu/', menu),
    path('vote/', vote_page),
    path('cast_vote/<int:cid>/', cast_vote),
    path('survey/', survey),
    path('results/', results),]

application = get_wsgi_application()

if __name__ == '__main__':
    if len(sys.argv) == 1: sys.argv.append('runserver')
    execute_from_command_line(sys.argv)
