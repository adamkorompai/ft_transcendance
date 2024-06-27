from django import forms

class TournamentForm(forms.Form):
    NUMBER_OF_PLAYERS_CHOICES = [
        (4, '4 Players'),
        (8, '8 Players'),
        (16, '16 Players'),
    ]
    number_of_players = forms.ChoiceField(choices=NUMBER_OF_PLAYERS_CHOICES, label='Number of Players')
    name = forms.CharField(max_length=100, label='Tournament Name')