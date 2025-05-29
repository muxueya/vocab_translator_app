#!/usr/bin/env python3
"""
Simple test script for the Karp API v7.
"""

import sys
import requests

# ← change to the host used in the docs
BASE_URL = "https://spraakbanken4.it.gu.se/karp/v7"
HEADERS = {"Accept": "application/json"}


def list_resources():
    """
    Retrieve the list of available resources.
    """
    url = f"{BASE_URL}/resources"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def get_resource(resource, limit=5):
    """
    Fetch up to `limit` entries from a given resource.
    """
    url = f"{BASE_URL}/resources/{resource}"
    params = {"limit": limit}
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def main():
    if len(sys.argv) > 1:
        resource = sys.argv[1]
        data = get_resource(resource)
        print(f"\nEntries for resource '{resource}':")
        # just dump whatever JSON you get back
        from pprint import pprint
        pprint(data)
    else:
        resources = list_resources()
        print("\nAvailable resources:")
        # handle either a list or an object
        if isinstance(resources, dict):
            for name in resources:
                print(f"  • {name}")
        else:
            for name in resources:
                print(f"  • {name}")


if __name__ == "__main__":
    main()
