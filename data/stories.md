## say hello
* greet
  - utter_greet

## say goodbye
* goodbye
  - utter_goodbye

## happy
* thankyou
  - utter_thankyou
  
## know about bot age
* bot_age
  - utter_bot_age
  
## know about bot who am i
* bot_who_am_i
  - utter_bot_who_am_i
  
## know about bot job
* bot_job
  - utter_bot_job
  
## know about bot mood
* bot_mood
  - utter_bot_mood
  
## know about bot location
* bot_location
  - utter_bot_location
  
## help request
* help
  - utter_help

  
## --------- ROBOTS --------- ##


## request robot states
* request_robot_states
  - utter_robot_states
  
## request info about a robot
* request_robot_info_by_name
  - action_robot_by_name
  
## request summary of robots + valid robot state + list with values + info about single robot
* request_summary_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"True"}
  - action_get_robots
  - action_summary_of_robots
  - slot{"empty_result":"False"}
  - utter_more_info_about_a_robot
* request_robot_info_by_list_idx
  - action_robot_by_list_idx
  
## request summary of robots + valid robot state + empty list + info about single robot
* request_summary_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"True"}
  - action_get_robots
  - action_summary_of_robots
  - slot{"empty_result":"True"}
  
## request summary of robots + valid robot state + list with values + deny info about single robot
* request_summary_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"True"}
  - action_get_robots
  - action_summary_of_robots
  - slot{"empty_result":"False"}
  - utter_more_info_about_a_robot
* deny
  - utter_further_question

  
## request summary of robots + wrong robot state
* request_summary_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_robot_state
  
## request number of robots + valid robot state
* request_number_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"True"}
  - action_get_robots
  - action_number_of_robots
  
## request number of robots + wrong robot state
* request_number_of_robots
  - action_robot_state_check
  - slot{"robot_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_robot_state
  
## request last robot + valid robot state
* request_last_robot
  - action_robot_state_check
  - slot{"robot_state_check":"True"}
  - action_get_robots
  - action_get_last_robot
  
## request last robot + wrong robot state
* request_last_robot
  - action_robot_state_check
  - slot{"robot_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_robot_state
  
## --------- JOBS --------- ##

## request job states
* request_job_states
  - utter_job_states
  
## request info about a job
* request_job_info_by_name
  - action_job_by_name
  
## request summary of jobs + valid job state + list with values + info about single job
* request_summary_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"True"}
  - action_get_jobs
  - action_summary_of_jobs
  - slot{"empty_result":"False"}
  - utter_more_info_about_a_job
* request_job_info_by_list_idx
  - action_job_by_list_idx
  
## request summary of jobs + valid job state + empty list + info about single job
* request_summary_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"True"}
  - action_get_jobs
  - action_summary_of_jobs
  - slot{"empty_result":"True"}
  
## request summary of jobs + valid job state + deny info about single job
* request_summary_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"True"}
  - action_get_jobs
  - action_summary_of_jobs
  - utter_more_info_about_a_job
* deny
  - utter_further_question
  
## request summary of jobs + wrong job state
* request_summary_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_job_state
  
## request number of jobs + valid job state
* request_number_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"True"}
  - action_get_jobs
  - action_number_of_jobs
  
## request info about number of jobs + wrong job state
* request_number_of_jobs
  - action_job_state_check
  - slot{"job_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_job_state
  
## request last job + valid job state
* request_last_job
  - action_job_state_check
  - slot{"job_state_check":"True"}
  - action_get_jobs
  - action_get_last_job
  
## request last job + wrong job state
* request_last_job
  - action_job_state_check
  - slot{"job_state_check":"False"}
  - slot{"state": null}
  - utter_wrong_job_state
  
  
## --------- ASSETS --------- ##
  
## request info about an asset
* request_asset_info_by_name
  - action_asset_by_name
  
## request summary of assets + list with values + info about single asset
* request_summary_of_assets
  - action_get_assets
  - action_summary_of_assets
  - slot{"empty_result":"False"}
  - utter_more_info_about_an_asset
* request_asset_info_by_list_idx
  - action_asset_by_list_idx
  
## request summary of assets + empty list + info about single asset
* request_summary_of_assets
  - action_get_assets
  - action_summary_of_assets
  - slot{"empty_result":"True"}
  
## request summary of assets + deny info about single asset
* request_summary_of_assets
  - action_get_assets
  - action_summary_of_assets
  - utter_more_info_about_an_asset
* deny
  - utter_further_question
  
## request number of assets
* request_number_of_assets
  - action_get_assets
  - action_number_of_assets
  
## request last asset
* request_last_asset
  - action_get_assets
  - action_get_last_asset
  
  
## --------- QUEUES --------- ##
  
## request info about a queue
* request_queue_info_by_name
  - action_queue_by_name
  
## request summary of queues + list with values + info about single queue
* request_summary_of_queues
  - action_get_queues
  - action_summary_of_queues
  - slot{"empty_result":"False"}
  - utter_more_info_about_a_queue
* request_queue_info_by_list_idx
  - action_queue_by_list_idx
  
## request summary of queues + empty list + info about single queue
* request_summary_of_queues
  - action_get_queues
  - action_summary_of_queues
  - slot{"empty_result":"True"}
  
## request summary of queues + deny info about single queue
* request_summary_of_queues
  - action_get_queues
  - action_summary_of_queues
  - utter_more_info_about_a_queue
* deny
  - utter_further_question
  
## request number of queues
* request_number_of_queues
  - action_get_queues
  - action_number_of_queues
  
## request last queue
* request_last_queue
  - action_get_queues
  - action_get_last_queue
  
  
## --------- PROCESSES --------- ##
  
## request info about a process
* request_process_info_by_name
  - action_process_by_name
  
## request summary of processes + list with values + info about single process
* request_summary_of_processes
  - action_get_processes
  - action_summary_of_processes
  - slot{"empty_result":"False"}
  - utter_more_info_about_a_process
* request_process_info_by_list_idx
  - action_process_by_list_idx
  
## request summary of processes + empty list + info about single process
* request_summary_of_processes
  - action_get_processes
  - action_summary_of_processes
  - slot{"empty_result":"True"}
  
## request summary of processes + deny info about single process
* request_summary_of_processes
  - action_get_processes
  - action_summary_of_processes
  - utter_more_info_about_a_process
* deny
  - utter_further_question
  
## request number of processes
* request_number_of_processes
  - action_get_processes
  - action_number_of_processes
  
## request last process
* request_last_process
  - action_get_processes
  - action_get_last_process