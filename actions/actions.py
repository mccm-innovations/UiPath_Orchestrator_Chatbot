# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import dateutil
import datetime
from actions.uipath import UiPathAPI


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")

        return []


class ActionJoke(Action):
    def name(self):  # type: () -> Text
        return "action_joke"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        request = requests.get('http://api.icndb.com/jokes/random').json()
        joke = request['value']['joke']
        dispatcher.utter_message(joke)
        return []


class ActionGetNumberOfAssets(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_assets"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        number_of_assets = len(api.get_all_assets())
        dispatcher.utter_message('Number of assets = {}'.format(number_of_assets))
        return []


class ActionGetNumberOfJobsInState(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_jobs_in_state"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        job_status = tracker.get_slot('job_status')
        jobs_data = api.get_all_jobs()
        counter = len([x for x in jobs_data if x['State'].lower() == job_status])
        dispatcher.utter_message('Number of jobs with state {} = {}'.format(job_status, counter))
        return []


class ActionGetNumberOfRobotsInState(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_robots_in_state"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        robot_status = tracker.get_slot('robot_status')
        robots_data = api.get_all_robots()
        counter = len([x for x in robots_data if x['State'].lower() == robot_status])
        dispatcher.utter_message('Number of robots with state {} = {}'.format(robot_status, counter))
        return []


class ActionGetSummaryOfJobs(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_jobs"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        entities = tracker.latest_message['entities']
        job_status = tracker.get_slot('job_status')
        print(job_status)
        start_time, end_time = _get_time_from_tracked_entities(entities)
        print(start_time, end_time)
        jobs_data = api.get_all_jobs(start_time_from=start_time, start_time_to=end_time, status=job_status)
        out_msg = ''
        for job in jobs_data:
            name = job.get('ReleaseName')
            start_time = job.get('StartTime')
            end_time = job.get('EndTime')
            state = job.get('State')
            out_msg += 'The job [{}] started at [{}] and finished at [{}] with the state [{}] \n'.format(name, start_time, end_time, state)
        if not out_msg:
            out_msg = '0 jobs found'
        dispatcher.utter_message(out_msg)
        return []


def _get_time_from_tracked_entities(entities):
    start_time = None
    end_time = None
    for entity in entities:
        if entity['entity'] == 'time' and entity['extractor'] == 'DucklingHTTPExtractor' and entity['value']['from']:
            start_time = entity['value']['from']
            end_time = entity['value']['to']
            break
        elif entity['entity'] == 'time' and entity['extractor'] == 'DucklingHTTPExtractor':
            start_time = entity['value']
            start_time_datetime = dateutil.parser.parse(start_time)
            end_time_datetime = start_time_datetime + datetime.timedelta(days=1)
            end_time = end_time_datetime.isoformat()
            break
    if start_time: start_time = start_time.replace('+02:00', 'Z')
    if end_time: end_time = end_time.replace('+02:00', 'Z')
    return start_time, end_time


