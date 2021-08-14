# Generated by Django 3.2.5 on 2021-08-14 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import services.account_recovery.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecoverPasswordCode',
            fields=[
                ('id', models.CharField(default=services.account_recovery.utils.generate_password_recover_code, editable=False, max_length=8, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'recover password code',
                'verbose_name_plural': 'recover password codes',
            },
        ),
    ]
