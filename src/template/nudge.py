# Contains functions to update search results for appropriate nudge
# See src/analysis/nudge_analysis.py for usage

import config


def nudge_color(seq_of_results):
    """
    :param seq_of_results: results after statistical analysis
    :return: seq_of_results with color information added for nudge form
    """
    text = {'text': 'P', 'text_full': 'Privacy Impact'}
    colors = {'green': {'text_color': 'white', 'circle_color': 'green'},
              'yellow': {'text_color': 'black', 'circle_color': 'yellow'},
              'red': {'text_color': 'white', 'circle_color': 'red'}}
    for result in seq_of_results:
        if result[config.PRIVACY_MARKER_HIGH_CONCERN]:
            result['circles'] = {**text, **colors['red']}
        if result[config.PRIVACY_MARKER_MED_CONCERN] and not result[config.PRIVACY_MARKER_HIGH_CONCERN]:
            result['circles'] = {**text, **colors['yellow']}
        if not result[config.PRIVACY_MARKER_MED_CONCERN]:
            result['circles'] = {**text, **colors['green']}
    return seq_of_results


def nudge_filter(seq_of_results):
    """
    :param seq_of_results: results after statistical analysis
    :return: seq_of_results with results filtered above configurated threshold
    """
    filtered_results = []
    for result in seq_of_results:
        if not result[config.PRIVACY_MARKER_FILTER_BOOL]:
            filtered_results.append(result)
    return filtered_results


def nudge_re_rank(seq_of_results):
    """
    :param seq_of_results: results after statistical analysis
    :return: seq_of_results with results re_ranked with lowest privacy score first
    """
    return sorted(seq_of_results, key=lambda k: k[config.PRIVACY_FIELD_NAME])


def no_nudge(seq_of_results):
    """
    :return: seq_of_results only as this is baseline/control
    """
    return seq_of_results


def update_nudge_for_interface(seq_of_results, participant_switch_defaulted, interface_name):
    """
    :param seq_of_results: results after statistical analysis
    :param participant_switch_defaulted: True if in default position for particular, False if not
    :param interface_name: name of interface associated with current state of participant experiement
    :return: seq_of_results for matching interface and participant default setting
    """
    # Return baseline results (no nudge) for the first 2 cases else return nudge results

    # Case 1) user has shutoff the nudge, we want to go back to basic results
    if (not participant_switch_defaulted) and (interface_name in ['nudge_stoplight', 'nudge_rank', 'nudge_filter']):
        return no_nudge(seq_of_results)

    # Case 2) Always basic results if user in control/baseline
    if interface_name in ['baseline', 'control']:
        return no_nudge(seq_of_results)

    # Remaining cases, then return results for particular nudge interface
    if interface_name == 'nudge_stoplight':
        return nudge_color(seq_of_results)
    if interface_name == 'nudge_rank':
        return nudge_re_rank(seq_of_results)
    if interface_name == 'nudge_filter':
        return nudge_filter(seq_of_results)
