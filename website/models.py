from django.db import models

# Create your models here.


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    side = models.CharField(max_length=1, default='D',
                            choices=[('D', 'D'), ('E', 'E')])
    pix = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')


class Doubles(models.Model):
    player1 = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name='player1_doubles')
    player2 = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name='player2_doubles')

    scored_points = models.PositiveIntegerField(null=True, blank=True)
    conc_points = models.PositiveIntegerField(null=True, blank=True)
    wins = models.PositiveIntegerField(null=True, blank=True)
    defeats = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1} and {self.player2}"


class Match(models.Model):
    date = models.DateTimeField()
    team_a = models.ForeignKey(
        Doubles, on_delete=models.CASCADE, related_name='team_a_matches')
    team_b = models.ForeignKey(
        Doubles, on_delete=models.CASCADE, related_name='team_b_matches')
    result_a = models.PositiveIntegerField(null=False, blank=False, default=0)
    result_b = models.PositiveIntegerField(null=False, blank=False, default=0)
    tournament = models.ForeignKey(
        'Tournament', on_delete=models.CASCADE, related_name='matches')

    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"

    def get_winner(self):
        if self.result_a > self.result_b:
            return self.team_a
        elif self.result_a < self.result_b:
            return self.team_b
        else:
            return None  # Indicar empate


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    max_players = models.IntegerField()
    players = models.ManyToManyField(Record)
    doubles = models.ManyToManyField(Doubles, blank=True)
    match_instances = models.ManyToManyField(
        Match, blank=True, related_name='tournament_matches')

    def __str__(self):
        return self.name
