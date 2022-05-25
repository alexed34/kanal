from django.db import models

class Orders(models.Model):
    num = models.IntegerField()
    order_num = models.IntegerField()
    cost_usd = models.IntegerField()
    delivery_time = models.DateField()
    cost_rub = models.IntegerField(blank=True, null=True)




