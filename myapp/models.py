from django.db import models



class Fighter(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Height in meters
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Weight in kilograms
    reach = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)   # Reach in centimeters
    stance = models.CharField(max_length=50, blank=True, null=True)  # Orthodox, Southpaw, etc.
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class FighterStats(models.Model):
    fighter = models.OneToOneField(Fighter, on_delete=models.CASCADE, related_name='stats')
    sig_strikes_perMin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    strikes_accuracy = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sig_strikes_abs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    strike_def = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    takedown_average_per15 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    takedowns_accuracy = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    takedown_defense = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sub_avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Stats for {self.fighter.name}"

import datetime

class Bout(models.Model):
    fighter_1 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='bouts_as_fighter_1')
    fighter_2 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='bouts_as_fighter_2')
    method = models.CharField(max_length=100)  # e.g., KO, submission, decision, etc.
    result = models.CharField(max_length=50)  # e.g., Win, Loss, Draw, No Contest
    winner = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='won_bouts')
    date = models.DateField(default=datetime.date.today)  # Set default to today

    def __str__(self):
        return f"{self.fighter_1.name} vs {self.fighter_2.name}"
