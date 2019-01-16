# This is start of analysis on nudge results.  You should consider running simulations with random seeds,
# Similar to the analysis in src/analysis/precision_and_rank_analysis.py

import copy
from collections import Counter


from src import experiment
from src.template import nudge

a = experiment.Experiment('T0001')
task_list = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']
for task_id in task_list:
    a.task_id = task_id
    a.get_task_payload()
    results = a.get_task_payload()
    print('______________________' + task_id + '______________________________')
    print('all')
    colors = nudge.nudge_color(copy.copy(results['all_results']))
    len(colors)
    colors_correct = list(map(lambda x: x['JUDGEMENTS'], colors))
    print(colors_correct)

    print('filter:')
    filter = nudge.nudge_filter(copy.copy(results['all_results']))
    filters_correct = list(map(lambda x: x['JUDGEMENTS'], filter))
    print(filters_correct)

    print('reranked:')
    re_ranked = nudge.nudge_re_rank(copy.copy(results['all_results']))
    re_ranked_correct = list(map(lambda x: x['JUDGEMENTS'], re_ranked))
    print(re_ranked_correct)

#
# T2
# T2
# ______________________T2______________________________
# all
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect']
# filter:
# ['Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct']
# reranked:
# ['Incorrect', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Incorrect', 'Incorrect']
# T5
# T5
# ______________________T5______________________________
# all
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct']
# filter:
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct']
# reranked:
# ['Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect']
# T6
# T6
# ______________________T6______________________________
# all
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct']
# filter:
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Incorrect', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect']
# reranked:
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Incorrect', 'Incorrect', 'Incorrect', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct']
# T8
# T8
# ______________________T8______________________________
# all
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct']
# filter:
# ['Correct', 'Incorrect', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct']
# reranked:
# ['Incorrect', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct']
# T9
# T9
# ______________________T9______________________________
# all
# ['Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct']
# filter:
# ['Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct']
# reranked:
# ['Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Incorrect', 'Correct', 'Correct', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Correct', 'Incorrect', 'Correct', 'Incorrect']
