from transport_subscriptions_back_app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetSubscriptions),
    path('subscription/<int:id>/', views.GetSubscription, name='subscription_url'),
]
