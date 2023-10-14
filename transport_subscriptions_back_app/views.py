from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect
from transport_subscriptions_back_app.models import *

# def getSubscriptionsData():
#     return [
#             {'title': 'Метро / МЦК', 'id': 1, 'src': 'images/subway.jpg', 'info': 'Стоимости тарифов зависят от количества поездок и варьируются от 250р. до 1300р.', 'rates':[{'title': '5 поездок', 'price': '250р.'}, {'title': '15 поездок', 'price': '700р.'}, {'title': '30 поездок', 'price': '1300р.'}],},
#             {'title': 'МЦД', 'id': 2, 'src': 'images/mcd.jpg', 'info': 'Стоимости тарифов зависят от зоны, в пределах которой вы будете путешествовать, и варьируются от 400р. до 1200р.', 'rates':[{'title': '5 поездок в пределах центральной зоны', 'price': '400р.'}, {'title': '5 поездок в пределах пригородной зоны', 'price': '650р.'}, {'title': '5 поездок в пределах дальней зоны', 'price': '1200р.'}],},
#             {'title': 'Автобусы / троллейбусы / трамваи', 'id': 3, 'src': 'images/bus.jpg', 'info': 'Стоимости тарифаов зависят от количества дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 1560р. до 14000р. Также данные абонементы распространяются на все 3 вида транспорта: автобусы, троллейбусы и трамваи', 'rates':[{'title': '30 дней', 'price': '1560р.'}, {'title': '90 дней', 'price': '4140р.'}, {'title': '365 дней', 'price': '14000р.'}],},
#             {'title': 'Велосипеды', 'id': 4, 'src': 'images/bike.jpeg', 'info': 'Стоимости тарифов зависят от количества дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 685р. до 6000р. Также вы можете использовать все велосипеды расположенныев на специальных велосипедных станциях по всей территории Москвы и Московской области.', 'rates':[{'title': '30 дней', 'price': '685р.'}, {'title': '90 дней', 'price': '1600р.'}, {'title': '365 дней', 'price': '6000р.'}],},
#             {'title': 'Самокаты', 'id': 5, 'src': 'images/scooter.jpeg', 'info': 'Стоимости тарифов зависят от колчиства дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 400р. до 3500р. Обратите внимание, что абонемент распространяется только на бесплатный старт проезда на самокате, последующие минуты проезда необходимо оплачивать по 7р./минута', 'rates':[{'title': 'Бесплатный старт 30 дней', 'price': '400р.'}, {'title': 'Бесплатный старт 90 дней', 'price': '1000р.'}, {'title': 'Бесплатный старт 365 дней', 'price': '3500р.'}],},
#         ]

def GetSubscriptions(request):
    query = request.GET.get("sub")
    subs = Subscription.objects.filter(status='enabled')
    print(subs[0].id_category.title, 'dskjdklsjdklsjlk')

    if query:
         subs = Subscription.objects.filter(status='enabled', id_category__title__icontains=query)
    else:
        query = ''
    
    return render(request, 'subscriptions.html', {'data' : {
        'subscriptions': subs,
        'inputValue': query
    }})

def GetSubscription(request, id):
    subscription = Subscription.objects.get(id=id)  
    return render(request, 'subscription.html', {'data' : {
        'subscription': subscription
    }})

def DeleteRecord(request, record_id):
    with connection.cursor() as cursor:
        req = "UPDATE subscriptions SET status = 'disabled' WHERE id = %s"
        cursor.execute(req, [record_id])
    return redirect('subscriptions_url')