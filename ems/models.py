from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"    


class Department(models.Model):
    name = models.CharField(max_length=100, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.company.name})" 

class Employee(models.Model):
    DESIGNATIONS = [
        ('Jr', 'Junior'),
        ('As', 'Associate'),
        ('Sr', 'Senior'),
        ('Mg', 'Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department)
    designation = models.CharField(choices=DESIGNATIONS, max_length=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
