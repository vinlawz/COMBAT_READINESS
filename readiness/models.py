from django.db import models

class Soldier(models.Model):
    RANK_CHOICES = [
        ('Private', 'Private'),
        ('Corporal', 'Corporal'),
        ('Sergeant', 'Sergeant'),
        ('Lieutenant', 'Lieutenant'),
        ('Captain', 'Captain'),
        ('Major', 'Major'),
        ('Colonel', 'Colonel'),
        ('General', 'General'),
    ]

    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=20, choices=RANK_CHOICES)
    unit = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return f"{self.rank} {self.name}"


class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('Weapon', 'Weapon'),
        ('Vehicle', 'Vehicle'),
        ('Communication', 'Communication'),
        ('Medical', 'Medical'),
        ('Other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Good', 'Good'),
        ('Needs Repair', 'Needs Repair'),
        ('Damaged', 'Damaged'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    assigned_to = models.ForeignKey(Soldier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
