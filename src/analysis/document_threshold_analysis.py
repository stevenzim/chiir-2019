"""Code below can be used to extract some simple descriptive statistics about the documents the user will retrieve in 
results page.  e.g. if document is in top quartile of privace threats"""


# Example to get statistics for participant 'TOOO1'
from src import experiment
from src import annotations


task_list = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']

# Get Descriptive statistics for each task
a = experiment.Experiment('T0001')
stats_dict = {}
for task_id in task_list:
    a.task_id = task_id
    a.get_task_payload()
    results = a.get_task_payload()
    results = results['all_results']

    stats_obj = annotations.Statistics(results, 'TOTAL_TRACKERS')
    print(task_id)
    stats_dict[task_id] = stats_obj.__dict__
stats_dict

# Get tests of threshold results for each task (e.g. above median, tukey outliers)
from collections import Counter

from src import experiment
from src import annotations

print("_________ON TOTAL TRACKERS__________")
a = experiment.Experiment('T0001')
stats_dict = {}
results = a.get_task_payload()
results = results['all_results']
for task_id in task_list:
    a.task_id = task_id
    a.get_task_payload()
    results = a.get_task_payload()
    results = results['all_results']
    stats_obj = annotations.Statistics(results, 'TOTAL_TRACKERS')
    threshold_data = stats_obj.get_all_statistical_test(results, 'TOTAL_TRACKERS')

    threshold_fields = ['above_mean','above_std', 'above_median', 'above_upper_quart', 'tukey_outlier']
    for threshold in threshold_fields:
        print(threshold)
        print(Counter(map(lambda x: x[threshold], threshold_data)))


print("_________ON REMAINING_TRACKERS__________")
a = experiment.Experiment('T0001')
stats_dict = {}
results = a.get_task_payload()
results = results['all_results']
for task_id in task_list:
    a.task_id = task_id
    a.get_task_payload()
    results = a.get_task_payload()
    results = results['all_results']
    print(len(results))
    stats_obj = annotations.Statistics(results, 'REMAINING_TRACKERS')
    threshold_data = stats_obj.get_all_statistical_test(results, 'REMAINING_TRACKERS')

    threshold_fields = ['above_mean','above_std', 'above_median', 'above_upper_quart', 'tukey_outlier']
    for threshold in threshold_fields:
        print(threshold)
        print(Counter(map(lambda x: x[threshold], threshold_data)))

# OUTPUT.... NOT A BIG DIFFERENCE
# _________ON TOTAL TRACKERS__________
# T2
# T2
# T2
# above_mean
# Counter({False: 12, True: 9})
# above_std
# Counter({False: 16, True: 5})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 21})
# _________ON REMAINING_TRACKERS__________
# T2
# T2
# T2
# above_mean
# Counter({False: 12, True: 9})
# above_std
# Counter({False: 16, True: 5})
# above_median
# Counter({False: 12, True: 9})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 21})

# _________ON TOTAL TRACKERS__________
# T5
# T5
# above_mean
# Counter({False: 12, True: 9})
# above_std
# Counter({False: 17, True: 4})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 21})
# _________ON REMAINING_TRACKERS__________
# T5
# T5
# above_mean
# Counter({False: 14, True: 7})
# above_std
# Counter({False: 18, True: 3})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 20, True: 1})


# _________ON TOTAL TRACKERS__________
# T6
# T6
# above_mean
# Counter({False: 11, True: 10})
# above_std
# Counter({False: 17, True: 4})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 21})
# _________ON REMAINING_TRACKERS__________
# T6
# T6
# above_mean
# Counter({False: 14, True: 7})
# above_std
# Counter({False: 17, True: 4})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 20, True: 1})

# _________ON TOTAL TRACKERS__________
# T8
# T8
# above_mean
# Counter({False: 11, True: 10})
# above_std
# Counter({False: 17, True: 4})
# above_median
# Counter({False: 11, True: 10})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 20, True: 1})
# _________ON REMAINING_TRACKERS__________
# T8
# T8
# above_mean
# Counter({False: 14, True: 7})
# above_std
# Counter({False: 17, True: 4})
# above_median
# Counter({False: 12, True: 9})
# above_upper_quart
# Counter({False: 16, True: 5})
# tukey_outlier
# Counter({False: 21})

# _________ON TOTAL TRACKERS__________
# T9
# T9
# above_mean
# Counter({False: 13, True: 9})
# above_std
# Counter({False: 19, True: 3})
# above_median
# Counter({True: 11, False: 11})
# above_upper_quart
# Counter({False: 16, True: 6})
# tukey_outlier
# Counter({False: 20, True: 2})
# _________ON REMAINING_TRACKERS__________
# T9
# T9
# above_mean
# Counter({False: 13, True: 9})
# above_std
# Counter({False: 18, True: 4})
# above_median
# Counter({True: 11, False: 11})
# above_upper_quart
# Counter({False: 16, True: 6})
# tukey_outlier
# Counter({False: 22})

