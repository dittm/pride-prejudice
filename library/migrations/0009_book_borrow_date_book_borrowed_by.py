# Generated by Django 4.2.2 on 2023-07-23 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0008_remove_book_borrow_date_remove_book_borrowed_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrow_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='borrowed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
