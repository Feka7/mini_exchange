# Generated by Django 3.0.5 on 2020-07-23 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ips', models.Field(default={})),
                ('order_list', models.Field(default={})),
                ('bitcoin', models.PositiveIntegerField()),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('SA', 'SALE'), ('PU', 'PURCHASE'), ('CL', 'CLOSE'), ('ST', 'STAND-BY')], default='ST', max_length=2)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ex.Profile')),
            ],
        ),
    ]