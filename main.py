import http.client
import json
import keys

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': keys.API_KEY
}

conn.request("GET", "/fixtures?live=all", headers=headers)

res = conn.getresponse()
data = res.read()
response_dict = json.loads(data)
total = response_dict['results']


def data():
    live = 0
    reds = 0
    if total == 0:
        print('No Results')

    for i in range(total):
        listed = response_dict['response'][i]['events']
        # print(response_dict)
        for k in listed:
            if k['detail'] == 'Red Card':

                fixture = response_dict['response'][i]['fixture']['id']
                conn.request("GET", "/odds/live?fixture=" + str(fixture), headers=headers)
                res = conn.getresponse()
                data = res.read()
                resp = json.loads(data)
                printer = ''
                if resp['results'] == 0:
                    print('No Live Mathes')
                    break

                for l in resp['response']:
                    if l['fixture']['status']['long'] == 'Match Finished':
                        live -= 1
                        print('No Live Matches with Red Cards')
                        break

                        printer = l['fixture']['status']['long'] + ' ' + str(l['fixture']['status']['elapsed'])
                    if live >= 0:
                        print(k['team']['name'], "| ", printer)
            else:
                reds -=1
        if reds != 0:
            print('No Live Matches with Red Cards')
            break


data()
