# models.py

from otree.api import *
import random

doc = """
Curiosity and Information Demand with Three Coins: Fair, Biased, and Very Biased
"""

class C(BaseConstants):
    NAME_IN_URL = 'economics_experiment'
    PLAYERS_PER_GROUP = None
    NUM_BLOCKS = 10  # Number of main rounds
    NUM_SUBROUNDS_PER_BLOCK = 3  # Each block has 3 subrounds
    NUM_ROUNDS = NUM_BLOCKS * NUM_SUBROUNDS_PER_BLOCK  # Total rounds

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
            # Determine block number and subround number
            block_number = (self.round_number - 1) // C.NUM_SUBROUNDS_PER_BLOCK + 1
            subround_number = (self.round_number - 1) % C.NUM_SUBROUNDS_PER_BLOCK

            # For the first subround of each block, randomize coin pairs
            if subround_number == 0:
                # Randomize the order of coin pairs for this block
                coin_pairs = C.COIN_PAIRS.copy()
                random.shuffle(coin_pairs)
                player.participant.vars[f'coin_pairs_block_{block_number}'] = coin_pairs
            else:
                # Use the existing coin_pairs for this block
                coin_pairs = player.participant.vars[f'coin_pairs_block_{block_number}']

            # Assign the coin pair for this subround
            player.coin1, player.coin2 = coin_pairs[subround_number]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Coins for the current subround
    coin1 = models.StringField()
    coin2 = models.StringField()

    # Player's choice between the two coins
    coin_choice = models.StringField()

    # Guessed outcomes for each coin
    coin1_outcome_guess = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the first coin",
        widget=widgets.RadioSelect
    )
    coin2_outcome_guess = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the second coin",
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
        self.coin1_result = 'H' if random.random() < p_coin1 else 'T'
        self.coin2_result = 'H' if random.random() < p_coin2 else 'T'

        # Store the result of the chosen coin
        if self.coin_choice == self.coin1:
            self.chosen_coin_result = self.coin1_result
        elif self.coin_choice == self.coin2:
            self.chosen_coin_result = self.coin2_result

    def calculate_winnings(self):
        # Calculate winnings for this subround
        round_winnings = cu(0)
        if self.coin1_outcome_guess == self.coin1_result and self.coin2_outcome_guess == self.coin2_result:
            round_winnings = cu(2)

        # Update total winnings
        if self.round_number == 1:
            self.total_winnings = round_winnings
        else:
            previous_total = self.in_round(self.round_number - 1).total_winnings
            self.total_winnings = previous_total + round_winnings

        # Store the winnings for this round
        self.payoff = round_winnings
