# Name: Dallin McRae
# Enter your python code below. Replace this line with a description.
import random
import datetime
from datetime import date, timedelta

class SoccerTeam:
    def __init__(self, team_number, team_name, wins = 0, losses = 0, goals_scored = 0, goals_allowed = 0):
        self.team_number = team_number
        self.team_name = team_name
        self.__wins = wins # makes the variable private
        self.__losses = losses # makes the variable private
        self.goals_scored = goals_scored
        self.goals_allowed = goals_allowed

    def record_win(self): # Adds 1 to the win
        self.__wins += 1 
    def record_loss(self): # Adds 1 to the loss
        self.__losses += 1
   
    def get_record_percentage(self):
        try:
            final_season_percentage = round((self.__wins/(self.__losses + self.__wins))*100)
            return final_season_percentage
        except ZeroDivisionError as e:
            return "You can't divide by 0"
        
    def get_team_info(self):
        print(f"Team Name: {self.team_name}\nSeason record: {self.__wins} - {self.__losses} (X%)\nTotal goals scored: {self.goals_scored} Total goals allowed: {self.goals_allowed}")

    def generate_score(self):
        random_number = random.randint(0, 3)
        return random_number

    def get_season_message(self):
        if self.get_record_percentage() > 74:
            print("Qualified for the NCAA Soccer Tournament!")
        elif self.get_record_percentage() > 49:
            print("You had a good season")
        else:
            print("Your team needs to practice!")



class SponsoredTeam(SoccerTeam):
    def __init__(self, team_number, team_name, sponsor_name):
        super().__init__(team_number, team_name)
        self.sponsor_name = sponsor_name
    
    def generate_score(self):
        random_number = random.randint(1, 3)
        return random_number

    def get_season_message(self):
        if self.get_record_percentage() > 74:
            print(f"Qualified for the NCAA Soccer Tournament! {self.sponsor_name} is very happy.")
        elif self.get_record_percentage() > 49:
            print(f"You had a good season. {self.sponsor_name} hopes you can do better.")
        else:
            print(f"Your team needs to practice! You are in danger of {self.sponsor_name} dropping you.")


class Game:
    def __init__(self, game_number, home_team, away_team, home_team_score = 0, away_team_score = 0):
        self.game_number = game_number
        self.game_date = date.today() + timedelta(days = self.game_number) # Instructions said to do this
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
    
    def get_game_status(self):
        return f"Results of game {self.game_number} on {self.game_date}: Home team {self.home_team.team_name} scored {self.home_team_score} - Away team {self.away_team.team_name} scored {self.away_team_score}."

    def play_game(self):
        print()
        x = True
        while x:
            self.home_team_score = self.home_team.generate_score()
            self.away_team_score = self.away_team.generate_score()
            if self.home_team_score == self.away_team_score:
                continue
            else:
                x = False
        self.home_team.goals_scored = self.home_team_score
        self.home_team.goals_allowed = self.away_team_score
        self.away_team.goals_scored = self.away_team_score
        self.away_team.goals_allowed = self.home_team_score
        if self.home_team_score > self.away_team_score:
            self.home_team.record_win()
            self.away_team.record_loss()
        else:
            self.home_team.record_loss()
            self.away_team.record_win()
        print(self.get_game_status())
        print()




###### LOGICAL FLOW  ########
continue_asking = True # To keep the loop running until an input is accepted
while continue_asking:
    try:
        num_soccer_team = int(input("Enter the number of soccer teams you want to enter (at least 2): ").strip())
        if num_soccer_team < 2:
            print("You must enter an integer of 2 or above. Try again.")
            continue # To start the loop over without chaning continue_asking to False
        continue_asking = False
    except ValueError as e:
        print("Invalid integer! Try again.")

teams = {}
for num in range(num_soccer_team):
    num += 1
    team_name = input(f"Enter a name for team {num}: ")
    sponsor = input(f"Enter Y if team {num} is sponsored, otherwise enter N (or anything else): ")
    if sponsor.strip().upper() == "Y":
        sponsor_name = input("Enter the name of your sponsor: ")
        team = SponsoredTeam(num, team_name, sponsor_name)
        teams[num] = team
    else:
        team = SoccerTeam(num, team_name)
        teams[num] = team
        pass



gum = 1
continue_asking_again = True
while continue_asking_again: ##The same kind of thing as ealier, just to make sure inputs are valid
        for key, value in teams.items(): #Show the teams
            print(f"{key}: {value.team_name}")
        hteam_input = input('Enter the team number of the HOME team or enter "exit" to end the season: ').strip().upper()
        if hteam_input == "EXIT":
                print("The soccer season is over!")
                break
        if hteam_input.isnumeric():
            hteam_input = int(hteam_input)
            if hteam_input > len(teams):
                print("Invalid team number! Try again.")
                continue
        else:
            print("Invalid team number! Try again.")
            continue
        # Away team input
        ateam_input = input('Enter the team number of the AWAY team or enter "exit" to end the season: ').strip().upper()
        if ateam_input == "EXIT":
                print("The soccer season is over!")
                break
        if ateam_input.isnumeric():
            ateam_input = int(ateam_input)
            if hteam_input == ateam_input:
                print("You can't choose the same team as the home and away team! Try again.")
                continue
            elif ateam_input > len(teams):
                print("Invalid team number! Try again.")
                continue  
        else:
            print("Invalid team number! Try again.")
            continue
        home_teamy = teams.get(hteam_input)
        away_teamy = teams.get(ateam_input)
        game = Game(gum, home_teamy, away_teamy)
        gum += 1
        game.play_game()
        





### POSTSEASON ####
while True:
    print()
    print(f"Postseason Menu: \n1: Go to Team Info Menu \n2: Go to Game Info Menu\nexit: End the program")
    menu_input = input("Enter an option: ").strip().upper()
    print()
    if menu_input.isnumeric():
        menu_input = int(menu_input)
        if menu_input == 1:
            print("Team Info Menu: ")
            for key, value in teams.items(): #Show the teams
                print(f"{key}: {value.team_name}")
            next_input = int(input('Enter a team number to see their info, or enter "exit" to go back to the Postseason Menu: ').strip().upper())
            glass = teams.get(next_input)
            glass.get_team_info()
    elif menu_input == 2:
        print('Enter a game number to see its info, or enter "exit" to go back to the Postseason Menu: ')
        break
    elif menu_input == "EXIT":

        print("Exiting the program.")
        break
    else:
        print("Invalid choice! Try again")
