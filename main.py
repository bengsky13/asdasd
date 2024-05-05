import random
import requests
import time
headers = {
    'Host': 'game-server.geoguessr.com',
    'Cookie': '_ncfa=bvHF2d%2FMASwzXYAlZ6F0eYOqB8LNxwGl91uuFMvXg9I%3DOyX8NXcYStQltr85XWzlZpwl85x8YWMVkpDm8tuokRHN6G3HWnanA%2FykfEhLPb8dLoWFaRalBBs2jtXJBnrgSvdsXNGihoU4pGW5aLcXAgs%3D; session=eyJTZXNzaW9uSWQiOiJtMTM3ZG1ndXJic2hzZGZ3Mzlxc2hsM3JtaDg1bDB5dSIsIkV4cGlyZXMiOiIyMDI0LTA0LTMwVDA3OjQyOjQ3LjgyNjU1ODJaIn0%3D',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Client': 'ios-2.1.2-5671',
    'User-Agent': 'GeoGuessr/5671 CFNetwork/1494.0.7 Darwin/23.4.0',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def getGameId():
    url = 'https://game-server.geoguessr.com/api/lobby/join-public'
    data = {
        'client': 'ios',
        'rated': True,
        'gameType': 'Duels'
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(response.json())
    return response.json()['gameLobbyId']
def getLocation(id):
    url = f'https://game-server.geoguessr.com/api/duels/{id}/reconnect'

    response = requests.get(url, headers=headers, timeout=10)
    return response.json()

def guess(id, lat, lng, round):
    url = f'https://game-server.geoguessr.com/api/duels/{id}/guess'
    data = {"lat":lat,"lng":lng,"roundNumber":round}
    isDone = False
    while isDone == False:
        try:
            print(("REQUESTING"))
            response = requests.post(url, headers=headers, json=data, timeout=3)
            isDone = True
            return response.json()
        except Exception as e:
            print(e)
            print("ERROR SLEEPING")
            time.sleep(3)
while True:
    try:
        time.sleep(5)
        location = False
        gameId = getGameId()
        print("GAMEID:", gameId)
        while location == False:
            try:
                time.sleep(3)
                location = getLocation(gameId)
                if 'teams' in location:
                    continue
                else:
                    location = []
            except:
                continue
        if location['teams'][0]['players'][0]['playerId'] == "662e74a4a70faac6a9c27e57":
            me = 0
            enemy = 1
        else:
            me = 1
            enemy = 0
        print("CURRENT RATING: ", location['teams'][me]['players'][0]['rating'])
        time.sleep(3)
        x = 1
        for i in location['rounds']:
            print(x)
            health = getLocation(gameId)
            print(f"MY HEALTH:", health['teams'][me]['health'])
            print(f"ENEMY HEALTH:", health['teams'][enemy]['health'])
            print()
            print()
            if health['teams'][0]['health'] == 0 or health['teams'][0]['health'] == 0 :
                print("ENDED")
                break
            else:
                print("CONTINUE")
            sucess = True
            minLat = float(str(random.randint(0,2))+"."+str(random.randint(1,25000000000000000)))
            minLng = float(str(random.randint(0,2))+"."+str(random.randint(1,25000000000000000)))
            random_bool = random.choice([True, False])
            realLat = i['panorama']['lat']
            realLng = i['panorama']['lng']
            if random_bool:
                lat = realLat - minLat
                lng = realLng - minLng
            else:
                lat = realLat + minLat
                lng = realLng + minLng
            # print("REAL:", realLat)
            # print("FAKE:", lat)
            # print("REAL:", realLng)
            # print("FAKE:", lng)
            while sucess:
                check = guess(gameId, lat, lng, x)
                if 'message' in check:
                    print(check)
                    if 'not started' in check['message']:
                        left = check['message'].split("not started (")[1].split("s")[0]
                        print("SLEEP: ", left)
                        left = int(left)+3
                        time.sleep(left)
                    else:
                        break
                else:
                    sucess = False
            if 'message' in check:
                if 'Unable to guess when game is over' in check['message']:
                    break
            x+=1
    except Exception as e:
        print(e)
        continue