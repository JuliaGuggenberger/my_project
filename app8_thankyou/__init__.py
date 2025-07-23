from otree.api import *

doc = """
    Thank you
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_thankyou'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    pass

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
        # Total payoff including any fixed amount
        final_payoff = float(player.participant.payoff_plus_participation_fee())
        player.final_payoff = final_payoff
        return dict(
            final_payoff=final_payoff
        )

page_sequence = [ThankYou]