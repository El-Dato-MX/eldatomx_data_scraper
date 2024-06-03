from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from dotenv import load_dotenv

load_dotenv()

conn, cursor = connect_to_database()

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

for _, row in nba_players.iterrows():
    player_id = row['PERSON_ID']
    team_id = row['TEAM_ID']
    to_year = row['TO_YEAR']
    season = f"{to_year}-{str(int(to_year) + 1)[-2:]}"
    query = "SELECT ID FROM player_team WHERE PLAYER_ID = %s AND TEAM_ID = %s AND SEASON = %s"
    cursor.execute(query, (player_id, team_id, season))
    result = cursor.fetchone()
    if result:
        # Update existing record
        # query = "UPDATE player_team SET PLAYER_ID = %s, TEAM_ID = %s, SEASON = %s WHERE ID = %s"
        # cursor.execute(query, (player_id, team_id, season, result[0]))
        pass
    else:
        # Insert new record
        query = "INSERT INTO player_team (PLAYER_ID, TEAM_ID, SEASON) VALUES (%s, %s, %s)"
        cursor.execute(query, (player_id, team_id, season))

conn.commit()
conn.close()
