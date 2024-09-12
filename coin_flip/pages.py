from otree.api import Page, WaitPage
from .models import C
import random

P_FAIR = 0.5
P_BIASED = 0.75  # Probability of heads for biased coin
P_VERY_BIASED = 0.95  # Probability of heads for very biased coin

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class ChooseFairOrBiased(Page):
    form_model = 'player'
    form_fields = ['first_coin_choice']  # This field is already defined

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)  # Randomly shuffle the list
        return {
            'round_number': self.round_number,
            'coins': coins  # Pass the randomized coins to the template
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.first_coin_choice)

class RevealFairOrBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

class GuessFairBiasedOutcome(Page):
    form_model = 'player'
    form_fields = ['coin_permutation_choice']  # You already have this field

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

class ChooseBiasedOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['second_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('biased', 'Biased'), ('very biased', 'Very Biased')]
        random.shuffle(coins)  # Randomly shuffle the list
        return {
            'round_number': self.round_number,
            'coins': coins  # Pass the randomized coins to the template
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.second_coin_choice)

class RevealBiasedOrVeryBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

class GuessBiasedVeryBiasedOutcome(Page):
    form_model = 'player'
    form_fields = ['coin_permutation_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

class ChooseFairOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['third_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('very biased', 'Very Biased')]
        random.shuffle(coins)  # Randomly shuffle the list
        return {
            'round_number': self.round_number,
            'coins': coins  # Pass the randomized coins to the template
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.third_coin_choice)

class RevealFairOrVeryBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

class GuessFairVeryBiasedOutcome(Page):
    form_model = 'player'
    form_fields = ['coin_permutation_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

class Results(Page):
    def vars_for_template(self):
        return {'winnings': sum([player.total_winnings for player in self.player.in_all_rounds()])}

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


# Update the sequence
page_sequence = [
    Introduction,
    ChooseFairOrBiased,
    RevealFairOrBiasedOutcome,
    GuessFairBiasedOutcome,
    ChooseBiasedOrVeryBiased,
    RevealBiasedOrVeryBiasedOutcome,
    GuessBiasedVeryBiasedOutcome,
    ChooseFairOrVeryBiased,
    RevealFairOrVeryBiasedOutcome,
    GuessFairVeryBiasedOutcome,
    Results
]
