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

    def get_template_names(self):
        coin_pair = sorted([self.player.coin1, self.player.coin2])
        if coin_pair == ['biased', 'fair']:
            return ['coin_flip/ChooseFairOrBiased.html']
        elif coin_pair == ['biased', 'very biased']:
            return ['coin_flip/ChooseBiasedOrVeryBiased.html']
        elif coin_pair == ['fair', 'very biased']:
            return ['coin_flip/ChooseFairOrVeryBiased.html']
        else:
            return ['coin_flip/CoinChoice.html']

    def vars_for_template(self):
        coins = [(self.player.coin1, self.player.coin1.replace('_', ' ').title()),
                 (self.player.coin2, self.player.coin2.replace('_', ' ').title())]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins

        p_fair = C.COIN_PROBABILITIES.get('fair')
        p_biased = C.COIN_PROBABILITIES.get('biased')
        p_very_biased = C.COIN_PROBABILITIES.get('very biased')

        return {
            'coins': coins,
            'round_number': self.round_number,
            'p_fair': p_fair,
            'p_biased': p_biased,
            'p_very_biased': p_very_biased,
        }

    def before_next_page(self):
        self.player.flip_coins()

class RevealCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'chosen_coin': self.player.coin_choice.replace('_', ' ').title(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'round_number': self.round_number
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
        return {
            'coins': coins,
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
