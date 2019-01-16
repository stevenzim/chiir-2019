from src import helper
import config


class Design:
    def __init__(self, variant_id):
        self.experiment_variant = str(variant_id)


    def get_experiment_design(self):
        """
        :return: a dictionary containing the values for self.experiment_variant
        """

        return helper.load_json_from_file(config.EXPERIMENT_VARIANT_FILE).get(self.experiment_variant)

    def get_experiment_state(self, state_id):
        """
        :param state_id: state_id, a sub key of variant_id
        :return: return the dictionary associated with state_id which contains info such as task template name and task id
        """
        design = self.get_experiment_design()
        return design.get(str(state_id))


class Annotation:
    """
    STUB: Consider moving all annotation resource management to here
    """
    def __init__(self):
        self.dummy = None



