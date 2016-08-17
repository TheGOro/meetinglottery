from django.shortcuts import render
from django.http import HttpResponse
from models import Candidate, Participation
from django.db.models import Count, Case, When

import random
from copy import deepcopy

def chances(request):
    candidates = get_candidates()

    # Calculate the chances
    calculate_probabilities(candidates)
    for candidate in candidates:
        candidate['chance'] = "{:.2%}".format(candidate['relative_probability'])

    return render(request, "chances.html",
        {
            'title': "Meeting lottery",
            'candidates': candidates
        }
    )

def pick(request):
    candidates = get_candidates()
    calculate_probabilities(candidates)
    candidate = pick_candidate(candidates)

    participant = Candidate.objects.get(pk=candidate['id'])
    participation = Participation(candidate=participant, classification=Participation.ALONE)
    participation.save()
    
    return render(request, "pick.html", {'candidate': candidate}) 

def get_candidates():
    # Get candidates along with the different participation counts
    candidates = Candidate.objects.annotate(
        num_participations_alone=Count(
            Case(
                When(participation__classification=Participation.ALONE, then=1)
            )
        ),
        num_participations_together=Count(
            Case(
                When(participation__classification=Participation.TOGETHER, then=1)
            )
        )
    )

    # Calculate the weighted participations
    participations = []
    for candidate in candidates:
        name = candidate.name
        participation = (candidate.num_participations_alone +
                         candidate.num_participations_together * 0.5)
        item = {
            'id': candidate.id,
            'name': candidate.name,
            'participation': participation
        }

        participations.append(item)

    return participations  

def calculate_probabilities(candidates):
    candidate_count = len(candidates)

    overall_participations = 0.0
    for candidate in candidates:
        overall_participations += candidate['participation']

    overall_probability = 0.0
    for candidate in candidates:
        probability = overall_participations - candidate['participation'] + 1.0
        overall_probability += probability
        candidate['probability'] = probability

    for candidate in candidates:
        relative_probability = candidate['probability'] / overall_probability
        candidate['relative_probability'] = relative_probability

    return candidates

def pick_candidate(candidates):
    candidate_pool = deepcopy(candidates)
    # Shuffling the order of candidates
    random.shuffle(candidate_pool)

    # Drawing the fortune number
    draw = random.uniform(0, 1)

    cumulative_probability = 0.0
    for candidate in candidate_pool:
        cumulative_probability += candidate['relative_probability']
        if draw < cumulative_probability: break
    return candidate
