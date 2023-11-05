from constants import PLAYERS, TEAMS


def clean_data(players):
    cleaned = []
    for player in players:
        fixed = {}
        fixed['name'] = player['name']
        # Get the height as a number from a string like "48 inches".
        height = player['height'].split(' ')[0]
        fixed['height'] = int(height)
        # Check if the player's experience is 'yes' and convert to True/False.
        fixed['experience'] = player['experience'].lower() == 'yes'
        # Split the guardians on 'and' and make a list.
        fixed['guardians'] = player['guardians'].split(' and ')
        cleaned.append(fixed)
    return cleaned


def balance_teams(players, teams):
    experienced = []
    inexperienced = []
    # Separate players into experienced and inexperienced lists.
    for player in players:
        if player['experience']:
            experienced.append(player)
        else:
            inexperienced.append(player)

    num_players_per_team = len(players) // len(teams)
    # Create a dictionary to hold the balanced teams.
    balanced_teams = {team: [] for team in teams}

    for team in teams:
        # Distribute players to each team until the number of players per team is reached.
        while len(balanced_teams[team]) < num_players_per_team:
            if experienced:
                balanced_teams[team].append(experienced.pop(0))
            if inexperienced and len(balanced_teams[team]) < num_players_per_team:
                balanced_teams[team].append(inexperienced.pop(0))

    return balanced_teams


def main():
    # Clean the data and prepare the teams.
    cleaned_players = clean_data(PLAYERS)
    teams = TEAMS
    balanced_teams = balance_teams(cleaned_players, teams)

    print("BASKETBALL TEAM STATS TOOL")
    print("---- MENU ----")

    # Start the main program loop.
    while True:
        choice = input("Press '1' to display team stats or '2' to quit: ")

        if choice == '1':
            for idx, team in enumerate(teams):
                print(f"{idx + 1}. {team}")

            team_choice = input("Choose the team by entering a number: ")
            try:
                team_choice = int(team_choice) - 1
                # Ensure the selected team number is valid.
                if 0 <= team_choice < len(teams):
                    team_name = teams[team_choice]
                    team_players = balanced_teams[team_name]
                    # Compile a list of player names and guardians.
                    team_players = sorted(team_players, key=lambda x: x['height'])
                    player_names = [player['name'] for player in team_players]
                    guardians = []
                    for player in team_players:
                        guardians.extend(player['guardians'])
                    # Count experienced and inexperienced players.
                    num_experienced = sum(1 for player in team_players if player['experience'])
                    num_inexperienced = sum(1 for player in team_players if not player['experience'])
                    total_players = len(team_players)
                    total_height = sum(player['height'] for player in team_players)
                    # Calculate the average height of the players.
                    average_height = total_height / total_players

                    # Display the team stats.
                    print(f"\nTeam: {team_name}")
                    print(f"Total players: {total_players}")
                    print("Player names:", ", ".join(player_names))
                    print(f"Number of inexperienced players: {num_inexperienced}")
                    print(f"Number of experienced players: {num_experienced}")
                    print(f"Average height: {average_height:.2f} inches")
                    print("Guardians:", ", ".join(guardians))
                else:
                    print("That team number is not valid.")
            except ValueError:
                # Catch non-integer inputs for the team choice.
                print("Please enter a number for the team choice.")
        elif choice == '2':
            # Exit the program.
            print("Goodbye!")
            break
        else:
            # Handle invalid options.
            print("Please enter '1' to display the team stats or '2' to quit.")


if __name__ == "__main__":
    main()
