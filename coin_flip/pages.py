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
        # Display only for real blocks (excluding practice blocks)
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        return block_number > C.NUM_PRACTICE_BLOCKS and (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK == 0

    def vars_for_template(self):
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        real_block_number = block_number - C.NUM_PRACTICE_BLOCKS if block_number > C.NUM_PRACTICE_BLOCKS else None
        return {
            'block_number': real_block_number
        }

class CoinChoice(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/CoinChoice.html'

    def vars_for_template(self):
        # Determine if it is a practice round
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        is_practice = block_number <= C.NUM_PRACTICE_BLOCKS

        # Use real block number only for experimental rounds
        real_block_number = block_number - C.NUM_PRACTICE_BLOCKS if not is_practice else None

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
            'block_number': real_block_number if real_block_number is not None else block_number,
            'subround_number': (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1,
            'is_practice': is_practice
        }

    def before_next_page(self):
        # Flip the coins before proceeding to RevealCoinOutcome
        self.player.flip_coins()

class RevealCoinOutcome(Page):
    template_name = 'coin_flip/RevealCoinOutcome.html'

    def vars_for_template(self):
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        is_practice = block_number <= C.NUM_PRACTICE_BLOCKS
        real_block_number = block_number - C.NUM_PRACTICE_BLOCKS if not is_practice else None

        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        # Use field_maybe_none() to safely access fields that may be None
        chosen_coin = self.player.field_maybe_none('coin_choice')
        chosen_coin_result = self.player.field_maybe_none('chosen_coin_result')
        coin1_result = self.player.field_maybe_none('coin1_result')
        coin2_result = self.player.field_maybe_none('coin2_result')

        return {
            'chosen_coin': chosen_coin.replace('_', ' ').title() if chosen_coin else None,
            'chosen_coin_result': chosen_coin_result,
            'coin1_result': coin1_result,
            'coin2_result': coin2_result,
            'block_number': real_block_number if real_block_number is not None else block_number,
            'subround_number': subround_number,
        }

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
        is_practice = block_number <= C.NUM_PRACTICE_BLOCKS
        real_block_number = block_number - C.NUM_PRACTICE_BLOCKS if not is_practice else None

        coins = self.participant.vars.get('coin_order', [])
        return {
            'coins': coins,
            'block_number': real_block_number if real_block_number is not None else block_number,
            'subround_number': (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1,
            'is_practice': is_practice
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
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    RoundInfo,
    CoinChoice,
    RevealCoinOutcome,
    GuessOutcomes,
    Results
]
