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
    template_name = 'coin_flip/CoinChoice.html'

    def vars_for_template(self):
        # Retrieve coin_order from participant.vars if it exists
        coins = [
            (self.player.coin1, self.player.coin1.replace('_', ' ').title()),
            (self.player.coin2, self.player.coin2.replace('_', ' ').title())
        ]
        # Randomize coins and store the order
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins

        # Get coin probabilities
        coin_probs = {
            coins[0][0]: C.COIN_PROBABILITIES[coins[0][0]],
            coins[1][0]: C.COIN_PROBABILITIES[coins[1][0]],
        }

        # Probabilities for the coins
        prob_coin0 = coin_probs[coins[0][0]]
        prob_coin1 = coin_probs[coins[1][0]]

        # Calculate block and subround numbers
        block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
        subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK + 1

        return {
            'coins': coins,
            'prob_coin0': prob_coin0,
            'prob_coin1': prob_coin1,
            'round_number': self.round_number,
            'block_number': block_number,
            'subround_number': subround_number,
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

        # Prepare a list of coins with their corresponding form field names
        coin_forms = []
        for coin in coins:
            coin_name = coin[0]
            coin_display_name = coin[1]

            # Get the corresponding form field name
            if coin_name == 'fair':
                field_name = 'fair_outcome'
            elif coin_name == 'biased':
                field_name = 'biased_outcome'
            elif coin_name == 'very biased':
                field_name = 'very_biased_outcome'
            else:
                field_name = None  # Should not happen

            coin_forms.append({
                'coin_name': coin_name,
                'coin_display_name': coin_display_name,
                'field_name': field_name,
            })

        return {
            'coins': coins,
            'coin_forms': coin_forms,
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
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,
    CoinChoice,
    RevealCoinOutcome,
    GuessOutcomes,
    Results
]
