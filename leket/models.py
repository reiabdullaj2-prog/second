from django.db import models
from django.contrib.auth.models import User
class fitimet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategoria = models.CharField(max_length=100)
    data = models.DateField()
    shuma = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-data']
    def __str__(self):
        return f"{self.kategoria} - {self.data} - {self.shuma}"
class shpenzimet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategoria = models.CharField(max_length=100)
    data = models.DateField()
    shuma = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-data']
    def __str__(self):
        return f"{self.kategoria} - {self.data} - {self.shuma}"
class totali(models.Model):
    fitimet_totale = models.DecimalField(max_digits=10, decimal_places=2)
    shpenzimet_totale = models.DecimalField(max_digits=10, decimal_places=2)
    gjendja = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-gjendja']
    def __str__(self):
        return f"Fitimet Totale: {self.fitimet_totale} - Shpenzimet Totale: {self.shpenzimet_totale} - Gjendja: {self.gjendja}"          
