import django
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome


class Viaggio(models.Model):
    TIPO_CHOICES_F = [
        (0, 'Non Fatturato'),
        (1, 'Fatturato'),
    ]
    TIPO_CHOICES_P = [
        (0, 'Non Pagato'),
        (1, 'Pagato'),
    ]

    data_viaggio = models.DateField(default=django.utils.timezone.now)
    distanza_km = models.DecimalField(max_digits=10, decimal_places=2)
    ddt = models.DecimalField(max_digits=10, decimal_places=0)
    prezzo_viaggio = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, related_name='viaggi_cliente')
    mittente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, related_name='viaggi_mittente')
    stato = models.IntegerField(choices=TIPO_CHOICES_F, default=0)
    pagato = models.IntegerField(choices=TIPO_CHOICES_P, default=0)

    def __str__(self):
        return f"{self.data_viaggio} - {self.cliente} - {self.prezzo_viaggio}€"

class Fattura(models.Model):
    TIPO_CHOICES = [
        ('T', 'Tasse'),
        ('B', 'Burocrazia'),
        ('C', 'Clienti'),
        ('S', 'Spese'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    data = models.DateField(default=django.utils.timezone.now)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    viaggi = models.ManyToManyField(Viaggio)

    def clean(self):
        if self.importo is None:
            raise ValidationError('L\'importo non può essere None.')

    def calcola_importo(self):
        return sum(viaggio.prezzo_viaggio for viaggio in self.viaggi.all())

    def __str__(self):
        return f"{self.numero} - {self.data} - {self.importo} - {self.tipo}"