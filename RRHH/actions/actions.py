# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime, timedelta
from custom_mail import send_email

class ActiongetNominas(Action):

    def name(self) -> Text:
        return "action_get_nomina"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender = tracker.sender_id
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

        sender = tracker.sender_id
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

class ActionsgetSchedule(Action):

    def name(self) -> Text:
        return "action_get_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender = tracker.sender_id
        utter_schedule = ""
        intent = tracker.latest_message["intent"]["name"]
        entity = tracker.latest_message["entities"][0]['entity']
        date = next(tracker.get_latest_entity_values(entity))
        print(date)
        if intent == "get_schedule_in":
            utter_schedule = "Tu entrada del " + date + " se registró a las 08:00 hrs"
        elif intent == "get_schedule_out":
            utter_schedule = "Tu salida del " + date + " se registró a las 18:00 hrs"

        dispatcher.utter_message(utter_schedule)

        return []


class ActionsetVacations(Action):

    def name(self) -> Text:
        return "action_set_vacations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender = tracker.sender_id
        entity = tracker.latest_message["entities"][0]['entity']

        if entity == 'interval':
            interval = next(tracker.get_latest_entity_values(entity))
            interval = interval.split(" ")
            date_format = "%d/%m/%Y"
            date_to = datetime.strptime(interval[1], date_format)
            date_to = date_to - timedelta(days=1)
            date_to = datetime.strptime(str(date_to), '%Y-%m-%d %H:%M:%S').strftime(
                '%d/%m/%Y')
            interval_str = "del " + interval[0] + " al " + date_to

            email_sender = "ifernandez@holahal.com"

            send_email(user=sender, user_mail=email_sender,subject="Peticion de Vacaciones",additional_data=[interval_str])

            dispatcher.utter_message(
                "Perfecto, tus dias de vacaciones " + interval_str + " han sido solicitadas a tu responsable, recibiras un email cuando estas sean aprobadas")

        elif entity == 'day':
            day = next(tracker.get_latest_entity_values(entity))
            utter_str = "OK, te he pedido vacaciones el día " + day + ", Recibiras una notificación en tu email cuando tu responsable lo apruebe"

            dispatcher.utter_message(utter_str)


        return []

class ActionPasswordReset(Action):

    def name(self) -> Text:
        return "action_pws_rst"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sender = tracker.sender_id
        dispatcher.utter_message("Hola "+ sender + " Tal vez esto puede servirte:")
        dispatcher.utter_message("https://support.google.com/mail/answer/41078")
        return []
