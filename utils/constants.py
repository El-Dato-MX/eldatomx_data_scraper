insert_to_player_table_query = '''
    INSERT INTO nba_player (PLAYER_ID, PLAYER_LAST_NAME, PLAYER_FIRST_NAME, PLAYER_SLUG)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    PLAYER_LAST_NAME = VALUES(PLAYER_LAST_NAME),
    PLAYER_FIRST_NAME = VALUES(PLAYER_FIRST_NAME),
    PLAYER_SLUG = VALUES(PLAYER_SLUG)
    '''

insert_to_team_table_query = '''
        INSERT INTO nba_team (TEAM_ID, TEAM_ABBREVIATION, TEAM_NICKNAME, TEAM_CITY)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        TEAM_ABBREVIATION = VALUES(TEAM_ABBREVIATION),
        TEAM_NICKNAME = VALUES(TEAM_NICKNAME),
        TEAM_CITY = VALUES(TEAM_CITY)
        '''

select_from_player_team_table_query = "SELECT ID FROM player_team WHERE PLAYER_ID = %s AND TEAM_ID = %s AND SEASON = %s"

insert_to_player_team_table_query = "INSERT INTO player_team (PLAYER_ID, TEAM_ID, SEASON) VALUES (%s, %s, %s)"

insert_to_player_shotchart_table_query = '''
INSERT INTO player_shotchart (
    GRID_TYPE,
    GAME_ID,
    GAME_EVENT_ID,
    PLAYER_ID,
    TEAM_ID,
    PERIOD,
    MINUTES_REMAINING,
    SECONDS_REMAINING,
    EVENT_TYPE,
    ACTION_TYPE,
    SHOT_TYPE,
    SHOT_ZONE_BASIC,
    SHOT_ZONE_AREA,
    SHOT_ZONE_RANGE,
    SHOT_DISTANCE,
    LOC_X,
    LOC_Y,
    SHOT_ATTEMPTED_FLAG,
    SHOT_MADE_FLAG,
    GAME_DATE,
    HTM,
    VTM
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    GRID_TYPE = VALUES(GRID_TYPE),
    GAME_ID = VALUES(GAME_ID),
    GAME_EVENT_ID = VALUES(GAME_EVENT_ID),
    PLAYER_ID = VALUES(PLAYER_ID),
    TEAM_ID = VALUES(TEAM_ID),
    PERIOD = VALUES(PERIOD),
    MINUTES_REMAINING = VALUES(MINUTES_REMAINING),
    SECONDS_REMAINING = VALUES(SECONDS_REMAINING),
    EVENT_TYPE = VALUES(EVENT_TYPE),
    ACTION_TYPE = VALUES(ACTION_TYPE),
    SHOT_TYPE = VALUES(SHOT_TYPE),
    SHOT_ZONE_BASIC = VALUES(SHOT_ZONE_BASIC),
    SHOT_ZONE_AREA = VALUES(SHOT_ZONE_AREA),
    SHOT_ZONE_RANGE = VALUES(SHOT_ZONE_RANGE),
    SHOT_DISTANCE = VALUES(SHOT_DISTANCE),
    LOC_X = VALUES(LOC_X),
    LOC_Y = VALUES(LOC_Y),
    SHOT_ATTEMPTED_FLAG = VALUES(SHOT_ATTEMPTED_FLAG),
    SHOT_MADE_FLAG = VALUES(SHOT_MADE_FLAG),
    GAME_DATE = VALUES(GAME_DATE),
    HTM = VALUES(HTM),
    VTM = VALUES(VTM);
'''

insert_to_game_log_table_query = '''
    INSERT INTO nba_game_log (
        SEASON_ID, TEAM_ID, GAME_ID,
        GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
        FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS,
        PLUS_MINUS
    ) VALUES (
        %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s,
        %s
    ) ON DUPLICATE KEY UPDATE
        SEASON_ID = VALUES(SEASON_ID),
        TEAM_ID = VALUES(TEAM_ID),
        GAME_DATE = VALUES(GAME_DATE),
        MATCHUP = VALUES(MATCHUP),
        WL = VALUES(WL),
        MIN = VALUES(MIN),
        FGM = VALUES(FGM),
        FGA = VALUES(FGA),
        FG_PCT = VALUES(FG_PCT),
        FG3M = VALUES(FG3M),
        FG3A = VALUES(FG3A),
        FG3_PCT = VALUES(FG3_PCT),
        FTM = VALUES(FTM),
        FTA = VALUES(FTA),
        FT_PCT = VALUES(FT_PCT),
        OREB = VALUES(OREB),
        DREB = VALUES(DREB),
        REB = VALUES(REB),
        AST = VALUES(AST),
        STL = VALUES(STL),
        BLK = VALUES(BLK),
        TOV = VALUES(TOV),
        PF = VALUES(PF),
        PTS = VALUES(PTS),
        PLUS_MINUS = VALUES(PLUS_MINUS)
'''