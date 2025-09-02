from otree.api import *
import pandas as pd

doc = """
    Thank you
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_thankyou'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_PAYOFF = 200
    CAP_PAYOFF = 400
    MAX_WINNER_PAYOFF = 700

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    def creating_session(self):
        # Pick exactly one winner among participants with base_payoff > CAP_PAYOFF
        if 'highpay_winner_code' not in self.session.vars:
            candidates = []
            for p in self.get_players():
                base = float(p.participant.payoff_plus_participation_fee())
                if base > C.CAP_PAYOFF:
                    candidates.append({
                        'player': p,
                        'code': p.participant.code,
                        'base_payoff': base
                    })

            if candidates:
                df = pd.DataFrame(candidates)
                # sample(n=1) returns a DataFrame, so we take .iloc[0] to get the row
                winner_row = df.sample(n=1, random_state=None).iloc[0]
                winner = winner_row['player']
                self.session.vars['highpay_winner_code'] = winner.participant.code
            else:
                self.session.vars['highpay_winner_code'] = None

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    final_payoff = models.CurrencyField()
    exact_payoff = models.CurrencyField()

#*******************************************************************************************************************
# PAGES

# ======== Thank You ========
class ThankYou(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        session = player.session
        fee = session.config.get('participation_fee', 0)

        # Prefer the values computed earlier; fall back gracefully if missing
        final_total = participant.vars.get('final_total')
        base_total = participant.vars.get('base_total')

        if final_total is None:
            # Fallback: reconstruct from official payoff + fee (still correct if earlier step ran)
            final_total = float(participant.payoff) + fee

        if base_total is None:
            base_total = float(participant.payoff_plus_participation_fee())

        is_candidate = participant.vars.get('is_candidate', base_total > C.CAP_PAYOFF)
        is_winner = participant.vars.get(
            'is_winner',
            is_candidate and (participant.code == session.vars.get('highpay_winner_code'))
        )

        # Store for record (optional, does NOT change official payoff)
        player.final_payoff = final_total
        player.exact_payoff = base_total

        return dict(
            base_payoff=base_total,
            final_payoff=final_total,
            is_candidate=is_candidate,
            is_winner=is_winner,
            min_payoff=C.MIN_PAYOFF,
            cap_payoff=C.CAP_PAYOFF,
            max_winner_payoff=C.MAX_WINNER_PAYOFF,
        )

page_sequence = [ThankYou]