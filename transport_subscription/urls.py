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
    # path('categories/<int:pk>', views.putСategory, name='categories-put'),
    path('categories/<int:pk>/delete', views.deleteСategory, name='categories-delete'),

    path('subscriptions', views.getSubscriptions, name='subscriptions-list'),
    path('subscriptions/<int:pk>', views.getSubscriptionById, name='subscriptions-by-id'),
    path('subscriptions/post', views.postSubscription, name='subscriptions-post'),
    path('subscriptions/<int:pk>/post', views.postImageToSubscription, name="post-image-to-subscription"),
    path('subscriptions/<int:pk>/put', views.putSubscription, name='subscriptions-put'),
    path('subscriptions/<int:pk>/delete', views.deleteSubscription, name='subscriptions-delete'),
    # path('subscriptions/<int:pk>/post', views.PostSubscriptionToApplication, name = 'add_subscription_to_application'),
    
    path('applications', views.getApplications, name = 'applications-list'), 
    path('applications/<int:pk>', views.getApplication, name = 'application'), # Поменять название метода !!!
    path('applications/<int:pk>/delete', views.DeleteApplication, name = 'application_delete'),
    path('applications/<int:pk>/put', views.PutApplication, name = 'application_put'),

    path('applications/<int:pk>/adminput', views.putApplicationByAdmin, name = 'application_by_admin'),
    path('applications/userput', views.putApplicationByUser, name = 'application_by_user'),

    path('application_subscription/<int:pk>/delete', views.DeleteApplicationSubscription, name = 'application_subscription_delete'),

    path('admin/', admin.site.urls),
]