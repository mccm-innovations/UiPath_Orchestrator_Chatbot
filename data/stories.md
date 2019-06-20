## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - action_joke
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - action_joke
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye
  
## request summary of queues
* request_summary_of_queues
  - action_summary_of_queues
  
## request info about a robot
* request_robot_info
  - action_robot_by_name
  
## ## request info about a robot path 1
* request_summary_of_robots
  - action_summary_of_robots
  - utter_more_info_about_a_robot
* request_robot_info
  - action_robot_by_name
  
## request info about a robot path 2
* request_summary_of_robots
  - action_summary_of_robots
  - utter_more_info_about_a_robot
* deny
  - utter_goodbye
  
## request info about a job
* request_job_info
  - action_job_by_name
  
## request info about a job path 1
* request_summary_of_jobs
  - action_summary_of_jobs
  - utter_more_info_about_a_job
* request_job_info
  - action_job_by_name
  
## request info about a job path 2
* request_summary_of_jobs
  - action_summary_of_jobs
  - utter_more_info_about_a_job
* deny
  - utter_goodbye