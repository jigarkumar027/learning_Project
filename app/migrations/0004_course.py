# Generated by Django 3.2.5 on 2021-08-18 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Code', models.IntegerField()),
                ('Description', models.CharField(max_length=100)),
                ('Duration', models.CharField(max_length=50)),
                ('Price', models.IntegerField()),
                ('Technology', models.CharField(max_length=50)),
                ('Pre_Requirment', models.CharField(max_length=50)),
                ('course_pic', models.ImageField(default='abc.jpg', upload_to='img/')),
                ('is_created', models.DateTimeField(auto_now_add=True)),
                ('is_update', models.DateTimeField(auto_now_add=True)),
                ('Category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('Tutor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tutor')),
            ],
        ),
    ]