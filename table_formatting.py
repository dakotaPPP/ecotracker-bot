#shows format of the sql tables when they were created/updated
"""
# Connect to the SQLite database (or create if it doesn't exist)

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create a table named 'users'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        puuid TEXT,
        ecoKills INTEGER,
        headshots INTEGER,
        bodyshots INTEGER,
        legshots INTEGER
        lastGame TEXT
    )
''')

conn.commit()
conn.close()
print("SQLite table 'users' has been created.")


# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create the 'game_logs' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_logs (
        id INTEGER PRIMARY KEY,
        player_id INTEGER,
        game_date INTEGER,
        stats TEXT,
        FOREIGN KEY (player_id) REFERENCES users (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'game_logs' has been created.")
"""

#puuids = {'plumyum':'cf4ab194-525e-5112-8914-4a72bcb5947b','Taevion':'85419e73-9077-5bf9-b7dc-683e19255b17','blum':'3665ab1a-8ab2-5d30-8a80-1daad1c773fa','Silly Baby':'073d7b29-ec93-5236-b0db-3fa4eaf6c0db','bruce':'f113f438-161a-5042-924d-2b82f8a28432','HenHen':'d30111a9-c151-5850-810b-00c93b31a94b','NUT Hunter40':'6b2240b0-f5e7-510d-a5f1-4d19b99c8364','mwe':'0ec81c7b-591d-5b1f-bec2-1831dc5ba035','Icydog':'2ee6cfbb-0647-5f7e-85d3-f8e3cbd1bd7d','TrendUniverse':'5b3337f3-09f4-59f6-870d-2cd127fcd000','Zammey':'bc8a014f-f3aa-58fc-9722-c50fb10d48cc','JojoTheDodo':'f2eb9e35-2006-591c-9bd3-2315d232cf39','Scoxy':'309aafac-20ec-5331-9fa5-7d7cb6da2d35'}