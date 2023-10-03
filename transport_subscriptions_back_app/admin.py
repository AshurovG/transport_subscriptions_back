from django.contrib import admin

from transport_subscriptions_back_app.models import *

admin.site.register(Users)
admin.site.register(Subscriptions)
admin.site.register(Applications)
admin.site.register(SubscriptionsRates)
admin.site.register(ApplicationsSubscriptions)


