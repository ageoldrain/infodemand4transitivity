# pages.py

from otree.api import Page
from .models import C
import random

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point5(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point6(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 1

class CoinChoice(Page):
    form_model = 'player'
    form_fields = ['coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [(self.player.coin1, self.player.coin1.replace('_', ' ').title()),
                 (self.player.coin2, self.player.coin2.replace('_', ' ').title())]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins  # For use in templates

        # Calculate block and subround numbers
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'coins': coins,
            'block_number': block_number,
            'subround_number': subround_number,
            'round_number': self.round_number
        }

    def before_next_page(self):
        self.player.flip_coins()

class RevealCoinOutcome(Page):
    def vars_for_template(self):
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'chosen_coin': self.player.coin_choice.replace('_', ' ').title(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'block_number': block_number,
            'subround_number': subround_number,
            'round_number': self.round_number
        }

class GuessOutcomes(Page):
    form_model = 'player'
    form_fields = ['coin1_outcome_guess', 'coin2_outcome_guess']

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        coin_labels = [coin[1] for coin in coins]

        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'coins': coins,
            'coin_labels': coin_labels,
            'block_number': block_number,
            'subround_number': subround_number,
            'round_number': self.round_number
        }

    def before_next_page(self):
        self.player.calculate_winnings()

class Results(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        total_winnings = self.player.total_winnings
        return {
            'total_winnings': total_winnings
        }

# Define the page sequence
page_sequence = [
    # Introduction pages
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    # Experiment pages
    CoinChoice,
    RevealCoinOutcome,
    GuessOutcomes,
    # The sequence above repeats for each round
    Results
]
