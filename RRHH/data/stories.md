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
* thanks
- utter_anything_else

## affirmative path 1
* affirmative
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

## reset password done
* password_reset
- action_pws_rst
- utter_ask_done
* affirmative
- utter_anything_else

## reset password not done
* password_reset
- action_pws_rst
- utter_ask_done
* negation
- utter_sorry
- utter_anything_else

## schedule simple appointment
* simple_appointment{"day": "00:00:00 27-11-2019"}
- slot{"day" : "00:00:00 27-11-2019"}
- utter_ask_preference
* category_appointment
- action_get_availabilty
* spec_hour
- action_set_appointment
- utter_anything_else

## schedule appointment not hour
* appointment_with_category
- action_get_availabilty
* spec_hour
- action_set_appointment
- utter_anything_else

## schedule appointment hour available
* appointment_with_hour{"day": "08:00:00 03-12-2019"}
- action_set_appointment

## schedule appointment hour not available
* spec_hour
- action_set_appointment
- utter_anything_else

## get availability of a period or day
* get_availability
- action_get_availabilty


