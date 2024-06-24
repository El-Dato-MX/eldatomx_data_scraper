from utils.db_connection import connect_to_database
from utils.constants import insert_to_mlb_player_table_query
from dotenv import load_dotenv
import pandas as pd
from dateutil import parser

ENVIRONMENT = 'DEV'

load_dotenv()

conn, cursor = connect_to_database(environment=ENVIRONMENT)

players = pd.read_csv('/Users/Diego/Desktop/SFBB Player ID Map - PLAYERIDMAP.csv')

# Insert or update data from gleague / nba dataframe into player table
for _, row in players.iterrows():
    # Convert BIRTHDATE to date object
    birthdate = parser.parse(row['BIRTHDATE']).date()

    # Create a tuple with the row data
    data_to_insert = (
        row['IDPLAYER'], row['PLAYERNAME'], birthdate, row['FIRSTNAME'], row['LASTNAME'],
        row['TEAM'], row['LG'], row['POS'], row['IDFANGRAPHS'], row['FANGRAPHSNAME'],
        row['MLBID'], row['MLBNAME'], row['CBSID'], row['CBSNAME'], row['RETROID'],
        row['BREFID'], row['NFBCID'], row['NFBCNAME'], row['ESPNID'], row['ESPNNAME'],
        row['KFFLNAME'], row['DAVENPORTID'], row['BPID'], row['YAHOOID'], row['YAHOONAME'],
        row['MSTRBLLNAME'], row['BATS'], row['THROWS'], row['FANTPROSNAME'],
        row['LASTCOMMAFIRST'], row['ROTOWIREID'], row['FANDUELNAME'], row['FANDUELID'],
        row['DRAFTKINGSNAME'], row['OTTONEUID'], row['HQID'], row['RAZZBALLNAME'],
        row['FANTRAXID'], row['FANTRAXNAME'], row['ROTOWIRENAME'], row['ALLPOS'],
        row['NFBCLASTFIRST'], row['ACTIVE'], row['UNDERDOG'], row['RAZZBALLID']
    )

    # Execute the query
    cursor.execute(insert_to_mlb_player_table_query, data_to_insert)

conn.commit()
conn.close()
