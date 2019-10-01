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
            months = next(tracker.get_latest_entity_values(entity))
            months = months.split("/")
            utter_months = ""
            month_str = ""

            if len(months) == 1:
                unit_month = months[0].split(" ")
                print("UNIT MONTH ",unit_month)
                month_str = unit_month[0] + "/" + unit_month[1]
                utter_months = "Aun no puedo darte la nomina del " + month_str + " porque no estoy integrado a ningún CRM"
            elif len(months) > 1:
                for month in months:
                    month = month.split(" ")
                    month_str = month_str + month[0] + "/" + month[1] + ", "
                utter_months = "Aun no puedo darte las nominas de los meses " + month_str.strip(
                    ", ") + " porque no estoy integrado a ningún CRM"

            dispatcher.utter_message(utter_months)

        return []

class ActionsetSchedule(Action):

    def name(self) -> Text:
        return "action_set_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        utter_schedule = ""
        intent = tracker.latest_message["intent"]["name"]
        entity = tracker.latest_message["entities"][0]['entity']
        date = next(tracker.get_latest_entity_values(entity))
        date = date.split(" ")
        print(date)
        if intent == "set_schedule_in":
            utter_schedule = "Tu entrada del " + date[1] + " ha sido registrada a las " + date[0]
        elif intent == "set_schedule_out":
            utter_schedule = "Tu salida del " + date[1] + " ha sido registrada a las " + date[0]

        dispatcher.utter_message(utter_schedule)

        return []
