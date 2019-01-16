import copy
import random
import math

import pandas as pd

import config
from src import helper


#### Helper functions for ranking of results ####
def rank_cleanse_function(result, rank_field_to_update, val_update=[[555, 31]], val_reweight=32):
    """
    :param result: Dictionary for single result (can be from a set of results)
    :param rank_field_to_update: Multiple fields to choose from e.g. ['AVERAGE_RANK_RND', 'WEIGHTED_RANK_RND']
    :param val_update: seq of seqs in template val to find, val to replace with if match found
    :param val_reweight: value to reweight ranks (useful for CDF sampling method), subtracts rank_field from this number,
    for example, if result has BING_RANK of 4 and val_reweight = 32, then reweighted_rank = 32-4 = 28
    :return: dictionary with reweighted rank for CDF
    """
    #TODO: Nothing currently in place to prevent wrong data structure or values for val_update field
    result = copy.copy(result)
    result[rank_field_to_update] = int(result[rank_field_to_update])
    for item in val_update:
        if result[rank_field_to_update] == item[0]:
            result[rank_field_to_update] = item[1]
    result[rank_field_to_update] = val_reweight - result[rank_field_to_update]
    return result


def build_cdf_sampling_list(results, rank_field_to_sort='WEIGHTED_RANK_RND'):
    """
    :param results: a list of results in dictionary template
    :param rank_field_to_sort: For example ['AVERAGE_RANK_RND', 'RANK_BING', 'WEIGHTED_RANK_RND']
    :return: a list containing of length sum of rank_field_to_sort * [result_dict]
    This is used to pass into CDF sampling function to determine final rank of results
    """
    list_for_sampling = []
    for result in results:
        result_list = [result]*result[rank_field_to_sort]
        list_for_sampling.extend(result_list)
    return list_for_sampling


def sample_and_rank_results(cdf_results_list, ranked_results, random_seed=None):
    """
    :param cdf_results_list: output of annotations.build_cdf_sampling_list(results)
    :param ranked_results: list of results, usually initallized with []
    :param random_seed: value to guarantee consistent ranking
    :return: return a ranked list of results using CDF sampling
    """
    # set random seed to guarantee rank order
    if random_seed is not None:
        random.seed(a=random_seed)
    # make copy to prevent mutation
    cdf_results_list = copy.copy(cdf_results_list)
    # make a random choise from cdf results list
    sampled_result = random.choice(cdf_results_list)
    # append ranked results list with the random choice, this is next result in list
    ranked_results.append(sampled_result)
    # get url for sampled result, used to filter out all occurences of this result in cdf sample
    url_sampled_result = sampled_result['URL']
    # filter out all results in cdf sample list matching url
    filtered_cdf_results_list = list(filter(lambda result: result['URL'] != url_sampled_result, cdf_results_list))
    # recursion to build rank results
    if filtered_cdf_results_list == []:
        return ranked_results
    else:
        return sample_and_rank_results(filtered_cdf_results_list, ranked_results, random_seed)



class Results:
    def __init__(self, task_id):
        self.task_id = task_id

    def get_all_results(self):
        """
        :return: dictionary of all web page annotations
        """
        judgements = helper.load_json_from_file(config.JUDGMENTS_PATH)
        return judgements

    def get_task_results(self):
        """
        :return: a list of all web page annotations for given task
        """
        judgements = self.get_all_results()
        results = []
        print(self.task_id)
        for item in judgements.keys():
            if self.task_id == judgements[item]['TASK_ID_FK']:
                results.append(judgements[item])
        # TODO: Need to do a bunch of stuff here to sort and pull out relevant search results
        return results

    def get_sample_of_results(self, results_list, min_percent_correct=.00):
        """
        :param results_list: iterable, usually the output of self.get_task_results()
        :param min_percent_correct: Minimum percentage of results that should be annotated as 'correct'
        :return: Return a filtered list of results
        Provided a minimum threshold of correct results needed from list of correct/incorrect results, using recursion:
        reduce the set of incorrect results until min_percent_correct is achieved
        """
        total_results = len(results_list)
        correct_results = list(filter(lambda x: x['JUDGEMENTS'] == 'Correct', results_list))
        incorrect_results = list(filter(lambda x: x['JUDGEMENTS'] == 'Incorrect', results_list))
        current_percent_correct = len(correct_results) / total_results
        if current_percent_correct > min_percent_correct:
            return results_list
        else:
            # we need to remove X number of incorrect results at random to reach percentage minimum
            incorrect_items_to_sample = len(incorrect_results) - 1
            incorrect_sample = random.sample(incorrect_results, incorrect_items_to_sample)
            updated_results = copy.copy(correct_results)
            updated_results.extend(incorrect_sample)
            return self.get_sample_of_results(updated_results, min_percent_correct)

    def get_ranked_results(self, results, rank_field_to_sort='WEIGHTED_RANK_RND', val_update=[[555, 31]], val_reweight=42,
                           random_seed=None):
        """
        :param results: a list of results in dictionary template, usually json import from annotations folder
        :param rank_field_to_sort: For example ['AVERAGE_RANK_RND', 'RANK_BING', 'WEIGHTED_RANK_RND']
        :param val_update: seq of seqs in template val to find, val to replace with if match found
        :param val_reweight: value to reweight ranks (useful for CDF sampling method), subtracts rank_field from this number,
        for example, if result has BING_RANK of 4 and val_reweight = 32, then reweighted_rank = 32-4 = 28
        :param random_seed: value to guarantee same re-rank of results
        :return: A sorted list of results.... first element contains first result to be displayed
        """
        # clean up results and filter out results
        cleansed_results = map(lambda result:
                               rank_cleanse_function(result, rank_field_to_sort, val_update, val_reweight),
                               results)
        cdf_results_list = build_cdf_sampling_list(cleansed_results, rank_field_to_sort)

        return sample_and_rank_results(cdf_results_list, [], random_seed)

    def merge_results_with_metadata(self, ranked_result_list, lookup_key='BASE_DOMAIN_FK'):
        """
        :param ranked_result_list: list of results in dictionary template, usually output of annotations.rank_cleanse_function
        :param lookup_key: key to lookup and match on url metadata dictionary
        :return: ranked list dictionaries with url metadata included in dictionaries
        """
        url_metadata = helper.load_json_from_file(config.URL_META_DATA)
        output_results = []
        for result in ranked_result_list:
            domain_lookup = result[lookup_key]
            # TODO: This is a short term fix to clean up BASE_DOMAIN_FK field in JUDGMENTS HELPFUL file
            domain_lookup = domain_lookup.replace('www.', '')
            output_results.append({**result, **url_metadata[domain_lookup]})
        return output_results

    def post_process_results(self, post_process_function):
        """
        :param post_process_function: 
        :return: results passed through post_process_function (e.g. statistical analysis for median)
        """
        return None


class Statistics:
    def __init__(self, sequence, target_field):
        """
        :param sequence: A list or list of dictionaries or other list
        :param target_field: If data nested in listed, then mapping to find the target val 
        e.g. key_name or element number of nested tuple
        :return: return a dictionary of basic stats
        """
        target_values = pd.Series(helper.extract_target_values(sequence, target_field))
        self.mean = target_values.mean()
        self.median = target_values.median()
        self.standard_dev = target_values.std()
        self.variance = target_values.var()
        self.lower_quartile = target_values.quantile(q=.25)
        self.upper_quartile = target_values.quantile(q=.75)
        self.IQR = self.upper_quartile - self.lower_quartile
        self.min = target_values.min()
        self.max = target_values.max()

        self.target_field = target_field

    def set_above_median(self, target_dict, key_name_to_test, key_name_result = 'above_median'):
        """
        :param target_dict: Dictionary containing target value for comparision
        :param key_name_to_test: name of key containing target value
        :param key_name_result: key_name where test result is stored
        :return: dictionary with added result e.g. {'target_val': 45, 'above_median':True}
        """
        if target_dict[key_name_to_test] > self.median:
            target_dict[key_name_result] = True
        else:
            target_dict[key_name_result] = False
        return target_dict

    def set_above_mean(self, target_dict, key_name_to_test, key_name_result = 'above_mean'):
        """
        :param target_dict: Dictionary containing target value for comparision
        :param key_name_to_test: name of key containing target value
        :param key_name_result: key_name where test result is stored
        :return: dictionary with added result e.g. {'target_val': 45, 'above_mean':True}
        """
        if target_dict[key_name_to_test] > self.mean:
            target_dict[key_name_result] = True
        else:
            target_dict[key_name_result] = False
        return target_dict

    def set_above_std(self, target_dict, key_name_to_test, key_name_result = 'above_std'):
        """
        :param target_dict: Dictionary containing target value for comparision
        :param key_name_to_test: name of key containing target value
        :param key_name_result: key_name where test result is stored
        :return: dictionary with added result e.g. {'target_val': 45, 'above_std':True}
        """
        if target_dict[key_name_to_test] > (self.mean + self.standard_dev):
            target_dict[key_name_result] = True
        else:
            target_dict[key_name_result] = False
        return target_dict

    def set_above_upper_quartile(self, target_dict, key_name_to_test, key_name_result = 'above_upper_quart'):
        """
        :param target_dict: Dictionary containing target value for comparision
        :param key_name_to_test: name of key containing target value
        :param key_name_result: key_name where test result is stored
        :return: dictionary with added result e.g. {'target_val': 45, 'above_upper_quart':True}
        """
        if target_dict[key_name_to_test] > self.upper_quartile:
            target_dict[key_name_result] = True
        else:
            target_dict[key_name_result] = False
        return target_dict

    def set_tukey_outlier(self, target_dict, key_name_to_test, key_name_result='tukey_outlier'):
        """
        :param target_dict: Dictionary containing target value for comparision
        :param key_name_to_test: name of key containing target value
        :param key_name_result: key_name where test result is stored
        :return: dictionary with added result e.g. {'target_val': 45, 'tukey_outlier':True}
        """
        if target_dict[key_name_to_test] > (self.median + 2.2 * self.IQR):
            target_dict[key_name_result] = True
        elif target_dict[key_name_to_test] < (self.median - 2.2 * self.IQR):
            target_dict[key_name_result] = True
        else:
            target_dict[key_name_result] = False
        return target_dict

    def get_all_statistical_test(self, sequence_of_dicts, key_name_to_test):
        """
        :param sequence_of_dicts: 
        :param key_name_to_test: name of key containing target value
        :return: sequence with all statistical tests added
        SEE: src/analysis/document_threshold_analysis.py for usage example
        """
        for item in sequence_of_dicts:
            #TODO: Consider alternative option to this line below. It is added as a workaround because privacy values
            # in URL_DOMAIN_METADATA.json file are currently saved as strings
            item[key_name_to_test] = float(item[key_name_to_test])
            self.set_above_median(item, key_name_to_test)
            self.set_above_mean(item, key_name_to_test)
            self.set_above_std(item, key_name_to_test)
            self.set_above_upper_quartile(item, key_name_to_test)
            self.set_tukey_outlier(item, key_name_to_test)
        return sequence_of_dicts

