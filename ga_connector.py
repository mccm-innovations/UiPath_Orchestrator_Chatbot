import inspect
import logging

from rasa.core.channels.channel import UserMessage, InputChannel, CollectingOutputChannel
from asyncio import CancelledError
from sanic import Blueprint, response
from sanic.request import Request

from typing import (
    Text,
    Optional,
    Callable,
    Awaitable,
)

logger = logging.getLogger(__name__)


class GoogleConnector(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "google_assistant"

    def __init__(
            self,
            username: Optional[Text] = None,
    ) -> None:
        self.username = username

    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[None]]):
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=['POST'])
        async def receive(request: Request):
            payload = request.json
            sender_id = payload['conversation']['conversationId']
            intent = payload['inputs'][0]['intent']
            if intent == 'actions.intent.MAIN':
                message = "Hello! Welcome to the Orchestrator Fun Google Assistant skill developed by MCCM Innovations. You can start by saying help."
            else:
                collector = CollectingOutputChannel()
                text = payload['inputs'][0]['rawInputs'][0]['query']
                try:
                    await on_new_message(
                        UserMessage(
                            text, collector, sender_id, input_channel=self.name()
                        )
                    )
                except CancelledError:
                    logger.error(
                        "Message handling timed out for "
                        "user message '{}'.".format(text)
                    )
                except Exception:
                    logger.exception(
                        "An exception occured while handling "
                        "user message '{}'.".format(text)
                    )
                responses = [m["text"].replace('*','').replace('_','').replace('-','').replace('\'','') for m in collector.messages]
                message = responses[0]

            out_dict = {
                "expectUserResponse": 'true',
                "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
                            }
                        ],
                        "inputPrompt": {
                            "richInitialPrompt": {
                                "items": [
                                    {
                                        "simpleResponse": {
                                            "textToSpeech": message,
                                            'displayText': message
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }

            return response.json(out_dict)

        return custom_webhook




