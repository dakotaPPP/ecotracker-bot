import requests
import time
from bs4 import BeautifulSoup
import json
import csv
import sqlite3

# GRAB LIST OF GROUP'S PUUIDs
# EVERY 30 MINUTES CHECK FOR EVERYONE

def get_all_puuids():
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Retrieve the puuid of all users
    cursor.execute('''SELECT puuid FROM users''')
    puuids = cursor.fetchall()

    cursor.execute('''SELECT username FROM users''')
    usernames = cursor.fetchall()

    puuidsDictionary = {}
    for i in range(len(puuids)):
      puuidsDictionary[usernames[i][0]] = puuids[i][0]
    # Close the connection
    conn.close()

    return puuidsDictionary

#format: killer_name, killer_gun, killer_gun_media, victim_name, victim_gun, victim_gun, time_in_match, time_match_start
most_recent_eco = ('plumyum#BZB','spectre', 'https://media.valorant-api.com/weapons/462080d1-4035-2937-7c09-27aa2a5c27a7/displayicon.png','some shitter','classic', 'https://media.valorant-api.com/weapons/29a0cfab-485b-f5d5-779a-b59f85e204a8/displayicon.png', 0, 0)

#format: eco_checker[killer_gun][victim_gun]
# Load the JSON data from the file
with open('eco_checker.json', 'r') as file:
    eco_checker = json.load(file)

# Function that inserts new player into database 
def insertPlayer(username, puuid, ecoKills=0, headshots=0, bodyshots=0, legshots=0, lastGame='0'):
  conn = sqlite3.connect('user_data.db')
  cursor = conn.cursor()
  
  cursor.execute('''
    INSERT INTO users (username, puuid, ecoKills, headshots, bodyshots, legshots, lastGame)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  ''', (username, puuid, ecoKills, headshots, bodyshots, legshots, lastGame))
    
  # Commit the changes and close the connection
  conn.commit()
  conn.close()
  
  print("Data has been inserted into the 'users' table.")
  
# Function that allows SQL SELECT command to be use
def get_by_puuid(keyVal, puuid):
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Execute a SELECT query with a WHERE clause to retrieve the keyVal value
    cursor.execute(f'SELECT {keyVal} FROM users WHERE puuid = ?', (puuid,))

    # Fetch the result
    
    returnVal = cursor.fetchone()

    # Close the connection
    conn.close()

    if returnVal:
        return returnVal[0]  # Extract the keyVal value from the result
    else:
        return None  # Player with the provided puuid not found

# Function that allows SQL UPDATE command to be use
def update_by_puuid(keyVal, new_keyVal_value, puuid):
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Execute an UPDATE query with a WHERE clause to update the keyVal value
    cursor.execute(f'UPDATE users SET {keyVal} = ? WHERE puuid = ?', (new_keyVal_value, puuid))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function that inserts game data into database
def insert_game_log(player_id, game_date, stats):
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Insert a new game log
    cursor.execute('''
        INSERT INTO game_logs (player_id, game_date, stats)
        VALUES (?, ?, ?)
    ''', (player_id, game_date, stats))

    # Delete oldest game logs if there are more than 10 for this player
    cursor.execute('''
        DELETE FROM game_logs
        WHERE id NOT IN (
            SELECT id FROM game_logs WHERE player_id = ? ORDER BY game_date DESC LIMIT 10
        ) AND player_id = ?
    ''', (player_id, player_id))
    print("Game log updated!")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function that gets the most recent game data of a player
def get_recent_game_stats(player_id, num_games=1):
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Retrieve the stats column for the specified player's most recent games
    cursor.execute('''
        SELECT stats
        FROM game_logs
        WHERE player_id = ?
        ORDER BY game_date DESC
        LIMIT ?
    ''', (player_id, num_games))

    game_stats = cursor.fetchall()

    # Close the connection
    conn.close()
    json_player_stats_list = []
    for i in range(num_games):
      json_player_stats = game_stats[i][0].replace("'", "\"")
      json_player_stats = json.loads(json_player_stats)
      json_player_stats_list.append(json_player_stats) 
    return json_player_stats_list

#-----------------------------------------------------------------------

#finds data from API
def fetch_data_from_api(puuid):
    global most_recent_eco
    # Example API endpoint
    url = f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/na/{puuid}?mode=competitive&size=1"
    response = requests.get(url)
    if response.status_code == 200:
      gameEcoCount = 0
      gameHeadshotsCount = 0
      gameBodyshotsCount = 0
      gameLegshotsCount = 0
      soup = BeautifulSoup(response.text, 'html.parser')
      site_json = json.loads(soup.text)


      if site_json["data"][0]["metadata"]["matchid"] != get_by_puuid("lastGame", puuid):
        player_stats = site_json["data"][0]["rounds"][0]["player_stats"]
        update_by_puuid("lastGame", site_json["data"][0]["metadata"]["matchid"], puuid)

        
        #grabs index of all the players making later processes faster
        playersIndices = {}
        for pos in range(0, 10):
          playersIndices[player_stats[pos]["player_puuid"]] = pos
          if player_stats[pos]["player_puuid"] == puuid:
            playerPos = pos
            playerName = player_stats[pos]['player_display_name']
  
        # iterates through rounds
        for roundNum in range(0, len(site_json["data"][0]["rounds"])):
          #adds headshots/bodyshots/legshots to user_data.db via users puuid
          headshots = int(site_json["data"][0]["rounds"][roundNum]["player_stats"][playerPos]["headshots"])
          
          gameHeadshotsCount += headshots          
          bodyshots = int(site_json["data"][0]["rounds"][roundNum]["player_stats"][playerPos]["bodyshots"])
          
          gameBodyshotsCount += bodyshots
          legshots = int(site_json["data"][0]["rounds"][roundNum]["player_stats"][playerPos]["legshots"])
          
          gameLegshotsCount += legshots
          try:
            update_by_puuid("headshots", get_by_puuid("headshots", puuid)+headshots, puuid)
            update_by_puuid("bodyshots", get_by_puuid("bodyshots", puuid)+bodyshots, puuid)
            update_by_puuid("legshots", get_by_puuid("legshots", puuid)+legshots, puuid)
          except:
            True
          #checks if player gets a kill that round
          kill_events = site_json["data"][0]["rounds"][roundNum]["player_stats"][playerPos]["kill_events"] 
          if (kill_events != False):
            killer_gun = site_json["data"][0]["rounds"][roundNum]["player_stats"][playersIndices[puuid]]["economy"]["weapon"]
            #iterates through all the kills the player gets that round
            for kill in kill_events:
              #gets victim's puuid then grabs their loadout_value
              victim_puuid = kill['victim_puuid']
              victim_gun = site_json["data"][0]["rounds"][roundNum]["player_stats"][playersIndices[victim_puuid]]["economy"]["weapon"]
              
              #adds an ecoKill to user_data.db via users puuid
              try:
                eco_checker[killer_gun["name"]][victim_gun["name"]]
                gameEcoCount += 1
                update_by_puuid("ecoKills", get_by_puuid("ecoKills", puuid)+1, puuid)
                if kill["kill_time_in_match"] > most_recent_eco[6] and site_json["data"][0]["metadata"]["game_start"] >= most_recent_eco[7]:
                  most_recent_eco = (kill["killer_display_name"], kill["damage_weapon_name"], kill["damage_weapon_assets"]["display_icon"], kill["victim_display_name"], victim_gun["name"], victim_gun["assets"]["display_icon"], kill["kill_time_in_match"], site_json["data"][0]["metadata"]["game_start"]) 
            
              except:
                True

        total_game_stats_dict ={"ecoKills":gameEcoCount, "headshots":gameHeadshotsCount, "bodyshots":gameBodyshotsCount, "legshots":gameLegshotsCount}
        total_game_stats = str({"ecoKills":gameEcoCount, "headshots":gameHeadshotsCount, "bodyshots":gameBodyshotsCount, "legshots":gameLegshotsCount})
        return total_game_stats_dict

        
        # CHECK IF USER IS IN DATA BASE ---------------------------------
        # IF NOT ADD THEM
        if get_by_puuid('id', puuid) is None:
          return [{"name": playerName[:playerName.index('#')], "puuid":puuid, "ecoKills":gameEcoCount, "headshots": gameHeadshotsCount, "bodyshots":gameBodyshotsCount, "legshots":gameLegshotsCount}]
        else:
          insert_game_log(get_by_puuid('id',puuid), site_json["data"][0]["metadata"]["game_start"], total_game_stats)
          
        # ---------------------------------------------------------------
        
    else:
      #if api is down then gives us the code; a slightly better try except statement
      print(f"Error Status code: {response.status_code}")

def get_puuid(name, tag):
  url = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    site_json = json.loads(soup.text)
    return site_json["data"]["puuid"]
  else:
    print(f"Error Status code: {response.status_code}")

#prints the entire database
"""
# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Execute a SELECT query to retrieve all data from the 'users' table
cursor.execute('SELECT * FROM users')

# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the retrieved data
for row in rows:
    print("ID:", row[0])
    print("Username:", row[1])
    print("PUUID:", row[2])
    print("Eco Kills:", row[3])
    print("Headshots:", row[4])
    print("Bodyshots:", row[5])
    print("Legshots:", row[6])
    print("Latest Match Id:", row[7])
    print("--------------------")

# Close the connection
conn.close()
"""

puuids = get_all_puuids()
#for username in puuids:
  #fetch_data_from_api(puuids[username])
  #print(f'User {username} has been update')
#INFINITY LOOP ONCE WE DONZO YAYAYAYAYA
#while True:
    #for username in puuids:
      #fetch_data_from_api(puuids[username])
      #print(f'User {username} has been update')
    #time.sleep(1800)  # 30 minutes in seconds


#grabs stats from last game in players logs
for i in range(1,14):
  player_stats = get_recent_game_stats(i,2)
  #json_player_stats = player_stats[0][0].replace("'", "\"")
  #json_player_stats = json.loads(json_player_stats)
  print(f"{i}:{player_stats[0]['ecoKills']}")
