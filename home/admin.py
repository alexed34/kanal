from django.contrib import admin

from home.models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['num', 'order_num', 'cost_usd','delivery_time', 'cost_rub']