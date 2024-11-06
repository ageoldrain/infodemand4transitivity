# models.py

from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'coin_flip'
    PLAYERS_PER_GROUP = None
    NUM_BLOCKS = 10
    NUM_SUBROUNDS_PER_BLOCK = 3
    NUM_ROUNDS = NUM_BLOCKS * NUM_SUBROUNDS_PER_BLOCK  # 10 blocks * 3 subrounds = 30 rounds

    COIN_PAIRS = [
        ('fair', 'biased'),
        ('biased', 'very biased'),
        ('fair', 'very biased'),
    ]

    COIN_PROBABILITIES = {
        'fair': 0.5,
        'biased': 0.75,
        'very biased': 0.95,
    }

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            # Calculate block and subround numbers
            block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
            subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK

            # At the start of each block (every 3 rounds), shuffle the coin pairs
            if subround_number == 0:
                coin_pairs = C.COIN_PAIRS.copy()
                random.shuffle(coin_pairs)
                player.participant.vars[f'coin_pairs_block_{block_number}'] = coin_pairs
            else:
                coin_pairs = player.participant.vars[f'coin_pairs_block_{block_number}']

            # Assign coins for the current subround
            coin_pair = coin_pairs[subround_number]
            player.coin1, player.coin2 = coin_pair

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Coins for the current subround
    coin1 = models.StringField()
    coin2 = models.StringField()

    # Player's coin choice
    coin_choice = models.StringField()

    # Guessed outcomes for each coin
    fair_outcome = models.StringField(
        choices=['Heads', 'Tails'],
        label="Your guess for the Fair coin",
        widget=widgets.RadioSelect
    )
    biased_outcome = models.StringField(
        choices=['Heads', 'Tails'],
        label="Your guess for the Biased coin",
        widget=widgets.RadioSelect
    )
    very_biased_outcome = models.StringField(
        choices=['Heads', 'Tails'],
        label="Your guess for the Very Biased coin",
        widget=widgets.RadioSelect
    )

    # Actual outcomes
    coin1_result = models.StringField()
    coin2_result = models.StringField()

    # Result of the chosen coin
    chosen_coin_result = models.StringField()

    # Total winnings (cumulative)
    total_winnings = models.CurrencyField(initial=cu(0))

    def flip_coins(self):
        # Flip both coins and store the results
        p_coin1 = C.COIN_PROBABILITIES[self.coin1]
        p_coin2 = C.COIN_PROBABILITIES[self.coin2]
        self.coin1_result = 'Heads' if random.random() < p_coin1 else 'Tails'
        self.coin2_result = 'Heads' if random.random() < p_coin2 else 'Tails'

        # Store the result of the chosen coin
        if self.coin_choice == self.coin1:
            self.chosen_coin_result = self.coin1_result
        elif self.coin_choice == self.coin2:
            self.chosen_coin_result = self.coin2_result

    def calculate_winnings(self):
        # Calculate winnings for this subround
        round_winnings = cu(0)

        # Check guesses and actual results for each coin
        if self.coin1 == 'fair':
            if self.fair_outcome == self.coin1_result:
                round_winnings += cu(1)
        elif self.coin2 == 'fair':
            if self.fair_outcome == self.coin2_result:
                round_winnings += cu(1)

        if self.coin1 == 'biased':
            if self.biased_outcome == self.coin1_result:
                round_winnings += cu(1)
        elif self.coin2 == 'biased':
            if self.biased_outcome == self.coin2_result:
                round_winnings += cu(1)

        if self.coin1 == 'very biased':
            if self.very_biased_outcome == self.coin1_result:
                round_winnings += cu(1)
        elif self.coin2 == 'very biased':
            if self.very_biased_outcome == self.coin2_result:
                round_winnings += cu(1)

        # Update total winnings
        if self.round_number == 1:
            self.total_winnings = round_winnings
        else:
            previous_total = self.in_round(self.round_number - 1).total_winnings
            self.total_winnings = previous_total + round_winnings

        # Store the winnings for this round
        self.payoff = round_winnings
