from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from dotenv import load_dotenv

# change to STAGE if needed
ENVIRONMENT = 'DEV'
# ENVIRONMENT = 'STAGE'

insert_DEV_query = '''
    INSERT INTO player (PLAYER_ID, PLAYER_LAST_NAME, PLAYER_FIRST_NAME, PLAYER_SLUG)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    PLAYER_LAST_NAME = VALUES(PLAYER_LAST_NAME),
    PLAYER_FIRST_NAME = VALUES(PLAYER_FIRST_NAME),
    PLAYER_SLUG = VALUES(PLAYER_SLUG)
    '''

insert_STAGE_query = '''
    INSERT INTO nba_player (PLAYER_ID, PLAYER_LAST_NAME, PLAYER_FIRST_NAME, PLAYER_SLUG)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    PLAYER_LAST_NAME = VALUES(PLAYER_LAST_NAME),
    PLAYER_FIRST_NAME = VALUES(PLAYER_FIRST_NAME),
    PLAYER_SLUG = VALUES(PLAYER_SLUG)
    '''

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

# Insert or update data from gleague / nba dataframe into player table
for _, row in g_league_players.iterrows():
    if ENVIRONMENT == 'DEV':
        insert_query = insert_DEV_query
    elif ENVIRONMENT == 'STAGE':
        insert_query = insert_STAGE_query
    cursor.execute(insert_query, (row['PERSON_ID'], row['PLAYER_LAST_NAME'], row['PLAYER_FIRST_NAME'], row['PLAYER_SLUG']))

conn.commit()
conn.close()
