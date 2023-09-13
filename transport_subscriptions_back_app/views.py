from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

def GetSubscriptions(request):
    return render(request, 'subscriptions.html', {'data' : {
        'current_date': date.today(),
        'subscriptions': [
            {'title': 'Книга с картинками', 'id': 1},
            {'title': 'Бутылка с водой', 'id': 2},
            {'title': 'Коврик для мышки', 'id': 3},
        ]
    }})

def GetSubscription(request, id):
    return render(request, 'sunbcription.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})