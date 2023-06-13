from django.db import models


class Checkerboard(models.Model):
    number = models.DecimalField('Номер', max_digits=3, decimal_places=0, null=True)
    infrastructure_id = models.OneToOneField('infrastructures_app.Infrastructure', on_delete=models.CASCADE)


class Floor(models.Model):
    number = models.DecimalField('Этаж номер', max_digits=3, decimal_places=0, null=True)
    section_id = models.ForeignKey('infrastructures_app.Section', on_delete=models.CASCADE)


class Riser(models.Model):
    number = models.DecimalField('Стояк номер', max_digits=3, decimal_places=0, null=True)
    section_id = models.ForeignKey('infrastructures_app.Section', on_delete=models.CASCADE)
