
"""Below is a script to build all 10 design variants for study
Step 1 - Build 10x10 Graeco Latin Square for the 5 different interfaces and 10 Cochrane questions
       - NOTE: The rows were randomly shuffled to produce 3 latin square designs 1 each for helpful/unhelpful + 1 interface
Step 2 - Overlay interface latin square with each helpful/unhelpful latin square
Step 3 - Shuffle the list of interface/medical question tuples for random order (done for all 5 rows
Step 4 - Randomly select order of practice tasks to occur before main 10 experiments
Step 5 - Do Steps 3 and 4 again for another 5 rows, to produce a set of 10 different variants
Step 6 - Build and output the Design Dictionary to be used for actual stuides... this is keyed on variant id which participant 
       - randomly assigned.   The participant will then go through each state of the design

"""
# TODO: You might consider option to set SEED...otherwise if you want to rebuild variants exactly the same, it becomes impossible.

import random
import copy

from src import helper

helpful = ['T2', 'T5', 'T6', 'T8', 'T9']

random.shuffle(helpful)
print(helpful)


# interfaces
a = 'control'
b = 'baseline'
c = 'nudge_stoplight'
d = 'nudge_filter'
e = 'nudge_rank'

# helpful
A = 'T2'
B = 'T5'
C = 'T6'
D = 'T8'
E = 'T9'

row_1_h = [(A, a), (B, d), (C, b), (D, e), (E, c)]
row_2_h = [(B, b), (C, e), (D, c), (E, a), (A, d)]
row_3_h = [(C, c), (D, a), (E, d), (A, b), (B, e)]
row_4_h = [(D, d), (E, b), (A, e), (B, c), (C, a)]
row_5_h = [(E, e), (A, c), (B, a), (C, d), (D, b)]


# not helpful
A = 'T1'
B = 'T3'
C = 'T4'
D = 'T7'
E = 'T10'

row_1_nh = [(A, a), (B, d), (C, b), (D, e), (E, c)]
row_2_nh = [(B, b), (C, e), (D, c), (E, a), (A, d)]
row_3_nh = [(C, c), (D, a), (E, d), (A, b), (B, e)]
row_4_nh = [(D, d), (E, b), (A, e), (B, c), (C, a)]
row_5_nh = [(E, e), (A, c), (B, a), (C, d), (D, b)]

row_1 = row_1_h + row_1_nh
row_2 = row_2_h + row_2_nh
row_3 = row_3_h + row_3_nh
row_4 = row_4_h + row_4_nh
row_5 = row_5_h + row_5_nh


# h1 = ['T8', 'T5', 'T2', 'T9', 'T6']
# h2 = ['T2', 'T8', 'T6', 'T5', 'T9']
# h3 = ['T5', 'T6', 'T9', 'T2', 'T8']
# h4 = ['T9', 'T2', 'T8', 'T6', 'T5']
# h5 = ['T6', 'T9', 'T5', 'T8', 'T2']
#
#
# # not helpful
# u1 = ['T4', 'T3', 'T10', 'T7', 'T1']
# u2 = ['T7', 'T1', 'T3', 'T10', 'T4']
# u3 = ['T1', 'T4', 'T7', 'T3', 'T10']
# u4 = ['T10', 'T7', 'T4', 'T1', 'T3']
# u5 = ['T3', 'T10', 'T1', 'T4', 'T7']
#
# # interface
# interfaces = ['control', 'baseline', 'nudge_stoplight', 'nudge_rank', 'nudge_filter']
# random.shuffle(interfaces)
# i1 = ['nudge_stoplight',    'nudge_rank',       'control',          'baseline',         'nudge_filter']
# i2 = ['nudge_filter',       'nudge_stoplight',  'baseline',         'nudge_rank',       'control']
# i3 = ['control',            'baseline',         'nudge_stoplight',  'nudge_filter',     'nudge_rank']
# i4 = ['baseline',            'nudge_filter',     'nudge_rank',       'control',          'nudge_stoplight']
# i5 = ['nudge_rank',           'control',          'nudge_filter',     'nudge_stoplight',  'baseline']
#
# # THIS IS i4 and i5 (FUCKED UP VERSIONS): This was fixed on September 29th.  30 participants were run with these
# # variants, 10x10 design means that 12 participants had either no baseline or no nudge_rank.
# # THIS SHOULD BE KEPT AS ARTIFACTORY COMMENT
# # i4 = ['nudge_rank',         'nudge_filter',     'nudge_rank',       'control',          'nudge_stoplight']
# # i5 = ['baseline',           'control',          'nudge_filter',     'nudge_stoplight',  'baseline']
#
#
# #STEP 2
# # graeco 1st 5
# row_1 = list(zip(h1, i1)) + list(zip(u1, i1))
# row_2 = list(zip(h2, i2)) + list(zip(u2, i2))
# row_3 = list(zip(h3, i3)) + list(zip(u3, i3))
# row_4 = list(zip(h4, i4)) + list(zip(u4, i4))
# row_5 = list(zip(h5, i5)) + list(zip(u5, i5))

# practice options
p1 = [('Practice-1', 'control'), ('Practice-2', 'baseline')]
p2 = [('Practice-2', 'control'), ('Practice-1', 'baseline')]
p3 = [('Practice-1', 'baseline'), ('Practice-2', 'control')]
p4 = [('Practice-2', 'baseline'), ('Practice-1', 'control')]
practice_opts = [p1, p2, p3, p4]

# randomize columns 2x and store in 10 by 10 matrix
graeco_ten_matrix = []
variant = 1
for i in [1,2]:
    for row in [row_1, row_2, row_3, row_4, row_5]:
        print("NEW ROW.....")
        # print(row)
        temp_row = copy.deepcopy(row)
        # print(temp_row)
        # STEP 3
        random.shuffle(temp_row)
        # print(temp_row)
        # STEP 4
        # randomly select order of practice tasks
        practice_tasks = copy.deepcopy(random.choice(practice_opts))
        # print(practice_tasks)
        # add all other tasks after practice tasks
        practice_tasks = practice_tasks + temp_row
        # print(practice_tasks)
        print("*****VARAIANT " + str(variant) + "*********")
        for task in practice_tasks:
            print(task)
        graeco_ten_matrix.append(practice_tasks)

        variant+=1




# Build Design Dictionary
def add_state_dict(task_tuple):
    return {"task_id": task_tuple[0],
            "interface_name": task_tuple[1],
            "interface_type": task_tuple[2]}


def create_question_message(question_num):
    if question_num < 3:
        return 'Practice ' + str(question_num)
    else:
        return str(question_num - 2)

design_dict = {}
message_question_dict = {}  # This dictionary is used to build config.MEDICAL_QUESTION_NUM_BY_STATE
reset_privacy_switch = [] #This list used to build config.RESET_PRIVACY_SWITCH_STATES

task_0 = [('login', 'login_screen', 'static')]
task_1 = [('instruction', 'instruction_page', 'static')]
task_2 = [('survey_instruct', 'survey_instructions', 'static')]
task_3 = [('survey_previous', 'survey_prev_experience', 'static')]
task_exit = [('exit_qualtrics', 'exit_page', 'static')]


for idx in list(range(10)):
    variant_id = 0
    variant_id = idx + 1
    variant_id = str(variant_id)
    design_dict[variant_id] = {}
    design_dict[variant_id]['0'] = add_state_dict(task_0[0])
    design_dict[variant_id]['1'] = add_state_dict(task_1[0])
    design_dict[variant_id]['2'] = add_state_dict(task_2[0])
    design_dict[variant_id]['3'] = add_state_dict(task_3[0])
    state_id = 4
    question_num = 1
    for design_variant in graeco_ten_matrix[idx]:

        # question message update 1
        message_question_dict[state_id] = create_question_message(question_num)

        # add pre task
        pre_task = (design_variant[0], 'survey_pre_task', 'decision_pre')
        design_dict[variant_id][str(state_id)] = add_state_dict(pre_task)
        state_id += 1

        # question message update 2
        message_question_dict[state_id] = create_question_message(question_num)

        # Add main interface (nudge/baseline/control)
        main_task = (design_variant[0], design_variant[1], 'decision')
        design_dict[variant_id][str(state_id)] = add_state_dict(main_task)
        state_id += 1


        # question message update 3
        message_question_dict[state_id] = create_question_message(question_num)

        # add post task
        post_task = (design_variant[0], 'survey_post_task', 'decision_post')
        design_dict[variant_id][str(state_id)] = add_state_dict(post_task)

        # add privacy switch reset state number
        if question_num == 1:
            reset_privacy_switch.append(state_id)

        state_id += 1

        question_num += 1

    # add exit to survey..
    design_dict[variant_id][str(state_id)] = add_state_dict(task_exit[0])


helper.dump_json_to_file("resources/data/design/ALL_VARIANTS.json", design_dict)


# TODO: You need to manually copy the output to config file
print(message_question_dict)  # This dictionary is used to build config.MEDICAL_QUESTION_NUM_BY_STATE
print(reset_privacy_switch)  # This list used to build config.RESET_PRIVACY_SWITCH_STATES



# Double Check!
interface_tasks = {}

for variant in design_dict.keys():
    for state in  design_dict[variant].keys():
        interface_name = design_dict[variant][state]["interface_name"]
        interface_type = design_dict[variant][state]["interface_type"]
        task_id = design_dict[variant][state]["task_id"]

        if interface_type == 'decision':
            if task_id in interface_tasks:
                if interface_name in interface_tasks[task_id]:
                    interface_tasks[task_id][interface_name] += 1
                else:
                    interface_tasks[task_id][interface_name] = 1
            else:
                interface_tasks[task_id] = {interface_name: 1}

print(interface_tasks)

#TODO: After testing of experiment you can remove below, as above code is what should be used


# Scripts to convert experiments variant csv files to json

import csv

from src import helper


########### DESIGN CONVERSIONS #######




# # variants_states_interfaces_tasks conversions
# csv_file = open('resources/data/design/experiment_variants_states_interfaces_tasks.csv', 'rb')
# reader = csv.reader(csv_file)
# fieldnames = reader.next()
# print(fieldnames)
# temp_dict = {}
# # needs to be format {task id: [{everything else}}}
# reader = csv.DictReader( csv_file, fieldnames)
# i = 1
# for row in reader:
#     variant_id = str(row["variant_id"])
#     state_id = str(row["state_id"])
#     state_interface_task_dict = {state_id: {fieldnames[2]: row[fieldnames[2]],
#                                             fieldnames[3]: row[fieldnames[3]],
#                                             fieldnames[4]: row[fieldnames[4]],
#                                             fieldnames[5]: row[fieldnames[5]],
#                                             fieldnames[6]: row[fieldnames[6]]}}
#     print (row.values())
#     try:
#         temp_dict[variant_id]
#         temp_dict[variant_id][row[fieldnames[1]]] = state_interface_task_dict[state_id]
#     except:
#         temp_dict[variant_id] = state_interface_task_dict
#
# print (temp_dict.keys())
# helper.dump_json_to_file('resources/data/design/EXPERIMENT_VARIANTS_STATES_INTERFACES_TASKS.json', temp_dict)
# csv_file.close()