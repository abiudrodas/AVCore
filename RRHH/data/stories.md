## fallback
- utter_default

## greeting path 1
* greet
- utter_greet

## fine path 1
* fine_normal
- utter_help

## fine path 2
* fine_ask
- utter_reply

## set vacations path
* set_vacations
- utter_set_vacations
* vacation_range
- action_set_vacations
- utter_anything_else

## set vacations path 2
* vacation_range
- action_set_vacations
- utter_anything_else

## get vacations path
* get_vacations_available
- utter_get_vacations
- utter_anything_else

## thanks path 1
* thanks OR affirmative
- utter_help

## negative path
* negation
- utter_bye_by_negation

## bye path 1
* bye
- utter_bye
- action_restart

## schedule  in 
* set_schedule_in
- action_set_schedule
- utter_anything_else

## schedule  out 
* set_schedule_out
- action_set_schedule
- utter_anything_else

## get schedule in
* get_schedule_in
- action_get_schedule
- utter_anything_else

## get schedule out
* get_schedule_out
- action_get_schedule
- utter_anything_else

## get nominas interval
* get_nomina{"interval": "05 2019 06 2019"}
- action_get_nomina
- utter_anything_else

## get nomina one month
* get_nomina{"month": "05 2019"}
- action_get_nomina
- utter_anything_else