from otree.api import *

doc = """
    Post Survey
"""

#*************************************************************************************************
# CONFIGURATION
class C(BaseConstants):
    NAME_IN_URL = 'app_feedback'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

#*************************************************************************************************
# MODELS
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    enough_time = models.StringField(blank=True)
    experiment_too_long = models.StringField(blank=True)
    decision = models.StringField(blank=True)
    not_liked = models.LongStringField(blank=True)
    not_understood = models.LongStringField(blank=True)
    most_confusing = models.LongStringField(blank=True)
    likely_failure_point = models.LongStringField(blank=True)
    favorite_thing = models.LongStringField(blank=True)
    comment = models.LongStringField(blank=True)

#*******************************************************************************************************************
# PAGES

# ======== Survey ========
class Survey(Page):
    form_model = 'player'
    form_fields = [
        'enough_time',
        'experiment_too_long',
        'decision',
        'not_liked',
        'not_understood',
        'most_confusing',
        'likely_failure_point',
        'favorite_thing',
        'comment',
    ]

    def is_displayed(player):
        return True


page_sequence = [Survey]