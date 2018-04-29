import urllib.parse
import json
import random
import http.client
import logging

class WhoIsTask:
    messages = {
        "none": [
            "Didn't find any players called that.",
            "Nope, no players by that name.",
            "I don't know of any players by that name.",
            "There has never been a player by that name",
        ],
        "no_more_options":[
            "Well that is all the players I know of.",
            "Well, that's all folks!",
            "There is no more players to choose from."
        ],
        "multiple": [
            "Did you mean {}?",
            "I know of {}",
            "How about {}?",
            "Did you mean {}?"
        ],
        "player_details_no_stats": [
            "There is {0} who was born on {1} but hasn't got any stats",
        ],
        "player_details": [
            "You have {0} who plays for {1}. They were born on {2} and their latest season stats are {3} goals, {4} assists, {5} total, {6} +/-, and {7} PIM in {8} games.",
            "There is {0} who plays for {1}. Born on {2} and their latest season stats are {3} goals, {4} assists, {5} total, {6} +/-, and {7} PIM in {8} games.",
        ]
    }

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def execute(self, parsedConverstation):
        filter = self.buildFilter(parsedConverstation.proEntities)
        data = self.fetch_player(filter)

        count = data["metadata"]["count"]

        if (count == 0):
            return random.choice(self.messages["none"]), None

        if (count == 1):
            return self.givePlayerDetails(data["data"][0]), None

        pro = len(parsedConverstation.affirmations)
        neg = len(parsedConverstation.denials)

        player = data["data"][neg]
        if (neg == count):
            return random.choice(self.messages["no_more_options"]), None
        if pro == 1:
            return self.givePlayerDetails(player), None

        name = "%s %s" % (player["firstName"], player["lastName"])
        message = random.choice(self.messages["multiple"])
        return message.format(name), parsedConverstation

    def givePlayerDetails(self, player):
        name = "%s %s" % (player["firstName"], player["lastName"])
        dob = player["dateOfBirth"]
        teamStats = player.get("latestPlayerStats")
        if teamStats == None:
            message = random.choice(self.messages["player_details_no_stats"])
            return message.format(name, dob)

        team =teamStats["team"]["name"]
        goals =teamStats.get("G")
        assists =teamStats.get("G")
        total =teamStats.get("TP")
        pim =teamStats.get("PIM")
        plusMinus =teamStats.get("PM")
        gamesPlayed =teamStats.get("GP")
        message = random.choice(self.messages["player_details"])
        return message.format(name, team, dob, goals, assists, total, plusMinus, pim, gamesPlayed)

    def fetch_player(self, filter):
        conn = http.client.HTTPConnection('api.eliteprospects.com:80')
        url = "/beta/players?filter=%s&apikey=%s" % (urllib.parse.quote_plus(filter), self.apiKey)
        logging.info("Making request %s" % (url))
        conn.request("GET", url)
        resp = conn.getresponse()
        returnData = resp.read().decode("utf-8")
        data = json.loads(returnData)
        return data

    def buildFilter(self, entities):
        filters = []
        for key, value in entities.items():
            filters.append(key+"="+value)
        return "&".join(filters)


class TeamRosterTask:

    messages = [
        [
            "Didn't find any teams called that",
            "Out of luck! I couldn't find any teams with that name"
        ],
        [
            "You have {}"
        ],
        [
            "Did you mean, {}?"
        ]
    ]

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def execute(self, parsedConverstation):
        team = parsedConverstation.proEntities["team"]

        conn = http.client.HTTPConnection('api.eliteprospects.com:80')
        url = "/beta/teams?filter=%s&apikey=%s" % (urllib.parse.quote_plus("name="+team), self.apiKey)
        conn.request("GET", url)
        resp = conn.getresponse()
        returnData = resp.read().decode("utf-8")
        data = json.loads(returnData)
        count = data["metadata"]["count"]

        if (count == 0):
            return random.choice(self.messages[0]), parsedConverstation

        firstTeam = data["data"][0]

        if (count == 1):
            message = random.choice(self.messages[1])
            return message.format(firstTeam["name"]), parsedConverstation

        message = random.choice(self.messages[2])
        return message.format(firstTeam["name"]), parsedConverstation