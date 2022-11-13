# Generated by Django 4.1.3 on 2022-11-13 17:45

import uuid

import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AirflowSearch",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="updated")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "state",
                    models.CharField(
                        choices=[("pending", "pending"), ("completed", "completed")],
                        default="pending",
                        max_length=15,
                        verbose_name="state",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="updated")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("title", models.CharField(db_index=True, max_length=3, unique=True)),
                ("fullname", models.CharField(max_length=300)),
                ("in_kzt", models.DecimalField(decimal_places=2, max_digits=12)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Provider",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="updated")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("title", models.CharField(db_index=True, max_length=300, unique=True)),
                ("url", models.URLField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="updated")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("base_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("tax_price", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "airflow_search",
                    models.ForeignKey(
                        help_text="airflow_search",
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="flights",
                        to="flights.airflowsearch",
                        verbose_name="airflow_search",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        help_text="currency",
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="flights",
                        to="flights.currency",
                        verbose_name="currency",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
