from django.shortcuts import render
from django.http import HttpResponse
import random

def home(request):
    # Candidate list with participations
    participations = [("Visor", 2), ("Xaero", 6), ("Anarki", 0), ("Phobos", 1), ("Uriel", 4)]
	
    test = {}
    cycles = 10000
    for i in range(0, cycles):
        relative_probabilities = calculate_probabilities(participations)
        candidate = pick(relative_probabilities)
        if candidate in test:
            test[candidate] += 1
        else:
            test[candidate] = 0

    for candidate, count in test.iteritems():
        test[candidate] = str((float(count) / float(cycles)) * 100.0) + '%'

    return render(request, "index.html",
        {
            'title': "Meeting lotteru",
            'message': str(test)
        }
    )

def calculate_probabilities(participations):
    candidate_count = len(participations)

    overall_participations = 0.0
    for _, participation_count in participations:
        overall_participations += participation_count

    probabilities = []
    overall_probability = 0.0
    for candidate, participation_count in participations:
        probability = overall_participations - participation_count + 1.0
        overall_probability += probability
        item = (candidate, probability)
        probabilities.append(item)

    relative_probabilities = []
    for candidate, probability in probabilities:
        relative_probability = probability / overall_probability
        item = (candidate, relative_probability)
        relative_probabilities.append(item)

    return relative_probabilities

def pick(candidates_with_relative_probabilities):
    candidates = candidates_with_relative_probabilities
    # Shuffling the order of candidates
    random.shuffle(candidates)

    # Drawing the fortune number
    draw = random.uniform(0, 1)

    cumulative_probability = 0.0
    for candidate, relative_probability in candidates:
        cumulative_probability += float(relative_probability)
        if draw < cumulative_probability: break
    return candidate
