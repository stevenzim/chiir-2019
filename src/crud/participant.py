import os

from src import helper
import config




def create_particpant_directory(participant_id, partipant_path, participant_subfolders_dict):
    '''
    :param participant_id: string that will name folder (e.g. 0004)
    :param partipant_path: path where folder will be recreated
    :param participant_subfolders_dict: A config dictionary containing subfolder details necessary for participant data
    :return: message
    Creates directories that capture interactive experiment data
    '''
    try:
        new_participant_path = partipant_path + "/" + participant_id
        if not os.path.exists(new_participant_path):
            os.makedirs(new_participant_path)
            for key in participant_subfolders_dict.keys():
                new_participant_subfolder = new_participant_path + "/" + participant_subfolders_dict[key][0]
                os.makedirs(new_participant_subfolder)
            return "PARTICIPANT DIRECTORY CREATED FOR " + participant_id
        else:
            raise Exception("PARTICIPANT ALREADY EXISTS!")
    except OSError as err:
        print("OS error: {0}".format(err))
    except:
        raise


class Participant:
    """Used to perform CRUD operations on participant data"""
    def __init__(self, participant_id,
                 variant_id=None,
                 qualtrics_link=None,
                 random_seed=None,
                 privacy_switch_default=True):

        # required for class
        self.participant_id = participant_id

        # necessary for creating new participant
        self.variant_id = variant_id
        self.qualtrics_link = qualtrics_link

        # control file paths
        self.participant_path = config.PARTICIPANT_PATH + "/" + self.participant_id
        self.participant_state_file_path = self.participant_path + "/" + config.PARTICIPANT_STATE_FILE_NAME

        # attributes only after creation of participant
        self.experiment_state = None
        self.time_created = None
        self.time_updated = None

        # nudge / privacy switch
        self.privacy_switch_default = privacy_switch_default  #Default is True, but if user switches, you should to store this

        #random seed
        self.random_seed = random_seed

    def save_participant_state(self):
        """dumps state of participant to file"""
        participant_state_dict = {'participant_id': self.participant_id,
                                  'variant_id': self.variant_id,
                                  'experiment_state': self.experiment_state,
                                  'qualtrics_link': self.qualtrics_link,
                                  'time_created': self.time_created,
                                  'time_updated': self.time_updated,
                                  'privacy_switch_default': self.privacy_switch_default,
                                  'random_seed': self.random_seed}
        helper.dump_json_to_file(self.participant_state_file_path, participant_state_dict)
        return "participant state SAVED for " + self.participant_id

    def create_new_participant(self):
        #TODO? You may want to add a test for None type on self.variant_id and self.qualtrics_link
        """This should not run if participant folder already exists, it should throw error"""
        try:
            create_particpant_directory(self.participant_id, config.PARTICIPANT_PATH, config.PARTICIPANT_SUBFOLDERS)
        except OSError as err:
            print("OS error: {0}".format(err))

        # intialize variables for creation
        self.experiment_state = 0
        self.time_created = helper.get_time_stamp()
        self.time_updated = helper.get_time_stamp()

        # create participant state file
        self.save_participant_state()
        return "participant state CREATED for " + self.participant_id

    def read_participant_state(self, return_dictionary=False):
        """Sets attributes to current values in state file"""
        participant_state_dict = helper.load_json_from_file(self.participant_state_file_path)

        if self.participant_id != participant_state_dict['participant_id']:
            raise Exception("PARTICIPANT ID passed into object does not match ID in state file!")

        # necessary for creating new participant
        self.variant_id = participant_state_dict['variant_id']
        self.qualtrics_link = participant_state_dict['qualtrics_link']

        # attributes only after creation of participant
        self.experiment_state = participant_state_dict['experiment_state']
        self.time_created = participant_state_dict['time_created']
        self.time_updated = participant_state_dict['time_updated']


        self.privacy_switch_default = participant_state_dict['privacy_switch_default']
        self.random_seed = participant_state_dict['random_seed']

        if return_dictionary:
            return participant_state_dict
        else:
            return "participant state LOADED for " + self.participant_id

    def update_experiment_state(self):
        """Increments the experimental state by 1.  Only done after successfully logging decisions and surveys"""
        self.read_participant_state()
        self.experiment_state += 1
        self.time_updated = helper.get_time_stamp()
        return "PARTICIPANT STATE UPDATED FOR " + self.participant_id

    ##########   PARTICIPANT LOGGING ###################
    #TODO: You might consider putting all of this elsewhere
    def log_generic(self, generic_dict, config_logging_key):
        """
        HELPER function to take an arbitrary dictionary to be logged
        :param generic_dict: dictionary containing data to be logged
        :param config_logging_key: key name from config.PARTICIPANT_SUBFOLDERS e.g. "SURVEY"
        :return: ????
        """
        # Logging of survey results
        uuid = {'uuid': helper.get_uuid()}
        time_logged = {'time_logged': helper.get_time_stamp()}
        logging_dict = {**generic_dict, **time_logged, **uuid}
        log_type = config.PARTICIPANT_SUBFOLDERS[config_logging_key][0]
        logging_dict = {**logging_dict, **{'log_type':log_type}}

        # Remove unnecessary keys
        for key in config.LOGGING_KEYS_TO_REMOVE.keys():
            logging_dict.pop(key, None)

        # create f_path of format e.g. 0001/survey/survey_0001_5676053a-8ba5-444a-aea0-bc6a805bd50d.
        file_path = self.participant_path + "/" + log_type + "/" + log_type + "_" + \
                    self.participant_id + "_" + uuid.get('uuid') + ".json"

        #TODO: Need to change this so it does NOT pretty print
        helper.dump_json_to_file(file_path, logging_dict)
        return "SUCCESS"

    def log_click(self, click_dict={'page_type':'results_page', 'rank': 3, 'result_page_num': 1, 'nudge_state':'Off', 'click_type':'back_button'}):
        "logs any clicks made by user (in results and document pages)"
        try:
            self.log_generic(click_dict, "CLICKS")
            return "SUCCESS"
        except:
            raise Exception("CLICK DATA NOT SAVED!!!")

    def log_survey(self, survey_dict):
        # Logging of survey results
        try:
            self.log_generic(survey_dict, "SURVEY")
            return "SUCCESS"
        except:
            raise Exception("USER SURVEY DATA NOT SAVED!!!")

    def log_decision(self, decision_dict):
        try:
            self.log_generic(decision_dict, "DECISIONS")
            return "SUCCESS"
        except:
            raise Exception("USER DECISION NOT SAVED!!!")

    def log_nudge(self, nudge_dict):
        try:
            self.log_generic(nudge_dict, "NUDGE_STATUS")
            return "SUCCESS"
        except:
            raise Exception("DEFAULT NUDGE SWITCH DATA NOT SAVED!!!")

    def log_error(self, error_dict):
        try:
            self.log_generic(error_dict, "ERRORS")
            return "SUCCESS"
        except:
            raise Exception("ERROR DATA NOT SAVED!!!")

    def log_other(self, message_dict):
        try:
            self.log_generic(message_dict, "OTHER")
            return "SUCCESS"
        except:
            raise Exception("LOGIN OR OTHER DATA NOT SAVED!!!")