from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from utils.constants import insert_to_player_table_query
from dotenv import load_dotenv

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

# Insert or update data from gleague / nba dataframe into player table
for _, row in g_league_players.iterrows():
    cursor.execute(insert_to_player_table_query, (row['PERSON_ID'], row['PLAYER_LAST_NAME'], row['PLAYER_FIRST_NAME'], row['PLAYER_SLUG']))

conn.commit()
conn.close()
