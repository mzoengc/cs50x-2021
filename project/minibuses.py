import os
import requests
import re

from flask import request


def minibuses_data():
    """
    Minibuses Information API

    """
    try:
        url = "https://static.data.gov.hk/td/routes-fares-geojson/JSON_GMB.json"
        response = requests.get(url)
        response.raise_for_status()
        result = []

        # format api data
        for d in response.json():
            for s in d["rstop"]:
                if len(s["features"]) > 0:
                    try:
                        routeSeq = s["features"][0]["properties"]["routeSeq"]
                        startName = d["locStartNameE"]
                        endName = d["locEndNameE"]
                        if routeSeq == 2:
                            startName = d["locEndNameE"]
                            endName = d["locStartNameE"]
                        f = {
                            "route_id": d["routeId"],
                            "district": d["district"],
                            "route_name": d["routeNameE"],
                            "company_code": d["companyCode"],
                            "start_name": startName,
                            "end_name": endName,
                            "url": d["hyperlinkE"],
                            "duration": d["journeyTime"],
                            "price": d["fullFare"],
                            "route_seq": routeSeq
                        }
                        result.append(f)
                    except (KeyError, TypeError, ValueError):
                        continue
        return result
    except requests.RequestException:
        return None


def minibus_route_stop_data(route_id, route_seq):
    """
    Minibus Route Information API

    """
    try:
        url = f"https://data.etagmb.gov.hk/route-stop/{route_id}/{route_seq}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def minibuses_stop_route_data(stop_id="20003337"):
    """
    Minibuses Stop Routes API

    """
    try:
        url = f"https://data.etagmb.gov.hk/stop-route/{stop_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except requests.RequestException:
        return None


def minibuses_eta_stop_data(stop_id="20003337"):
    """
    Minibuses ETA Stop API

    """
    try:
        url = f"https://data.etagmb.gov.hk/eta/stop/{stop_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except requests.RequestException:
        return None


def minibuses_eta_route_stop_data(route_id, route_seq, stop_seq):
    """
    Minibuses ETA Route Stop API

    """
    try:
        url = f"https://data.etagmb.gov.hk/eta/route-stop/{route_id}/{route_seq}/{stop_seq}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except requests.RequestException:
        return None


def minibus_stop_data(stop_id):
    """
    Minibuses Stop API

    """
    try:
        url = f"https://data.etagmb.gov.hk/stop/{stop_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"]
    except requests.RequestException:
        return None

