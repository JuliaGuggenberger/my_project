from otree.api import *
from _common.functions import *
from _common.pages import *


doc = """
    Test Phase II
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app3_testII'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    INITIAL_PRICE = 20.00
    PRICE_CHANGE_RATE = 0.05
    TRANSACTION_COSTS = 4
    AUTO_FEE = 50

    DAY_ABBREVIATIONS = {'Monday': 'Mo','Tuesday': 'Tu','Wednesday': 'We','Thursday': 'Th',
                         'Friday': 'Fr','Saturday': 'Sa','Sunday': 'Su'}

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        # Only group one eligible participant at a time
        for p in waiting_players:
            if p.participant.vars.get('advance_to_phase_III', False):
                return [p]
            
class Group(BaseGroup):
    token_price = models.FloatField(initial=C.INITIAL_PRICE)

class Player(BasePlayer):
    choice = models.StringField()
    budget = models.FloatField()
    token = models.IntegerField()
    token_purchased = models.IntegerField(initial=0,min=0)
    token_sold = models.IntegerField(initial=0,min=0)
    price_change = models.StringField(
        choices=[('1', 'The Token price does not change'), ('2', 'Amount of Token you trade'), ('3', 'Amount of Token everyone trades'),],
        label="What causes the Token price to change?",
        widget=widgets.RadioSelect,
        blank=False
    )
    token_buy = models.StringField(
        choices=[('1', 'Yes, if you have enough money'), ('2', 'No, you can buy/sell maximum 5 Token'), ('3', 'No, it depends on the use'),],
        label="Can you buy as many Token as you want?",
        widget=widgets.RadioSelect,
        blank=False
    )
    timeout_occurred = models.BooleanField(initial=False)

#*******************************************************************************************************************
# PAGES
class SyncWaitPage(WaitPage):
    body_text = "Waiting for other participants to proceed..."

    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get('advance_to_phase_III', False)
    
class ConditionalChoiceOrNoCommuteWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        # Only show this wait page to players who have the *same* trip type
        trips = player.participant.vars['all_trips']
        index = (player.round_number - 1) % len(trips)
        current_mode = trips[index].get('mode')
        return current_mode != 'no_commute'  # only Choice players wait

    @staticmethod
    def after_all_players_arrive(group):
        pass  # optional synchronization logic

# ======== Instruction ========
class Instruction(Page):
    form_model = 'player'
    form_fields = ['price_change', 'token_buy']

    @staticmethod
    def error_message(player, values):
        correct_answers = {'price_change': '3', 'token_buy': '3'}
    
        errors = {}
        for field, correct in correct_answers.items():
            if values.get(field) != correct:
                errors[field] = "Incorrect. Please review this part."
        
        return errors or None

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 

    @staticmethod
    def vars_for_template(player):
        # Initialize Week and Budget
        player.budget = player.participant.vars['initial_budget']
        player.token = player.participant.vars['initial_token']
        player.group.token_price = player.participant.vars.get('token_price_next_round', C.INITIAL_PRICE)

        # Return Template Variables
        return dict(
            budget=clean_zero(player.budget),
            token=int(player.token),
            token_price=clean_zero(player.group.token_price),
            page_name='intro',
            transaction_costs=C.TRANSACTION_COSTS
        )

# ======== WeekPreview ========
class WeekPreview(Page):
    timeout_seconds = timeout_sec('else')

    @staticmethod
    def is_displayed(player):
        return (
            player.round_number == 1 and
            player.participant.vars.get('advance_to_phase_III', False)
        )

    @staticmethod
    def vars_for_template(player):
        # Initialize Week and Budget
        current_week = (player.round_number - 1) // 5 + 1
        player.budget = player.participant.vars['initial_budget']
        player.token = player.participant.vars['initial_token']
        player.group.token_price = player.participant.vars.get('token_price_next_round', C.INITIAL_PRICE)

        # Load Trip Data for Preview 
        trips = player.participant.vars['all_trips']
        player.participant.vars['trip_choices'] = []
        preview_data, total_base, _ = preview_overview_data(trips, weekly_choices=False)

        # Return Template Variables
        return dict(
            budget=clean_zero(player.budget),
            token=int(player.token),
            token_price=clean_zero(player.group.token_price),
            preview_data=preview_data,
            current_week=current_week,
            total_base_token=total_base,
            page_name='weekpreview'
        )


# ======== Choice ========
class Choice(Page):
    timeout_seconds = timeout_sec('choice')

    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def is_displayed(player):
        trips = player.participant.vars['all_trips']
        index = (player.round_number - 1) % len(trips)
        trip = trips[index]
        return trip.get('mode') != 'no_commute'

    @staticmethod
    def vars_for_template(player):
        return choice_vars_for_template(player, C.NUM_ROUNDS, current_phase = 'testII', AUTO_FEE=C.AUTO_FEE)
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout_occurred = True
        return choice_before_next_page(player, C.NUM_ROUNDS, timeout_happened, current_phase = 'testII', AUTO_FEE=C.AUTO_FEE)


# ======== NoCommute ========
class NoCommute(Page):
    timeout_seconds = timeout_sec('choice')

    @staticmethod
    def is_displayed(player):
        trips = player.participant.vars['all_trips']
        index = (player.round_number - 1) % len(trips)
        trip = trips[index]
        return trip.get('mode') == 'no_commute'

    @staticmethod
    def vars_for_template(player):
        return choice_vars_for_template(player, C.NUM_ROUNDS, current_phase = 'testII')
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        return choice_before_next_page(player, C.NUM_ROUNDS, timeout_happened, current_phase = 'testII', choice='no_commute')


# ======== Market ========
class Market(Page):
    timeout_seconds = timeout_sec('market')

    form_model = 'player'
    form_fields = ['token_purchased', 'token_sold']

    @staticmethod
    def vars_for_template(player):
        return market_vars_for_template(player, C.DAY_ABBREVIATIONS, C.NUM_ROUNDS, C.TRANSACTION_COSTS, current_phase = 'testII')

    @staticmethod
    def before_next_page(player, timeout_happened):
        return market_before_next_page(player, C.NUM_ROUNDS, C.TRANSACTION_COSTS, C.PRICE_CHANGE_RATE)


# ======== Results ========
class Results(Page):
    timeout_seconds = timeout_sec()

    @staticmethod
    def is_displayed(player):
        return player.round_number % 5 == 0

    @staticmethod
    def vars_for_template(player):
        return results_vars_for_template(player, C.NUM_ROUNDS, C.TRANSACTION_COSTS, C.INITIAL_PRICE, current_phase='testII')


page_sequence = [Instruction, SyncWaitPage, WeekPreview, SyncWaitPage, Market, SyncWaitPage, NoCommute, Choice, SyncWaitPage, Results]