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
- utter_user_number
* user_number
- utter_set_vacations
* vacation_range
- utter_set_vacations_confirmation
- utter_anything_else

## get vacations path
* get_vacations_available
- utter_user_number
* user_number
- utter_get_vacations
- utter_anything_else

## thanks path 1
* thanks
- utter_anything_else

## bye path 1
* bye
- utter_bye
- action_restart

## schedule  in 
* set_schedule_in
- utter_user_number
* user_number
- utter_set_schedule_in
- utter_anything_else

## schedule  out 
* set_schedule_out
- utter_user_number
* user_number
- utter_set_schedule_out
- utter_anything_else

## get nominas
* get_nomina
- utter_user_number
* user_number
- utter_nomina
- utter_anything_else