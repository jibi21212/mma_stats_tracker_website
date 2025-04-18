from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.TextField()
    date = models.TextField()
    location = models.TextField()
    
    class Meta:
        db_table = 'event'
        managed = False

class Fight(models.Model):
    fight_id = models.AutoField(primary_key=True)
    event_name = models.TextField()
    date = models.TextField()
    title_bout = models.IntegerField()
    method = models.TextField()
    round_ended = models.IntegerField()
    time_ended = models.IntegerField()
    referee = models.TextField()
    event = models.ForeignKey(Event, models.CASCADE, db_column='event_id')
    
    class Meta:
        db_table = 'fight'
        managed = False

class Fighters(models.Model):
    fighters_id = models.AutoField(primary_key=True)
    name = models.TextField()
    nationality = models.TextField()
    nickname = models.TextField()
    height = models.IntegerField()
    weight = models.IntegerField()
    reach = models.IntegerField()
    stance = models.TextField()
    date_of_birth = models.TextField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    draws = models.IntegerField()
    no_contests = models.IntegerField()
    was_champion = models.BooleanField()
    championship_bouts_won = models.IntegerField()
    
    class Meta:
        db_table = 'fighters'
        managed = False

class CareerStats(models.Model):
    stat_id = models.AutoField(primary_key=True)
    strikes_per_minute = models.FloatField()
    strike_accuracy = models.FloatField()
    strikes_absorbed_per_minute = models.FloatField()
    strike_defense = models.FloatField()
    takedown_average = models.FloatField()
    takedown_accuracy = models.FloatField()
    takedown_defense = models.FloatField()
    submission_average = models.FloatField()
    fighter = models.ForeignKey(Fighters, models.CASCADE, db_column='fighters_id')
    
    class Meta:
        db_table = 'career_stats'
        managed = False

class StrikeStats(models.Model):
    strike_stats_id = models.AutoField(primary_key=True)
    landed = models.IntegerField()
    attempted = models.IntegerField()
    percentage = models.FloatField()
    
    class Meta:
        db_table = 'strike_stats'
        managed = False

class FightPerformance(models.Model):
    fightp_id = models.AutoField(primary_key=True)
    fighter_name = models.TextField()
    fighter = models.ForeignKey(Fighters, models.CASCADE, db_column='fighters_id')
    fight = models.ForeignKey(Fight, models.CASCADE, db_column='fight_id')
    result = models.TextField()  # 'w', 'l', 'd', 'nc'
    
    class Meta:
        db_table = 'fight_performance'
        managed = False

class StrikeBreakdown(models.Model):
    strike_breakdown_id = models.AutoField(primary_key=True)
    significant_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='significant', db_column='significant_strikes_id')
    total_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='total', db_column='total_strikes_id')
    head_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='head', db_column='head_strikes_id')
    body_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='body', db_column='body_strikes_id')
    leg_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='leg', db_column='leg_strikes_id')
    distance_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='distance', db_column='distance_strikes_id')
    clinch_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='clinch', db_column='clinch_strikes_id')
    ground_strikes = models.ForeignKey(StrikeStats, models.CASCADE, related_name='ground', db_column='ground_strikes_id')
    
    class Meta:
        db_table = 'strike_breakdown'
        managed = False

class RoundStats(models.Model):
    round_id = models.AutoField(primary_key=True)
    round_number = models.IntegerField()
    knockdowns = models.IntegerField()
    submission_attempts = models.IntegerField()
    reversals = models.IntegerField()
    control_time = models.IntegerField()
    fight_performance = models.ForeignKey(FightPerformance, models.CASCADE, db_column='fightp_id')
    strike_stats = models.ForeignKey(StrikeStats, models.CASCADE, db_column='strike_stats_id')
    strike_breakdown = models.ForeignKey(StrikeBreakdown, models.CASCADE, db_column='strike_breakdown_id')
    
    class Meta:
        db_table = 'round_stats'
        managed = False