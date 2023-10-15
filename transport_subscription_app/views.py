from django.shortcuts import render
from django.shortcuts import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from transport_subscription_app.serializers import *
from transport_subscription_app.models import *
from rest_framework.decorators import api_view
from datetime import datetime


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

    # category = get_object_or_404(Category, pk=pk)
    # category.delete()
    # return Response(status=status.HTTP_204_NO_CONTENT)


#Subscriptions

@api_view(['GET'])
def getSubscriptions(request):
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


#Orders

@api_view(['GET'])
def GetApplications(request):
    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get('start', '2023-01-01')
    end_date_str = request.query_params.get('end', '2023-12-31')
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()
    applications = Application.objects.filter(creation_date__range=(start, end)).order_by('creation_date')
    serializer = ApplicationSerializer(applications, many=True)
    
    return Response(serializer.data)

# @api_view(['GET'])                                  # 1 заказ
# def GetOrder(request, pk):
#     if not Orders.objects.filter(id=pk).exists():
#         return Response(f"Заказа с таким id нет")

#     order = Orders.objects.get(id=pk)
#     serializer = OrderSerializer(order)
#     return Response(serializer.data)

# @api_view(['DELETE'])                               # удалить заказ?
# def DeleteOrder(request, pk):
#     if not Orders.objects.filter(id=pk).exists():
#         return Response(f"Заказа с таким id нет")
#     order = Orders.objects.get(id=pk)
#     order.status = "отказ"
#     order.save()

#     order = Orders.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)

# @api_view(['PUT'])                                  # изменить заказ
# def PutOrder(request, pk):
#     try:
#         order = Orders.objects.get(id=pk)
#     except Orders.DoesNotExist:
#         return Response("Заказа с таким id нет")
#     serializer = OrderSerializer(order, data=request.data, partial=True)
#     if not serializer.is_valid():
#         return Response(serializer.errors)
#     serializer.save()

#     order = Orders.objects.all()
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)