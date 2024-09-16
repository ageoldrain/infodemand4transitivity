from otree.api import Page, WaitPage
from .models import C
import random

P_FAIR = 0.5
P_BIASED = 0.75  # Probability of heads for biased coin
P_VERY_BIASED = 0.95  # Probability of heads for very biased coin

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction1point5(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 1

class ChooseFairOrBiased(Page):
    form_model = 'player'
    form_fields = ['first_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        # Store coin order in session vars to align with the next page
        self.session.vars['fair_or_biased_order'] = coins
        return {
            'round_number': self.round_number,
            'coins': coins,
            'p_fair': P_FAIR,
            'p_biased': P_BIASED
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
    form_fields = ['fair_outcome', 'biased_outcome']

    def vars_for_template(self):
        # Retrieve the coin order from the previous choice page
        coins = self.session.vars['fair_or_biased_order']
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.coin_permutation_choice = f"{self.player.fair_outcome}{self.player.biased_outcome}"

class ChooseBiasedOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['second_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('biased', 'Biased'), ('very biased', 'Very Biased')]
        random.shuffle(coins)
        # Store coin order in session vars to align with the next page
        self.session.vars['biased_or_very_biased_order'] = coins
        return {
            'round_number': self.round_number,
            'coins': coins,
            'p_biased': P_BIASED,
            'p_very_biased': P_VERY_BIASED
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
    form_fields = ['biased_outcome', 'very_biased_outcome']

    def vars_for_template(self):
        # Retrieve the coin order from the previous choice page
        coins = self.session.vars['biased_or_very_biased_order']
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.coin_permutation_choice = f"{self.player.biased_outcome}{self.player.very_biased_outcome}"

class ChooseFairOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['third_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('very biased', 'Very Biased')]
        random.shuffle(coins)
        # Store coin order in session vars to align with the next page
        self.session.vars['fair_or_very_biased_order'] = coins
        return {
            'round_number': self.round_number,
            'coins': coins,
            'p_fair': P_FAIR,
            'p_very_biased': P_VERY_BIASED
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
    form_fields = ['fair_outcome', 'very_biased_outcome']

    def vars_for_template(self):
        # Retrieve the coin order from the previous choice page
        coins = self.session.vars['fair_or_very_biased_order']
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.coin_permutation_choice = f"{self.player.fair_outcome}{self.player.very_biased_outcome}"

class Results(Page):
    def vars_for_template(self):
        return {'winnings': sum([player.total_winnings for player in self.player.in_all_rounds()])}

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

# Update the sequence
page_sequence = [
    Introduction,
    Introduction1point5,
    Introduction2,
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
