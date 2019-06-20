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
import json
from actions.uipath import UiPathAPI


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


class ActionGetSummaryOfRobots(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_robots"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        entities = tracker.latest_message['entities']
        start_time, end_time = _get_time_from_tracked_entities(entities)
        robot_state = tracker.get_slot('robot_state')
        robots_data = api.get_all_robots(reporting_time_from=start_time, reporting_time_to=end_time, state=robot_state)
        out_msg = ''
        for robot in robots_data:
            name = robot.get('Robot').get('Name')
            state = robot.get('State')
            reporting_time = robot.get('Robot').get('ReportingTime')
            out_msg += 'The robot [{}] is in the state [{}] and its reporting time is [{}] \n'.format(name, state, reporting_time)
        if not out_msg:
            out_msg = '0 robots found'
        dispatcher.utter_message(out_msg)
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
        job_state = tracker.get_slot('job_state')
        start_time, end_time = _get_time_from_tracked_entities(entities)
        jobs_data = api.get_all_jobs(start_time_from=start_time, start_time_to=end_time, state=job_state)
        out_msg = ''
        for job in jobs_data:
            name = job.get('ReleaseName')
            start_time = job.get('StartTime')
            end_time = job.get('EndTime')
            state = job.get('State')
            info = job.get('Info')
            out_msg += 'The job [{}] started at [{}] and finished at [{}] with the state [{}]. '.format(name, start_time, end_time, state)
            # if state == 'Faulted':
            #     out_msg += 'The error was [{}]'.format(info)
            out_msg += '\n'
        if not out_msg:
            out_msg = '0 jobs found'
        dispatcher.utter_message(out_msg)
        return []


class ActionGetSummaryOfQueues(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_queues"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        entities = tracker.latest_message['entities']
        start_time, end_time = _get_time_from_tracked_entities(entities)
        queues_data = api.get_all_queues(creation_time_from=start_time, creation_time_to=end_time)
        out_msg = ''
        for queue in queues_data:
            name = queue.get('Name')
            creation_time = queue.get('CreationTime')
            out_msg += 'The queue [{}] was created at [{}] \n'.format(name, creation_time)
        if not out_msg:
            out_msg = '0 queues found'
        dispatcher.utter_message(out_msg)
        return []


class ActionGetJobByName(Action):
    def name(self):  # type: () -> Text
        return "action_job_by_name"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        job_name = tracker.get_slot('job_name')
        job_data = api.get_job_by_name(name=job_name)
        out_msg = 'Job not found'
        if job_data:
            job = job_data[0]
            out_msg = json.dumps(job)
        dispatcher.utter_message(out_msg)
        return []


class ActionGetRobotByName(Action):
    def name(self):  # type: () -> Text
        return "action_robot_by_name"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        api = UiPathAPI()
        robot_name = tracker.get_slot('robot_name')
        robot_data = api.get_robot_by_name(name=robot_name)
        out_msg = 'Robot not found'
        if robot_data:
            robot = robot_data[0]
            out_msg = json.dumps(robot)
        dispatcher.utter_message(out_msg)
        return []



