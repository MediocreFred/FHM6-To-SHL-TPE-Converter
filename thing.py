import mysql.connector

class Player:
  def __init__(self, raw_data):
    self.attributes = {'first_name': raw_data[0], 'last_name': raw_data[1], 'aggression': raw_data[9],
                       'bravery': raw_data[10], 'Determination': raw_data[11]}



mydb = mysql.connector.connect(
  host="192.168.10.53",
  user="ckalinowski",
  passwd="Windforce",
  database="fhm6"
)


mycursor = mydb.cursor()

mycursor.execute("SELECT fhm6.player_master.`First Name`, fhm6.player_master.`Last Name`, fhm6.player_ratings.*, fhm6.team_data.Name, fhm6.team_data.Nickname, fhm6.league_data.Name AS Expr1 \
                  FROM fhm6.player_ratings \
                  INNER JOIN fhm6.player_master \
                    ON fhm6.player_ratings.PlayerId = fhm6.player_master.PlayerId \
                      INNER JOIN fhm6.team_data \
                        ON fhm6.player_master.TeamId = fhm6.team_data.TeamId \
                          INNER JOIN fhm6.league_data \
                            ON fhm6.team_data.LeagueId = fhm6.league_data.LeagueId \
                              ORDER BY fhm6.league_data.Name")

myresult = mycursor.fetchall()



for x in myresult:
  player = Player(x)
  print(player.attributes)






#with open('player.txt', 'w+') as file:
#  for x in myresult:
#    file.write(str(x)+'\n')