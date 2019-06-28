import requests
# from dotenv import load_dotenv
import os
import json
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set logger
logger_format = '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO, format=logger_format)
logger = logging.getLogger('UiPathAPI')
# create file handler which logs even debug messages
fh = logging.FileHandler('UiPathAPI.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(logger_format)
logger.addHandler(fh)


class UiPathAPI:

    JOB_STATES = ['pending', 'running', 'successful', 'faulted', 'stopping', 'terminating', 'stopped']
    ROBOT_STATES = ['available', 'busy', 'unresponsive', 'disconnected']

    def __init__(self):
        # load_dotenv()
        self.host = os.getenv('HOST')
        self.token = None
        self.headers = {
            'Content-Type': "application/json",
        }

    def authenticate(self):
        logger.info('Calling authenticate method...')
        url = self.host + '/api/Account/Authenticate'
        payload = {
            'tenancyName': os.getenv('TENANCY_NAME'),
            'usernameOrEmailAddress': os.getenv('USERNAME_OR_EMAIL_ADDRESS'),
            'password': os.getenv('PASSWORD')
        }

        response = requests.request("POST", url, data=json.dumps(payload), headers=self.headers, verify=False).json()
        if response.get('success'):
            logger.info('User authenticated')
            self.token = response.get('result')
            self.headers['Authorization'] = 'Bearer {}'.format(self.token)

    def make_request(self, url, payload, method='GET'):
        response = requests.request(method, url, params=payload, headers=self.headers, verify=False).json()
        if 'error' in response and response['error']['code'] == 0:
            self.authenticate()
            response = requests.request("GET", url, params=payload, headers=self.headers, verify=False).json()
        return response.get('value')

    def get_logs(self, filter_key, filter_value):
        url = self.host + '/odata/RobotLogs'
        payload = {
            "$top": "5",
            "$filter": "{} eq {}".format(filter_key, filter_value)
        }
        logs = self.make_request(url, payload)
        log_messages = []
        if logs:
            log_messages = [x.get('Message') for x in logs]
        return log_messages

    def get_all_sessions(self):
        logger.info('Calling get_all_sessions method...')
        url = self.host + '/odata/Sessions'
        sessions = self.make_request(url, None)
        logger.info('Returning sessions')
        return sessions

    def get_all_robots(self, reporting_time=None, state=None):
        logger.info('Calling get_all_robots method...')
        url = self.host + '/odata/Sessions'
        payload = {
            '$select': 'State',
            '$expand': 'Robot'
        }
        output_list = []
        # Get full list of robots
        full_list = self.make_request(url, payload)
        logger.info('[get_all_robots] Filtering robots by ReportingTime = {} and State  = {}'.format(reporting_time, state))
        # Get list filtered by Reporting Time
        payload['$filter'] = 'ReportingTime gt {}'.format(reporting_time)
        filtered_list = self.make_request(url, payload)
        # Get IDs of robots that are responsive
        responsive_robot_ids = []
        if filtered_list:
            responsive_robot_ids = [x['Robot']['Id'] for x in filtered_list]
        # Set real state to robots within the full list
        for robot in full_list:
            if robot['Robot']['Id'] not in responsive_robot_ids:
                robot['State'] = 'Unresponsive'
            if (state is not None and robot['State'].lower() == state) or state is None:
                log_messages = self.get_logs('RobotName', "'{}'".format(robot['Robot']['Name']))
                robot['Logs'] = log_messages
                output_list.append(robot)
        logger.info('Returning robots')
        return output_list

    def get_robot_by_name(self, name, reporting_time):
        logger.info('Calling get_robot_by_name method...')
        url = self.host + '/odata/Sessions'
        payload = {
            '$select': 'State',
            '$expand': 'Robot',
            '$top': '1',
            '$filter': "Robot/Name eq '{}'".format(name)
        }
        robot = None
        robots = self.make_request(url, payload)
        if robots:
            robot = robots[0]
            # Filter by reporting time to check whether it is unresponsive or not
            payload['$filter'] = payload['$filter'] + ' and ReportingTime gt {}'.format(reporting_time)
            filtered_robot = self.make_request(url, payload)
            if not filtered_robot: # empty list, so it is unresponsive
                robot['State'] = 'Unresponsive'
            log_messages = self.get_logs('RobotName', "'{}'".format(robot['Robot']['Name']))
            robot['Logs'] = log_messages
            logger.info('Returning robot info with name: {}'.format(name))
        else:
            logger.info('Robot with name [{}] not found'.format(name))
        return robot

    def get_all_jobs(self, start_time_from=None, start_time_to=None, end_time_from=None, end_time_to=None, state=None, count=None):
        logger.info('Calling get_all_jobs method...')
        url = self.host + '/odata/Jobs'
        filter_clauses = []
        if start_time_from: filter_clauses.append('StartTime gt {}'.format(start_time_from))
        if start_time_to: filter_clauses.append('StartTime lt {}'.format(start_time_to))
        if end_time_from: filter_clauses.append('EndTime gt {}'.format(end_time_from))
        if end_time_to: filter_clauses.append('EndTime lt {}'.format(end_time_to))
        if state: filter_clauses.append("State eq '{}'".format(state.title()))
        payload = {}
        if filter_clauses:
            filter_clause = ' and '.join(filter_clauses)
            payload['$filter'] = filter_clause
            logger.info('[get_all_jobs] Filter clause = {}'.format(filter_clause))
        if count: payload['$top'] = count
        jobs = self.make_request(url, payload)
        for job in jobs:
            job_key = job.get('Key')
            log_messages = self.get_logs('JobKey', job_key)
            job['Logs'] = log_messages
        logger.info('Returning jobs')
        return jobs

    def get_job_by_name(self, name):
        logger.info('Calling get_job_by_name method...')
        url = self.host + '/odata/Jobs'
        payload = {
            '$top': '1',
            '$filter': "ReleaseName eq '{}'".format(name)
        }
        job = None
        jobs = self.make_request(url, payload)
        if jobs:
            job = jobs[0]
            job_key = job.get('Key')
            log_messages = self.get_logs('JobKey', job_key)
            job['Logs'] = log_messages
            logger.info('Returning job info with name: {}'.format(name))
        else:
            logger.info('Job with name [{}] not found'.format(name))
        return job

    def get_all_assets(self):
        logger.info('Calling get_all_assets method...')
        url = self.host + '/odata/Assets'
        payload = {
            '$expand': 'RobotValues'
        }
        assets = self.make_request(url, payload)
        logger.info('Returning assets')
        return assets

    def get_asset_by_name(self, name):
        logger.info('Calling get_asset_by_name method...')
        url = self.host + '/odata/Assets'
        payload = {
            '$top': '1',
            '$filter': "Name eq '{}'".format(name)
        }
        asset = None
        assets = self.make_request(url, payload)
        if assets:
            asset = assets[0]
            logger.info('Returning asset info with name: {}'.format(name))
        else:
            logger.info('Asset with name [{}] not found'.format(name))
        return asset

    def get_all_queues(self, creation_time_from=None, creation_time_to=None):
        logger.info('Calling get_all_queues method...')
        url = self.host + '/odata/QueueDefinitions'
        filter_clauses = []
        if creation_time_from: filter_clauses.append('CreationTime gt {}'.format(creation_time_from))
        if creation_time_to: filter_clauses.append('CreationTime lt {}'.format(creation_time_to))
        payload = {}
        if filter_clauses:
            filter_clause = ' and '.join(filter_clauses)
            payload['$filter'] = filter_clause
            logger.info('[get_all_queues] Filter clause = {}'.format(filter_clause))
        queues = self.make_request(url, payload)
        processing_status_url = self.host + '/odata/QueueProcessingRecords/UiPathODataSvc.RetrieveQueuesProcessingStatus'
        for queue in queues:
            name = queue.get('Name')
            payload = {"$filter": "QueueDefinitionName eq '{}'".format(name)}
            processing_status = self.make_request(processing_status_url, payload)[0]
            queue['ProcessingStatus'] = processing_status
        logger.info('Returning queues')
        return queues

    def get_queue_by_name(self, name):
        logger.info('Calling get_queue_by_name method...')
        url = self.host + '/odata/QueueDefinitions'
        payload = {
            '$top': '1',
            '$filter': "Name eq '{}'".format(name)
        }
        queues = self.make_request(url, payload)
        queue = None
        if queues:
            queue = queues[0]
            processing_status_url = self.host + '/odata/QueueProcessingRecords/UiPathODataSvc.RetrieveQueuesProcessingStatus'
            payload = {"$filter": "QueueDefinitionName eq '{}'".format(name)}
            processing_status = self.make_request(processing_status_url, payload)[0]
            queue['ProcessingStatus'] = processing_status
            logger.info('Returning queue info with name: {}'.format(name))
        else:
            logger.info('Queue with name [{}] not found'.format(name))
        return queue

    def get_all_processes(self, published_from=None, published_to=None):
        logger.info('Calling get_all_processes method...')
        url = self.host + '/odata/Processes'
        filter_clauses = []
        if published_from: filter_clauses.append('Published gt {}'.format(published_from))
        if published_to: filter_clauses.append('Published lt {}'.format(published_to))
        payload = {}
        if filter_clauses:
            filter_clause = ' and '.join(filter_clauses)
            payload['$filter'] = filter_clause
            logger.info('[get_all_processes] Filter clause = {}'.format(filter_clause))
        processes = self.make_request(url, payload)
        for process in processes:
            log_messages = self.get_logs('ProcessName', "'{}'".format(process.get('Id')))
            process['Logs'] = log_messages
        logger.info('Returning processes')
        return processes

    def get_process_by_id(self, id):
        logger.info('Calling get_process_by_id method...')
        url = self.host + '/odata/Processes'
        payload = {
            '$top': '1',
            '$filter': "Id eq '{}'".format(id)
        }
        process = None
        processes = self.make_request(url, payload)
        if processes:
            process = processes[0]
            log_messages = self.get_logs('ProcessName', "'{}'".format(process.get('Id')))
            process['Logs'] = log_messages
            logger.info('Returning process info with name: {}'.format(id))
        else:
            logger.info('Process with name [{}] not found'.format(id))
        return process
