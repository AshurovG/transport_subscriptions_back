from django.shortcuts import render
from django.shortcuts import *
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from transport_subscription_app.serializers import *
from transport_subscription_app.models import *
from datetime import datetime
from minio import Minio
from rest_framework.decorators import api_view, parser_classes, permission_classes, authentication_classes, permission_classes, action
from django.http import HttpResponseServerError
import os
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from transport_subscription_app.permissions import *


class CurrentUserSingleton: 
    _instance = None 
 
    @classmethod 
    def get_instance(cls): 
        if not cls._instance: 
            cls._instance = cls._get_user() 
        return cls._instance 
 
    @classmethod 
    def _get_user(cls): 
        return CustomUser.objects.get(email='test@mail.ru', password='pbkdf2_sha256$600000$PxEZbMzzP7Ixb2f8TULs5e$UB+lN2K7/gpblGhsncTxQx7v8t0vMR4awzHEiOfIB1c=')
    

#Categories

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @permission_classes([IsAdmin])
# @permission_classes([IsManager])
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
    category = request.query_params.get("category")
    title = request.query_params.get("title")
    max_price = request.query_params.get("max_price")

    subscriptions = Subscription.objects.filter(status="enabled")

    if category:
        subscriptions = subscriptions.filter(id_category__title__icontains=category)
    if title:
        subscriptions = subscriptions.filter(title__icontains=title)
    if max_price:
        subscriptions = subscriptions.filter(price__lte=max_price)

    try: 
        current_user = CurrentUserSingleton.get_instance()
        application = Application.objects.filter(id_user=current_user, status="Зарегистрирован").latest('creation_date')
        serializer = SubscriptionSerializer(subscriptions, many=True)
        application_serializer = ApplicationSerializer(application)
        result = {
            'application_id': application_serializer.data['id'],
            'subscriptions': serializer.data
        }
        return Response(result)
    except:
        serializer = SubscriptionSerializer(subscriptions, many=True)
        result = serializer.data
        return Response(result)

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
    data = request.data.copy()  # Создаем копию данных запроса
    data['status'] = 'enabled'  # Устанавливаем значение "enabled" для поля "status"
    
    serializer = SubscriptionSerializer(data=data)
    if serializer.is_valid():
        new_option = serializer.save()
        client = Minio(endpoint="localhost:9000",
               access_key='minioadmin',
               secret_key='minioadmin',
               secure=False)
        i=new_option.id-1
        try:
            i = new_option.id
            img_obj_name = f"{i}.jpg"
            file_path = f"assets/{request.data.get('src')}"  
            client.fput_object(bucket_name='images',
                            object_name=img_obj_name)
                            # file_path=file_path)
            new_option.src = f"localhost:9000/images/{img_obj_name}"
            new_option.save()
        except Exception as e:
            return Response({"error": str(e)})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def postImageToSubscription(request, pk):
    if 'file' in request.FILES:
        file = request.FILES['file']
        subscription = Subscription.objects.get(pk=pk, status='enabled')
        
        client = Minio(endpoint="localhost:9000",
                       access_key='minioadmin',
                       secret_key='minioadmin',
                       secure=False)

        bucket_name = 'images'
        file_name = file.name
        file_path = "http://localhost:9000/images/" + file_name
        
        try:
            client.put_object(bucket_name, file_name, file, length=file.size, content_type=file.content_type)
            print("Файл успешно загружен в Minio.")
            
            serializer = SubscriptionSerializer(instance=subscription, data={'src': file_path}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Image uploaded successfully.')
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            returnHttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

@api_view(['GET']) # Желательно сделать чтобы выводились поля услуг а не м-м
@permission_classes([IsAuthenticated])
def getApplication(request, pk):
    try:
        application = Application.objects.get(pk=pk)
        if application.status == "Удалено" or not application:
            return Response("Заявки с таким id нет")

        application_serializer = ApplicationSerializer(application)
        application_subscriptions = ApplicationSubscription.objects.filter(id_application=application)
        application_subscriptions_serializer = ApplicationSubscriptionSerializer(application_subscriptions, many=True)
        print(application_subscriptions)

        response_data = {
            'application': application_serializer.data,
            'subscriptions': application_subscriptions_serializer.data
        }

        return Response(response_data)
    except Application.DoesNotExist:
        return Response("Заявки с таким id нет")

@api_view(['DELETE']) # Делает проверку на пользователя и проверяет если ли у такого пользователя заявка с таким id=pk
@permission_classes([IsAuthenticated])
def DeleteApplication(request, pk):
    current_user = CurrentUserSingleton.get_instance()
    try: 
        application = Application.objects.filter(id=pk, id_user=current_user, status="Зарегистрирован").latest('creation_date')
        print(current_user.id)
        if not Application.objects.filter(pk=pk).exists():
            return Response(f"Заявки с таким id нет")
        application = Application.objects.get(pk=pk)
        application.status = "Удалено"
        application.save()

        application = Application.objects.all()
        serializer = ApplicationSerializer(application, many=True)
        return Response(serializer.data)
    except:
        print('У данного пользователя нет заявки')
        return Response("У данного пользователя нет заявки", status=400)
    

@api_view(['PUT']) # НУЖНО ДОБАВИТЬ ФИЛЬТР НА УДАЛЕННУЮ ЗАЯВКУ !!! И ЗАЧЕМ ВООБЩЕ ЭТОТ PUT ???
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
        return Response("Неверный статус!")
    application.status = request.data["status"]
    application.publication_date=datetime.now().date()
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

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
        except ApplicationSubscription.DoesNotExist:
            return Response("Заявка не найдена", status=404)
    except Subscription.DoesNotExist:
        return Response("Такой услуги нет", status=400)
    

#Auth
@permission_classes([AllowAny])
@authentication_classes([])
@csrf_exempt
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
def login_view(request):
    email = request.POST["email"] # допустим передали username и password
    password = request.POST["password"]
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("{'status': 'ok'}")
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

def logout_view(request):
    logout(request._request)
    return Response({'status': 'Success'})


class UserViewSet(viewsets.ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     full_name=serializer.data['full_name'],
                                     phone_number=serializer.data['phone_number'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)