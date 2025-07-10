from otree.api import *
import os
import pandas as pd
from _common.functions import *
from _common.pages import *

#*************************************************************************************************
# CONFIGURATION

class C(BaseConstants):
    NAME_IN_URL = 'app_intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INITIAL_PRICE = 5.00
    PRICE_CHANGE_RATE = 0.01
    TRANSACTION_COSTS = 0.5

    DAY_ABBREVIATIONS = {'Monday': 'Mo','Tuesday': 'Tu','Wednesday': 'We','Thursday': 'Th',
                         'Friday': 'Fr','Saturday': 'Sa','Sunday': 'Su'}
    PHASE_ORDER = ['I', 'II', 'III', 'IV', 'V']

    APP_DIR = os.path.dirname(__file__)
    TRAVEL_DIARY_PATH = os.path.join(APP_DIR, 'choice_set.csv')   

#*************************************************************************************************
# MODELS

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass 

class Player(BasePlayer):
    entered_code = models.StringField(blank=True, label="Please enter your personal code.")
    travel_decision = models.StringField()
    not_enough_token = models.StringField()
    price_change = models.StringField()
    final_payoff = models.StringField()
    token_valid = models.StringField()
    cost_structure = models.StringField()
    equal_allocation = models.StringField()
    default_mode = models.StringField()

#*************************************************************************************************
# FUNCTIONS
def load_clean_csv():
    return pd.read_csv(C.TRAVEL_DIARY_PATH, na_values=['', 'NA', 'nan', 'NaN'], keep_default_na=True, encoding='latin1')

#**************************************************************************************************
# PAGES

# ======== CodeEntry ========
class CodeEntry(Page):
    form_model = 'player'
    form_fields = ['entered_code']
    
    @staticmethod
    def vars_for_template(player):
        df = load_clean_csv()
        valid_codes = df['id_code'].dropna().str.upper().unique().tolist()
        valid_codes_str = ",".join(valid_codes)
        return dict(valid_codes_str=valid_codes_str)
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        entered_code = player.entered_code.strip().upper()
        df = load_clean_csv()
        trips = df[df['id_code'].str.upper() == entered_code].sort_values('day_number')

        if trips.empty:
            player.participant.vars['code_invalid'] = True
            return

        player.participant.vars['code_invalid'] = False
        player.participant.vars['all_trips'] = trips.to_dict('records')
        player.participant.vars['trip_choices'] = []
        player.participant.vars['entered_code'] = entered_code
        player.participant.vars['initial_budget'] = float(trips['total_monetary_budget_per_id'].iloc[0])
        player.participant.vars['initial_token'] = int(trips['total_token_budget_per_id'].iloc[0])
        player.participant.vars['initial_budget_reduced'] = float(trips['total_monetary_budget_per_id'].iloc[0])
        player.participant.vars['initial_token_reduced'] = int(trips['total_token_budget_reduced_per_id'].iloc[0])
        player.participant.vars['token_price_history'] = [C.INITIAL_PRICE]
        player.participant.vars['advance_to_phase_III'] = True

    @staticmethod
    def error_message(player, value):
        entered_code = value.get('entered_code')
        if not entered_code:
            return "Please enter your personal code."

        df = load_clean_csv()
        trips = df[df['id_code'].str.upper() == entered_code]
        if trips.empty:
            return "Invalid code. Please check and re-enter your personal code."

        return None
    
# ======== Introduction ========
class Introduction(Page):
    form_model = 'player'
    form_fields = [
        'travel_decision',
        'not_enough_token',
        'price_change',
        'final_payoff',
        'token_valid',
        'cost_structure',
        'equal_allocation',
        'default_mode'
    ]

    @staticmethod
    def error_message(player, values):
        correct_answers = {
            'travel_decision': '2',
            'not_enough_token': '2',
            'price_change': '3',
            'final_payoff': '1',
            'token_valid': '2',
            'cost_structure': '1',
            'equal_allocation': '3',
            'default_mode': '1'
        }
    
        for field, correct in correct_answers.items():
            if values.get(field) != correct:
                return "Please answer all questions correctly before continuing."
        
        return None
    
    @staticmethod
    def vars_for_template(player):    
        # Load Trip Data for Preview
        trips = player.participant.vars['all_trips']
        trip_index = (player.round_number - 1) % len(trips)
        while trip_index < len(trips) and trips[trip_index]['mode'] == 'no_commute':
            trip_index += 1
        player.participant.vars['trip_choices'] = []
        trip = trips[trip_index]
        buffer = trip['early_buffer']
        preview_data, total_avg, total_base, total_token_used = preview_overview_data(trips, weekly_choices=False, day_abbreviations=C.DAY_ABBREVIATIONS)

        # === Mode Information for Current Trip ===
        poss_modes = trip.get('possible_modes')
        poss_modes = ast.literal_eval(poss_modes)
        modes = choice_set(poss_modes, trip, 'II')

        # Return Template Variables
        return dict(
            budget=clean_zero(player.participant.vars['initial_budget']),
            token=int(player.participant.vars['initial_token']),
            budget_reduced = player.participant.vars['initial_budget'],
            token_reduced = player.participant.vars['initial_token_reduced'],
            token_price=clean_zero(player.participant.vars['token_price_history'][-1]),
            current_phase='XTRA',
            default_mode=trip['mode'],
            preview_data=preview_data,
            total_base_token=total_base,
            total_avg_token=clean_zero(total_avg),
            total_token_used=total_token_used,
            page_name='weekpreview',
            buffer=buffer,
            modes=modes,
            modes_js=json.dumps({m['mode']: m for m in modes}),
        )

page_sequence = [CodeEntry, Introduction]