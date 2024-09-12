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
    form_fields = ['first_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.first_coin_choice)

class RevealFairOrBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

# This method will combine individual outcomes into a single "coin_permutation_choice"
class GuessFairBiasedOutcome(Page):
    form_model = 'player'
    form_fields = []  # Handle the fields manually

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass the round number to the template
        }

    def before_next_page(self):
        # Combine fair and biased coin outcomes into coin_permutation_choice
        fair_outcome = self._get_outcome('fair_outcome')
        biased_outcome = self._get_outcome('biased_outcome')
        self.player.coin_permutation_choice = f"{fair_outcome}{biased_outcome}"

    def _get_outcome(self, field):
        return self.request.POST.get(field)


class ChooseBiasedOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['second_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('biased', 'Biased'), ('very biased', 'Very Biased')]
        random.shuffle(coins)
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.second_coin_choice)

class RevealBiasedOrVeryBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

# This method will combine individual outcomes into a single "coin_permutation_choice"
class GuessBiasedVeryBiasedOutcome(Page):
    form_model = 'player'
    form_fields = []  # Handle the fields manually

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass the round number to the template
        }

    def before_next_page(self):
        # Combine biased and very biased coin outcomes into coin_permutation_choice
        biased_outcome = self._get_outcome('biased_outcome')
        very_biased_outcome = self._get_outcome('very_biased_outcome')
        self.player.coin_permutation_choice = f"{biased_outcome}{very_biased_outcome}"

    def _get_outcome(self, field):
        return self.request.POST.get(field)

class ChooseFairOrVeryBiased(Page):
    form_model = 'player'
    form_fields = ['third_coin_choice']

    def vars_for_template(self):
        # Randomize coin positions
        coins = [('fair', 'Fair'), ('very biased', 'Very Biased')]
        random.shuffle(coins)
        return {
            'round_number': self.round_number,
            'coins': coins
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.third_coin_choice)

class RevealFairOrVeryBiasedOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result
        }

# This method will combine individual outcomes into a single "coin_permutation_choice"
class GuessFairVeryBiasedOutcome(Page):
    form_model = 'player'
    form_fields = []  # Handle the fields manually

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass the round number to the template
        }

    def before_next_page(self):
        # Combine fair and very biased coin outcomes into coin_permutation_choice
        fair_outcome = self._get_outcome('fair_outcome')
        very_biased_outcome = self._get_outcome('very_biased_outcome')
        self.player.coin_permutation_choice = f"{fair_outcome}{very_biased_outcome}"

    def _get_outcome(self, field):
        return self.request.POST.get(field)


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
