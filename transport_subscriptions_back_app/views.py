from django.shortcuts import render
from django.http import HttpResponse
from transport_subscriptions_back_app.models import *

# def GetVacancies(request):
#     keyword = request.GET.get('keyword')
#     a = Vacancies.objects.filter(status='enabled')
#     if keyword:
#          keyword = keyword[0].upper()+keyword[1:]
#          a = Vacancies.objects.filter(status='enabled').filter(title=keyword)
#     return render(request, 'vacancies.html', {'data': {
#         'current_date': date.today(),
#         'vacancies': a},
#         "search_query": keyword if keyword else ""})

# def GetVacancy(request, id):
#     return render(request, 'vacancy.html', {'data' : {
#         'current_date': date.today(),
#         'vacancy': Vacancies.objects.get(id = id)
#     }})

def getSubscriptionsData():
    return [
            {'title': 'Метро / МЦК', 'id': 1, 'src': 'images/subway.jpg', 'info': 'Стоимости тарифов зависят от количества поездок и варьируются от 250р. до 1300р.', 'rates':[{'title': '5 поездок', 'price': '250р.'}, {'title': '15 поездок', 'price': '700р.'}, {'title': '30 поездок', 'price': '1300р.'}],},
            {'title': 'МЦД', 'id': 2, 'src': 'images/mcd.jpg', 'info': 'Стоимости тарифов зависят от зоны, в пределах которой вы будете путешествовать, и варьируются от 400р. до 1200р.', 'rates':[{'title': '5 поездок в пределах центральной зоны', 'price': '400р.'}, {'title': '5 поездок в пределах пригородной зоны', 'price': '650р.'}, {'title': '5 поездок в пределах дальней зоны', 'price': '1200р.'}],},
            {'title': 'Автобусы/троллейбусы/трамваи', 'id': 3, 'src': 'images/bus.jpg', 'info': 'Стоимости тарифаов зависят от количества дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 1560р. до 14000р. Также данные абонементы распространяются на все 3 вида транспорта: автобусы, троллейбусы и трамваи', 'rates':[{'title': '30 дней', 'price': '1560р.'}, {'title': '90 дней', 'price': '4140р.'}, {'title': '365 дней', 'price': '14000р.'}],},
            {'title': 'Велосипеды', 'id': 4, 'src': 'images/bike.jpeg', 'info': 'Стоимости тарифов зависят от количества дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 685р. до 6000р. Также вы можете использовать все велосипеды расположенныев на специальных велосипедных станциях по всей территории Москвы и Московской области.', 'rates':[{'title': '30 дней', 'price': '685р.'}, {'title': '90 дней', 'price': '1600р.'}, {'title': '365 дней', 'price': '6000р.'}],},
            {'title': 'Самокаты', 'id': 5, 'src': 'images/scooter.jpeg', 'info': 'Стоимости тарифов зависят от колчиства дней, на которое вы приобритаете абонемент. Можно приобрести абонемент на определенное количесто дней от 30 до 365, и цена будет составлять от 400р. до 3500р. Обратите внимание, что абонемент распространяется только на бесплатный старт проезда на самокате, последующие минуты проезда необходимо оплачивать по 7р./минута', 'rates':[{'title': 'Бесплатный старт 30 дней', 'price': '400р.'}, {'title': 'Бесплатный старт 90 дней', 'price': '1000р.'}, {'title': 'Бесплатный старт 365 дней', 'price': '3500р.'}],},
        ]

def GetSubscriptions(request):
    query = request.GET.get("sub")
    print(query)
    subs = getSubscriptionsData()
    res = []
    
    for sub in subs:
        if (query is not None):
            if query.lower() in sub["title"].lower():
                res.append(sub)
        else:
            res = subs

    return render(request, 'subscriptions.html', {'data' : {
        'subscriptions': res,
        'inputValue': query
    }})

def GetSubscription(request, id):
    subscriptionsData = getSubscriptionsData()
    subscription = next((sub for sub in subscriptionsData if sub['id'] == id), None)
    if subscription:
        print(subscription['rates'])
    else:
        print("Not found")
    return render(request, 'subscription.html', {'data' : {
        'subscription': subscription
    }})