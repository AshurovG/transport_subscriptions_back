from django.contrib import admin
from django.urls import include, path
from transport_subscription_app import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('categories', views.getСategories, name='categories-list'),
    path('categories/<int:pk>', views.getCategoryById, name='categories-by-id'),
    path('categories/post', views.postСategory, name='categories-post'),
    path('categories/<int:pk>/put', views.putСategory, name='categories-put'),
    path('categories/<int:pk>/delete', views.deleteСategory, name='categories-delete'),

    path('subscriptions', views.getSubscriptions, name='subscriptions-list'),
    path('subscriptions/<int:pk>', views.getSubscriptionById, name='subscriptions-by-id'),
    path('subscriptions/post', views.postSubscription, name='subscriptions-post'),
    path('subscriptions/<int:pk>/put', views.putSubscription, name='subscriptions-put'),
    path('subscriptions/<int:pk>/delete', views.deleteSubscription, name='subscriptions-delete'),
    
    path('applications', views.GetApplications, name = 'applications-list'),

    path('admin/', admin.site.urls),
]