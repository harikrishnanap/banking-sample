from django.db import models

# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name


class AccountType(models.Model):
    Type_name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('Type_name',)

    def __str__(self):
        return '{}'.format(self.Type_name)


class District(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.name)


class Branches(models.Model):
    name = models.CharField(max_length=250, unique=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return '{}'.format(self.name)


class Application(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    age = models.IntegerField()
    dob = models.DateField()
    phone = models.CharField(max_length=12, unique=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branches', on_delete=models.CASCADE)
    account = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, default="material")
    

    class Meta:
        ordering = ('name',)
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return '{}'.format(self.name)


