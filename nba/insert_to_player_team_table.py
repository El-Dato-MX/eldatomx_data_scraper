from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from dotenv import load_dotenv
from utils.constants import select_from_player_team_table_query, insert_to_player_team_table_query

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

# Insert or update data from gleague / nba dataframe into player_tem table
for _, row in nba_players.iterrows():
    player_id = row['PERSON_ID']
    team_id = row['TEAM_ID']
    # check this to season id
    to_year = row['TO_YEAR']
    season = f"{to_year}-{str(int(to_year) + 1)[-2:]}"
    cursor.execute(select_from_player_team_table_query, (player_id, team_id, season))
    result = cursor.fetchone()
    if result:
        # Update existing record
        # query = "UPDATE player_team SET PLAYER_ID = %s, TEAM_ID = %s, SEASON = %s WHERE ID = %s"
        # cursor.execute(query, (player_id, team_id, season, result[0]))
        pass
    else:
        # Insert new record
        cursor.execute(insert_to_player_team_table_query, (player_id, team_id, season))

conn.commit()
conn.close()
