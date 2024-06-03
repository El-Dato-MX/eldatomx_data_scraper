from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from dotenv import load_dotenv

load_dotenv()

conn, cursor = connect_to_database()

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

# Insert or update data from gleague dataframe into player table
for _, row in nba_players.iterrows():
    insert_query = '''
    INSERT INTO player (PLAYER_ID, PLAYER_LAST_NAME, PLAYER_FIRST_NAME, PLAYER_SLUG)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    PLAYER_LAST_NAME = VALUES(PLAYER_LAST_NAME),
    PLAYER_FIRST_NAME = VALUES(PLAYER_FIRST_NAME),
    PLAYER_SLUG = VALUES(PLAYER_SLUG)
    '''
    cursor.execute(insert_query, (row['PERSON_ID'], row['PLAYER_LAST_NAME'], row['PLAYER_FIRST_NAME'], row['PLAYER_SLUG']))

conn.commit()
conn.close()
