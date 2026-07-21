import json

import requests

from ..config import URL, TOKEN


HEADERS = {"X-API-Key": TOKEN}


def get_all_test():
    return requests.get(url=URL + '/test/all', headers=HEADERS).json()

def create_user(tid):
    json = {
        "tid": int(tid)
    }

    return requests.post(url=URL + "/user/create", headers=HEADERS, json=json)

def create_session(answers: dict, tid: int, test_id: int):
    json = {
          "tid1": tid,
          "answer1": answers,
          "test_id": test_id
        }
    result =  requests.post(url=URL + "/session/create/by_tid",
                         headers=HEADERS, json=json).json()
    return result.get("session_id")

def join_session(answers: dict,tid: int, session_id: int):
    json = {
          "tid2": tid,
          "answer2": answers
        }
    result = requests.post(url=URL + f"/session/{session_id}/join/by_id", headers=HEADERS, json=json).json()
    return result.get("result")

if __name__ == "__main__":
    pass