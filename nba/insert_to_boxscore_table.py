from nba_api.stats.endpoints import boxscoreadvancedv3
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import teamyearbyyearstats

pcs = playercareerstats.PlayerCareerStats(201142).get_data_frames()[0]
tyby = teamyearbyyearstats.TeamYearByYearStats(1610612760).get_data_frames()[0]
leaguelog = leaguegamelog.LeagueGameLog().get_data_frames()[0]

unique_game_ids = leaguelog['GAME_ID'].unique()

for game_id in unique_game_ids:
    boxscore = boxscoreadvancedv3.BoxScoreAdvancedV3(game_id).get_data_frames()[0]
    print(boxscore)

print()

