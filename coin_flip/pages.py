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

# pages.py

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
        coin_probs = {}
        for coin in [self.player.coin1, self.player.coin2]:
            coin_probs[coin] = C.COIN_PROBABILITIES[coin]

        # Prepare probabilities for coins in this round
        # Since we can't access coin_probs[coins.0.0] in the template, we pass the probabilities directly
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

# pages.py

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
            coin_name = coin[0]  # 'fair', 'biased', etc.
            coin_display_name = coin[1]  # 'Fair', 'Biased', etc.
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
