from src import annotations


# TEST to verify results sampling is working correctly
result_obj = annotations.Results('Practice-2')
results = result_obj.get_task_results()

sample = result_obj.get_sample_of_results(results, .75)
assert len(sample) == 9

# TEST to verify result cleansing is handled correctly
a = {'WEIGHTED_RANK_RND': '14'}
b = {'WEIGHTED_RANK_RND': '31'}
c = {'WEIGHTED_RANK_RND': '555'}

a_expected = {'WEIGHTED_RANK_RND': 18}
b_expected = {'WEIGHTED_RANK_RND': 1}
c_expected = {'WEIGHTED_RANK_RND': 1}

assert annotations.rank_cleanse_function(a, rank_field_to_update='WEIGHTED_RANK_RND') == a_expected
assert annotations.rank_cleanse_function(b, rank_field_to_update='WEIGHTED_RANK_RND') == b_expected
assert annotations.rank_cleanse_function(c, rank_field_to_update='WEIGHTED_RANK_RND') == c_expected


# TEST to verify result list built correct for build CDF sampling list
a = {'WEIGHTED_RANK_RND': 3}
b = {'WEIGHTED_RANK_RND': 4}
c = {'WEIGHTED_RANK_RND': 1}

combined_results = [a, b, c]
expected_length = 8
assert len(annotations.build_cdf_sampling_list(combined_results)) == expected_length


# Tests to verify annotations.sample_and_rank_results function is working
a = {'WEIGHTED_RANK_RND': 1,
     'URL': 'A'}
b = {'WEIGHTED_RANK_RND': 3,
     'URL': 'B'}
c = {'WEIGHTED_RANK_RND': 2,
     'URL': 'C'}
# TEST 1
combined_results = [a, b, c]
expected_results = [{'URL': 'A', 'WEIGHTED_RANK_RND': 1},
                     {'URL': 'B', 'WEIGHTED_RANK_RND': 3},
                     {'URL': 'C', 'WEIGHTED_RANK_RND': 2}]
cdf_list = annotations.build_cdf_sampling_list(combined_results)
ranked_results = annotations.sample_and_rank_results(cdf_list, [], random_seed=2)
assert ranked_results == expected_results

# TEST 2
combined_results = [a, b, c]
expected_results = [{'URL': 'B', 'WEIGHTED_RANK_RND': 3},
                     {'URL': 'A', 'WEIGHTED_RANK_RND': 1},
                     {'URL': 'C', 'WEIGHTED_RANK_RND': 2}]
cdf_list = annotations.build_cdf_sampling_list(combined_results)
ranked_results = annotations.sample_and_rank_results(cdf_list, [], random_seed=22)
assert ranked_results == expected_results