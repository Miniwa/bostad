"""
Wraps the studentbostäder API.
"""
import json
import re
import requests
from model import Housing


_ALL_URL = "https://marknad.studentbostader.se/widgets/?actionId=&omraden=&egenskaper=&objektTyper=&callback=api&widgets%5B%5D=koerochprenumerationer%40STD&widgets%5B%5D=objektfilter%40lagenheter&widgets%5B%5D=objektsortering%40lagenheter&widgets%5B%5D=objektlista%40lagenheter&widgets%5B%5D=pagineringgonew%40lagenheter&widgets%5B%5D=pagineringlista%40lagenheter&widgets%5B%5D=pagineringgoold%40lagenheter&_=1488982816968"
_DIRECT_URL = "https://marknad.studentbostader.se/widgets/?actionId=&omraden=&egenskaper=SNABB&objektTyper=&callback=api&widgets%5B%5D=koerochprenumerationer%40STD&widgets%5B%5D=objektfilter%40lagenheter&widgets%5B%5D=objektsortering%40lagenheter&widgets%5B%5D=objektlista%40lagenheter&widgets%5B%5D=pagineringgonew%40lagenheter&widgets%5B%5D=pagineringlista%40lagenheter&widgets%5B%5D=pagineringgoold%40lagenheter&_=1488984919502"


def get_all():
    """
    Returns the result of querying all housings.
    """
    return _get(_ALL_URL)


def get_direct():
    """
    Returns the result of a "bostad direkt" query.
    """
    return _get(_DIRECT_URL)


def _get(url):
    """
    Queries given url and returns the parsed results.
    """
    resp = requests.get(url)
    match = re.search("api\((.*)\);", resp.text)
    if match:
        result = []
        for housing in json.loads(match.group(1))["data"]["objektlista@lagenheter"]:
            result.append(parse_json_housing(housing))

        return result
    else:
        raise ValueError("Could not parse response.")


def parse_json_housing(_obj):
    """
    Parses given json object into a housing model and returns the result.
    """
    return Housing(_obj["adress"], _obj["detaljUrl"], _obj["hyra"])
