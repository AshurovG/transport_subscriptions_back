from transport_subscriptions_back_app import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetSubscriptions, name='subscriptions_url'),
    path('subscription/<int:id>/', views.GetSubscription, name='subscription_url'),
    # path('subscription/<int:id>/', views.GetSubscription, name='subscription_url'),
    path('delete/<int:record_id>/', views.DeleteRecord, name='delete_record'),
]
