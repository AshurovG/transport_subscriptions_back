from transport_subscription_app.models import *
from rest_framework import serializers
from datetime import datetime


class SubscriptionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='id_category.title', read_only=True)
    
    class Meta:
        model = Subscription
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'phone_number', 'is_staff', 'is_superuser']

class ApplicationSerializer(serializers.ModelSerializer):
 user = serializers.CharField(source='id_user.email', read_only=True)

 class Meta:
     model = Application
     fields = "__all__"



class ApplicationSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationSubscription
        fields = ['id_application', 'id_subscription']