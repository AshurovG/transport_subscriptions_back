from django.shortcuts import render
from django.shortcuts import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from transport_subscription_app.serializers import *
from transport_subscription_app.models import *
from rest_framework.decorators import api_view
from datetime import datetime


class CurrentUserSingleton: 
    _instance = None 
 
    @classmethod 
    def get_instance(cls): 
        if not cls._instance: 
            cls._instance = cls._get_user() 
        return cls._instance 
 
    @classmethod 
    def _get_user(cls): 
        return User.objects.get(login='user1', password='1234', isModerator=False)
    

# user = User(id=2, login="user1", password='1234', isModerator=False)

#Categories

@api_view(['GET'])
def getСategories(request):
    categories = Category.objects.filter(status="enabled")
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def getCategoryById(request, pk, format=None):
    if not Category.objects.filter(pk=pk).exists():
        return Response(f"Категории с таким id нет")
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
 
@api_view(['POST'])
def postСategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def putСategory(request, pk):
    if not Category.objects.filter(pk=pk).exists():
        return Response(f"Категории с таким id нет")
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteСategory(request, pk):    
    if not Category.objects.filter(pk=pk).exists():
        return Response(f"Категории с таким id нет")
    category = Category.objects.get(pk=pk)
    category.status = "deleted"
    category.save()

    category = Category.objects.filter(status="enabled")
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

#Subscriptions

@api_view(['GET'])
def getSubscriptions(request):
    value = request.query_params.get("value")

    if value:
        subscriptions = Subscription.objects.filter(status="enabled", id_category__title__icontains=value)
    else:
        subscriptions = Subscription.objects.filter(status="enabled")

    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def getSubscriptionById(request, pk):
    if not Subscription.objects.filter(pk=pk).exists():
        return Response(f"Абонемента с таким id нет")
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
 
@api_view(['POST'])
def postSubscription(request):
    serializer = SubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def PostSubscriptionToApplication(request, pk):
    current_user = CurrentUserSingleton.get_instance()
    try: 
        application = Application.objects.filter(id_user=current_user, status="Зарегистрирован").latest('creation_date')
    except:
        application = Application(
            status='Зарегистрирован',
            creation_date=datetime.now(),
            id_user=current_user,
        )
        application.save()
    id_application = application
    try:
        subscription = Subscription.objects.get(pk=pk, status='enabled')
    except Subscription.DoesNotExist:
        return Response("Такой услуги нет", status=400)
    try:
        application_subscription = ApplicationSubscription.objects.get(id_application=id_application, id_subscription=subscription)
        return Response("Такой абонемент уже добавлен в заявку")
    except ApplicationSubscription.DoesNotExist:
        application_subscription = ApplicationSubscription(
            id_application=id_application,
            id_subscription=subscription,
        )
        application_subscription.save()
    application_subscription = ApplicationSubscription.objects.filter(id_application = id_application)
    serializer = ApplicationSubscriptionSerializer(application_subscription, many=True)
    # applications = Application.objects.all()
    # serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def putSubscription(request, pk):
    if not Subscription.objects.filter(pk=pk).exists():
        return Response(f"Абонемента с таким id нет")
    subscription = get_object_or_404(Subscription, pk=pk)
    serializer = SubscriptionSerializer(subscription, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteSubscription(request, pk):
    if not Subscription.objects.filter(pk=pk).exists():
        return Response(f"Абонемента с таким id нет")
    subscription = Subscription.objects.get(pk=pk)
    subscription.status = "deleted"
    subscription.save()

    subscription = Subscription.objects.filter(status="enabled")
    serializer = SubscriptionSerializer(subscription, many=True)
    return Response(serializer.data)


#Applications

from django.db.models import Q

@api_view(['GET'])
def getApplications(request):
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get('start', '2023-01-01')
    end_date_str = request.query_params.get('end', '2023-12-31')
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()
    
    status = request.data.get('status')

    applications = Application.objects.filter(
        ~Q(status="Удалено"),
        creation_date__range=(start, end)
    )
    
    if status:
        applications = applications.filter(status=status)

    applications = applications.order_by('creation_date')
    serializer = ApplicationSerializer(applications, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getApplication(request, pk):
    try:
        application = Application.objects.get(pk=pk)
        if application.status == "Удалено":
            return Response("Заявки с таким id нет")

        application_serializer = ApplicationSerializer(application)
        application_subscriptions = ApplicationSubscription.objects.filter(id_application=application)
        application_subscriptions_serializer = ApplicationSubscriptionSerializer(application_subscriptions, many=True)

        response_data = {
            'application': application_serializer.data,
            'subscriptions': application_subscriptions_serializer.data
        }

        return Response(response_data)
    except Application.DoesNotExist:
        return Response("Заявки с таким id нет")


@api_view(['DELETE'])
def DeleteApplication(request, pk):
    if not Application.objects.filter(pk=pk).exists():
        return Response(f"Заявки с таким id нет")
    application = Application.objects.get(pk=pk)
    application.status = "Удалено"
    application.save()

    application = Application.objects.all()
    serializer = ApplicationSerializer(application, many=True)
    return Response(serializer.data)

@api_view(['PUT']) # можно добавить фильтр на удаленную заявку
def PutApplication(request, pk):
    try:
        order = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response("Заявки с таким id нет")
    serializer = ApplicationSerializer(order, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors)
    serializer.save()

    order = Application.objects.all()
    serializer = ApplicationSerializer(order, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def putApplicationByAdmin(request, pk):
    if not Application.objects.filter(pk=pk).exists():
        return Response(f"Заявки с таким id нет")
    application = Application.objects.get(pk=pk)
    if application.status != "Проверяется":
        return Response("Такой заявки нет на проверке")
    if request.data["status"] not in ["Отказано", "Принято"]:
        print(11111111)
        return Response("Неверный статус!")
    application.status = request.data["status"]
    application.publication_date=datetime.now().date()
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

# @api_view(['PUT'])
# def putApplicationByUser(request, pk):
#     if not Application.objects.filter(pk=pk).exists():
#         return Response(f"Заявки с таким id нет")
#     application = Application.objects.get(pk=pk)
#     if application.status != "Зарегистрирован":
#         return Response("Такой заявки не зарегистрировано")
#     application.status = "Проверяется"
#     application.processed_at=datetime.now().date()
#     application.save()
#     serializer = ApplicationSerializer(application)
#     return Response(serializer.data)

@api_view(['PUT'])
def putApplicationByUser(request):
    current_user = CurrentUserSingleton.get_instance()
    try:
        application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
    except:
        return Response("Такой заявки не зарегистрировано")
    
    application.status = "Проверяется"
    application.processed_at=datetime.now().date()
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['PUT'])
def PutApplicationSubscription(request, pk):
    current_user = CurrentUserSingleton.get_instance()
    application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
    
    try:
        subscription = Subscription.objects.get(pk=pk, status='enabled')
    except Subscription.DoesNotExist:
        return Response("Такой услуги нет", status=400)
    
    application_subscription = ApplicationSubscription.objects.filter(id_application=application, id_subscription=subscription).first()
    if application_subscription:
        id_subscription = request.data.get('id_subscription')
        try:
            subscription = Subscription.objects.get(id=id_subscription, status='enabled')
            application_subscription.id_subscription = subscription
            application_subscription.save()
            serializer = ApplicationSubscriptionSerializer(application_subscription, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Subscription.DoesNotExist:
            return Response("Такой услуги нет", status=400)
    else:
        return Response("Заявка не найдена", status=404)
    
@api_view(['DELETE'])
def DeleteApplicationSubscription(request, pk):
    current_user = CurrentUserSingleton.get_instance()
    application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
    try:
        subscription = Subscription.objects.get(pk=pk, status='enabled')
        try:
            application_subscription = get_object_or_404(ApplicationSubscription, id_application=application, id_subscription=subscription)
            application_subscription.delete()
            return Response("Абонемент удален", status=200)
            # application_subscription = ApplicationSubscription.objects.all()
            # serializer = ApplicationSubscriptionSerializer(application_subscription, many=True)
            # return Response(serializer.data)
        except ApplicationSubscription.DoesNotExist:
            return Response("Заявка не найдена", status=404)
    except Subscription.DoesNotExist:
        return Response("Такой услуги нет", status=400)
    

# {
#   "title": "Тестовый абонемент",
#   "price": "5000р.",
#   "info": "Дополнительная информация об абонементе",
#   "src": "images/mcd.jpg",
#   "id_category": 1,
#   "status": "enabled"
# }