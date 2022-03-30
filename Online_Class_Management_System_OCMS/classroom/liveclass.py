import datetime
import json
import requests
import jwt
from time import time

API_KEY = 'm8mpOJZ8QIakPgQ89ENtIw'
API_SEC = 'XUWLRD0d6dDNxpdJgaRGV3qY8TsnUJrrSCXT'
email = "nikhilsaraswat@kgpian.iitkgp.ac.in"

# # this is the json data that you need to fill as per your requirement to create zoom meeting, look up here for documentation
# # https://marketplace.zoom.us/docs/api-reference/zoom-api/meetings/meetingcreate


meetingdetails = {"topic": "My Title",
                  "duration": 60,
                  "start_time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                  "password": "12345",
                  "agenda": "CLassroom",
                  "type": 2,

                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "False",
                               "join_before_host": "true",
                               "watermark": "true",
                               "participant_video": "true",
                               "audio": "voip",
                               "auto_recording": "cloud",
                               "mute_upon_entry": "False",
                               "waiting_room": "False",
                               "show_share_button": "true",
                               "who_can_share_screen": "all",
                               "who_can_share_screen_when_someone_is_sharing": "all",
                               "screen_sharing": "true",
                               "co_host": "True",
                               "alternative_hosts": "",
                               }
                  }


# sourcery skip: avoid-builtin-shadow
def createMeeting(meetingName="My Meeting", Email=""):
    # sourcery skip: avoid-builtin-shadow

    meetingdetails["topic"] = meetingName
    time_now = datetime.datetime.now()
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
    print(time_now.strftime("%Y-%m-%d %H:%M:%S"))
    print(expiration_time.strftime("%Y-%m-%d %H:%M:%S"))
    rounded_off_exp_time = round(expiration_time.timestamp())

    headers = {'algorithm': 'HS256', 'typ': 'JWT'}
    payload = {'iss': API_KEY, 'exp': rounded_off_exp_time}
    encoded_jwt = jwt.encode(payload, API_SEC, algorithm="HS256")
    url = f"https://api.zoom.us/v2/users/{email}/meetings"
    header = {"Authorization": f"Bearer {encoded_jwt}"}
    obj = {"topic": "The title of your zoom meeting", "start_time": datetime.datetime.now(
    ).strftime("%Y-%m-%dT%H:%M:%S"), "duration": 30, "password": "12345"}
    r = requests.post(url, json=meetingdetails, headers=header)
    dict = r.json()
    return dict["join_url"]
