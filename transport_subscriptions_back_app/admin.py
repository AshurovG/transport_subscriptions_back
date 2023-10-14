from django.contrib import admin

from transport_subscriptions_back_app.models import *

admin.site.register(User)
admin.site.register(Subscription)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(ApplicationSubscription)


