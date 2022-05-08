import pdb
from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import json

from recommendation.models import Movie, Rating
from recommendation_engine.recommendationengine import TriggerRecommendationEngine

# Create your views here.

def main(request):
    return render(request, 'index.html')

def result(request):
    movie_name = request.GET.get('movie_name')
    recommendation_list = TriggerRecommendationEngine(movie_name).trigger()
    
    json_records = recommendation_list.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}

    return render(request, 'result.html', {'movie_name': movie_name, 'context': context})