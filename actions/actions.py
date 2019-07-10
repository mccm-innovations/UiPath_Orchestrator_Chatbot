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
from rasa_sdk.events import SlotSet
from actions.uipath import UiPathAPI
import actions.utils as utils

api = UiPathAPI()


class ActionDefaultFallback(Action):
    def name(self):  # type: () -> Text
        return 'action_default_fallback'
    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        dispatcher.utter_template('utter_msg_not_understood_and_reformulate', tracker)
        return []


'''
-------- ROBOTS --------
'''

class ActionRobotStateCheck(Action):
    def name(self):  # type: () -> Text
        return 'action_robot_state_check'
    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        state = tracker.get_slot('state').lower() if tracker.get_slot('state') else None
        slots = [SlotSet('robot_state_check', state is None or state in api.ROBOT_STATES)]
        if state not in api.ROBOT_STATES:
            slots.append(SlotSet('state', None))
        return slots

class ActionGetRobots(Action):
    def name(self):  # type: () -> Text
        return "action_get_robots"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        state = tracker.get_slot('state')
        robots = api.get_all_robots(reporting_time=utils.calc_reporting_time(), state=state)
        return [SlotSet('robot_list', robots), SlotSet('state', None), SlotSet('robot_state_check', None), SlotSet('empty_result', not bool(robots))]


class ActionGetSummaryOfRobots(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_robots"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        robots = tracker.get_slot('robot_list')
        out_msg = 'Robots not found' if not robots else ''
        for idx, robot in enumerate(robots):
            name = robot.get('Robot').get('Name')
            state = robot.get('State')
            out_msg += '{}. The robot **{}** is in the state **{}**. \n'.format(idx, name, state)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetNumberOfRobots(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_robots"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        robots = tracker.get_slot('robot_list')
        num_robots = len(robots)
        dispatcher.utter_message("Number of robots: {}".format(num_robots))
        return []

class ActionGetRobotByListIdx(Action):
    def name(self):  # type: () -> Text
        return "action_robot_by_list_idx"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        robot_idx = utils.get_number_from_tracked_entities(entities)
        robots = tracker.get_slot('robot_list')
        try:
            robot = robots[robot_idx]
            out_msg = utils.dict_to_markdown(robot)
        except IndexError:
            out_msg = 'Robot not found'
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
        robot_name = tracker.get_slot('robot_name')
        robot = api.get_robot_by_name(name=robot_name, reporting_time=utils.calc_reporting_time())
        out_msg = 'Robot not found'
        if robot:
            out_msg = utils.dict_to_markdown(robot)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetLastRobot(Action):
    def name(self):  # type: () -> Text
        return "action_get_last_robot"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        robots = tracker.get_slot('robot_list')
        try:
            robot = robots[0]
            out_msg = utils.dict_to_markdown(robot)
        except IndexError:
            out_msg = 'Robot not found'
        dispatcher.utter_message(out_msg)
        return []

'''
-------- JOBS --------
'''

class ActionJobStateCheck(Action):
    def name(self):  # type: () -> Text
        return 'action_job_state_check'
    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        state = tracker.get_slot('state').lower() if tracker.get_slot('state') else None
        slots = [SlotSet('job_state_check', state is None or state in api.JOB_STATES)]
        if state not in api.JOB_STATES:
            slots.append(SlotSet('state', None))
        return slots

class ActionGetJobs(Action):
    def name(self):  # type: () -> Text
        return "action_get_jobs"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        state = tracker.get_slot('state')
        start_time, end_time = utils.get_time_from_tracked_entities(entities)
        count = utils.get_number_from_tracked_entities(entities)
        jobs = api.get_all_jobs(start_time_from=start_time, start_time_to=end_time, state=state, count=count)
        return [SlotSet('job_list', jobs), SlotSet('state', None), SlotSet('job_state_check', None), SlotSet('empty_result', not bool(jobs))]


class ActionGetSummaryOfJobs(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_jobs"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        jobs = tracker.get_slot('job_list')
        out_msg = 'Jobs not found' if not jobs else ''
        for idx, job in enumerate(jobs):
            name = job.get('ReleaseName')
            start_time = job.get('StartTime')
            end_time = job.get('EndTime')
            state = job.get('State')
            out_msg += '{}. The job **{}** started **{}** and finished **{}** with the state **{}**. '.format(idx, name, utils.format_datetime(start_time), utils.format_datetime(end_time), state)
            out_msg += '\n'
        dispatcher.utter_message(out_msg)
        return []


class ActionGetNumberOfJobs(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_jobs"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        jobs = tracker.get_slot('job_list')
        num_jobs = len(jobs)
        dispatcher.utter_message("Number of jobs: {}".format(num_jobs))
        return []


class ActionGetJobByListIdx(Action):
    def name(self):  # type: () -> Text
        return "action_job_by_list_idx"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        job_idx = utils.get_number_from_tracked_entities(entities)
        jobs = tracker.get_slot('job_list')
        try:
            job = jobs[job_idx]
            out_msg = utils.dict_to_markdown(job)
        except IndexError:
            out_msg = 'Job not found'
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
        job_name = tracker.get_slot('job_name')
        job = api.get_job_by_name(name=job_name)
        out_msg = 'Job not found'
        if job:
            out_msg = utils.dict_to_markdown(job)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetLastJob(Action):
    def name(self):  # type: () -> Text
        return "action_get_last_job"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        jobs = tracker.get_slot('job_list')
        try:
            job = jobs[0]
            out_msg = utils.dict_to_markdown(job)
        except IndexError:
            out_msg = 'Job not found'
        dispatcher.utter_message(out_msg)
        return []


'''
-------- ASSETS --------
'''

class ActionGetAssets(Action):
    def name(self):  # type: () -> Text
        return "action_get_assets"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        assets = api.get_all_assets()
        return [SlotSet('asset_list', assets), SlotSet('empty_result', not bool(assets))]


class ActionGetSummaryOfAssets(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_assets"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        assets = tracker.get_slot('asset_list')
        out_msg = 'Assets not found' if not assets else ''
        for idx, asset in enumerate(assets):
            name = asset.get('Name')
            # robot_values = asset.get('RobotValues')
            value_scope = asset.get('ValueScope')
            value_type = asset.get('ValueType')
            value = asset.get('Value')
            out_msg += '{}. The asset **{}** with scope **{}** and type **{}** has the value **{}**. \n'.format(idx, name, value_scope, value_type, value)
        dispatcher.utter_message(out_msg)
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
        assets = tracker.get_slot('asset_list')
        num_assets = len(assets)
        dispatcher.utter_message("Number of assets: {}".format(num_assets))
        return []


class ActionGetAssetByListIdx(Action):
    def name(self):  # type: () -> Text
        return "action_asset_by_list_idx"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        asset_idx = utils.get_number_from_tracked_entities(entities)
        assets = tracker.get_slot('asset_list')
        try:
            asset = assets[asset_idx]
            out_msg = utils.dict_to_markdown(asset)
        except IndexError:
            out_msg = 'Asset not found'
        dispatcher.utter_message(out_msg)
        return []

class ActionGetAssetByName(Action):
    def name(self):  # type: () -> Text
        return "action_asset_by_name"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        asset_name = tracker.get_slot('asset_name')
        asset = api.get_asset_by_name(name=asset_name)
        out_msg = 'Asset not found'
        if asset:
            out_msg = utils.dict_to_markdown(asset)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetLastAsset(Action):
    def name(self):  # type: () -> Text
        return "action_get_last_asset"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        assets = tracker.get_slot('asset_list')
        try:
            asset = assets[0]
            out_msg = utils.dict_to_markdown(asset)
        except IndexError:
            out_msg = 'Asset not found'
        dispatcher.utter_message(out_msg)
        return []

'''
-------- QUEUES --------
'''

class ActionGetQueues(Action):
    def name(self):  # type: () -> Text
        return "action_get_queues"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        start_time, end_time = utils.get_time_from_tracked_entities(entities)
        queues = api.get_all_queues(creation_time_from=start_time, creation_time_to=end_time)
        return [SlotSet('queue_list', queues), SlotSet('empty_result', not bool(queues))]


class ActionGetSummaryOfQueues(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_queues"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        queues = tracker.get_slot('queue_list')
        out_msg = 'Queues not found' if not queues else ''
        for idx, queue in enumerate(queues):
            name = queue.get('Name')
            creation_time = queue.get('CreationTime')
            items_to_process = queue.get('ProcessingStatus').get('ItemsToProcess')
            successful_transactions = queue.get('ProcessingStatus').get('SuccessfulTransactionsNo')
            out_msg += '{}. The queue **{}** was created **{}** and there are **{}** remaining items and **{}** successful transactions. \n'.format(idx, name, utils.format_datetime(creation_time), items_to_process, successful_transactions)
        dispatcher.utter_message(out_msg)
        return []


class ActionGetNumberOfQueues(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_queues"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        queues = tracker.get_slot('queue_list')
        num_queues = len(queues)
        dispatcher.utter_message("Number of queues: {}".format(num_queues))
        return []


class ActionGetQueueByListIdx(Action):
    def name(self):  # type: () -> Text
        return "action_queue_by_list_idx"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        queue_idx = utils.get_number_from_tracked_entities(entities)
        queues = tracker.get_slot('queue_list')
        try:
            queue = queues[queue_idx]
            out_msg = utils.dict_to_markdown(queue)
        except IndexError:
            out_msg = 'Queue not found'
        dispatcher.utter_message(out_msg)
        return []

class ActionGetQueueByName(Action):
    def name(self):  # type: () -> Text
        return "action_queue_by_name"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        queue_name = tracker.get_slot('queue_name')
        queue = api.get_queue_by_name(name=queue_name)
        out_msg = 'Queue not found'
        if queue:
            out_msg = utils.dict_to_markdown(queue)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetLastQueue(Action):
    def name(self):  # type: () -> Text
        return "action_get_last_queue"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        queues = tracker.get_slot('queue_list')
        try:
            queue = queues[0]
            out_msg = utils.dict_to_markdown(queue)
        except IndexError:
            out_msg = 'Queue not found'
        dispatcher.utter_message(out_msg)
        return []


'''
-------- PROCESSES --------
'''


class ActionGetProcesses(Action):
    def name(self):  # type: () -> Text
        return "action_get_processes"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        start_time, end_time = utils.get_time_from_tracked_entities(entities)
        processes = api.get_all_processes(published_from=start_time, published_to=end_time)
        return [SlotSet('process_list', processes), SlotSet('empty_result', not bool(processes))]


class ActionGetSummaryOfProcesses(Action):
    def name(self):  # type: () -> Text
        return "action_summary_of_processes"

    def run(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
        ):  # type: (...) -> List[Dict[Text, Any]]
        processes = tracker.get_slot('process_list')
        out_msg = 'Processes not found' if not processes else ''
        for idx, process in enumerate(processes):
            name = process.get('Id')
            published_time = process.get('Published')
            out_msg += '{}. The process **{}** was published **{}**. \n'.format(idx, name, utils.format_datetime(published_time))
        dispatcher.utter_message(out_msg)
        return []


class ActionGetNumberOfProcesses(Action):
    def name(self):  # type: () -> Text
        return "action_number_of_processes"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        processes = tracker.get_slot('process_list')
        num_processes = len(processes)
        dispatcher.utter_message("Number of processes: {}".format(num_processes))
        return []


class ActionGetProcessByListIdx(Action):
    def name(self):  # type: () -> Text
        return "action_process_by_list_idx"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        entities = tracker.latest_message['entities']
        process_idx = utils.get_number_from_tracked_entities(entities)
        processes = tracker.get_slot('process_list')
        try:
            process = processes[process_idx]
            out_msg = utils.dict_to_markdown(process)
        except IndexError:
            out_msg = 'Process not found'
        dispatcher.utter_message(out_msg)
        return []

class ActionGetProcessByName(Action):
    def name(self):  # type: () -> Text
        return "action_process_by_name"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        process_name = tracker.get_slot('process_name')
        process = api.get_process_by_id(id=process_name)
        out_msg = 'Process not found'
        if process:
            out_msg = utils.dict_to_markdown(process)
        dispatcher.utter_message(out_msg)
        return []

class ActionGetLastProcess(Action):
    def name(self):  # type: () -> Text
        return "action_get_last_process"

    def run(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type:  Dict[Text, Any]
    ):  # type: (...) -> List[Dict[Text, Any]]
        processes = tracker.get_slot('process_list')
        try:
            process = processes[0]
            out_msg = utils.dict_to_markdown(process)
        except IndexError:
            out_msg = 'Process not found'
        dispatcher.utter_message(out_msg)
        return []
