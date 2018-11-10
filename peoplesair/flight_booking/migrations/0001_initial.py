# Generated by Django 2.1.3 on 2018-11-10 14:15

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
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128, unique=True, verbose_name='Number')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=128, unique=True, verbose_name='Number')),
                ('origin', models.CharField(max_length=128, verbose_name='Origin')),
                ('destination', models.CharField(max_length=128, verbose_name='Destination')),
                ('departure', models.DateTimeField(verbose_name='Departure')),
                ('arrival', models.DateTimeField(verbose_name='Arrival')),
                ('available_seats', models.IntegerField(verbose_name='Available Seats')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='flight_booking.Flight'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]
