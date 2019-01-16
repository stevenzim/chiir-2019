from collections import Counter

from src import annotations
from src.template import nudge
import config
from src import experiment

# Script below can be used to determine expected precision at 2 and 10 for different nudges
# We can therfore use this to make hypotheses about which nudges will perform better with different tasks
# For instance we know that T10 has a high number of incorrect results with re-rank and filter nudge,
# thus participant decisions will likely perform much worse than without nudge


nudge_list = ['color', 'rank', 'filter']
task_list = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']
# task_list = ['T10']
num_simulations = 1000
for task in task_list:
# for nudge_type in nudge_list:
    print()
    print()
    print('___________________________' + task + '______________________________')

    # for task in task_list:
    for nudge_type in nudge_list:
        # print('_________________________________________________________')
        print('___________________________' + nudge_type + '______________________________')
        result_obj = annotations.Results(task)
        results = result_obj.get_task_results()

        sample = result_obj.get_sample_of_results(results, .00)

        correct_incorrect_at_2 = []
        correct_incorrect_at_10 = []

        colors_at_2 = []
        colors_at_10 = []

        no_red_at_2 = []
        no_red_at_10 = []

        for i in range(num_simulations):
            ranks = result_obj.get_ranked_results(sample, val_reweight=42, random_seed=None)
            ranks = result_obj.merge_results_with_metadata(ranks)

            stats_obj = annotations.Statistics(ranks, config.PRIVACY_FIELD_NAME)
            ranks = stats_obj.get_all_statistical_test(ranks, config.PRIVACY_FIELD_NAME)
            if nudge_type == 'color':
                ranks = nudge.nudge_color(ranks)
                # print(ranks[1].keys())
                colors = list(map(lambda result: result['circles']['circle_color'], ranks[0:10]))
                colors_at_10.extend(colors)
                colors_at_2.extend(colors[0:2])

                red_filter = lambda result: result['circles']['circle_color'] != 'red'

                no_red = list(filter(red_filter, ranks))
                # reds = list(map(lambda result: result['circles']['circle_color'], no_red))
                # print(reds)
                no_red_at_10.extend(list(map(lambda result: result['JUDGEMENTS'], no_red[0:10])))
                no_red_at_2.extend(list(map(lambda result: result['JUDGEMENTS'], no_red[0:2])))

                # print(colors)
            if nudge_type == 'rank':
                ranks = nudge.nudge_re_rank(ranks)
            if nudge_type == 'filter':
                ranks = nudge.nudge_filter(ranks)
            correct_incorrect_10 = list(map(lambda result: result['JUDGEMENTS'], ranks[0:10]))

            if num_simulations<6:
                privacy_score = list(map(lambda result: result[config.PRIVACY_FIELD_NAME], ranks[0:10]))
                print(correct_incorrect_10)
                print(config.PRIVACY_FIELD_NAME)
                print(privacy_score)
            correct_incorrect_at_10.extend(correct_incorrect_10)
            correct_incorrect_at_2.extend(correct_incorrect_10[0:2])


        print ('Total correct and incorrect in top 2 after 1000 runs: ')
        print(Counter(correct_incorrect_at_2))

        print ('Total correct and incorrect in top 10 after 1000 runs: ')
        print(Counter(correct_incorrect_at_10))

        if nudge_type == 'color':
            print('Colors in top 2 after 1000 runs: ')
            print(Counter(colors_at_2))

            print('Colors in top 10 after 1000 runs: ')
            print(Counter(colors_at_10))

            print('No Red in top 2 after 1000 runs: ')
            print(Counter(no_red_at_2))

            print('No Red in top 10 after 1000 runs: ')
            print(Counter(no_red_at_10))
