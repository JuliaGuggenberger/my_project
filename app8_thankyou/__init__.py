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

#*******************************************************************************************************************
# PAGES

# ======== Thank You ========
class ThankYou(Page):
    @staticmethod
    def vars_for_template(player):
        session = player.session
        participant = player.participant

        base_payoff = float(participant.payoff_plus_participation_fee())
        is_candidate = base_payoff > C.CAP_PAYOFF
        winner_code = session.vars.get('highpay_winner_code', None)
        is_winner = is_candidate and (participant.code == winner_code)

        if not is_candidate:
            # Clamp to [MIN_PAYOFF, CAP_PAYOFF]
            final_payoff = max(C.MIN_PAYOFF, min(base_payoff, C.CAP_PAYOFF))
        else:
            # Candidate with base > 400
            if is_winner:
                final_payoff = min(base_payoff, C.MAX_WINNER_PAYOFF)
            else:
                final_payoff = C.CAP_PAYOFF

        # Round all payoffs to nearest 5
        final_payoff = round(final_payoff / 5) * 5

        # Persist on the player for record
        player.final_payoff = final_payoff

        return dict(
            base_payoff=round(base_payoff, 2),
            final_payoff=round(final_payoff, 2),
            is_candidate=is_candidate,
            is_winner=is_winner,
            min_payoff=C.MIN_PAYOFF,
            cap_payoff=C.CAP_PAYOFF,
            max_winner_payoff=C.MAX_WINNER_PAYOFF,
        )

page_sequence = [ThankYou]