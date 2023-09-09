# Generated by Django 4.2.5 on 2023-09-08 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mock", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mockwritingquestion",
            name="writing_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="writing_question",
                to="mock.mockwriting",
            ),
        ),
    ]
