#Desperate Defenders 
#Chan Yanliang (S10239777G)

import random
import sys

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    'num_of_row': 5,                # No of rows on field
    'num_of_col': 7,                # No of columns on field
    'field': [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]
    }


defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHealth': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       'display_name': 'ARCHR'
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      'display_name': 'WALL'
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'HP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves': 1,
                      'reward': 2,
                      'display_name': 'ZOMBI',
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'HP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves': 2,
                      'reward': 3,
                      'display_name': 'WWOLF',
                      }
            }


#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu(game_vars):
    #Printing out the menu
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")
    #loops till correct input is typed
    while True:
        menu_input = input('Your choice? ')
        if menu_input == '1':
            #Check if user would like to change game options
            option_input = input('Would you want to customize your game options (Y/N): ').upper()
            if option_input == 'Y':
                initialize_game(game_vars)
                try:
                    game_vars['monster_kill_target'] = int(input('Target monster to kill: '))
                except ValueError:
                    print('Invalid Input')
            else:
                print('Initializing game with default options')
                initialize_game(game_vars)
            return
        if menu_input == '2':
            load_game(game_vars)
            return
        if menu_input == '3':
            print('See you next time')
            sys.exit()
        print('Invalid Input')



#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    #print combat menu
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")
    # loops till player enter correct input
    while True:
        combat_input = input('Your choice?')
        if combat_input == '1':
            for i in range(len(game_vars['field'])):
                for j in range(4):
                    if game_vars['field'][i][j] ==  None:
                        buy_unit(game_vars)
                        return
            # In the event that all rows and columns are filled up with either defenders or monsters
            print('Board is full, buy unit unavalible')
            return
        elif combat_input == '2':
            return
        elif combat_input == '3':
            save_game(game_vars)
            continue
        elif combat_input == '4':
            print('See you next time')
            sys.exit()
        else:
            print('Invalid input')
            continue


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------
def draw_field(game_vars):
    row_alpha = 65 
    print('    1     2     3')

    row = ' +' + game_vars['num_of_col'] * '-----+'
    for i in game_vars['field']:
        print(row)
        layer1 = '|'
        layer2 = '|'
        for j in i:
            if j == None:
                layer1 += '     |'
                layer2 += '     |'
            else:
                layer1 += '{:<5}'.format(j[0]) + '|'
                layer2 += '{:^5}'.format(str(j[1]) + '/' + str(j[2])) + '|'
        print(chr(row_alpha) + layer1)
        print(' ' + layer2)
        row_alpha += 1
    print(row)

    #prints game varibles 
    print('Turn {:<8}Threat = [{:10}]   Danger Level: {}'.format(game_vars['turn'], (game_vars['threat'] * '-'), game_vars['danger_level']))
    print('Gold = {:<6}Monsters killed = {}/{}'.format(game_vars['gold'], game_vars['monsters_killed'], game_vars['monster_kill_target']))
    return


#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------
def place_unit(game_vars, defender):   
    while True:
        position_input = input('Place where? ').upper()
        try:
            if len(position_input) != 2:
                print('Invalid position')
                continue
            if ord(position_input[0]) < 65 or ord(position_input[0]) > (game_vars['num_of_row'] + 65) or int(position_input[1]) < 1 or int(position_input[1]) > 3:
                print('Invalid position')
                continue
        except ValueError:
            print('Invalid position')
            continue

        if game_vars['field'][ord(position_input[0])-65][int(position_input[1]) -1] != None:
            print('Position occupied')
            return False
                
        game_vars['field'][ord(position_input[0])-65][int(position_input[1])-1] = (defenders[defender]['display_name'], defenders[defender]['maxHP'], defenders[defender]['maxHP'])
        game_vars['gold'] -= defenders[defender]['price']    

        return True


#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(game_vars):   
    #Print buy unit menu
    print('What unit do you wish to buy? ')
    for i in range(len(defender_list)):
        name = defender_list[i]
        price = defenders[name]['price']
        print('{}. {} ({} gold)'.format(i + 1, name, price))
    print("{}. Don't Buy".format(i + 2))
    #Check if input is valid and player has enough gold
    while True:
        try:
            buy_input = int(input('Your choice: '))
        except ValueError:
            print('Invaild input')
            continue

        if buy_input < 1 and buy_input > (len(defender_list)+1):
            print('Invalid input')
            continue

        if buy_input == len(defender_list)+1:
            return

        defender = defender_list[buy_input-1]
        if game_vars['gold'] < defenders[defender]['price']:
            print('Not enough gold')
            continue

        if place_unit(game_vars, defender):
            return


#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(game_vars, monster_list):
    while True:
        lane = random.randint(0, len(game_vars['field']) - 1)  
        monster = monster_list[random.randint(0, len(monster_list) - 1)]
        if game_vars['field'][lane][len(game_vars['field'][lane]) - 1] == None:
            game_vars['field'][lane][len(game_vars['field'][lane]) - 1] = (monsters[monster]['display_name'], monsters[monster]['maxHP'], monsters[monster]['maxHP'])
            game_vars['num_monsters'] += 1
            return


#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(game_vars, row, col):
    for i in range(col+1,game_vars['num_of_col']):
        # no unit here
        if game_vars['field'][row][i] == None:
            continue
        # Checks if troop is a monster
        if game_vars['field'][row][i][0] in monster_list: 
            damage = random.randint(defenders[game_vars['field'][row][col][0]]['min_damage'], defenders[game_vars['field'][row][col][0]]['max_damage'])
            new_health = int(game_vars['field'][row][i][1]) - damage
            if new_health <= 0:
                # monster died from attack
                unit = game_vars['field'][row][i][0]
                game_vars['field'][row][i] = None
                game_vars['monsters_killed'] += 1
                game_vars['num_monsters'] -= 1
                game_vars['gold'] += monsters[unit]['reward']
                game_vars['threat'] += monsters[unit]['reward']
                print(f'{unit} has died in lane {chr(row+65)}')
                return
            else:
                game_vars['field'][row][i] = (game_vars['field'][row][i][0], new_health ,game_vars['field'][row][i][2])

                if damage != 0:
                    # monster suffer damages
                    print(game_vars['field'][row][col][0] + ' in lane ' + chr(row+65) + ' shoots ' + game_vars['field'][row][i][0] + ' for ' + str(damage) + ' damage!' )
                return
        

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(game_vars, row, col):
    monster = game_vars['field'][row][col][0]
    damage = random.randrange(monsters[monster]['min_damage'],monsters[monster]['max_damage'])
    moves = monsters[monster]['moves']
    for i in range(1, moves + 1):
        #event of player lose
        #monster reachs the end of the field
        if col - i < 0:
            print('A', monster, 'has reached the city! All is lost!  You have lost the game. :(')
            print('game over')
            sys.exit()
        
        #monster advances if the spot is empty
        if game_vars['field'][row][col - i] == None:
            game_vars['field'][row][col - i] = game_vars['field'][row][col - i + 1]
            game_vars['field'][row][col - (i - 1)] = None
            if i == 1:
                print(monster, 'in lane', str(chr(row+65)),'advances') 
            continue
        #monster deals damage to the defender unit
        if game_vars['field'][row][col - i][0] in defender_list: 
            new_health = int(game_vars['field'][row][col - i][1]) - damage
            unit = game_vars['field'][row][col - i][0]
            if new_health <= 0:
                # monster died from attack
                game_vars['field'][row][col - i] = None
                print(monster + ' in lane ' + chr(row+65) + ' hit ' + unit + ' for ' + str(damage) + ' damage!' )
                print(f'{unit} has died in lane {chr(row+65)}')
                return
            else:
                # defender suffer damages
                game_vars['field'][row][col - i] = (game_vars['field'][row][col - i][0], new_health ,game_vars['field'][row][col - i][2])
                print(monster + ' in lane ' + chr(row+65) + ' hit ' + unit + ' for ' + str(damage) + ' damage!' )
                return


#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game(game_vars):
    file = open('save.txt', 'w')
    file.write(str(game_vars))
    file.close()
    print("Game saved.")


#-----------------------------------------
# load_game()
# 
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    try:
        file = open('save.txt', 'r')
        data = file.read()
        file.close()
        data = data.strip('{')
        data = data.strip('}')
        index = data.find('field')
        parameters = data[:index-1]
        parameter_list = parameters.split(',')
        parameter_list.pop()

        for element in parameter_list:
            key_value_pair = element.split(':')
            try:
                game_vars.update({key_value_pair[0].strip("' "): int(key_value_pair[1].strip("' "))})
            except ValueError:
                print('Please key in valid input')
        field = data[index:]
        field = field.split(':')
        field = field[1].split(']')
        field.pop()
        field.pop()
        game_vars['field'] =[]
        for row in field:    
            field_row = []
            row = row.strip(', [')
            row_elements = row.split(',')
    
            i = 0
            while i < len(row_elements):
                if row_elements[i].strip() == 'None':
                    field_row.append(None)
                    i += 1
                else:
                    for j in range(i, i+3):
                        row_elements[j] = row_elements[j].strip("(') ")
                    field_row.append((row_elements[i].strip(), int(row_elements[i+1].strip("' ")), int(row_elements[i+2].strip(" '"))))
                    i += 3

            game_vars['field'].append(field_row)
            print("Game Loaded")
            return

    except FileNotFoundError:
        print("File not found")
        return

    except:
        print('File load error try again')
        return


#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game(game_vars):
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    game_vars['num_of_row'] = 5       
    game_vars['num_of_col'] = 7         
    game_vars['field'] = [[None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None],
                          [None, None, None, None, None, None, None]]
    return game_vars
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
show_main_menu(game_vars)
while True:
    # When theres no monster onn few, it spawns monster
    if game_vars["num_monsters"] == 0:
        spawn_monster(game_vars, monster_list)
    game_vars['turn'] += 1
    # If threat greater than 10 spawn monster 
    while game_vars['threat'] >= 10:
        spawn_monster(game_vars, monster_list)
        game_vars['threat'] -= 10
    # Increase danger level ever 12 turns
    if game_vars['turn'] % 12 == 0:
        game_vars['danger_level'] += 1
        # With the increase of danger levl, monsters become harder to kill and rewards are higher
        for monster in monster_list:
            monsters[monster]['HP'] += 1
            monsters[monster]['maxHP'] += 1
            monsters[monster]['min_damage'] += 1
            monsters[monster]['max_damage'] += 1
            monsters[monster]['reward'] += 1
    #If win condition is met
    if game_vars['monsters_killed'] == game_vars['monster_kill_target']:
        print('You have protected the city! You win!')
        sys.exit()
    draw_field(game_vars)
    show_combat_menu(game_vars)
    # Runs through every row and column to check is it is defender or monster
    for i in range(game_vars['num_of_row']):
        for j in range(game_vars['num_of_col']):
            if game_vars['field'][i][j] == None:
                continue
            if game_vars['field'][i][j][0] in defender_list:
                defender_attack(game_vars, i, j)
            else:
                monster_advance(game_vars, i, j)
                
    game_vars['gold'] += 1
    game_vars['threat'] += random .randint(1,game_vars['danger_level'])
