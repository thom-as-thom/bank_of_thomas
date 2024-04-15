# Generated by Django 5.0.4 on 2024-04-15 21:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_account_id_alter_account_account_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_number",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="routing_number",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]