from otree.api import Page, WaitPage
from .models import C


P_FAIR = 0.5
P_BIASED = 0.75  # Probability of heads for biased coin
P_VERY_BIASED = 0.95  # Probability of heads for very biased coin

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class ChooseFirstCoin(Page):
    form_model = 'player'
    form_fields = ['first_coin_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass round_number to the template
        }


    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.first_coin_choice)

class RevealFirstCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result  # Result of the first coin flip
        }




class ChooseSecondCoin(Page):
    form_model = 'player'
    form_fields = ['second_coin_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass round_number to the template
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.second_coin_choice)

class RevealSecondCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result  # Result of the second coin flip
        }
}


class ChooseThirdCoin(Page):
    form_model = 'player'
    form_fields = ['third_coin_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass round_number to the template
        }

    def before_next_page(self):
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED, p_very_biased=P_VERY_BIASED, chosen_coin=self.player.third_coin_choice)

class RevealThirdCoinOutcome(Page):
    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'chosen_coin_result': self.player.chosen_coin_result  # Result of the third coin flip
        }



class ChoosePermutation(Page):
    form_model = 'player'
    form_fields = ['coin_permutation_choice']

    def vars_for_template(self):
        return {
            'round_number': self.round_number  # Pass round_number to the template
        }

    def is_displayed(self):
        return self.round_number <= C.NUM_ROUNDS


class Results(Page):
    def vars_for_template(self):
        return {'winnings': sum([player.total_winnings for player in self.player.in_all_rounds()])}

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

page_sequence = [
    Introduction,
    ChooseFirstCoin,
    RevealFirstCoinOutcome,  # Show the outcome after first coin choice
    ChooseSecondCoin,
    RevealSecondCoinOutcome,  # Show the outcome after second coin choice
    ChooseThirdCoin,
    RevealThirdCoinOutcome,  # Show the outcome after third coin choice
    ChoosePermutation,
    Results
]


