from django.urls import include, path
from transport_subscription_app import views
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'user', views.UserViewSet, basename='user')

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
    path('subscriptions/<int:pk>/image/post', views.postImageToSubscription, name="post-image-to-subscription"),
    path('subscriptions/<int:pk>/put', views.putSubscription, name='subscriptions-put'),
    path('subscriptions/<int:pk>/delete', views.deleteSubscription, name='subscriptions-delete'),
    path('subscriptions/<int:pk>/post', views.PostSubscriptionToApplication, name = 'add_subscription_to_application'),
    
    path('applications', views.getApplications, name = 'applications-list'), 
    path('applications/<int:pk>', views.getApplication, name = 'application'),
    path('applications/delete', views.DeleteApplication, name = 'application_delete'),
    path('applications/<int:pk>/put', views.PutApplication, name = 'application_put'),

    path('applications/<int:pk>/adminput', views.putApplicationByAdmin, name = 'application_by_admin'),
    path('applications/userput', views.putApplicationByUser, name = 'application_by_user'),

    path('application_subscription/<int:pk>/delete', views.DeleteApplicationSubscription, name = 'application_subscription_delete'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login',  views.login_view, name='auth'),
    path('logout', views.logout_view, name='logout'),
    path('user_info', views.user_info, name='user_info')
]