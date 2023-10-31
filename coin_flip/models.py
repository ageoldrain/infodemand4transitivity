from otree.api import *
from otree.models.participant import Participant as oTreeParticipant
import numpy as np

doc = """
Curiosity and Information Demand
"""

debug = False

class C(BaseConstants):
    NAME_IN_URL = 'Curiosity'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
   # NUM_PRACTICE_ROUNDS=2
    # WINNINGS = cu(0)

# class Participant(oTreeParticipant):
#     total_winnings = models.CurrencyField(initial=cu(0))

class Player(BasePlayer):
    
    # Choice between 'fair' or 'biased' coin
    coin_choice = models.StringField(choices=['fair', 'biased'])
    # Choice between HH, TT, HT, TH  where format is [Fair][Bias]
    coin_permutation_choice = models.StringField(choices=['HH', 'TT', 'HT', 'TH'], initial='')
    
    # Results
    chosen_coin_result = models.StringField(initial='')
    chosen_coin_permutation = models.StringField(initial='')
    coin_permutation_result = models.StringField(initial='')

    total_winnings = models.CurrencyField(initial=cu(0))

    def flip_chosen_coin(self, p_fair: float, p_biased: float):
        """
        Flip the chosen coin and store the result.
        
        For simplicity, we assume:
        - 'fair' coin has equal probability of Heads or Tails (e.g., 0.5).
        - 'biased' coin's probability is given by p_biased.
        """
        assert 0 <= p_fair <= 1, "Probability for the fair coin must be between 0 and 1."
        assert 0 <= p_biased <= 1, "Probability for the biased coin must be between 0 and 1."

        # Check second question was not answered yet and is empty
        if self.coin_permutation_choice == '':
            if self.coin_choice == 'fair':
                self.chosen_coin_result = 'H' if np.random.rand() < p_fair else 'T'
            else:
                self.chosen_coin_result = 'H' if np.random.rand() < p_biased else 'T'
        else:
            if self.coin_choice == 'fair':
                # Flip the biased coin since fair was already flipped
                second_coin_result = 'H' if np.random.rand() < p_biased else 'T'
                # Concatenate the string outcomes
                self.coin_permutation_result = self.chosen_coin_result + second_coin_result
            else:
                # Flip the fair coin since biased was already flipped
                second_coin_result = 'H' if np.random.rand() < p_fair else 'T'
                # Concatenate the string outcomes
                self.coin_permutation_result =  second_coin_result + self.chosen_coin_result

            # Concatenate the string outcomes
            self.coin_permutation_result = self.chosen_coin_result + second_coin_result

            # Add winnings if the chosen permutation matched the simulated flippings
            if self.coin_permutation_result == self.coin_permutation_choice:
                # Give a dollar
                self.total_winnings += cu(1)

            if debug:
                print(f'permutation choice: {self.coin_permutation_choice}')
                print(f'permutation result: {self.coin_permutation_result}')
                print(self.coin_permutation_result==self.coin_permutation_choice)
                print(sum([player.total_winnings for player in self.in_all_rounds()]))


class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass
