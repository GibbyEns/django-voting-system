/* ================================
   Accessible Voting System - JavaScript
   Created by: Xolewe, Nongcebo, Wendy, Asemahle
   GirlCode Project
   ================================ */

// ================================
// Data Storage
// ================================
const CANDIDATES = {
    1: 'Accessible Transport',
    2: 'Inclusive Education',
    3: 'Assistive Technology',
    4: 'Healthcare Accessibility',
    5: 'Digital Inclusion'
};

const SURVEY_QUESTIONS = [
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
];

const OPTIONS = ["Yes", "No", "Partially"];

let voteCount = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
let voters = { 1: [], 2: [], 3: [], 4: [], 5: [] };
let surveyResponses = [];
let currentUser = null;
let audioEnabled = false;

// ================================
// Page Navigation
// ================================
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    
    // Announce page change if audio enabled
    if (audioEnabled) {
        const pageTitle = document.querySelector('#' + pageId + ' h2');
        if (pageTitle) {
            speak(pageTitle.innerText);
        }
    }
}

// ================================
// Accessibility Functions
// ================================
function toggleAudio() {
    audioEnabled = !audioEnabled;
    alert(audioEnabled ? 'Audio ON' : 'Audio OFF');
    
    if (audioEnabled && 'speechSynthesis' in window) {
        let text = document.querySelector('.page.active').innerText;
        speechSynthesis.cancel();
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }
}

function speak(text) {
    if (audioEnabled && 'speechSynthesis' in window) {
        speechSynthesis.cancel();
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }
}

function toggleContrast() {
    document.body.classList.toggle('high-contrast');
}

function increaseFont() {
    document.body.style.fontSize = 'larger';
}

function decreaseFont() {
    document.body.style.fontSize = 'smaller';
}

// ================================
// Login Functions
// ================================
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    
    // Validate: username = 4 letters, password = 2 letters + 2 numbers
    const usernameValid = username.length === 4 && /^[a-zA-Z]+$/.test(username);
    const passwordValid = password.length === 4 && /^[a-zA-Z]{2}[0-9]{2}$/.test(password);
    
    if (usernameValid && passwordValid) {
        currentUser = username;
        document.getElementById('welcome-user').innerText = 'Welcome, ' + username + '!';
        errorDiv.style.display = 'none';
        showPage('menu-page');
        speak('Welcome ' + username);
    } else {
        errorDiv.innerText = 'Invalid credentials. Username must be 4 letters, password must be 2 letters + 2 numbers.';
        errorDiv.style.display = 'block';
        speak('Invalid credentials');
    }
}

// ================================
// Voting Functions
// ================================
function loadCandidates() {
    const container = document.getElementById('candidates-container');
    container.innerHTML = '';
    
    for (const [cid, name] of Object.entries(CANDIDATES)) {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>${name}</h3>
            <button class="btn" onclick="castVote(${cid})">Vote</button>
        `;
        container.appendChild(card);
    }
}

function castVote(cid) {
    voteCount[cid]++;
    if (currentUser) {
        voters[cid].push(currentUser);
    }
    
    document.getElementById('voted-candidate').innerText = CANDIDATES[cid];
    showPage('vote-success-page');
    speak('Thank you! Your vote has been recorded for ' + CANDIDATES[cid]);
}

// ================================
// Survey Functions
// ================================
function loadSurveyQuestions() {
    const container = document.getElementById('survey-questions');
    container.innerHTML = '';
    
    SURVEY_QUESTIONS.forEach((question, index) => {
        const div = document.createElement('div');
        div.className = 'survey-question';
        div.innerHTML = `
            <p onmouseover="speak('${question}')">${index + 1}. ${question}</p>
            ${OPTIONS.map(opt => `
                <label>
                    <input type="radio" name="q${index}" value="${opt}" required onchange="updateProgress()">
                    ${opt}
                </label>
            `).join('')}
        `;
        container.appendChild(div);
    });
}

function updateProgress() {
    const answered = document.querySelectorAll('#survey-form input[type=radio]:checked').length;
    const total = SURVEY_QUESTIONS.length;
    const percent = (answered / total) * 100;
    document.getElementById('progressFill').style.width = percent + '%';
}

function handleSurvey(event) {
    event.preventDefault();
    
    const answers = [];
    SURVEY_QUESTIONS.forEach((_, index) => {
        const selected = document.querySelector(`input[name="q${index}"]:checked`);
        answers.push(selected ? selected.value : '');
    });
    
    surveyResponses.push(answers);
    
    // Reset form
    document.getElementById('survey-form').reset();
    document.getElementById('progressFill').style.width = '0%';
    
    showPage('survey-success-page');
    speak('Thank you! Your survey has been submitted.');
}

// ================================
// Results Functions
// ================================
function displayResults() {
    const totalVotes = Object.values(voteCount).reduce((a, b) => a + b, 0) || 1;
    const colors = ["#0ea5e9", "#0284c7", "#38bdf8", "#7dd3fc", "#bae6fd"];
    
    // Build pie chart
    let pieGradient = [];
    let start = 0;
    let voteResultsHTML = '';
    
    Object.entries(CANDIDATES).forEach(([cid, name], index) => {
        const pct = (voteCount[cid] / totalVotes) * 100;
        const end = start + pct;
        pieGradient.push(`${colors[index]} ${start}% ${end}%`);
        
        const votersList = voters[cid].length > 0 ? voters[cid].join(', ') : 'None';
        voteResultsHTML += `
            <li>
                <span class="legend-color" style="background:${colors[index]}; display:inline-block; width:15px; height:15px; border-radius:3px;"></span>
                <strong>${name}</strong>: ${pct.toFixed(1)}% (${voteCount[cid]} votes)
                <br><small>Voters: ${votersList}</small>
            </li>
        `;
        start = end;
    });
    
    document.getElementById('pie-chart').style.background = `conic-gradient(${pieGradient.join(', ')})`;
    document.getElementById('vote-results').innerHTML = voteResultsHTML;
    
    // Build survey results
    let surveyHTML = '';
    if (surveyResponses.length > 0) {
        const counts = { "Yes": 0, "No": 0, "Partially": 0 };
        
        surveyResponses.forEach(resp => {
            resp.forEach(ans => {
                if (ans in counts) {
                    counts[ans]++;
                }
            });
        });
        
        const totalAnswers = Object.values(counts).reduce((a, b) => a + b, 0);
        
        for (const [opt, count] of Object.entries(counts)) {
            const pct = totalAnswers > 0 ? (count / totalAnswers) * 100 : 0;
            surveyHTML += `<div class="bar" style="width:${Math.max(pct, 10)}%">${opt}: ${pct.toFixed(1)}%</div>`;
        }
    } else {
        surveyHTML = '<p>No survey responses yet.</p>';
    }
    
    document.getElementById('survey-results').innerHTML = surveyHTML;
}

// ================================
// Initialize on Page Load
// ================================
document.addEventListener('DOMContentLoaded', function() {
    loadCandidates();
    loadSurveyQuestions();
});
