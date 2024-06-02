from nba_api.stats.endpoints import teamdetails
import pandas as pd
from utils.db_connection import connect_to_database
from dotenv import load_dotenv

load_dotenv()

conn, cursor = connect_to_database()

teams = pd.read_csv('unique_team_ids.csv')

for _, row in teams.iterrows():
    if row['TEAM_ID'] == 0:
        team_id = 0
        team_abbreviation = 'NA'
        team_nickname = 'NA'
        team_city = 'NA'
    else:
        individual_team = teamdetails.TeamDetails(row['TEAM_ID']).get_data_frames()[0]
        # Extract values from the Series
        team_id = int(individual_team['TEAM_ID'].values[0])
        team_abbreviation = individual_team['ABBREVIATION'].values[0]
        team_nickname = individual_team['NICKNAME'].values[0]
        team_city = individual_team['CITY'].values[0]
    insert_query = '''
        INSERT INTO team (TEAM_ID, TEAM_ABBREVIATION, TEAM_NICKNAME, TEAM_CITY)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        TEAM_ABBREVIATION = VALUES(TEAM_ABBREVIATION),
        TEAM_NICKNAME = VALUES(TEAM_NICKNAME),
        TEAM_CITY = VALUES(TEAM_CITY)
        '''
    cursor.execute(insert_query, (team_id, team_abbreviation, team_nickname, team_city))
    conn.commit()

conn.close()
