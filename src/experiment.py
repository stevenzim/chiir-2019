import math

from src.crud import participant, resource
from src.template import text, nudge
from src import annotations
from src import helper
import config

# Example to get task payload for participant 'TOOO1'
# from src import task
# a = task.Experiment('T0001')
# results = a.get_task_payload()
# results['interface_details']
# results['participant_state']
# results['cochrane_definitions']
# results['search_results']

# results = results['search_results']


class Experiment:
    def __init__(self, participant_id):
        # participant data necessary for task
        self.participant_id = participant_id
        self.participant = participant.Participant(participant_id)
        self.participant_state = self.participant.read_participant_state(True)  # get participant state details
        self.participant_state_id = self.participant_state['experiment_state']
        self.participant_switch_default = self.participant_state['privacy_switch_default']
        self.participant_random_seed = self.participant_state['random_seed']

        # design data for variant_id that participant is on
        self.design = resource.Design(self.participant_state['variant_id'])

        # experiment state dictionary for current participant state + variant
        self.experiment_state = self.design.get_experiment_state(self.participant_state_id)

        # extracted interface and task id based on participant id --> variant id and state id
        self.task_id = self.experiment_state['task_id']
        self.interface_type = self.experiment_state['interface_type']
        self.interface_name = self.experiment_state['interface_name']
        # self.interface_resource_list = self.experiment_state['interface_resources'].split()

    def get_cochrane_definitions(self):
        """
        :return: Cochrane definitions dictionary
        """
        definitions = helper.load_json_from_file(config.QUESTIONS_AND_DEFINITIONS_PATH)
        return definitions[self.task_id]

    def get_search_results(self):
        search_obj = annotations.Results(self.task_id)
        results = search_obj.get_task_results()
        sampled_results = search_obj.get_sample_of_results(results, min_percent_correct=config.MIN_PERCENT_CORRECT)
        # ranked_results = search_obj.get_ranked_results(sampled_results, random_seed=self.participant_random_seed)
        ranked_results = search_obj.get_ranked_results(sampled_results,
                                                       val_reweight=config.REWEIGHT_VAL,
                                                       random_seed=self.participant_random_seed)
        merged_results = search_obj.merge_results_with_metadata(ranked_results)

        # Do statistical processing
        stats_obj = annotations.Statistics(merged_results, config.PRIVACY_FIELD_NAME)
        stats_tested_results = stats_obj.get_all_statistical_test(merged_results, config.PRIVACY_FIELD_NAME)

        # update results based on inteface_name and default_switch to get correct nudge
        results_for_interface = nudge.update_nudge_for_interface(stats_tested_results,
                                                                 self.participant_switch_default,
                                                                 self.interface_name)

        for val, result in enumerate(results_for_interface):
            result['final_rank'] = val + 1
        return results_for_interface

    def build_pagination_url_strings(self, total_hits, current_results_page):
        '''
        :param total_hits: total number of hits in search results... necessary so pagination does not exceed limits
        :param current_results_page: Current page user is on in results
        :return: list of tuples containing page number and url results string with parameters 
        [(page#, url parameters string), (2, &page_num=2)]
        '''
        RESULTS_URL_STRING = 'results'  # TODO: You might consider putting results link in app params

        max_pages = int(math.ceil(
            total_hits / 10))  # max possible pages in pagination based on total results returned from search engine / 10 results per page
        # current_results_page = int(int(current_page) / 10)  #What page of pagination is user currently viewing???

        # IF current page is 5 or less, then don't shift the page numbers!!!
        if current_results_page <= 5:
            start_results_page = 0
        else:
            start_results_page = int(current_results_page - 5)

        # BUILD PAGINATION LIST -->  Will populate html
        full_pagination_url_list = []
        base_http_get_string = 'experiment?participant_id=' + self.participant_id
        for page_num in range(start_results_page, start_results_page + 10):
            if page_num >= max_pages:
                break
            if page_num == current_results_page:
                full_pagination_url_list.extend([(page_num + 1, base_http_get_string + '&page_num=' + '99999')])
            else:
                full_pagination_url_list.extend([(page_num + 1, base_http_get_string + '&page_num=' + str(page_num ))])
        return full_pagination_url_list

    def produce_results_to_display(self, results, page_num):
        """
        :param results: Finalized list of results that COULD be displayed to user
        :param page_num: Current page number user is requesting
        :return: return only results for page number user has requested (10 max)
        """
        start_result = page_num*10
        if len(results) > (page_num+1) * 10:
            max_end_result = (page_num+1) * 10
        else:
            max_end_result = len(results)
        return results[start_result: max_end_result]

    def get_task_payload(self, page_num=0):
        """
        :param page_num: Pagination of current SERP that user is REQUESTING (default is page 0 for first page).  
        Only necessary for producing payload for SERP.  This is used for pagination, should 
        :return: payload to pass into html form
        """
        payload = {'interface_details': self.experiment_state,
                   'participant_state': self.participant_state,
                   'text': text.text['static'],
                   'max_state_val': config.MAX_EXPERIMENT_STATE,
                   'current_med_question_num': config.MEDICAL_QUESTION_NUM_BY_STATE.get(self.participant_state_id)}

        if self.participant_state_id == 0:
            return payload

        if self.interface_type == 'static':
            return payload

        if self.interface_type == 'decision_pre' or self.interface_type == 'decision_post':
            payload = {**payload, **{'cochrane_definitions': self.get_cochrane_definitions()}}
            return payload

        if self.interface_type == 'decision':
            #TODO: SOMEHOW THE CALL TO GET SEARCH RESULTS IS HAPPENING TWICE.  See output when you turn on printing in nudge
            results_final = self.get_search_results()
            total_results = len(results_final)
            pagination_string_list = self.build_pagination_url_strings(total_results, page_num)
            results_to_display = self.produce_results_to_display(results_final, page_num)
            payload = {**payload, **{'cochrane_definitions': self.get_cochrane_definitions()}}
            payload = {**payload, **{'search_results': results_to_display}}
            payload = {**payload, **{'all_results': results_final}}
            payload = {**payload, **{'total_results': len(results_final)}}
            payload = {**payload, **{'pagination': pagination_string_list}}
            payload = {**payload, **{'page_num': page_num + 1}}
            return payload