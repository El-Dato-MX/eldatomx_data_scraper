from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerindex
from utils.db_connection import connect_to_database
from utils.constants import insert_to_player_stats_table_query
from dotenv import load_dotenv

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

g_league_players = playerindex.PlayerIndex(league_id=20).get_data_frames()[0]
nba_players = playerindex.PlayerIndex().get_data_frames()[0]

for _, row in g_league_players.iterrows():
    player_career_stats = playercareerstats.PlayerCareerStats(row['PERSON_ID']).get_data_frames()[0]
    for _, row in player_career_stats.iterrows():
        cursor.execute(insert_to_player_stats_table_query, (
            row['PLAYER_ID'], row['SEASON_ID'], row['LEAGUE_ID'], row['TEAM_ID'], row['TEAM_ABBREVIATION'],
            row['PLAYER_AGE'], row['GP'], row['GS'], row['MIN'], row['FGM'], row['FGA'], row['FG_PCT'], row['FG3M'],
            row['FG3A'],
            row['FG3_PCT'], row['FTM'], row['FTA'], row['FT_PCT'], row['OREB'], row['DREB'], row['REB'], row['AST'],
            row['STL'],
            row['BLK'], row['TOV'], row['PF'], row['PTS']
        ))

conn.commit()
conn.close()