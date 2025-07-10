from otree.api import *
from _common.functions import *
from _common.pages import *

doc = """
    Phase II
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_phaseII'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    INITIAL_PRICE = 5.00
    PRICE_CHANGE_RATE = 0.01
    TRANSACTION_COSTS = 0.5

    DAY_ABBREVIATIONS = {'Monday': 'Mo','Tuesday': 'Tu','Wednesday': 'We','Thursday': 'Th',
                         'Friday': 'Fr','Saturday': 'Sa','Sunday': 'Su'}
    PHASE_ORDER = ['I', 'II', 'III', 'IV', 'V']

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
        player.group.token_price = C.INITIAL_PRICE

        # Load Trip Data for Preview
        trips = player.participant.vars['all_trips']
        player.participant.vars['trip_choices'] = []
        preview_data, total_avg, total_base, _ = preview_overview_data(trips, weekly_choices=False, day_abbreviations=C.DAY_ABBREVIATIONS)

        # Return Template Variables
        return dict(
            budget=clean_zero(player.budget),
            token=int(player.token),
            token_price=round(player.group.token_price, 2),
            preview_data=preview_data,
            current_week=current_week,
            total_base_token=total_base,
            total_avg_token=clean_zero(total_avg),
            current_phase='II',
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
        return choice_vars_for_template(player, C.DAY_ABBREVIATIONS, C.NUM_ROUNDS, current_phase = 'II')

    
    @staticmethod
    def before_next_page(player, timeout_happened):
        return choice_before_next_page(player, C.NUM_ROUNDS, timeout_happened, current_phase = 'II')

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
        return choice_vars_for_template(player, C.DAY_ABBREVIATIONS, C.NUM_ROUNDS, current_phase = 'II')
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        return choice_before_next_page(player, C.NUM_ROUNDS, timeout_happened, current_phase = 'II', choice='no_commute')

# ======== Results ========
class Results(Page):
    timeout_seconds = timeout_sec()

    @staticmethod
    def is_displayed(player):
        return player.round_number % 5 == 0

    @staticmethod
    def vars_for_template(player):
        return results_vars_for_template(player, C.NUM_ROUNDS, C.TRANSACTION_COSTS, C.PHASE_ORDER, C.DAY_ABBREVIATIONS, C.INITIAL_PRICE, current_phase='II')


page_sequence = [SyncWaitPage, WeekPreview, SyncWaitPage, NoCommute, Choice, SyncWaitPage, Results]