# static configuratons (e.g. File paths and directories for data files)

# index
INDEX_FILE = "resources/data/INDEX.json"
INDEX_KEY = "current_index"

# annotations
QUESTIONS_AND_DEFINITIONS_PATH = "resources/data/annotations/json/COCHRANE_QUESTION_DEFINITIONS.json"
JUDGMENTS_PATH = "resources/data/annotations/json/ALL_JUDGMENTS_HELPFUL.json"
URL_META_DATA = "resources/data/annotations/json/ALL_URL_DOMAIN_METADATA.json"

# DESIGN AND INTERFACE PRESENTATION CONTROLS
MAX_EXPERIMENT_STATE = 40 #useful for control of progress bar
RESET_PRIVACY_SWITCH_STATES = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39] # useful to know when it's safe to switch back to default

MEDICAL_QUESTION_NUM_BY_STATE = {4: 'Practice 1', 5: 'Practice 1', 6: 'Practice 1',
                                 7: 'Practice 2', 8: 'Practice 2', 9: 'Practice 2',
                                 10: '1', 11: '1', 12: '1', 13: '2', 14: '2', 15: '2',
                                 16: '3', 17: '3', 18: '3', 19: '4', 20: '4', 21: '4',
                                 22: '5', 23: '5', 24: '5', 25: '6', 26: '6', 27: '6',
                                 28: '7', 29: '7', 30: '7', 31: '8', 32: '8', 33: '8',
                                 34: '9', 35: '9', 36: '9', 37: '10', 38: '10', 39: '10'}


# TODO: Change active value below for full experiment
# EXPERIMENT_VARIANT_FILE = "resources/data/design/EXPERIMENT_VARIANTS_STATES_INTERFACES_TASKS.json"
EXPERIMENT_VARIANT_FILE = "resources/data/design/ALL_VARIANTS.json"


# CDF ranking values (for annotations.py)
# These values tuned emperically to get roughly 81% correct in top 10 documents
# The min percent correct is set to 0 now to ensure all documents are kept.
REWEIGHT_VAL = 42
MIN_PERCENT_CORRECT = .00



# this dictionary acts as a lookup between the interface_name field from above json file.
# This is used to look up the html template file name
EXPERIMENT_TEMPLATE_LOOK = {"survey_instructions": "survey_instructions.html",
                            "survey_prev_experience": "survey_prev_experience.html",
                            "survey_pre_task": "survey_pre_task.html",
                            "decision": "survey_decision.html",   # NOTE: DECISION IS NOT LISTED IN DESIGN JSON FILE,
                                                                  # this is only called when hitting decsion button
                            "control": "survey_decision.html",
                            "baseline": "search_results.html",
                            "nudge_filter": "search_results.html",
                            "nudge_rank": "search_results.html",
                            "nudge_stoplight": "search_results.html",
                            "survey_post_task": "survey_post_task.html",
                            "exit_page": "exit_page.html"}

# participants
PARTICIPANT_PATH = "resources/data/participant/"
PARTICIPANT_STATE_FILE_NAME = "participant_state.json"
## participant subfolder structure "{"GLOBAL_NAME",("name_of_folder","description of folder contents")}
PARTICIPANT_SUBFOLDERS = {"CLICKS": ("clicks","where click data is stored"),
                          "DECISIONS": ("decisions","where participant decisions are stored"),
                          "SURVEY": ("survey","where participant survey/questionnare responses are stored"),
                          "ERRORS": ("errors","folder for any errors recorded during participant experiment"),
                          "NUDGE_STATUS": ("nudge_switch", "records everytime user clicks the nudge switch on/off"),
                          "OTHER": ("misc", "records other stuff, such as login attempts")}
LOGGING_KEYS_TO_REMOVE = {
    "interface_resources": "text, participant_state, cochrane_definitions, search_results",
    "interface_task_purpose": "capture user interaction with different SERPs and control",
    "qualtrics_link": "http://test1.com",
    "time_created": "Timestamp: 2018-08-20 16:33:36",
    "time_updated": "2018-08-24 17:28:45",
}

# Search Results Fields
PRIVACY_FIELD_NAME = "REMAINING_TRACKERS"
# PRIVACY_FIELD_NAME = "TOTAL_TRACKERS"
PRIVACY_MARKER_MED_CONCERN = "above_median"
PRIVACY_MARKER_HIGH_CONCERN = "above_upper_quart"
PRIVACY_MARKER_FILTER_BOOL = "above_median"

# reporting
REPORT_PATH = "resources/data/reports"
STATES_PRE_TASK = [4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37]
STATES_DECISIONS = [5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38]
DESIGN_ERROR_PARTICIPANT_IDS = ['S1016', 'S1021', 'S1041', 'S1046', 'S1066', 'S1071',
                                'S1091', 'S1096', 'S1116', 'S1121', 'S1141', 'S1146']



