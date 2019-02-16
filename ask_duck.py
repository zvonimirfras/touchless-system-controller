import requests
import urllib.parse

duckSearchUrl = "https://api.duckduckgo.com/?q={query}&format=json"


def ask_duck(what):
    url = duckSearchUrl.replace("{query}", prepare_duck_query(what))
    r = requests.get(url)
    return r.json()


def prepare_duck_query(query):
    query = urllib.parse.quote_plus(query.strip())
    query = query.replace("%2B", "+")

    return query


if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        print("Ask something first ;)")
    else:
        print(ask_duck(sys.argv[1])["Abstract"])
