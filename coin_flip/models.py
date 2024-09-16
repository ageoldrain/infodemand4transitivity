from otree.api import *
import numpy as np

doc = """
Curiosity and Information Demand with Three Coins: Fair, Biased, and Very Biased
"""

class C(BaseConstants):
    NAME_IN_URL = 'economics_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10


class Player(BasePlayer):
    # Player's coin choices
    first_coin_choice = models.StringField(choices=['fair', 'biased'])
    second_coin_choice = models.StringField(choices=['biased', 'very biased'])
    third_coin_choice = models.StringField(choices=['fair', 'very biased'])

    # Player's guessed outcomes for each coin
    fair_outcome = models.StringField(choices=['H', 'T'], initial='', blank=True)
    biased_outcome = models.StringField(choices=['H', 'T'], initial='', blank=True)
    very_biased_outcome = models.StringField(choices=['H', 'T'], initial='', blank=True)

    # Combined outcome choice and other fields
    coin_permutation_choice = models.StringField(choices=['HH', 'TT', 'HT', 'TH'], initial='')
    chosen_coin_result = models.StringField(initial='')
    chosen_coin_permutation = models.StringField(initial='')
    coin_permutation_result = models.StringField(initial='')
    total_winnings = models.CurrencyField(initial=cu(0))

    # New fields to store coin positions (left or right)
    first_coin_position = models.StringField()  # Stores 'left' or 'right' for the first choice
    second_coin_position = models.StringField()  # Stores 'left' or 'right' for the second choice
    third_coin_position = models.StringField()  # Stores 'left' or 'right' for the third choice

    def flip_chosen_coin(self, p_fair: float, p_biased: float, p_very_biased: float, chosen_coin: str):
        assert 0 <= p_fair <= 1, "Probability for the fair coin must be between 0 and 1."
        assert 0 <= p_biased <= 1, "Probability for the biased coin must be between 0 and 1."
        assert 0 <= p_very_biased <= 1, "Probability for the very biased coin must be between 0 and 1."
        
        if chosen_coin == 'fair':
            self.chosen_coin_result = 'H' if np.random.rand() < p_fair else 'T'
        elif chosen_coin == 'biased':
            self.chosen_coin_result = 'H' if np.random.rand() < p_biased else 'T'
        elif chosen_coin == 'very biased':
            self.chosen_coin_result = 'H' if np.random.rand() < p_very_biased else 'T'
        
        # Add permutation logic and winnings as needed
        if self.coin_permutation_choice == self.coin_permutation_result:
            self.total_winnings += cu(1)

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass
