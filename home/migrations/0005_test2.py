# Generated by Django 4.0.4 on 2022-05-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_orders_cost_rub2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('order_num', models.IntegerField()),
                ('cost_usd', models.IntegerField()),
                ('delivery_time', models.DateField()),
                ('cost_rub', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
