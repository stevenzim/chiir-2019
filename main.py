from flask import Flask, render_template, request, redirect, url_for

from src import experiment as exp
from src.template import survey
from src.crud import participant, resource
import config


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def handle_form_survey_data(task_obj):
    """
    :param task_obj: Experiment object initiliazed from src.task with participant_id
    :return: survey_response, form, message
    survey_response = None or Dictionary containing {question key names : participant response values}
    form = None or Form data from src.template.survey to be passed into template
    message = "" or message to be flashed to participant (e.g. YOU NEED TO PROVIDE ANSWERS)
    """
    # Default survey_response
    survey_response = None
    message = ""

    # DETERMINE FORM data (e.g. survey object) based on interface_name
    if task_obj.interface_name == 'survey_instructions':
        form = survey.InstructionsQuiz()
    elif task_obj.interface_name == 'survey_prev_experience':
        form = survey.PreviousSearchForm()
    elif task_obj.interface_name == 'survey_pre_task':
        form = survey.PreTaskForm()
    elif task_obj.interface_name == 'survey_post_task':
        form = survey.PostTaskForm()
    else:
        form = None

    # Validate form if not None and send message if form not validated
    # TODO: Figure out why this form.validate mysteriously still works even though object is not passed in.
    if form is not None:
        if not form.validate_on_submit():
            print("Form not validated ")
            message = "PLEASE ANSWER ALL QUESTIONS"
            return survey_response, form, message

    # DETERMINE FORM data (e.g. survey object) based on interface_name
    # INSTRUCTIONS QUIZ
    if task_obj.interface_name == 'survey_instructions':

        # Users must get both answers correct!  Set to true
        survey_response = {"instruction_decision_question_1": form.decision_question_1.data,
                           "instruction_task_question_1": form.task_question_1.data}
        for key in survey_response.keys():
            if survey_response[key] == '0':
                message = "ONE OR MORE ANSWERS INCORRECT"
                return survey_response, form, message
    # PREVIOUS EXPERIENCE
    elif task_obj.interface_name == 'survey_prev_experience':
        form = survey.PreviousSearchForm()
        survey_response = {"prev_search_question_1": form.prev_search_question_1.data,
                           "prev_search_question_2": form.prev_search_question_2.data}
    # PRE-TASK-SURVEY
    elif task_obj.interface_name == 'survey_pre_task':
        survey_response = {"pre_task_health_question": form.health_question.data,
                           "pre_task_treatment_question": form.treatment_question.data}
    # POST-TASK-SURVEY
    elif task_obj.interface_name == 'survey_post_task':
        survey_response = {"post_task_confidence_question": form.confidence_question.data,
                           "post_task_uncertainty_question": form.uncertainty_question.data}
    # USER NOT IN SURVEY PAGE SO RETURN NONE
    else:
        survey_response = None
    return survey_response, form, message


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Only runs if user goes to URL/login"""
    if request.method == 'POST':
        # TEST that user exist and flash message if they don't
        try:
            user_obj = participant.Participant(request.form.get('participant_id'))
            user_dict = user_obj.read_participant_state(True)
        except Exception as err:
            print(err)
            return render_template('login.html', message='INCORRECT PARTICIPANT ID')

        design_obj = resource.Design(user_obj.variant_id)
        design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

        # logging
        logging_dict = {**user_dict, **design_dict, **{"login_status": "SUCCESSFUL"}}
        user_obj.log_other(logging_dict)

        # Update user state if user state is 0 or 1 (sends them to instruction & quiz page) and log data
        if (user_obj.experiment_state == 0) or (user_obj.experiment_state == 1):
            user_obj.experiment_state = 2  #2 is currently the state for instructions + quiz (we skip instructions only page)
            user_obj.save_participant_state()
            user_dict = user_obj.read_participant_state(True)
            logging_dict = {**user_dict, **design_dict, **{"login_status": "SUCCESSFUL"}}
            user_obj.log_other(logging_dict)

        # redirect and open correct form for current state
        return redirect(url_for('experiment', participant_id=user_obj.participant_id))

    # GET REQUEST
    return render_template('login.html', message="")


@app.route('/experiment', methods=['GET'])
def experiment():
    # This is only used to load forms.  For GET requests, I see no need to record anything but errors

    participant_id = request.args.get('participant_id')
    change_privacy_switch = request.args.get('ps')
    page_num_request = request.args.get('page_num')
    if page_num_request is None:
        page_num_request = 0
    else:
        page_num_request = int(page_num_request)
    print(page_num_request)
    print(participant_id)

    # if the swich is changed then update state and reload page
    if change_privacy_switch == '1':
        print("CHANGE PRIVACY SWITCH")
        user_obj = participant.Participant(participant_id)
        user_dict = user_obj.read_participant_state(True)  # LOAD USER STATE

        design_obj = resource.Design(user_obj.variant_id)
        design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

        privacy_change_dict = {**user_dict, **design_dict, **{'change_privacy_from_current': True}}
        user_obj.log_nudge(privacy_change_dict)

        #Change and save privacy switch setting in participant state
        if user_obj.privacy_switch_default:
            user_obj.privacy_switch_default = False
        else:
            user_obj.privacy_switch_default = True
        user_obj.save_participant_state()

        # RELOAD PAGE (WITH UPDATED PRIVACY SETTINGS)
        return redirect(url_for('experiment', participant_id=user_obj.participant_id))

    # GET PARTICIPANT PAYLOAD
    task_obj = exp.Experiment(participant_id)
    payload = task_obj.get_task_payload(page_num_request)
    print(payload['interface_details'])

    # IF STATE IS LESS THAN 2, send back to login...
    if task_obj.participant_state_id < 2:
        return redirect(url_for('login'))

    # DETERMINE FORM data (e.g. survey object) based on interface_name
    if task_obj.interface_name == 'survey_instructions':
        form = survey.InstructionsQuiz()
    elif task_obj.interface_name == 'survey_prev_experience':
        form = survey.PreviousSearchForm()
    elif task_obj.interface_name == 'survey_pre_task':
        form = survey.PreTaskForm()
    elif task_obj.interface_name == 'survey_post_task':
        form = survey.PostTaskForm()
    else:
        form = None

    # DETERMINE HTML TEMPLATE NAME
    html_template = config.EXPERIMENT_TEMPLATE_LOOK[task_obj.interface_name]

    return render_template(html_template, form=form, payload=payload, message="")


@app.route('/experiment', methods=['POST'])
def experiment_post():
    # This is only used to retrieve data from experiment forms that are posted
    # (these are mainly survey type forms and search resulst pages)
    # And then log data from forms and maintain/update experiement state

    # print(request.__dict__)
    participant_id = request.args.get('participant_id')

    # GET PARTICIPANT PAYLOAD
    task_obj = exp.Experiment(participant_id)
    payload = task_obj.get_task_payload()


    # DETERMINE HTML TEMPLATE NAME
    html_template = config.EXPERIMENT_TEMPLATE_LOOK[task_obj.interface_name]

    # Get/handle form survey data
    survey_data, form, message = handle_form_survey_data(task_obj)

    # reload same form with updated message if message not none:
    if message != "":
        return render_template(html_template, form=form, payload=payload, message=message)

    # Only if Survey complete: log survey data, update state and go to next form
    if survey_data is not None:
        user_obj = participant.Participant(participant_id)
        user_dict = user_obj.read_participant_state(True)  # LOAD USER STATE

        design_obj = resource.Design(user_obj.variant_id)
        design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

        survey_response = {**user_dict, **design_dict, **survey_data}

        # Clean up for post survey logging (i.e. update state)
        if user_obj.log_survey(survey_response) == 'SUCCESS':

            # reset privacy switch to default setting ONLY if experiment state in post_task position
            if user_obj.experiment_state in config.RESET_PRIVACY_SWITCH_STATES:
                user_obj.privacy_switch_default = True
                user_obj.save_participant_state()

            # Increment experiment state by 1
            user_obj.update_experiment_state()

            # save experiment state
            user_obj.save_participant_state()

            # redirect and open correct form for updated state
            return redirect(url_for('experiment', participant_id=user_obj.participant_id))

    # Everything remaining gets handled here:
    return render_template(html_template, form=form, payload=payload, message="")


@app.route('/webpage', methods=['GET', 'POST'])
def webpage():
    """
    Handles the webpage call 
    GET: is when someone clicks on link from results page
    POST: is when someone clicks on "go back" button on the page itself
    """

    # POST HAPPENS WHEN USER CLICKS ON BACK BUTTON TO GO BACK TO RESULTS
    if request.method == 'POST':
        # redirect and open correct form for current state
        participant_id = request.form.get('participant_id')
        page_id = request.form.get('page_id')
        page_rank = request.form.get('page_rank')
        pagination_num = request.form.get('pagination_num')

        # LOG THE CLICK DEPARTURE / PAGE HIT / NOTE DEPARTURE!!!
        # Recording the information below allows for time on page analysis
        click_dict = {'page_id': page_id,
                      'page_rank': page_rank,
                      'pagination_num': pagination_num,
                      'click_type': "departure"}

        user_obj = participant.Participant(participant_id)
        user_dict = user_obj.read_participant_state(True)  # LOAD USER STATE

        design_obj = resource.Design(user_obj.variant_id)
        design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

        click_dict = {**click_dict, **user_dict, **design_dict}

        user_obj.log_click(click_dict)
        return redirect(url_for('experiment', participant_id=user_obj.participant_id, page_num=pagination_num))

    # FOR GET REQUEST
    # Build image path and collect all necessary arguments
    image_path =  'webpage_img/' + request.args.get('name') + ".jpg"
    participant_id = request.args.get('pid')
    page_rank = request.args.get('rank')
    page_id = request.args.get('pg_id') # used for id of specific page user views
    pagination_num = request.args.get('pg_num')  # used for pagination of results

    # LOG THE CLICK ARRIVAL / PAGE HIT / ARRIVAL!!!
    click_dict = {'page_id': page_id,
                  'page_rank': page_rank,
                  'pagination_num': pagination_num,
                  'click_type': "arrival"}

    print(click_dict)

    user_obj = participant.Participant(participant_id)
    user_dict = user_obj.read_participant_state(True)  # LOAD USER STATE

    design_obj = resource.Design(user_obj.variant_id)
    design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

    click_dict = {**click_dict, **user_dict, **design_dict}

    user_obj.log_click(click_dict)

    # PARTICIPANT PAYLOAD AND STATE
    task_obj = exp.Experiment(participant_id)
    payload = task_obj.get_task_payload()

    # SEND CLICK DICT, as the data is used for hidden fields when form is posted
    return render_template('result_page.html', image_path=image_path,
                           payload=payload, message="", click_dict=click_dict)


@app.route('/decision', methods=['GET'])
def decision():
    """
    :return: A rendered template
    This function renders the decision page for current user state.  
    It is called either via button on results page, 
    or when user makes a decision
    """
    # Load payload
    participant_id = request.args.get('participant_id')
    decision = request.args.get('decision')
    task_obj = exp.Experiment(participant_id)
    payload = task_obj.get_task_payload()

    # IF participant id is missing or decision is missing, something fishy...send back to login
    if (participant_id is None) or (decision is None):
        return redirect(url_for('login'))

    # Control for when user clicks button on results page
    if decision == 'makedecision':
        return render_template(config.EXPERIMENT_TEMPLATE_LOOK["decision"],  payload=payload, message="")

    #EVERYTHING GOOD SO FAR SO LOG DECISION AND UPDATE STATE
    user_obj = participant.Participant(participant_id)
    user_dict = user_obj.read_participant_state(True)  # LOAD USER STATE

    design_obj = resource.Design(user_obj.variant_id)
    design_dict = design_obj.get_experiment_state(user_obj.experiment_state)

    decision_dict = {**user_dict, **design_dict, **{'decision': decision}}

    # Only if user decision successfully logged do we update state
    if user_obj.log_decision(decision_dict) == 'SUCCESS':
        user_obj.update_experiment_state()
        user_obj.save_participant_state()
        return redirect(url_for('experiment', participant_id=user_obj.participant_id))
    else:
        raise Exception("DECISION NOT SAVED, REPORT TO ADMINISTRATOR!")




if __name__ == '__main__':
    # app.run(port='4998')
    app.run()
    # app.run(host='0.0.0.0', port='4998')