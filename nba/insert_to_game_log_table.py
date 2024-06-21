from nba_api.stats.endpoints import leaguegamelog
from utils.db_connection import connect_to_database
from dotenv import load_dotenv
from utils.constants import insert_to_game_log_table_query

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

leaguelog = leaguegamelog.LeagueGameLog().get_data_frames()[0]

for _, row in leaguelog.iterrows():
    cursor.execute(insert_to_game_log_table_query, (
        row['SEASON_ID'], row['TEAM_ID'], row['GAME_ID'],
        row['GAME_DATE'], row['MATCHUP'], row['WL'], row['MIN'], row['FGM'], row['FGA'],
        row['FG_PCT'], row['FG3M'], row['FG3A'], row['FG3_PCT'],
        row['FTM'], row['FTA'], row['FT_PCT'], row['OREB'], row['DREB'], row['REB'],
        row['AST'], row['STL'], row['BLK'], row['TOV'], row['PF'], row['PTS'],
        row['PLUS_MINUS']
    ))

conn.commit()
conn.close()
