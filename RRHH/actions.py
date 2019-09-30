# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActiongetNominas(Action):

    def name(self) -> Text:
        return "action_get_nomina"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity = tracker.latest_message["entities"][0]['entity']
        if entity == 'interval':
            interval = next(tracker.get_latest_entity_values(entity))
            interval = interval.split(" ")

            interval_str = "del " + interval[0] + "/" + interval[1] + " al " + interval[2] + "/" + interval[3]

            dispatcher.utter_message(
                "Aún no puedo darte las nóminas del periodo " + interval_str + " porque no estoy integrado a ningún CRM")

        elif entity == 'month':
            month = next(tracker.get_latest_entity_values(entity))
            month = month.split(" ")

            month_str = month[0] + "/" + month[1]

            dispatcher.utter_message(
                "Aún no puedo darte la nómina del " + month_str + " porque no estoy integrado a ningún CRM")

        return []
