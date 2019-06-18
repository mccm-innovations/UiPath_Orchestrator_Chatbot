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
  
## ask_about_jobs
* ask_about_jobs
  - action_number_of_jobs_in_state
  
## ask_about_robots
* ask_about_robots
  - action_number_of_robots_in_state
  
## request_summary_of_jobs
* request_summary_of_jobs
  - action_summary_of_jobs