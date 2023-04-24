#!/usr/bin/env python3

import json
import os
import re
import sys
import unicodedata
from string import Template

import requests

#####################
# PARAMS
playSession = sys.argv[1]
year = 2023
lang = "fr-FR"
#####################

debug = False
day_mapping = {"wed": "wednesday", "thu": "thursday", "fri": "friday"}
favorite_regex = r"\"fav_(.*?)\"[.\r\n]*\s*class=\"\s*fas"
cookies = {'PLAY_SESSION': playSession}


def create_entry(folder: str, title: str, type: str, summary: str, speakers):
    if not os.path.exists(folder):
        os.makedirs(folder)
    sanitized_title = slugify(title)
    d = {
        'title': title,
        'type': type,
        'speakers': '\n'.join([f"link:{i[1]}[{i[0]}]" for i in speakers]),
        'summary': summary
    }

    with open('template.adoc', 'r') as f:
        src = Template(f.read())
        result = src.substitute(d)
        with open(f"{folder}/{sanitized_title}.adoc", "w+") as f:
            f.writelines(result)


def slugify(value, allow_unicode=False):
    """
    https://stackoverflow.com/a/295466
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def process_day(day: str):
    print(f"Processing day {day_mapping[day]}")
    cfp_html_slots = requests.get(
        f"https://cfp.devoxx.fr/{year}/byday/{day}", cookies=cookies)

    matches = re.finditer(favorite_regex, cfp_html_slots.text, re.MULTILINE)

    favorites_talk_ids = []

    for _, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            favorite_talk = match.group(groupNum)
            favorites_talk_ids.append(favorite_talk)

    cfp_api = f"https://cfp.devoxx.fr/api/conferences/DevoxxFR{year}/schedules/{day_mapping[day]}"

    talk_for_day = requests.get(cfp_api, headers={
                                "Accept": "application/json", "Accept-language": lang})

    slots = talk_for_day.json()['slots']

    for slot in slots:
        id = slot["slotId"]
        if slot["break"] and "id" in slot["break"]:
            continue
        else:
            if debug:
                print(slot)
                print(json.dumps(slot, indent=4))
            if slot["talk"]:
                talk_id = slot["talk"]["id"]
                title = slot["talk"]["title"]
                type = slot["talk"]["talkType"]
                summary = slot["talk"]["summary"]
                speakers = [(s["name"], s["link"]["href"])
                            for s in slot["talk"]["speakers"]]
                if talk_id in favorites_talk_ids:
                    print(f"Creating entry for favorite talk : {talk_id} {title}")
                    create_entry(folder=day_mapping[day], title=title,
                                type=type, summary=summary, speakers=speakers)


process_day("wed")
process_day("thu")
process_day("fri")
