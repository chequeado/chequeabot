import json
import requests
from typing import List
from itertools import product
from dateutil import parser
from datetime import datetime, timezone


RASA_HOST = '127.0.0.1'
RASA_PORT = 5005



ENTITIES_DATA = {
    "DATE": {"relevance": 0.5, "match_type": "exact_match", "ignore": False},
    "DATE_ABSTRACT": {"relevance": 0.5, "match_type": "exact_match", "ignore": False},
    "GPE": {"relevance": 0.3, "match_type": "exact_match", "ignore": False},
    "MONEY": {"relevance": 0.3, "match_type": "exact_match", "ignore": False},
    "LOC": {"relevance": 0.3, "match_type": "exact_match", "ignore": True},
    "ORG": {"relevance": 0.3, "match_type": "exact_match", "ignore": False},
    "PER": {"relevance": 0.2, "match_type": "exact_match", "ignore": False},
    "PERCENT": {"relevance": 0.6, "match_type": "exact_match", "ignore": True},
    "QUANTITY": {"relevance": 0.4, "match_type": "exact_match", "ignore": True},
    "TOPIC": {"relevance": 0.3, "match_type": "exact_match", "ignore": False},
    "MISC": {"relevance": 0.3, "match_type": "exact_match", "ignore": True},
    "amount-of-money": {"relevance": 0.5, "match_type": "close_match", "ignore": False},
    "duration": {"relevance": 0.3, "match_type": "close_match", "ignore": True},
    "number": {"relevance": 0.3, "match_type": "close_match", "ignore": False},
    "ordinal": {"relevance": 0.3, "match_type": "exact_match", "ignore": False},
    "time": {"relevance": 0.3, "match_type": "close_match", "ignore": False},
}

PERCENTAGE_TRESHOLD = 10
TIME_TRESHOLD = 30


class RasaExtractor():
    def __init__(self, output_type="count_matches"):
        self.points = 0
        self.matches = 0
        self.output_type = output_type
        self.rasa_endpoint = "http://{0}:{1}/model/parse".format(RASA_HOST, RASA_PORT)

    def get_claim_entities(self, claim):
        res = requests.post(self.rasa_endpoint, json={"text": claim})
        data = res.json()
        if "entities" in data:
            ent_data = {}
            for entity in data["entities"]:
                key = entity["entity"]
                # addind to the dict only the desired entity types
                if ENTITIES_DATA[key]["ignore"] is False:
                    if key not in ent_data:
                        ent_data[key] = [entity]
                    else:
                        ent_data[key].append(entity)

            return ent_data
        return None

    def exact_match(self, ent_data_a: List[dict], ent_data_b: List[dict]) -> int:
        ent_values_a = set([e["value"] for e in ent_data_a])
        ent_values_b = set([e["value"] for e in ent_data_b])
        intersection = ent_values_a.intersection(ent_values_b)
        matches_num = len(intersection)

        return matches_num

    def close_match_money(self, ent_data_a: List[dict], ent_data_b: List[dict]) -> int:
        matches_num = 0

        for ent_a in ent_data_a:
            coin_a = ent_a["additional_info"]["unit"]
            amount_a = ent_a["additional_info"]["value"]
            for ent_b in ent_data_b:
                coin_b = ent_b["additional_info"]["unit"]
                amount_b = ent_b["additional_info"]["value"]
                if coin_a == coin_b:
                    percentage_difference = (
                        (abs(float(amount_a) - amount_b))
                        / ((amount_a + amount_b) / 2.0)
                        * 100
                    )
                    if percentage_difference <= PERCENTAGE_TRESHOLD:
                        matches_num += 1

        return matches_num

    def close_match_time(self, ent_data_a: List[dict], ent_data_b: List[dict]) -> int:
        """
        Given two list of entities of the "time" category return number of matches between them

        Parameters
        ----------
        ent_data_a : list of duckling "time" objects extracted from claim
        ent_data_b : list of duckling "time" objects extracted from media sentence

        Returns
        -------
        int - number of matches between ent_data_a and ent_data_b
        """

        def days_between(d1, d2):
            """ Given two dates in str format return int representing number of days between both dates """
            d1 = parser.parse(d1)
            d2 = parser.parse(d2)
            return abs((d2 - d1).days)

        def interval_overlap(d1_start, d1_end, d2_start, d2_end):
            """ Given two intervals represented by a start and end date in str format return int representing number of days that those intervals overlap """
            d1_start, d1_end = parser.parse(d1_start), parser.parse(d1_end)
            d2_start, d2_end = parser.parse(d2_start), parser.parse(d2_end)

            latest_start = max(d1_start, d2_start)
            earliest_end = min(d1_end, d2_end)
            delta = (earliest_end - latest_start).days
            return delta

        def match(ent_a, ent_b):
            """ Given two "time" entities, return wether they match or not """
            info_a, info_b = ent_a["additional_info"], ent_b["additional_info"]
            type_a, type_b = info_a["type"], info_b["type"]

            if type_a == type_b:
                if type_a == "value":
                    return (
                        days_between(info_a["value"], info_b["value"]) < TIME_TRESHOLD
                    )
                elif type_a == "interval":
                    if "from" not in info_a or "from" not in info_b:
                        return False

                    if "to" not in info_a:
                        info_a["to"] = {"value": str(datetime.now(timezone.utc))}
                    if "to" not in info_b:
                        info_b["to"] = {"value": str(datetime.now(timezone.utc))}

                    d1_start, d1_end = info_a["from"]["value"], info_a["to"]["value"]
                    d2_start, d2_end = info_b["from"]["value"], info_b["to"]["value"]

                    length_1 = days_between(d1_start, d1_end)
                    length_2 = days_between(d2_start, d2_end)

                    if abs(length_1 - length_2) < TIME_TRESHOLD:
                        overlap = interval_overlap(d1_start, d1_end, d2_start, d2_end)
                        if overlap > (length_1 + length_2) / 2 - TIME_TRESHOLD * 2:
                            return True

            return False

        matches = [i for i, j in product(ent_data_a, ent_data_b) if match(i, j)]
        return len(matches)

    def close_match_number(self, ent_data_a: List[dict], ent_data_b: List[dict]) -> int:
        matches_num = 0

        for ent_a in ent_data_a:
            amount_a = ent_a["value"]
            for ent_b in ent_data_b:
                amount_b = ent_b["value"]

                if abs(amount_a) == abs(amount_b):
                    matches_num += 1
                else:
                    try:
                        percentage_difference = (
                            (abs(float(amount_a) - amount_b))
                            / ((amount_a + amount_b) / 2.0)
                            * 100
                        )
                    except:
                        import pdb; pdb.set_trace()
                   
                    if percentage_difference <= 10:
                        matches_num += 1

        return matches_num

    def close_match(self, ent_data_a: List[dict], ent_data_b: List[dict]) -> int:
        matches_num = 0
        ent_type = ent_data_a[0]["entity"]

        if ent_type == "amount-of-money":
            matches_num = self.close_match_money(ent_data_a, ent_data_b)
        elif ent_type == "number":
            matches_num = self.close_match_number(ent_data_a, ent_data_b)
        elif ent_type == "time":
            matches_num = self.close_match_time(ent_data_a, ent_data_b)

        return matches_num

    def compute_points(self, relevance_score: float, matches_num: int) -> float:
        return relevance_score * matches_num

    def output(self, ent_claim_a: dict, ent_claim_b: dict) -> dict:
        """
        Return several types of output
        A) matches_count: counts the number of entity matches between two claims
        B) matches_points: similar to (A) but uses an "entity relevance" weight in order to get a score.
        C) matches_entities: if there's an entity type match, then that entity type is True, if not is False
        D) matches_count_by_entity: counts the number of entity matches between two claims for each entity 
        """

        #Matches points is highly opinionated and probably it'll be better for the modeling algorithm to make
        #the decision about the weight each entity type has on the predictive power

        matches_count = 0
        matches_points = 0
        matches_entities = {ent_type: False for ent_type in ENTITIES_DATA}
        matches_count_by_entity = {ent_type: 0 for ent_type in ENTITIES_DATA}

        for ent_type_a, ent_data_a in ent_claim_a.items():

            if ent_type_a in ent_claim_b:
                ent_data_b = ent_claim_b[ent_type_a]
            else:
                continue

            match_num = getattr(self, ENTITIES_DATA[ent_type_a]["match_type"])(
                ent_data_a, ent_data_b
            )
            match_points = self.compute_points(
                ENTITIES_DATA[ent_type_a]["relevance"], match_num
            )
            matches_count += match_num
            matches_points += match_points

            if match_num >= 1:
                matches_entities[ent_type_a] = True
                matches_count_by_entity[ent_type_a] = match_num

        return {
            "matches_count": matches_count,
            "matches_entities": matches_entities,
            "matches_points": matches_points,
            "matches_count_by_entity": matches_count_by_entity,
        }

    def process_claims(self, claims: List) -> List:
        self.claim_ents = [
            self.get_claim_entities(claim.get("claim")) for claim in claims
        ]
        self.num_claims = len(claims)

    def process_sentences(self, sentences: List) -> List:
        self.sentence_ents = [
            self.get_claim_entities(sentence.get("sentence_text"))
            for sentence in sentences
        ]
        self.num_sentences = len(sentences)

    def extract_feature(self, claim_idx: int, sentence_idx: int) -> List:
        cl_ents = self.claim_ents[claim_idx]
        se_ents = self.sentence_ents[sentence_idx]
        # d = self.finder.entity_distance(cl_ents, se_ents)
        # print(cl_ents, se_ents, d)
        res = self.output(cl_ents, se_ents)
        return [res["matches_points"], res["matches_count"]]


if __name__ == "__main__":


    with open('data/claims.json') as json_file: 
        claims = json.load(json_file) 

    with open('data/output_all.jsonl', 'r') as json_file: 
        json_list = list(json_file)
    

    ex = RasaExtractor()
    ex.process_claims(claims)
    ex.process_sentences(sentences)
    for c in range(len(claims)):
        for s in range(len(sentences)):
            row = ex.extract_feature(c, s)
            print("claim:  ", claims[c]["claim"])
            print("text : ", sentences[s]["sentence_text"])
            print("score: {:4.3f} {:4.3f} ".format(*row))
