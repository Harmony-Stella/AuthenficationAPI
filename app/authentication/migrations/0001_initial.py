# Generated by Django 4.2.4 on 2023-08-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('type_utilisateur', models.CharField(choices=[('client', 'Client'), ('administrateur', 'Administrateur'), ('manager', 'Manager'), ('chauffeur', 'Chauffeur')], max_length=20)),
                ('last_login_start', models.DateTimeField()),
                ('last_login_end', models.DateTimeField()),
                ('prenom_utilisateur', models.CharField(blank=True, max_length=50)),
                ('nom_utilisateur', models.CharField(blank=True, max_length=50)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('numero_telephone', models.CharField(blank=True, max_length=20, null=True)),
                ('addresse', models.CharField(blank=True, max_length=100, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('genre', models.CharField(blank=True, max_length=10, null=True)),
                ('pays', models.CharField(blank=True, max_length=50, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('code_matricule', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
