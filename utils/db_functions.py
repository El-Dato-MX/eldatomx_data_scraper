import pandas as pd

def get_player_team_df(cursor):
    query = "SELECT * FROM player_team"
    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    return df
