from otree.api import *

doc = """
    Post Survey
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_postsurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Fianancial Literacy Questions
    literacy_1 = models.StringField(
        choices=[('1', 'More than 1020 DKK'), ('2', 'Exactly 1020 DKK'), ('3', 'Less than 1020 DKK'), ('4', 'Do not know'), ('5', 'Refuse to answer'),],
        label="Suppose you had 1000 DKK in a savings account and the interest rate was 2% per year. After 5 years, how much do you think you would have in the account if you left the money to grow?",
        widget=widgets.RadioSelect,
        blank=False
    )
    literacy_2 = models.StringField(
        choices=[('1', 'More than today'), ('2', 'Exactly the same'), ('3', 'Less than today'), ('4', 'Do not know'), ('5', 'Refuse to answer'),],
        label="Imagine that the interest rate on your savings account was 1 % per year and inflation was 2 % per year. After 1 year, how much would you be able to buy with the money in this account?",
        widget=widgets.RadioSelect,
        blank=False
    )
    literacy_3 = models.StringField(
        choices=[('1', 'True'), ('2', 'False'), ('3', 'Do not know'), ('4', 'Refuse to answer'),],
        label="Please tell me whether this statement is true or false. 'Buying a single company's stock usually provides a safer return than a stock mutual fund'.",
        widget=widgets.RadioSelect,
        blank=False
    )

    # Post-survey Questions 1
    # Understanding and Clarity
    understanding_level = models.StringField(
        choices=[('1', 'Very well'), ('2', 'Fairly well'), ('3', 'Not very well'), ('4', 'Not at all'),],
        label="How well did you understand how the scheme worked?",
        widget=widgets.RadioSelect,
        blank=False
    )
    clarity_of_rules = models.StringField(
        choices=[('1', 'Yes'), ('2', 'Somewhat'), ('3', 'No'),],
        label="Were the rules and objectives of the scheme clear to you during the experiment?",
        widget=widgets.RadioSelect,
        blank=False
    )
    interface_ease = models.StringField(
        choices=[('1', 'Yes'), ('2', 'Somewhat'), ('3', 'No'),],
        label="Was the game interface easy to use?",
        widget=widgets.RadioSelect,
        blank=False
    )

    # Familiarity
    familiar_currency = models.StringField(
        choices=[('1', 'Euros'), ('2', 'U.S. Dollars'), ('3', 'DKK'), ('4', 'Other'),],
        label="Which currency or credit system are you most familiar with?",
        widget=widgets.RadioSelect,
        blank=False
    )
    familiar_currency_other = models.StringField(
        label="Please specify:",
        blank=True
    )

    # Strategy & Behavior
    strategy_description = models.StringField(
        choices=[('1', 'Maximize my budget'), ('2', 'Be environmentally friendly'), ('3', 'Try to replicate my behavior from the real-world'),],
        label="What was your overall strategy or approach during the experiment?",
        widget=widgets.RadioSelect,
        blank=False
    )
    minimization_focus = models.StringField(
        choices=[('1', 'Token use'), ('2', 'Cost'), ('3', 'A mix of both'), ('4', 'Not sure'),],
        label="Did you try to minimize your Token use or the costs?",
        widget=widgets.RadioSelect,
        blank=False
    )

    fair_price_token = models.FloatField(
        label="What do you consider a fair price for 1 Token (1 kg of CO₂ equivalent)?",
        blank=False
    )

    # Post-survey Questions 2
    # Opinion scale (Likert)
    fun_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Trading Tokens seems fun.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    difficulty_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Trading Tokens seems difficult.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    intuitive_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Using Tokens feels intuitive to me.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    system_vs_tax = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="I think this system would work better than a tax.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    prefer_over_tax = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="I prefer this scheme over a standard carbon tax.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    permit_fairness = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Allocating permits is a fair approach.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )

    # Post-survey Questions 3
    # Implementation Opinion
    support_local_scheme = models.StringField(
        choices=[('1', 'Yes'), ('2', 'Maybe'), ('3', 'No'),],
        label="Would you support implementing such a scheme in your city?",
        widget=widgets.RadioSelect,
        blank=False
    )
    effectiveness_opinion = models.StringField(
        choices=[('1', 'Yes'), ('2', 'No'), ('3', 'Not sure'),],
        label="Do you think such a scheme could effectively reduce CO2eq emissions?",
        widget=widgets.RadioSelect,
        blank=False
    )
    who_benefits = models.StringField(
        choices=[('1', 'Low-income households'), ('2', 'Middle-income households'), ('3', 'High-income households'), ('4', 'Government'), ('5', 'Corporations'), ('6', 'Other'),],
        label="Who do you think would benefit most from this scheme?",
        widget=widgets.RadioSelect,
        blank=False
    )
    who_benefits_other = models.StringField(
        label="Please specify:",
        blank=True
    )
    user_response_if_implemented = models.StringField(
        choices=[('1', 'Reduce my CO2 emissions'), ('2', 'Switch to electric or low-emission transportation'),
                    ('3', 'Offset emissions by purchasing extra Token'), ('4', 'Change how I plan travel or shopping'), ('5', 'Participate actively in the trading market'),
                    ('6', 'Do nothing / Continue as before'), ('7', 'Other'),],
        label="What would you do if such a scheme were implemented in your city?",
        widget=widgets.RadioSelect,
        blank=False
    )
    user_response_if_implemented_other = models.StringField(
        label="Please specify:",
        blank=True
    )
    confusing_part = models.StringField(
        choices=[('1', 'Trading'), ('2', 'Travel choice'), ('3', 'Other'),],
        label="Which part of the experiment did you find most confusing or frustrating?",
        widget=widgets.RadioSelect,
        blank=False
    )
    confusing_part_other = models.StringField(
        label="Please specify:",
        blank=True
    )

#*******************************************************************************************************************
# PAGES

# ======== Literacy ========
class Literacy(Page):
    form_model = 'player'
    form_fields = ['literacy_1', 'literacy_2', 'literacy_3',]

# ======== Survey1 ========
class Survey1(Page):
    form_model = 'player'
    form_fields = ['understanding_level', 'clarity_of_rules', 'interface_ease', 'familiar_currency', 'familiar_currency_other', 'strategy_description', 'minimization_focus',
                    'fair_price_token',]
    
# ======== Survey2 ========
class Survey2(Page):
    form_model = 'player'
    form_fields = ['fun_rating', 'difficulty_rating', 'intuitive_rating', 'system_vs_tax', 'prefer_over_tax', 'permit_fairness',]
    
# ======== Survey3 ========
class Survey3(Page):
    form_model = 'player'
    form_fields = ['support_local_scheme', 'effectiveness_opinion', 'who_benefits', 'user_response_if_implemented', 'confusing_part',
                    'who_benefits_other', 'familiar_currency_other', 'user_response_if_implemented_other', 'confusing_part_other',]

page_sequence = [Literacy, Survey1, Survey2, Survey3]