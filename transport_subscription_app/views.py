from django.shortcuts import render
from django.shortcuts import *
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from django.http import HttpResponseForbidden
from transport_subscription_app.serializers import *
from transport_subscription_app.models import *
from datetime import datetime
from minio import Minio
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes, action
from django.http import HttpResponseServerError
import os
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from transport_subscription_app.permissions import *
from django.conf import settings
import redis
import uuid
from django.contrib.sessions.models import Session


session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

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

# @permission_classes([IsAuthenticated])
# @permission_classes([IsAdmin])
# @permission_classes([IsManager])

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
@permission_classes([IsManager])
def postСategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsManager])
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
@permission_classes([IsManager])
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
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")

    subscriptions = Subscription.objects.filter(status="enabled")

    if category:
        subscriptions = subscriptions.filter(id_category__title__icontains=category)
    if title:
        subscriptions = subscriptions.filter(title__icontains=title)
    if min_price and max_price:
        subscriptions = subscriptions.filter(price__range=(min_price, max_price))
    elif min_price:
        subscriptions = subscriptions.filter(price__gte=min_price)
    elif max_price:
        subscriptions = subscriptions.filter(price__lte=max_price)
    print('before try')
    try:
        ssid = request.COOKIES["session_id"]
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
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
        result = {
            'subscriptions': serializer.data
        }
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
@permission_classes([IsManager])
def postSubscription(request):
    data = request.data.copy()  # Создаем копию данных запроса
    data['status'] = 'enabled'  # Устанавливаем значение "enabled" для поля "status"
    
    serializer = SubscriptionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsManager])
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
                return HttpResponse(file_path)
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            returnHttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')

@api_view(['POST'])
@permission_classes([IsAuth])
def PostSubscriptionToApplication(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
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
        return Response("Такой абонемент уже добавлен в заявку", status=400)
    except ApplicationSubscription.DoesNotExist:
        application_subscription = ApplicationSubscription(
            id_application=id_application,
            id_subscription=subscription,
        )
        application_subscription.save()
    addedSubscription = Subscription.objects.get(pk = pk)
    serializer = SubscriptionSerializer(addedSubscription)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsManager])
def putSubscription(request, pk):
    if not Subscription.objects.filter(pk=pk).exists():
        return Response(f"Абонемента с таким id нет")
    subscription = get_object_or_404(Subscription, pk=pk)
    print(subscription.price)
    serializer = SubscriptionSerializer(subscription, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsManager])
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

# @permission_classes([IsManager])
@api_view(['GET'])
# @permission_classes([IsAuth])
def getApplications(request):
   try:
       if "session_id" in request.COOKIES:
          ssid = request.COOKIES["session_id"]
       else: 
          return HttpResponseForbidden('Сессия не найдена')
       
       email = session_storage.get(ssid).decode('utf-8')
       current_user = CustomUser.objects.get(email=email)
       date_format = "%Y-%m-%d"
       start_date_str = request.query_params.get('start', '2022-01-01')
       end_date_str = request.query_params.get('end', '2024-12-31')
       start = datetime.strptime(start_date_str, date_format).date()
       end = datetime.strptime(end_date_str, date_format).date()
       
       status = request.query_params.get('status')
       email_filter = request.query_params.get('email', None)

       if current_user.is_superuser: # Модератор может смотреть заявки всех пользователей
           print('модератор')
           applications = Application.objects.filter(
               ~Q(status="Удалено"),
               publication_date__range=(start, end)
           )
       else: # Авторизованный пользователь может смотреть только свои заявки
           applications = Application.objects.filter(
               ~Q(status="Удалено"),
               id_user=current_user.id,
               publication_date__range=(start, end)
           )
       
       if email_filter:
           
           applications = applications.filter(Q(user__icontains=email_filter))

       if status:
           applications = applications.filter(status=status)

       applications = applications.order_by('publication_date')
       serializer = ApplicationSerializer(applications, many=True)
       
       return Response(serializer.data)
   except:
       return HttpResponseForbidden('Сессия не найдена')

@api_view(['GET']) # Желательно сделать чтобы выводились поля услуг а не м-м
@permission_classes([IsAuth])
def getApplication(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    
    try:
        application = Application.objects.get(pk=pk)
        if application.status == "Удалено" or not application:
            return Response("Заявки с таким id нет")
        application_serializer = ApplicationSerializer(application)
        if (not current_user.is_superuser and current_user.id == application_serializer.data['id_user']) or (current_user.is_superuser):
            application_subscriptions = ApplicationSubscription.objects.filter(id_application=application)
            subscription_ids = [subscription.id_subscription_id for subscription in application_subscriptions]
            print(subscription_ids)
            subscriptions_queryset = Subscription.objects.filter(id__in=subscription_ids)
            subscriptions_serializer = SubscriptionSerializer(subscriptions_queryset, many=True)
            response_data = {
                'application': application_serializer.data,
                'subscriptions': subscriptions_serializer.data
            }
            return Response(response_data)
        else: 
            return Response("Заявки с таким id нет")
    except Application.DoesNotExist:
        return Response("Заявки с таким id нет")

@api_view(['DELETE']) # Делает проверку на пользователя и проверяет если ли у такого пользователя заявка с таким id=pk
@permission_classes([IsAuth])
def DeleteApplication(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')

    try: 
        application = Application.objects.get(id_user=current_user, status="Зарегистрирован")
        application.status = "Удалено"
        application.save()
        return Response({'status': 'Success'})
    except:
        return Response("У данного пользователя нет заявки", status=400)
    

@api_view(['PUT']) # НУЖНО ДОБАВИТЬ ФИЛЬТР НА УДАЛЕННУЮ ЗАЯВКУ !!! И ЗАЧЕМ ВООБЩЕ ЭТОТ PUT ???
@permission_classes([IsManager])
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

@api_view(['PUT']) # Сделать зполнение столбца модератора в таблице заявок
@permission_classes([IsManager])
def putApplicationByAdmin(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')

    if not Application.objects.filter(pk=pk).exists():
        return Response(f"Заявки с таким id нет")
    application = Application.objects.get(pk=pk)
    if application.status != "Проверяется":
        return Response("Такой заявки нет на проверке")
    if request.data["status"] not in ["Отказано", "Принято"]:
        return Response("Неверный статус!")
    application.status = request.data["status"]
    application.approving_date=datetime.now().date()
    if request.data["status"] != "Отказано":
        application.active_date=datetime.now().date()
    application.id_moderator = current_user
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuth])
def send_application(request):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    try:
        application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
    except:
        return Response("Такой заявки не зарегистрировано")
    
    application.status = "Проверяется"
    application.publication_date=datetime.now().date()
    application.save()
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)
    
@api_view(['DELETE'])
@permission_classes([IsAuth])
def DeleteApplicationSubscription(request, pk):
    ssid = request.COOKIES["session_id"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = CustomUser.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
    try:
        subscription = Subscription.objects.get(pk=pk, status='enabled')
        subscriptionsFromApplication = ApplicationSubscription.objects.filter(id_application = application)
        try:
            application_subscription = get_object_or_404(ApplicationSubscription, id_application=application, id_subscription=subscription)
            application_subscription.delete()
            if (len(subscriptionsFromApplication) == 0):
                application = get_object_or_404(Application, id_user=current_user, status="Зарегистрирован")
                application.status = 'Удалено'
                application.save()
            return Response("Абонемент удален", status=200)
        except ApplicationSubscription.DoesNotExist:
            return Response("Заявка не найдена", status=404)
    except Subscription.DoesNotExist:
        return Response("Такой услуги нет", status=400)


# Authorization methods

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        print('req is', request.data)
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     full_name=serializer.data['full_name'],
                                     phone_number=serializer.data['phone_number'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data['email'])
            user_data = {
                "email": request.data['email'],
                "full_name": request.data['full_name'],
                "phone_number": request.data['phone_number'],
                "is_superuser": False
            }

            print('user data is ', user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)
    
    if user is not None:
        print(user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone_number": user.phone_number,
            "password": user.password,
            "is_superuser": user.is_superuser,
        }
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="Lax", max_age=30 * 24 * 60 * 60)
        return response
    else:
        return HttpResponse("login failed", status=400)

@api_view(['POST'])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'status': 'Success'}
    else:
        response_data = {'status': 'Error', 'message': 'Session does not exist'}
    return Response(response_data)

@api_view(['GET'])
# @permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = CustomUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})