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

class RoundInfo(Page):
    template_name = 'coin_flip/RoundInfo.html'

    def is_displayed(self):
        # Display only before each round, excluding practice rounds
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        return (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK == 0

    def vars_for_template(self):
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        return {
            'block_number': block_number
        }

class CoinChoice(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/CoinChoice.html'

    def vars_for_template(self):
        # Determine if it is a practice round
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        is_practice = block_number <= C.NUM_PRACTICE_BLOCKS

        coins = [
            (self.player.coin1, self.player.coin1.replace('_', ' ').title()),
            (self.player.coin2, self.player.coin2.replace('_', ' ').title())
        ]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins
        self.player.coin_position = f'{coins[0][0]}_{coins[1][0]}'

        coin_probs = {
            coins[0][0]: C.COIN_PROBABILITIES[coins[0][0]],
            coins[1][0]: C.COIN_PROBABILITIES[coins[1][0]],
        }

        prob_coin0 = coin_probs[coins[0][0]]
        prob_coin1 = coin_probs[coins[1][0]]

        return {
            'coins': coins,
            'prob_coin0': prob_coin0,
            'prob_coin1': prob_coin1,
            'block_number': block_number,
            'subround_number': (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1,
            'is_practice': is_practice
        }

    def before_next_page(self):
        self.player.flip_coins()

class GuessOutcomes(Page):
    form_model = 'player'

    def get_form_fields(self):
        coins_in_subround = [self.player.coin1, self.player.coin2]
        form_fields = []
        if 'fair' in coins_in_subround:
            form_fields.append('fair_outcome')
        if 'biased' in coins_in_subround:
            form_fields.append('biased_outcome')
        if 'very biased' in coins_in_subround:
            form_fields.append('very_biased_outcome')
        return form_fields

    def vars_for_template(self):
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        is_practice = block_number <= C.NUM_P
