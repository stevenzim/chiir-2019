# To answer: To what extent (if any) is quality of decisions changed w.r.t 3 nudges and baseline?
# (Similar to Waterloo Tables 1/2 of waterloo)

import os
import csv
import copy
import config
from src import helper



def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_immediate_subfiles(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]


# Get list of participant folders
participant_folders = get_immediate_subdirectories(config.PARTICIPANT_PATH)
participant_folders = list(filter(lambda f_name: 'S' in f_name, participant_folders))
len(participant_folders)

# Clicks per experiment
for p_f_name in participant_folders:
    f_list = get_immediate_subfiles(config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["CLICKS"][0])
    print(p_f_name)
    print(len(f_list))

# Nudges (Not a single switch in first 40 participants)
for p_f_name in participant_folders:
    # p_f_name should be = to participant ID
    p_click_path = config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["NUDGE_STATUS"][0]
    f_list_clicks = get_immediate_subfiles(p_click_path)
    print(p_f_name)
    print(len(f_list_clicks))



# Get correct/incorrect per interface type
# check decisions per user!! ---> Print if not equal 12
# TODO: Figure out why participant S1026 recorded 17 decsions...everything looks okay
#       It recorded decisions for some pre-post task states for S1026.  e.g. states 10,12,13,18,37 ---> These should have been recorded as survey responses. Hmmm..

base_interface_report = {"control": {"correct": 0, "incorrect": 0},
                        "baseline": {"correct": 0, "incorrect": 0},
                        "nudge_filter": {"correct": 0, "incorrect": 0},
                        "nudge_rank": {"correct": 0, "incorrect": 0},
                        "nudge_stoplight": {"correct": 0, "incorrect": 0}}

base_interface_report_harmful = {"control": {"correct": 0, "harmful": 0},
                                "baseline": {"correct": 0, "harmful": 0},
                                "nudge_filter": {"correct": 0, "harmful": 0},
                                "nudge_rank": {"correct": 0, "harmful": 0},
                                "nudge_stoplight": {"correct": 0, "harmful": 0}}

for p_f_name in participant_folders:
    p_decision_path = config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["DECISIONS"][0]
    f_list_decisions = get_immediate_subfiles(p_decision_path)

    if len(f_list_decisions) != 12:
        print("TO MANY FILES!!!")
        print(p_f_name)
        print(len(f_list_decisions))

    # decision correct/incorrect
    question_defs = helper.load_json_from_file(config.QUESTIONS_AND_DEFINITIONS_PATH)
    for decision_file in f_list_decisions:
        decision_dict = helper.load_json_from_file(p_decision_path + '/' + decision_file)
        user_decision = decision_dict["decision"]
        user_interface = decision_dict["interface_name"]
        user_task_id = decision_dict["task_id"]
        correct_decision = question_defs[user_task_id]["QUESTION_CLASS"]
        if 'Practice' in user_task_id:
            continue
        if decision_dict["interface_type"] == "decision":
            if user_decision == correct_decision:
                base_interface_report[user_interface]['correct'] += 1
                base_interface_report_harmful[user_interface]['correct'] += 1
            if user_decision != correct_decision:
                base_interface_report[user_interface]['incorrect'] += 1
                if user_decision != 'inconclusive':
                    base_interface_report_harmful[user_interface]['harmful'] += 1


# Print percentage correct per interface
N = 80
for interface in base_interface_report.keys():
    print(interface + " \t%correct= " + str(base_interface_report[interface]['correct']/N)
          + " \t% incorrect= " + str(base_interface_report[interface]['incorrect']/N))


# Print percentage correct/HARMFUL per interface
N = 80
for interface in base_interface_report_harmful.keys():
    print(interface + " \t%correct= " + str(base_interface_report_harmful[interface]['correct']/N)
          + " \t% harmful= " + str(base_interface_report_harmful[interface]['harmful']/N))


# produce interface detail report
# includes participant_id/task/interface_name/decision/correct_decision/correct_bool/harmful_bool/date_time
participant_decision_report = {}
experiment_time_report = {}
for p_f_name in participant_folders:
    # p_f_name should be = to participant ID
    p_decision_path = config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["DECISIONS"][0]
    f_list_decisions = get_immediate_subfiles(p_decision_path)

    if len(f_list_decisions) != 12:
        print("TO MANY FILES!!!")
        print(p_f_name)
        print(len(f_list_decisions))

    if p_f_name not in participant_decision_report:
        # p_f_name  = t participant ID
        # we need to add the participant ID to dictionary if it is not already there
        participant_decision_report[p_f_name] = {}

    # decision correct/incorrect
    question_defs = helper.load_json_from_file(config.QUESTIONS_AND_DEFINITIONS_PATH)
    for decision_file in f_list_decisions:
        decision_dict = helper.load_json_from_file(p_decision_path + '/' + decision_file)
        user_decision = decision_dict["decision"]
        user_interface = decision_dict["interface_name"]
        user_task_id = decision_dict["task_id"]
        user_variant_id = decision_dict["variant_id"]
        correct_decision = question_defs[user_task_id]["QUESTION_CLASS"]

        # add blank dictionary for task_id (includes initialized clicke info)
        if user_task_id not in participant_decision_report[p_f_name]:
            participant_decision_report[p_f_name][user_task_id] = {"max_trackers_encountered": 0,
                                                                   "total_trackers_encountered": 0,
                                                                   "total_clicks": 0,
                                                                   "ranking_judgement": []}

        # HANDLE ERRORS FOR VARIANTS
        participant_decision_report[p_f_name][user_task_id]['design_error'] = False
        participant_decision_report[p_f_name][user_task_id]['wrong_interface'] = False
        if p_f_name in config.DESIGN_ERROR_PARTICIPANT_IDS:
            # print("DESIGN ERROR FOUND!!")
            # print(p_f_name)
            participant_decision_report[p_f_name][user_task_id]['design_error'] = True
            if (user_variant_id in ["4", "9"]) and (user_task_id in ["T9", "T10"]):
                participant_decision_report[p_f_name][user_task_id]['design_error'] = True
                participant_decision_report[p_f_name][user_task_id]['wrong_interface'] = True
                # print("WRONG INTERFACE FOUND!!")
                # print(p_f_name)
                # print(user_task_id)
            if (user_variant_id in ["5", "10"]) and (user_task_id in ["T3", "T6"]):
                # print("WRONG INTERFACE FOUND!!")
                # print(p_f_name)
                # print(user_task_id)
                participant_decision_report[p_f_name][user_task_id]['design_error'] = True
                participant_decision_report[p_f_name][user_task_id]['wrong_interface'] = True


        if 'Practice' in user_task_id:
            continue
        if decision_dict["interface_type"] == "decision":
            # add required data from decision dictionary
            participant_decision_report[p_f_name][user_task_id]["decision"] = user_decision
            participant_decision_report[p_f_name][user_task_id]["correct_decision"] = correct_decision
            participant_decision_report[p_f_name][user_task_id]["interface"] = user_interface
            participant_decision_report[p_f_name][user_task_id]["experiment_state"] = decision_dict["experiment_state"]
            participant_decision_report[p_f_name][user_task_id]["time_logged"] = decision_dict["time_logged"]
            participant_decision_report[p_f_name][user_task_id]["privacy_switch_default"] = decision_dict["privacy_switch_default"]

            if user_decision == correct_decision:
                base_interface_report[user_interface]['correct'] += 1
                base_interface_report_harmful[user_interface]['correct'] += 1
                participant_decision_report[p_f_name][user_task_id]["correct_bool"] = True
                participant_decision_report[p_f_name][user_task_id]["incorrect_bool"] = False
                participant_decision_report[p_f_name][user_task_id]["harmful_bool"] = False
            if user_decision != correct_decision:
                base_interface_report[user_interface]['incorrect'] += 1
                participant_decision_report[p_f_name][user_task_id]["correct_bool"] = False
                participant_decision_report[p_f_name][user_task_id]["incorrect_bool"] = True
                if user_decision != 'inconclusive':
                    base_interface_report_harmful[user_interface]['harmful'] += 1
                    participant_decision_report[p_f_name][user_task_id]["harmful_bool"] = True
                else:
                    participant_decision_report[p_f_name][user_task_id]["harmful_bool"] = False


        # TIME STUFF !!!!!!!
        # ADD START AND END TIMES FOR TASK (TIME DIFF BETWEEN pre task completion and decision completion)
        if decision_dict["experiment_state"] in config.STATES_DECISIONS:
            participant_decision_report[p_f_name][user_task_id]["task_end_time_logged"] = decision_dict["time_logged"]

        if decision_dict['experiment_state'] in config.STATES_PRE_TASK:
            # Used to handle the error cases e.g. S1056
            participant_decision_report[p_f_name][user_task_id]["task_start_time_logged"] = decision_dict["time_logged"]

        p_survey_path = config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["SURVEY"][0]
        f_list_survey = get_immediate_subfiles(p_survey_path)

        # Get times for each task
        for survey_file in f_list_survey:
            survey_dict = helper.load_json_from_file(p_survey_path + '/' + survey_file)
            if (survey_dict['experiment_state'] in config.STATES_PRE_TASK) and (survey_dict['task_id'] == user_task_id):
                participant_decision_report[p_f_name][user_task_id]["task_start_time_logged"] = survey_dict["time_logged"]

        # Get start and finish times for experiment time report
        min_time = ''
        max_time = ''
        experiment_time_report[p_f_name] = {'min_time': '',
                                            'max_time': ''}
        for survey_file in f_list_survey:
            survey_dict = helper.load_json_from_file(p_survey_path + '/' + survey_file)

            # intialize
            if experiment_time_report[p_f_name]['min_time'] == '':
                experiment_time_report[p_f_name]['min_time'] = survey_dict["time_logged"]
                experiment_time_report[p_f_name]['max_time'] = survey_dict["time_logged"]
                continue

            if survey_dict["time_logged"] < experiment_time_report[p_f_name]['min_time']:
                experiment_time_report[p_f_name]['min_time'] = survey_dict["time_logged"]
                continue

            if survey_dict["time_logged"] > experiment_time_report[p_f_name]['max_time']:
                experiment_time_report[p_f_name]['max_time'] = survey_dict["time_logged"]
                continue




# write dcitionary to json
helper.dump_json_to_file(config.REPORT_PATH + '/interface_decisions.json', participant_decision_report)




# click_report
base_click_report = {"max_trackers_encountered":0,
                     "total_trackers_encountered":0,
                     "total_clicks": 0,
                     "ranking_judgement": []}  #format [(rank_of_doc, judgement_of_doc)]

annotations = helper.load_json_from_file(config.JUDGMENTS_PATH)
domain_metadata = helper.load_json_from_file(config.URL_META_DATA)
"page_id"
domain_metadata['portobellophysio.ie']

for p_f_name in participant_folders:
    # p_f_name should be = to participant ID
    p_click_path = config.PARTICIPANT_PATH + '/' + p_f_name + '/' + config.PARTICIPANT_SUBFOLDERS["CLICKS"][0]
    f_list_clicks = get_immediate_subfiles(p_click_path)
    print(p_f_name)
    print(len(f_list_clicks))
    for decision_file in f_list_clicks:
        decision_dict = helper.load_json_from_file(p_click_path + '/' + decision_file)
        if "Practice" in decision_dict["task_id"]:
            continue

        user_task_id = decision_dict["task_id"]
        user_click_page_id = decision_dict["page_id"]
        user_click_page_rank = decision_dict["page_rank"]
        user_interface = decision_dict["interface_name"]
        page_judgement = annotations[user_click_page_id]['JUDGEMENTS']
        page_url_domain = annotations[user_click_page_id]['BASE_DOMAIN_FK']
        page_trackers = int(domain_metadata[page_url_domain][config.PRIVACY_FIELD_NAME])

        if page_trackers > 0 and user_interface == 'control':
            print(p_f_name)

        # update click counts
        if participant_decision_report[p_f_name][user_task_id]["max_trackers_encountered"] < page_trackers:
            participant_decision_report[p_f_name][user_task_id]["max_trackers_encountered"] = page_trackers
        participant_decision_report[p_f_name][user_task_id]["total_trackers_encountered"] += page_trackers
        participant_decision_report[p_f_name][user_task_id]["total_clicks"] += 1


# write participant decion report dictionary to csv
field_names = ["participant_id", "task_id"] + list(participant_decision_report['A1001']['T1'].keys())
with open(config.REPORT_PATH + '/interface_decisions.csv', 'w') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter='|')
    field_names.remove("ranking_judgement")
    csvwriter.writerow(field_names)
    print("SUCCESS")
    for participant_id in participant_decision_report.keys():
        for task_id in participant_decision_report[participant_id].keys():
            if 'Practice' in task_id:
                continue
            field_values = [participant_id, task_id]
            for field in field_names[2:]:
                if field == "ranking_judgement":
                    continue
                # print(task_id)
                # print(participant_id)
                field_values.append(participant_decision_report[participant_id][task_id].get(field))
            csvwriter.writerow(field_values)
csv_file.close()

print(participant_decision_report['A1001']['T3'])



# write experiment report dictionary to csv
field_names = ["participant_id"] + list(experiment_time_report['A1001'].keys())
with open(config.REPORT_PATH + '/experiment_times.csv', 'w') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter='|')
    csvwriter.writerow(field_names)
    print("SUCCESS")
    for participant_id in experiment_time_report.keys():
        # for time_def in experiment_time_report[participant_id].keys():
        field_values = [participant_id]
        for field in field_names[1:]:
            field_values.append(experiment_time_report[participant_id].get(field))
        csvwriter.writerow(field_values)
csv_file.close()

