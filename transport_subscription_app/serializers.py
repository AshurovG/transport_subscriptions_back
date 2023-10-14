from models import *
from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"

class ApplicationSubscriptionSerializer(serializers.ModelSerializer):
    id_subscription = serializers.StringRelatedField(read_only=True)
    id_application = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ApplicationSubscription
        fields = "__all__"