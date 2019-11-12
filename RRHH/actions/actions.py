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
from pdf_gen import generate_nomina

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
            interval_str = "del " + interval[0] + "-" + interval[1] + " al " + interval[2] + "-" + interval[3]

            end_range = int(interval[2])
            links = []

            if int(interval[3]) > int(interval[1]):
                end_range = int(interval[0]) + (12-int(interval[0])) + int(interval[2])

            for x in range(int(interval[0]), end_range + 1):
                if x <= 12:
                    links.append(generate_nomina(str(x) + "-" + interval[1]))

            dispatcher.utter_message(
                "Aquí tienes las nóminas del periodo " + interval_str)

            for link in links:
                dispatcher.utter_message("media " + link)

        elif entity == 'month':
            months = next(tracker.get_latest_entity_values(entity))
            months = months.split("/")
            utter_months = ""
            month_str = ""

            links = []

            if len(months) == 1:
                unit_month = months[0].split(" ")
                # print("UNIT MONTH ", unit_month)
                month_str = unit_month[0] + "-" + unit_month[1]
                utter_months = "Aqui tienes la nomina del " + month_str

                links.append(generate_nomina(month_str))

            elif len(months) > 1:
                for month in months:
                    month = month.split(" ")
                    links.append(generate_nomina(month[0] + "-" + month[1]))
                    month_str = month_str + month[0] + "-" + month[1] + ", "
                utter_months = "Aqui están las nominas de los meses " + month_str.strip(
                    ", ")

            dispatcher.utter_message(utter_months)

            for link in links:
                dispatcher.utter_message("media " + link)

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
        #print(date)
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
        #print(date)
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
        email_sender = "ifernandez@holahal.com"

        if entity == 'interval':
            interval = next(tracker.get_latest_entity_values(entity))
            interval = interval.split(" ")
            date_format = "%d/%m/%Y"
            date_to = datetime.strptime(interval[1], date_format)
            date_to = date_to - timedelta(days=1)
            date_to = datetime.strptime(str(date_to), '%Y-%m-%d %H:%M:%S').strftime(
                '%d/%m/%Y')
            interval_str = "del " + interval[0] + " al " + date_to

            send_email(user=sender, user_mail=email_sender,subject="Peticion de Vacaciones",additional_data=[interval_str])

            dispatcher.utter_message(
                "Perfecto, tus dias de vacaciones " + interval_str + " han sido solicitadas a tu responsable, recibiras un email cuando estas sean aprobadas")

        elif entity == 'day':
            day = next(tracker.get_latest_entity_values(entity))

            send_email(user=sender, user_mail=email_sender, subject="Peticion de Vacaciones",
                       additional_data=[day])
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
