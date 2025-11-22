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

