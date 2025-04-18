#!/usr/bin/env python3

import os
import re
import unicodedata
from string import Template

import html2markdown
import requests

#####################
# PARAMS
lang = "fr-FR"
api_url="https://devoxxfr2025.cfp.dev/api/public/talks"
#####################

def create_entry(id: str, title: str, type: str, summary: str, speakers):
    folder="talks"
    if not os.path.exists("talks"):
        os.makedirs(folder)
    sanitized_title = slugify(title)
    d = {
        'title': title,
        'type': type,
        'speakers': '\n'.join([f"{i[0]} ({i[2]}) - {i[1]}" for i in speakers]),
        'summary': html2markdown.convert(summary),
        'link': f"https://app.voxxr.in/events/devoxxfr2024/talks/{id}/details"
    }

    with open('template.adoc', 'r') as f:
        src = Template(f.read())
        result = src.substitute(d)
        with open(f"{folder}/{sanitized_title}.adoc", "w+", encoding="utf-8") as f:
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

talks = requests.get(
        api_url,
        headers={"Accept": "application/json", "Accept-language": lang}
    )

for talk in talks.json():
    talk_id = talk["id"]
    title = talk["title"]
    type = talk["sessionType"]['name']
    summary = talk["description"]
    speakers = [(s["fullName"], s['company'], s["twitterHandle"]) for s in talk["speakers"]]

    print(f"Processing {title} - {talk_id}")
    create_entry(id=talk_id, title=title, speakers=speakers,summary=summary, type=type)

