
# UiPath Orchestrator Chatbot
## Online demo
You can find an online demo of the chatbot in our website: [https://mccminnovations.com/webchat](https://mccminnovations.com/webchat).
It is connected to the public Orchestrator of UiPath: https://platform.uipath.com.

TODO GOOGLE ASSISTANT
## Inspiration

Imagine a personal assistant that is capable to listen to your voice commands and read your typed texts in order to perform different daily work tasks, saving time and energy.  The UiPath Orchestrator Chatbot developed by MCCM Innovations allows you to review robots, processes, jobs, queues and assets of your UiPath Orchestrator environmnet using your voice or text questions.

Probably there are people in your RPA team that do not have access to the Orchestrator dashboard but they need to know in which state is a specific robot for example. This chatbot can help your teammates improving their productivity since they will not need to ask information to the robot controller. 

Chatbots Market was worth USD 864.9 million in 2017 and is projected to reach USD 3146.4 million by 2023 growing at a CAGR of 24.1% over the period 2018 - 2023. The evolution and utilization of artificial intelligence applications are skyrocketing owing to its numerous benefits offered and rising consumer base. The rising number of messengers across the globe, the demand for chatbots which is capable of imitating human conversation and solving various tasks are on the rise. Numerous companies and startups are investing in the technology to ease their businesses and tackle customer’s queries. Source: [Chatbots market](https://www.mordorintelligence.com/industry-reports/chatbots-market).

## What it does
This chatbot can assist you with the **UiPath Orchestrator**. You can ask information about **jobs**, **robots**, **processes**, **queues** and **assets**. However, it cannot create new queues or start jobs. In other words, it only has read access to your Orchestrator. Find below a detailed list of things that this chatbot can do for you:
_Robots_
- Show which are the robot states.
- Request info about a robot by its name.
- Request a summary of robots filtered by state and date.
- Show how many robots are available filtered by state and date.

_Jobs_
- Show which are the job states.
- Request info about a job by its name.
- Request a summary of jobs filtered by state and date.
- Show how many jobs are available filtered by state and date.

_Processes_
- Request info about a process by its name.
- Request a summary of processes filtered by date.
- Show how many processes are available filtered by date.

_Assets_
- Request info about an asset by its name.
- Request a summary of assets.
- Show how many assets are available.

_Queues_
- Request info about a queue by its name.
- Request a summary of queues.
- Show how many queues are available.

### Examples
- Please, show me the summary of robots
- Show me the the summary of jobs of yesterday with the state faulted
- How many jobs are running?
- Show me the possible states of a job
- Please, explain me how this chatbot works
- Show me the summary of robots that started the 14th of August between the 13 and 14 hours and are in the state busy
- Please, show me the summary of jobs with the state successful
- Is there any robot with the state unresponsive?
- Which is the latest process that started the 21th of March?


## How we built it
We built this chatbot using [Rasa](https://rasa.com/). Rasa is an open source framework that provides machine learning tools for developers to build, improve, and deploy contextual chatbots and assistants. We also developed an UiPath Orchestrator API connector in Python that makes calls to retrieve the information asked to the chatbot. Moreover, messages are stored in a MongoDB [MongoDB](https://www.mongodb.com) so they can be extracted, processed and used for re-training the Deep Learning models of Rasa. 

Once the user has asked something to the chatbot, it recognizes the user's intent applying a Deep Neural Network and the Python connector translates this information to make a query to the Orchestrator API. Finally, the Orchestrator's info is returned to the chatbot and displayed to the user in a user-friendly format.

Furthermore, this chabot can be connected to several messaging and voice channels easily. In this project, we provide configurations to deploy the Orchestrator Chatbot in a webchat (`webchat folder`) and in Google Assistant (`action.json file`), just for demo purposes. 

## Video demo
### Webchat
TODO RECORD VIDEO USING THE WEBCHAT
### Google Assistant
TODO RECORD VIDEO USING THE GOOGLE ASSISTANT

## Installation

### Requirements
The first step is to install Docker and Docker Compose on your OS.

- Docker CE: [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/), [Windows](https://docs.docker.com/docker-for-windows/install/)
- Docker Compose: [macOS, Windows, and 64-bit Linux](https://docs.docker.com/compose/install/)

We provide a Docker container with the following required images:

- Rasa
- Rasa Action Server
- Duckling
- MongoDB
- MongoDB Express
- NGINX

**NOTE:** This Docker container has been tested in Ubuntu 18.04.

### How to run it
Please, follow the next steps:

1. Download or clone this project.
```bash
git clone https://github.com/mccm-innovations/UiPath_Orchestrator_Chatbot
```
2. Go to the donwloaded folder.
```bash
cd UiPath_Orchestrator_Chatbot
```
3. Edit the `.env` file to set the environment variables with your data.
4. Create the `rasa_network` network:
```bash
docker network create rasa_network
```
5. Deploy the Docker container:
```bash
docker-compose up
```

Only the steps **2** and **5** are required after the first execution.

### How to use it
Once the Docker container is running you can start using the chatbot in the webchat service. You should have access to the following services in your local machine:
- Webchat: http://localhost:8080
- Rasa: http://localhost:8081
- Rasa action server:  http://localhost:8082
- Duckling server: http://localhost:8083
- Mongo Express: http://localhost:8084
