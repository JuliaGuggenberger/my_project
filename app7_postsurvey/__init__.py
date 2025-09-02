from otree.api import *
import pandas as pd

doc = """
    Post Survey
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_postsurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_PAYOFF = 200
    CAP_PAYOFF = 400
    MAX_WINNER_PAYOFF = 700

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Fianancial Literacy Questions
    literacy_1 = models.StringField(
        choices=[('1', 'More than 1020 DKK'), ('2', 'Exactly 1020 DKK'), ('3', 'Less than 1020 DKK'), ('4', 'Do not know'), ('5', 'Prefer not to answer'),],
        label="Suppose you had 1000 DKK in a savings account and the interest rate was 2% per year. After 5 years, how much do you think you would have in the account if you left the money to grow?",
        widget=widgets.RadioSelect,
        blank=False
    )
    literacy_2 = models.StringField(
        choices=[('1', 'More than today'), ('2', 'Exactly the same'), ('3', 'Less than today'), ('4', 'Do not know'), ('5', 'Prefer not to answer'),],
        label="Imagine that the interest rate on your savings account was 1 % per year and inflation was 2 % per year. After 1 year, how much would you be able to buy with the money in this account?",
        widget=widgets.RadioSelect,
        blank=False
    )
    literacy_3 = models.StringField(
        choices=[('1', 'True'), ('2', 'False'), ('3', 'Do not know'), ('4', 'Prefer not to answer'),],
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
    # Strategy & Behavior - now per phase
    strategy_description_phase1 = models.StringField(
        choices=[('1', 'Maximize my budget'), ('2', 'Be environmentally friendly'),
                ('3', 'Try to replicate my behavior from the real-world'), ('4', 'I decided according to the travel time'), ('5', 'I decided randomly'), ('6', 'Other')],
        label="Phase I strategy",
        widget=widgets.RadioSelect,
        blank=False
    )
    strategy_description_phase1_other = models.StringField(
        label="Please specify:",
        blank=True
    )

    strategy_description_phase2 = models.StringField(
        choices=[('1', 'Maximize my budget'), ('2', 'Be environmentally friendly'),
                ('3', 'Try to replicate my behavior from the real-world'), ('4', 'I decided according to the travel time'), ('5', 'I decided randomly'), ('6', 'Other')],
        label="Phase II strategy",
        widget=widgets.RadioSelect,
        blank=False
    )
    strategy_description_phase2_other = models.StringField(
        label="Please specify:",
        blank=True
    )

    strategy_description_phase3 = models.StringField(
        choices=[('1', 'Maximize my budget'), ('2', 'Be environmentally friendly'),
                ('3', 'Try to replicate my behavior from the real-world'), ('4', 'I decided according to the travel time'), ('5', 'I decided randomly'), ('6', 'Other')],
        label="Phase III strategy",
        widget=widgets.RadioSelect,
        blank=False
    )
    strategy_description_phase3_other = models.StringField(
        label="Please specify:",
        blank=True
    )

    minimization_focus_1 = models.StringField(
        choices=[('1', 'I tried to minimize token use'), ('2', 'I tried to minimize costs'), ('3', 'I tried to minimze travel time'), ('4', 'I tried to minimize car use'),],
        label="always",
        widget=widgets.RadioSelect,
        blank=False
    )

    minimization_focus_2 = models.StringField(
        choices=[('1', 'I tried to minimize token use'), ('2', 'I tried to minimize costs'), ('3', 'I tried to minimze travel time'), ('4', 'I tried to minimize car use'),],
        label="often",
        widget=widgets.RadioSelect,
        blank=False
    )

    minimization_focus_3 = models.StringField(
        choices=[('1', 'I tried to minimize token use'), ('2', 'I tried to minimize costs'), ('3', 'I tried to minimze travel time'), ('4', 'I tried to minimize car use'),],
        label="sometimes",
        widget=widgets.RadioSelect,
        blank=False
    )

    minimization_focus_4 = models.StringField(
        choices=[('1', 'I tried to minimize token use'), ('2', 'I tried to minimize costs'), ('3', 'I tried to minimze travel time'), ('4', 'I tried to minimize car use'),],
        label="rarely",
        widget=widgets.RadioSelect,
        blank=False
    )

    minimization_focus_5 = models.StringField(
        choices=[('1', 'I tried to minimize token use'), ('2', 'I tried to minimize costs'), ('3', 'I tried to minimze travel time'), ('4', 'I tried to minimize car use'),],
        label="never",
        widget=widgets.RadioSelect,
        blank=False
    )

    fair_price_token = models.FloatField(
        label="What do you consider a fair price for 1 token (1 kg of CO₂ emissions) [in DKK]?",
        blank=False
    )

    # Post-survey Questions 2
    # Opinion scale (Likert)
    fun_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Trading tokens seems fun.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    difficulty_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Trading tokens seems difficult.",
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    intuitive_rating = models.StringField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        label="Needing tokens for driving feels intuitive to me.",
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
    trading_real_life = models.StringField(
        choices=[('1', 'Several times a day'), ('2', 'Once a day'), ('3', 'Several times a week'),  ('4', 'Once a week'),  ('5', 'Several times a month'), ('6', 'Once a month'), ('7', 'Never'),],
        label="If you had to use the system in real life, how frequently would you feel comfortable trading?",
        widget=widgets.RadioSelect,
        blank=False
    )
    effectiveness_opinion = models.StringField(
        choices=[('1', 'Yes'), ('2', 'No'), ('3', 'Not sure'),],
        label="Do you think such a scheme could effectively reduce CO₂ emissions?",
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
        choices=[('1', 'Reduce my CO₂ emissions'), ('2', 'Switch to electric or low-emission transportation'),
                    ('3', 'Offset CO₂ emissions by purchasing extra tokens'), ('4', 'Change how I plan travel or shopping'), ('5', 'Participate actively in the trading market'),
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
        choices=[('1', 'Trading'), ('2', 'Travel choice'), ('3', 'Other'), ('4', 'None')],
        label="Which part of the experiment did you find most confusing or frustrating?",
        widget=widgets.RadioSelect,
        blank=False
    )
    confusing_part_other = models.StringField(
        label="Please specify:",
        blank=True
    )

    payoff_expectation = models.FloatField(
        label="Before completing the experiment, how much did you expect to earn [in DKK]?",
        blank=False
    )

    inform_experiment = models.StringField(
        choices=[('1', 'Yes'), ('2', 'No')],
        label="Would you like to be informed about the results of this experiment?",
        widget=widgets.RadioSelect,
        blank=False
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
    form_fields = ['understanding_level', 'clarity_of_rules', 'interface_ease', 'familiar_currency', 'familiar_currency_other', 
                    'strategy_description_phase1', 'strategy_description_phase1_other', 'strategy_description_phase2', 
                    'strategy_description_phase2_other', 'strategy_description_phase3', 'strategy_description_phase3_other',
                    'minimization_focus_1', 'minimization_focus_2', 'minimization_focus_3', 'minimization_focus_4', 'minimization_focus_5', 'fair_price_token',]
    
# ======== Survey2 ========
class Survey2(Page):
    form_model = 'player'
    form_fields = ['fun_rating', 'difficulty_rating', 'intuitive_rating', 'system_vs_tax', 'prefer_over_tax', 'permit_fairness',]
    
# ======== Survey3 ========
class Survey3(Page):
    form_model = 'player'
    form_fields = ['support_local_scheme', 'trading_real_life', 'effectiveness_opinion', 'who_benefits', 'user_response_if_implemented', 'confusing_part',
                    'who_benefits_other', 'user_response_if_implemented_other', 'confusing_part_other','payoff_expectation', 'inform_experiment']
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        session = player.session
        participant = player.participant
        fee = session.config.get('participation_fee', 0)

        # ---------- 1) Draw winner ONCE across the whole session (anyone > 400) ----------
        if 'highpay_winner_code' not in session.vars:
            rows = []
            for part in session.get_participants():  # all participants in session
                base_total = float(part.payoff_plus_participation_fee())
                if base_total > C.CAP_PAYOFF:
                    rows.append({'code': part.code, 'base_payoff': base_total})

            if rows:
                df = pd.DataFrame(rows)
                winner_row = df.sample(n=1, random_state=None).iloc[0]
                session.vars['highpay_winner_code'] = winner_row['code']
            else:
                session.vars['highpay_winner_code'] = None

        winner_code = session.vars.get('highpay_winner_code')

        # ---------- 2) Compute this participant's final total (incl. fee) ----------
        base_total = float(participant.payoff_plus_participation_fee())  # includes fee
        is_candidate = base_total > C.CAP_PAYOFF
        is_winner = is_candidate and (participant.code == winner_code)

        if not is_candidate:
            final_total = max(C.MIN_PAYOFF, min(base_total, C.CAP_PAYOFF))
        else:
            final_total = min(base_total, C.MAX_WINNER_PAYOFF) if is_winner else C.CAP_PAYOFF

        # Round to nearest 5
        final_total = -(-final_total // 5) * 5

        # ---------- 3) Persist for the thank-you app & set official oTree payoff ----------
        # Store display values for the thank-you page (keep totals incl. fee here)
        participant.vars['base_total'] = round(base_total, 2)
        participant.vars['final_total'] = round(final_total, 2)
        participant.vars['is_candidate'] = is_candidate
        participant.vars['is_winner'] = is_winner

        # oTree's official payoff excludes the fee:
        final_excl_fee = final_total - fee
        player.payoff = final_excl_fee
        participant.payoff = final_excl_fee

page_sequence = [Literacy, Survey1, Survey2, Survey3]