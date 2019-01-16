# Stores all class/data to be used for survey forms

from flask_wtf import FlaskForm
from wtforms import RadioField


class InstructionsQuiz(FlaskForm):
    """FOR simplicity in programing, all answers should be true"""
    # Users understanding of instructions
    # You have 3 possible decisions available to you for each treatment and health issue?
    decision_question_1 = RadioField('Label', choices=[('1', 'True'),
                                                       ('0', 'False')])
    # # There are only 2 possible decisions available to you for each treatment and health issue?
    # decision_question_2 = RadioField('Label', choices=[('1', 'True'),
    #                                                   ('0', 'False')])
    # Including practice, there are 11 decision tasks in total for the treatment and medical conditions you will review?
    task_question_1 = RadioField('Label', choices=[('1', 'True'),
                                                   ('0', 'False')])
    #
    # # 1 of these tasks will be used for practice?
    # task_question_2 = RadioField('Label', choices=[('1', 'True'),
    #                                                ('0', 'False')])


class PreviousSearchForm(FlaskForm):
    # Understanding previous experience of search by user for health topics
    # I use search systems (such as Google or Bing) for all of my questions and concerns about health and medicine.
    prev_search_question_1 = RadioField('Label', choices=[('1', 'Strongly disagree'),
                                                           ('2', ''),
                                                           ('3', ''),
                                                           ('4', 'Neither agree nor disagree'),
                                                           ('5', ''),
                                                           ('6', ''),
                                                           ('7', 'Strongly agree')])
    # I never go online to find additional information before visiting the doctor about a medical concern
    prev_search_question_2 = RadioField('Label',  choices=[('1', 'Strongly disagree'),
                                                           ('2', ''),
                                                           ('3', ''),
                                                           ('4', 'Neither agree nor disagree'),
                                                           ('5', ''),
                                                           ('6', ''),
                                                           ('7', 'Strongly agree')])


class PreTaskForm(FlaskForm):
    # Understanding your prior knowledge of treatment and health issue
    # How knowledgeable are you of this health issue?
    health_question = RadioField('Label', choices=[('1', 'I have no knowledge'),
                                                   ('2', ''),
                                                   ('3', ''),
                                                   ('4', 'Neither/Nor'),
                                                   ('5', ''),
                                                   ('6', ''),
                                                   ('7', 'I have expert knowledge')])
    # What level of knowledge do you have in regards to this treatment?
    treatment_question = RadioField('Label',  choices=[('1', 'I have no knowledge'),
                                                       ('2', ''),
                                                       ('3', ''),
                                                       ('4', 'Neither/Nor'),
                                                       ('5', ''),
                                                       ('6', ''),
                                                       ('7', 'I have expert knowledge')])

class PostTaskForm(FlaskForm):
    # Understanding confidence in participant decision
    # How confident are you in your decision about the effectiveness of the treatment for the medical condition?
    confidence_question = RadioField('Label', choices=[('1', 'I am very unconfident in my decision'),
                                                   ('2', ''),
                                                   ('3', ''),
                                                   ('4', 'Neither confident nor unconfident'),
                                                   ('5', ''),
                                                   ('6', ''),
                                                   ('7', 'I am very confident in my decision' )])
    # To what extent are your certain about your decision?
    uncertainty_question = RadioField('Label',  choices=[('1', 'I am very uncertain about my decision'),
                                                       ('2', ''),
                                                       ('3', ''),
                                                       ('4', 'Neither certain nor uncertain'),
                                                       ('5', ''),
                                                       ('6', ''),
                                                       ('7', 'I am very certain about my decision')])

