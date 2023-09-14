from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

# subscriptionsData =

def GetSubscriptions(request):
    return render(request, 'subscriptions.html', {'data' : {
        'current_date': date.today(),
        'subscriptions': [
            {'title': 'Метро', 'id': 1},
            {'title': 'МЦД', 'id': 2},
            {'title': 'МЦК', 'id': 3},
            {'title': 'Автобусы/троллейбусы/трамваи', 'id': 4},
            {'title': 'Велосипеды', 'id': 5},
            {'title': 'Самокаты', 'id': 6},
        ]
    }})

def GetSubscription(request, id):
    return render(request, 'sunbcription.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})