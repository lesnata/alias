# Generated by Django 3.1.6 on 2021-02-10 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=255)),
                ('start', models.DateTimeField(auto_now=True)),
                ('end', models.DateTimeField(null=True)),
                ('target', models.ForeignKey(db_constraint=False, max_length=24, on_delete=django.db.models.deletion.DO_NOTHING, to='app.object')),
            ],
        ),
    ]