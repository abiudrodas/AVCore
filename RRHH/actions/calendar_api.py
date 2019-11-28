#from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datefinder
from datetime import timedelta
import pytz


class manage_calendar:
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        self.tz = pytz.timezone('Europe/Madrid')
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds, cache_discovery=False)

    def get_event(self, num_events=1):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming {} events'.format(num_events))
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=num_events, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def create_event(self, summary, description, start, end=None, duration=1):
        available = self.is_avalable(date_start=start)
        if not available[0]:
            next_app = self.next_available(start=available[1], iterations=3)
            return {'kind': 'calendar#event', 'status': 'unavailable', 'availables': next_app}
        else:
            matches = list(datefinder.find_dates(start))

            if len(matches):
                start_time = matches[0]
            if end is not None:
                matches_2 = list(datefinder.find_dates(end))
                if len(matches):
                    end_time = matches[0]
                else:
                    end_time = start_time + timedelta(hours=duration)
            else:
                end_time = start_time + timedelta(hours=duration)

            event_result = self.service.events().insert(calendarId='primary',
                                                        body={
                                                            "summary": summary,
                                                            "description": description,
                                                            "start": {"dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                                                      "timeZone": 'Europe/Madrid'},
                                                            "end": {"dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                                                    "timeZone": 'Europe/Madrid'},
                                                        }
                                                        ).execute()

            return event_result

    def free_busy_state(self, start, end=None, duration=1):

        matches = list(datefinder.find_dates(start))
        if len(matches):
            start_time = matches[0]
        if end is not None:
            matches_2 = list(datefinder.find_dates(end))
            if len(matches):
                end_time = matches_2[0]
            else:
                end_time = start_time + timedelta(hours=duration)
        else:
            end_time = start_time + timedelta(hours=duration)

        init_val = self.tz.localize(start_time)
        end_val = self.tz.localize(end_time)

        # This event should be returned by freebusy
        body = {
            "timeMin": init_val.isoformat(),
            "timeMax": end_val.isoformat(),
            "timeZone": 'Europe/Madrid',
            "items": [{"id": 'primary'}]
        }

        eventsResult = self.service.freebusy().query(body=body).execute()
        cal_dict = eventsResult[u'calendars']

        return cal_dict['primary']['busy']

    def is_avalable(self, date_start, date_end = None, duration = 1):
        # matches = list(datefinder.find_dates(date_start))
        #
        # if len(matches):
        #     start_time = matches[0]
        # ref_date = self.tz.localize(start_time).isoformat()
        appointments = self.free_busy_state(date_start, date_end, duration)

        if appointments:
            num_app = len(appointments)
            availability = appointments[num_app-1]['end']
            return [False, availability]
        else:
            return [True, None]

    def next_available(self, start=None, end=None, iterations=1):
        available_hours = []
        for x in range(iterations):
            date_ = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S+01:00") + timedelta(hours=x)
            date_ = date_.strftime("%Y-%m-%dT%H:%M:%S")
            if self.is_avalable(date_start=date_, date_end=end)[0]:
                available_hours.append(date_)
        return available_hours

    def get_schedule_fixed(self, date, category='all'):
        iter = 4
        morning = '08:00:00+01:00'
        noon = '13:00:00+01:00'
        afternoon = '17:00:00+01:00'
        hours = ''

        if category == 'morning':
            hours = morning
        elif category == 'noon':
            hours = noon
        elif category == 'afternoon':
            hours = afternoon

        date = date.split('T')
        date = date[0]+'T'+hours

        return self.next_available(start=date, iterations=iter)


def main():
    calend = manage_calendar()

    all = False

    # if all:
    #     events = calend.get_event()
    #     if not events:
    #         print('No upcoming events found.')
    #     for event in events:
    #         start = event['start'].get('dateTime', event['start'].get('date'))
    #
    # result = calend.create_event("Reunion mañana con Ignacio", "Prueba de que aqui no hay nada de nada", "12-28-2019 19:00:00")
    # print("result: ", result)
    # # print(calend.is_avalable(date_start="28/11/2019 15:00"))
    # #date = '2019-11-28T00:00:00+01:00'
    # #print(calend.get_schedule_fixed(date=date,category='noon'))


if __name__ == '__main__':
    main()
