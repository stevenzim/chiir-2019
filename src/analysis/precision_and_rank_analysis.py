from src import annotations

# Script below can be used to tune paramaters of of sampling and ranking functions
# In current setup, .75 is sampled, and val_reweight is set to 60
# This gives around 81% precision at rank 10 and 77% precision at rank 20
# Only on set T9 do we have more than 20 results, which results in around 78.9% prec


task_list = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']



all_correct_incorrect_at_10 = []

from collections import Counter
for task in task_list:
    print('_________________________________________________________')
    print(task)
    result_obj = annotations.Results(task)
    results = result_obj.get_task_results()

    print('Total results available:')
    print(len(results))

    print('Total results sampled after removal of excess incorrects:')
    sample = result_obj.get_sample_of_results(results, .00)
    print(len(sample))

    correct_incorrect_at_10 = []
    correct_incorrect_at_20 = []
    correct_incorrect_at_all = []
    rank_1_list = []
    rank_2_list = []
    rank_3_list = []
    rank_4_list = []
    rank_5_list = []
    rank_6_list = []
    rank_7_list = []
    rank_8_list = []
    rank_9_list = []
    rank_10_list = []
    for i in range(1000):
        ranks = result_obj.get_ranked_results(sample, val_reweight=42, random_seed=None)
        correct_incorrect_10 = list(map(lambda result: result['JUDGEMENTS'], ranks[0:10]))
        correct_incorrect_at_10.extend(correct_incorrect_10)

        correct_incorrect_20 = list(map(lambda result: result['JUDGEMENTS'], ranks[0:20]))
        correct_incorrect_at_20.extend(correct_incorrect_20)
        correct_incorrect_all = list(map(lambda result: result['JUDGEMENTS'], ranks))
        correct_incorrect_at_all.extend(correct_incorrect_all)
        rank_1_list.append(ranks[0]['JUDGEMENTS'])
        rank_2_list.append(ranks[1]['JUDGEMENTS'])
        rank_3_list.append(ranks[2]['JUDGEMENTS'])
        rank_4_list.append(ranks[3]['JUDGEMENTS'])
        rank_5_list.append(ranks[4]['JUDGEMENTS'])
        rank_6_list.append(ranks[5]['JUDGEMENTS'])
        rank_7_list.append(ranks[6]['JUDGEMENTS'])
        rank_8_list.append(ranks[7]['JUDGEMENTS'])
        rank_9_list.append(ranks[8]['JUDGEMENTS'])
        rank_10_list.append(ranks[9]['JUDGEMENTS'])


    print ('Total correct and incorrect in top 10 after 10000 runs: ')
    print(Counter(correct_incorrect_at_10))
    all_correct_incorrect_at_10.append(dict(Counter(correct_incorrect_at_10)))


    print('Total correct and incorrect in top 20 after 10000 runs: ')
    print(Counter(correct_incorrect_at_20))

    print('Total correct and incorrect in for all after 10000 runs: ')
    print(Counter(correct_incorrect_at_all))
    #
    # print('--ranks--')
    # print ('Total correct and incorrect at rank 1 after 10000 runs: ')
    # print(Counter(rank_1_list))
    #
    # print('Total correct and incorrect at rank 2 after 10000 runs: ')
    # print(Counter(rank_2_list))
    #
    # print('Total correct and incorrect at rank 3 after 10000 runs: ')
    # print(Counter(rank_3_list))
    #
    # print('Total correct and incorrect at rank 4 after 10000 runs: ')
    # print(Counter(rank_4_list))
    #
    # print('Total correct and incorrect at rank 5 after 10000 runs: ')
    # print(Counter(rank_5_list))
    #
    # print('Total correct and incorrect at rank 6 after 10000 runs: ')
    # print(Counter(rank_6_list))
    #
    # print('Total correct and incorrect at rank 7 after 10000 runs: ')
    # print(Counter(rank_7_list))
    #
    # print('Total correct and incorrect at rank 8 after 10000 runs: ')
    # print(Counter(rank_8_list))
    #
    # print('Total correct and incorrect at rank 9 after 10000 runs: ')
    # print(Counter(rank_9_list))
    #
    # print('Total correct and incorrect at rank 10 after 10000 runs: ')
    # print(Counter(rank_10_list))


total_correct = 0
total_incorrect = 0
for item in all_correct_incorrect_at_10:
    total_correct += item['Correct']
    total_incorrect += item['Incorrect']

print(total_correct)
print(total_incorrect)