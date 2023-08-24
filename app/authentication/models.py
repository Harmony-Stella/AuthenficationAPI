from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UtilisateurManager(BaseUserManager):
    # Gestionnaire personnalisé pour la classe Utilisateur
    def create_user(self, username, email, password, type_utilisateur, **extra_fields):
        # Crée un utilisateur avec les informations fournies
        # Normalize l'adresse e-mail pour une cohérence
        user = self.model(username=username, email=self.normalize_email(email), type_utilisateur=type_utilisateur, **extra_fields)
        user.set_password(password)  # Hache le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, type_utilisateur, **extra_fields):
        # Crée un superutilisateur avec des privilèges d'administration
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, type_utilisateur, **extra_fields)

class Utilisateur(AbstractBaseUser):
    TYPE_UTILISATEUR_CHOICES = (
        ('client', 'Client'),
        ('administrateur', 'Administrateur'),
        ('manager', 'Manager'),
        ('chauffeur', 'Chauffeur'),
    )
    
    # Attributs de la classe Utilisateur
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    type_utilisateur = models.CharField(max_length=20, choices=TYPE_UTILISATEUR_CHOICES)
    last_login_start = models.DateTimeField()
    last_login_end = models.DateTimeField()
    
    # Informations personnelles
    prenom_utilisateur = models.CharField(max_length=50, blank=True)
    nom_utilisateur = models.CharField(max_length=50, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    addresse = models.CharField(max_length=100, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    
    # Informations de connexion
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Code matricule de l'entreprise pour les agents
    code_matricule = models.CharField(max_length=20, null=True, blank=True)
    
    objects = UtilisateurManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'type_utilisateur']
    
    def __str__(self, *args, **kwargs):
        self.type_utilisateur="utilisateur"
        super().save(*args,**kwargs)
        return self.username

