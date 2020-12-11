import mysql.connector
import csv


class Player:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.attributes = {'First Name': raw_data[0], 'Last Name': raw_data[1], 'League': raw_data[62],
                           'Team Name': raw_data[60],
                           'Team Nickname': raw_data[61], 'Aggression': raw_data[9],
                           'Bravery': raw_data[10], 'Determination': raw_data[11], 'Teamplayer': raw_data[12],
                           'Leadership': raw_data[13], 'Temperament': raw_data[14], 'Professionalism': raw_data[15],
                           'Mental Toughness': raw_data[16], 'Goalie Stamina': raw_data[17],
                           'Acceleration': raw_data[18],
                           'Agility': raw_data[19], 'Balance': raw_data[20], 'Speed': raw_data[21],
                           'Stamina': raw_data[22],
                           'Strength': raw_data[23], 'Fighting': raw_data[24], 'Screening': raw_data[25],
                           'Getting Open': raw_data[26], 'Passing': raw_data[27], 'Puck Handling': raw_data[28],
                           'Shooting Accuracy': raw_data[29], 'Shooting Range': raw_data[30],
                           'Offensive Read': raw_data[31], 'Checking': raw_data[32], 'Faceoffs': raw_data[33],
                           'Hitting': raw_data[34], 'Positioning': raw_data[35], 'Shot Blocking': raw_data[36],
                           'Stickchecking': raw_data[37], 'Defensive Read': raw_data[38], 'G Positioning': raw_data[39],
                           'G Passing': raw_data[40], 'G Pokecheck': raw_data[41], 'Blocker': raw_data[42],
                           'Glove': raw_data[43], 'Rebound': raw_data[44], 'Recovery': raw_data[45],
                           'G Puckhandling': raw_data[46], 'Low Shots': raw_data[47], 'G Skating': raw_data[48],
                           'Reflexes': raw_data[49]}
        self.attributes['Position'] = self.get_position()
        self.attributes['TPE'] = self.calculate_tpe()

    def calculate_tpe(self):
        tpe_total = 0
        # for value in self.attributes.values():
        for attribute in self.attributes:
            if self.attributes['Position'] == 'Goalie':
                no_count = ['Aggression', 'Determination', 'Teamplayer', 'Leadership', 'Professionalism']
            else:
                no_count = ['Determination', 'Teamplayer', 'Leadership', 'Temperament', 'Professionalism']
            value = self.attributes[attribute]
            if isinstance(value, int) and attribute not in no_count:
                current_level = 0
                while value > 17:
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 40)
                current_level = 0
                while value > 15:
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 25)
                current_level = 0
                while value > 13:
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 15)
                current_level = 0
                while value > 11:
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 8)
                current_level = 0
                while value > 9 and attribute != 'Stamina':
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 5)
                current_level = 0
                while value > 7 and attribute != 'Stamina':
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 2)
                current_level = 0
                while value > 5 and attribute != 'Stamina':
                    value -= 1
                    current_level += 1
                tpe_total += (current_level * 1)
        return tpe_total

    def get_position(self):
        positions = [self.raw_data[3], self.raw_data[4], self.raw_data[5], self.raw_data[6], self.raw_data[7],
                     self.raw_data[8]]
        position = ''
        if positions.index(max(positions)) == 0:
            position = 'Goalie'
        elif positions.index(max(positions)) == 1:
            position = 'Left Defender'
        elif positions.index(max(positions)) == 2:
            position = 'Right Defender'
        elif positions.index(max(positions)) == 3:
            position = 'Left Wing'
        elif positions.index(max(positions)) == 4:
            position = 'Center'
        elif positions.index(max(positions)) == 5:
            position = 'Right Wing'
        return position


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="password",
        database="fhm6"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT fhm6.player_master.`First Name`, fhm6.player_master.`Last Name`, fhm6.player_ratings.*, "
                     "fhm6.team_data.Name, fhm6.team_data.Nickname, fhm6.league_data.Name AS Expr1 \
                      FROM fhm6.player_ratings \
                      INNER JOIN fhm6.player_master \
                        ON fhm6.player_ratings.PlayerId = fhm6.player_master.PlayerId \
                          INNER JOIN fhm6.team_data \
                            ON fhm6.player_master.TeamId = fhm6.team_data.TeamId \
                              INNER JOIN fhm6.league_data \
                                ON fhm6.team_data.LeagueId = fhm6.league_data.LeagueId \
                                  ORDER BY fhm6.league_data.Name")

    myresult = mycursor.fetchall()

    player_list = list()
    count = 0

    # player = Player(myresult[1])
    # player_list.append(player.attributes)

    for x in myresult:
        player = Player(x)
        player_list.append(player.attributes)
        count += 1
    csv_file = 'fhm6_all_players.csv'
    csv_columns = player_list[0].keys()
    with open(csv_file, 'w+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in player_list:
            writer.writerow(data)
    print("Processed", count, "players.")
