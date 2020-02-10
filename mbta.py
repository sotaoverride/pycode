import requests
import json

mbta_api_url = "https://api-v3.mbta.com/"


def api_call_get(url):
    try:
        r = requests.get(mbta_api_url + url)
    except (requests.ConnectionError,
            requests.RequestException,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects) as e:
        print 'API Request cant be completed "%s"' % str(e)
    try:
        api_result = json.loads(r.text)
    except ValueError:
        print ('Value Error')
    try:
        if api_result['data'] == '':
            print ('API Error')
    except KeyError as e:
        print 'can not find data key in response "%s"' % str(e),
    return api_result


def getuserinput():
    userInput = ""
    print("Start")
    while "quit" not in userInput:
        # Prompt for a new transaction
        userInput = raw_input(
            "Enter list, stops, or quit.")
        userInput = userInput.lower()
        if "list" not in userInput and "stops" not in userInput:
            print("list, stops, or quit please.")
        if "list" in userInput:
            subwayLinePrint(api_call_get("routes?filter[type]=0,1"))
        if "stops" in userInput:
            sid = raw_input("Enter a subway-line id (case sensitive) to list all its stops")
            stationsPrint(api_call_get("stops?filter[route]="+sid))
    print("Good bye")


def subwayLinePrint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    resp = json.loads(text)
    try:
        for each in resp['data']:
            print "ID: ",
            try:
                print each['id'],
            except KeyError as e:
                print 'can not find id key in response "%s"' % str(e),
            print "Name: ",
            try:
                print each['attributes']['long_name']
            except KeyError as e:
                print 'can not find name key in response "%s"' % str(e),
    except KeyError as e:
        print 'No data in response "%s"' % str(e)


def stationsPrint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    resp = json.loads(text)
    try:
        for each in resp['data']:
            print "Name: ",
            try:
                print each['attributes']['name']
            except KeyError as e:
                print 'can not find name key in response "%s"' % str(e),
    except KeyError as e:
        print 'No data in response "%s"' % str(e)


# Main program
getuserinput()
