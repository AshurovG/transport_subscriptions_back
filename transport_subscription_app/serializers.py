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

class ApplicationSerializer(serializers.ModelSerializer):
    # publication_date = serializers.DateTimeField(default=datetime.now)

    class Meta:
        model = Application
        fields = '__all__'

class ApplicationSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationSubscription
        fields = ['id_application', 'id_subscription']

class UserSerializer(serializers.ModelSerializer):
    isModerator = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = User
        # fields = ['email', 'password', 'isModerator', 'phone_number', "full_name"]
        fields = '__all__'