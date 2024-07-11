from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from utils.constants import insert_to_player_game_log_table_query
from dotenv import load_dotenv
from datetime import datetime

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

def parse_date(date_string):
    # Parse the date string and format it as YYYY-MM-DD
    return datetime.strptime(date_string, "%b %d, %Y").strftime("%Y-%m-%d")

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]



for _, row in nba_players.iterrows():
    player_game_logs = playergamelog.PlayerGameLog(row['PERSON_ID']).get_data_frames()[0]
    for _, row in player_game_logs.iterrows():
        parsed_date = parse_date(row['GAME_DATE'])
        cursor.execute(insert_to_player_game_log_table_query, (
            row['SEASON_ID'], row['Player_ID'], row['Game_ID'], parsed_date, row['MATCHUP'], row['WL'],
            row['MIN'], row['FGM'], row['FGA'], row['FG_PCT'], row['FG3M'], row['FG3A'], row['FG3_PCT'],
            row['FTM'], row['FTA'], row['FT_PCT'], row['OREB'], row['DREB'], row['REB'], row['AST'],
            row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS'], row['PLUS_MINUS']
        ))

conn.commit()
conn.close()