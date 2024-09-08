from otree.api import *
from otree.models.participant import Participant as oTreeParticipant
import numpy as np

doc = """
Curiosity and Information Demand with Three Coins: Fair, Biased, and Very Biased
"""

debug = False

class C(BaseConstants):
    NAME_IN_URL = 'Economics Experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10

class Player(BasePlayer):
    
    # Choices for three stages
    first_coin_choice = models.StringField(choices=['fair', 'biased'])
    second_coin_choice = models.StringField(choices=['biased', 'very biased'])
    third_coin_choice = models.StringField(choices=['fair', 'very biased'])

    # Choice between HH, TT, HT, TH
    coin_permutation_choice = models.StringField(choices=['HH', 'TT', 'HT', 'TH'], initial='')
    
    # Results
    chosen_coin_result = models.StringField(initial='')
    chosen_coin_permutation = models.StringField(initial='')
    coin_permutation_result = models.StringField(initial='')

    total_winnings = models.CurrencyField(initial=cu(0))

    def flip_chosen_coin(self, p_fair: float, p_biased: float, p_very_biased: float, chosen_coin: str):
        """
        Flip the chosen coin and store the result.
        
        The function flips coins based on the player's choice:
        - 'fair': p_fair is the probability for heads
        - 'biased': p_biased is the probability for heads
        - 'very biased': p_very_biased is the probability for heads
        """
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
            
        if debug:
            print(f'Permutation choice: {self.coin_permutation_choice}')
            print(f'Permutation result: {self.coin_permutation_result}')
            print(self.coin_permutation_result == self.coin_permutation_choice)
