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
    template_name = 'coin_flip/CoinChoice.html'  # Specify the template name

    def vars_for_template(self):
        # Randomize coin positions
        coins = [
            (self.player.coin1, self.player.coin1.replace('_', ' ').title()),
            (self.player.coin2, self.player.coin2.replace('_', ' ').title())
        ]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins  # For use in templates

        # Get coin probabilities
        p_fair = C.COIN_PROBABILITIES.get('fair')
        p_biased = C.COIN_PROBABILITIES.get('biased')
        p_very_biased = C.COIN_PROBABILITIES.get('very biased')

        # Prepare probabilities for coins in this round
        coin_probs = {}
        for coin in [self.player.coin1, self.player.coin2]:
            coin_key = coin.replace(' ', '_')
            coin_probs[coin] = C.COIN_PROBABILITIES[coin]

        # Calculate block and subround numbers
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'coins': coins,
            'coin_probs': coin_probs,
            'round_number': self.round_number,
            'block_number': block_number,
            'subround_number': subround_number,
            'p_fair': p_fair,
            'p_biased': p_biased,
            'p_very_biased': p_very_biased,
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
            'round_number': self.round_number,
            'block_number': block_number,
            'subround_number': subround_number,
        }

class GuessOutcomes(Page):
    form_model = 'player'

    def get_form_fields(self):
        coins = [self.player.coin1, self.player.coin2]
        form_fields = []
        if 'fair' in coins:
            form_fields.append('fair_outcome')
        if 'biased' in coins:
            form_fields.append('biased_outcome')
        if 'very biased' in coins:
            form_fields.append('very_biased_outcome')
        return form_fields

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']

        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'coins': coins,
            'round_number': self.round_number,
            'block_number': block_number,
            'subround_number': subround_number,
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
    # The sequence repeats for each round
    Results
]
