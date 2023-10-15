from django.shortcuts import render
from django.shortcuts import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from transport_subscription_app.serializers import *
from transport_subscription_app.models import *
from rest_framework.decorators import api_view


#Categories

@api_view(['GET'])
def getСategories(request):
    categories = Category.objects.all()
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


# ВОЗМОЖНО ПРИДЕТСЯ ПЕРЕДЕЛАТЬ НА УДАЛЕНИЕ ЧЕРЕЗ СТАТУС ! ! !

# def DeleteDish(request, pk):
#     if not Dishes.objects.filter(id=pk).exists():
#         return Response(f"Блюда с таким id нет")
#     dish = Dishes.objects.get(id=pk)
#     dish.status = "удаленo"
#     dish.save()

#     dish = Dishes.objects.filter(status="есть")
#     serializer = DishSerializer(dish, many=True)
#     return Response(serializer.data)

@api_view(['DELETE'])
def deleteСategory(request, pk):    
    if not Category.objects.filter(pk=pk).exists():
        return Response(f"Категории с таким id нет")
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#Subscriptions

@api_view(['GET'])
def getSubscriptions(request):
    subscriptions = Subscription.objects.all()
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
    subscription = get_object_or_404(Subscription, pk=pk)
    subscription.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)