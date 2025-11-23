from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll

def poll_list(request):
    polls = Poll.objects.all()
    return render(request, 'polls/poll_list.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/poll_detail.html', {'poll': poll})

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST['choice']
    selected_choice = poll.choice_set.get(pk=choice_id)
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('results', poll_id=poll.id)

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

import json
from pathlib import Path
from django.shortcuts import render

def poll_view(request):

    questions_file = Path(__file__).resolve().parent / "poll_questions.json"
    with open(questions_file) as f:
        questions = json.load(f)
    return render(request, "poll.html", {"questions": questions})


QUESTIONS = [
    
  {
    "question": "Do you enjoy going to school?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Which subject do you like the most?",
    "options": ["Maths", "Science", "Languages", "Arts"]
  },
  {
    "question": "Do you think schools should have more sports activities?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Would you like more computers and technology in your classroom?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Do you feel safe at school?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Should schools give extra help to children who struggle with reading or maths?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Do you like the meals provided at school?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Would you prefer shorter school days or longer holidays?",
    "options": ["Shorter school days", "Longer holidays"]
  },
  {
    "question": "Do teachers listen to children’s ideas enough?",
    "options": ["Yes", "No"]
  },
  {
    "question": "Should schools teach more about South African history and culture?",
    "options": ["Yes", "No"]
  }
]

def poll_view(request):
    return render(request, "poll.html", {"questions": QUESTIONS})
