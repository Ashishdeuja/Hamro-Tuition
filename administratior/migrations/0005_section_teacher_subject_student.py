# Generated by Django 4.1.3 on 2022-12-23 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administratior', '0004_alter_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=22)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administratior.level')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=35)),
                ('phone_number', models.CharField(max_length=25)),
                ('gender', models.CharField(max_length=15)),
                ('education', models.CharField(max_length=35)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administratior.level')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=25)),
                ('marks', models.IntegerField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administratior.level')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administratior.level')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administratior.section')),
            ],
        ),
    ]
