import json
from pathlib import Path
from django.shortcuts import render

def poll_view(request):
    questions_file = Path(__file__).resolve().parent / "poll_questions.json"
    with open(questions_file) as f:
        questions = json.load(f)
    return render(request, "poll.html", {"questions": questions})

def poll_view(request):
    return render(request, "index.html")

def poll_view(request):
    return render(request, "poll.html")

def results_view(request):
    return render(request, "results.html")
