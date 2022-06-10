from random import randrange
from setup import Setup
from tree import TreeNode, Tree
from time import time
from math import inf


class State(object):

    def __init__(self):
        self._setup = Setup()

    def is_closed_morris(self, current_coordinates, coordinates, current_player, _print): #coordinates je lista koordinata
        morries = []
        
       # morries.append(self._setup._morrises.get(current_coordinates))
        for item in self._setup._chained_morrises[current_coordinates]:
            morries.append(item)
        
        vec_postoji = False
        for morris in morries:
            for coor in item:
                if coor == current_coordinates:
                    vec_postoji = True
                    break

        for morris in morries:
            if vec_postoji == False:
                morris.insert(0, current_coordinates)

        for item in morries: 
            if _print == True: print("kombinacije mogucih mica: " + str(item))
            poklapanja = 0
            for pozicija in item:
                for koordinata in coordinates:
                    if pozicija == koordinata:
                        poklapanja += 1
                        break
            if poklapanja == 3:
                if _print == True: print("Napravljena mica.")
                if current_player == "W":
                    return True, 1
                return True, -1
        return False, 0

    def number_of_morrises(self, player_morrises, opponents_morrises):
        return player_morrises - opponents_morrises

    def num_of_blocked_pieces(self, player_blocked_pieces, opponent_blocked_pieces):
        return opponent_blocked_pieces - player_blocked_pieces

    def num_of_two_piece_config(self, your_pieces, opponents_pieces):
        return abs(your_pieces-opponents_pieces)

    def num_of_pieces(self, player_pieces, opponent_pieces):
        return player_pieces - opponent_pieces

    def num_of_three_piece_config(self, your_pieces, opponents_pieces):
        return abs(your_pieces-opponents_pieces)

    def num_double_morris(self, your_pieces, opponents_pieces): #zajebancija
        return abs(your_pieces-opponents_pieces)

    def is_end(self, number_of_player_pieces_left, number_of_opponent_pieces_left):
        #print(number_of_player_pieces_left, number_of_opponent_pieces_left)
        
        if number_of_player_pieces_left == 2:
            print("Izgubili Ste.")
            exit()
            
        if number_of_opponent_pieces_left == 2:
            print("Pobedili Ste.")
            exit()

    def is_end_of_first_phase(self, player_moves):
        if player_moves == 0:
            print("kraj prve faze")
            print("\nDruga faza.\nPomeranje figura.\n")
            return True
            
        return False    


class Game(object):
    def __init__(self):
        self.current_state = None
        self.player_turn = "W"
        self._setup = Setup()
        self._state = State()
        self._ocena_poteza = Ocena_poteza()
        self.initialize_game()
        self._phase = 1
        self._key_valid = False
        self._coordinates = ""
        self._player_coor =[]
        self._opponent_coor = []
        self._opponent_setup_moves = 5
        self._player_pieces = 5
        self._opponent_pieces = 5
        self._num_of_player_morrises = 0
        self._num_of_opponent_morrises = 0
        self._outcome = 0
        self.number_of_player_blocked_pieces = 0
        self.number_of_opponent_blocked_pieces = 0
        self.all_players_coordinates = []
        self.two_piece_config_player = 0
        self.two_piece_config_opponent = 0
        self.three_piece_config_player = 0
        self.three_piece_config_opponent = 0
        self.double_morris_config_player = 0
        self.double_morris_config_opponent = 0

    def initialize_game(self):
        self._setup.setup_game("", 0, False)

    def player_setup(self, current_player):
        self.two_piece_config(current_player, self._opponent_coor)
        #calculate_path(self._setup._next_hop, self._setup._taken_places)

        print("\nWhite moves.")

        print("Dostupna mesta:")
        s = ""
        for place in self._setup._taken_places:
            if self._setup._taken_places.get(place) == False:
                s += place + " "
        print(s)
        
        x_coor = int(input("Unesite koordinatu X: "))
        while x_coor > 6 or x_coor < 0:
            x_coor = int(input("Unesite koordinatu X: "))

        y_coor = int(input("Unesite koordinatu Y: "))
        while y_coor > 6 or y_coor < 0:
            y_coor = int(input("Unesite koordinatu Y: "))

        self._coordinates = str(x_coor) + str(y_coor)

        for key in self._setup._taken_places:
            if key == self._coordinates: 
                self._key_valid = True
                break
        if self._key_valid == True and self._coordinates not in self._player_coor:
            self.is_piece_blocked(current_player)
            print(self._coordinates)
            self._player_coor.append(self._coordinates)

            self.all_players_coordinates.append(self._coordinates)
        else:
            self.player_setup(current_player)

        if self._key_valid == True:
            if self._setup._taken_places[self._coordinates] == False:
                self._setup.setup_game(current_player, self._coordinates, False)
                got_morris, self._outcome = self._state.is_closed_morris(self._coordinates, self._player_coor, current_player, True)

                #ako jeste mica oduzmi crnom figuru
                if got_morris == True:
                    self._num_of_player_morrises += 1    
                    self.take_away(current_player)
                    self._opponent_pieces -= 1
                self._setup._taken_places[self._coordinates] = True
                self._key_valid = False
                current_player = "B"
            else: 
                print("Mesto već zauzeto.\n")
                self.player_setup(current_player)
                  
            self.opponent_setup(current_player)
    
    #OPPONENT MOVES
    def opponent_setup(self, current_player):
        self.two_piece_config(current_player, self._opponent_coor)

        tree = Tree()
        ocena_poteza = Ocena_poteza()
        ocena_poteza._trenutne_koordinate = self._coordinates
        ocena_poteza._current_player = current_player
        ocena_poteza.evaluated_value = 0
        tree.root = TreeNode(ocena_poteza)
        self.tree_development("B", "W", 1, 1, self.all_players_coordinates, tree.root)
        
        node_evaluation = Ocena_poteza()
        start = time()
        node_evaluation = self.minimax(tree.root, 2, current_player, 1)    
        end = time()
        print("vreme pretrage: ", end="")
        print(end - start)
        self._coordinates = node_evaluation._trenutne_koordinate
        #input()        
        # print("\nBlack moves.")
        # x_coor = int(input("Unesite koordinatu X: "))
        # while x_coor > 6 or x_coor < 0:
        #     x_coor = int(input("Unesite koordinatu X: "))

        # y_coor = int(input("Unesite koordinatu Y: "))
        # while y_coor > 6 or y_coor < 0:
        #     y_coor = int(input("Unesite koordinatu Y: "))

        # self._coordinates = str(x_coor) + str(y_coor)
       
        for key in self._setup._taken_places:
            if key == self._coordinates: 
                self._key_valid = True
                break
        if self._key_valid == True and self._coordinates not in self._opponent_coor:
            self.is_piece_blocked(current_player)
            print(self._coordinates)
            self._opponent_coor.append(self._coordinates)
            self.all_players_coordinates.append(self._coordinates)            
        else:
            self.opponent_setup(current_player)   
        
        if self._key_valid == True:
            if self._setup._taken_places[self._coordinates] == False:
                self._setup.setup_game(current_player, self._coordinates, False) 
                got_morris, self._outcome = self._state.is_closed_morris(self._coordinates, self._opponent_coor, current_player, True)
                #ako jeste mica oduzmi crnom figuru
                if got_morris == True:
                    self._num_of_opponent_morrises += 1
                    self.take_away(current_player)
                    self._player_pieces -= 1                              
                self._setup._taken_places[self._coordinates] = True
                self._key_valid = False
                current_player = "W"
                self._opponent_setup_moves -= 1            
                kraj = self._state.is_end_of_first_phase(self._opponent_setup_moves)
                if kraj == True:
                    self._phase = 2
                    self.druga_faza("W")                
            else: 
                print("Mesto već zauzeto.\n")
                self.opponent_setup(current_player)

            self.player_setup(current_player)

    def druga_faza(self, current_player):
        self._state.is_end(self._player_pieces, self._opponent_pieces)
        self.two_piece_config(current_player, self._opponent_coor)

        if current_player == "W":
            print("Beli igra.\n")
        else:
            print("Crni igra.\n")

            print(self._opponent_coor)
            niz = []
            for item in self._opponent_coor:
                #index = 0
                self._coordinates = item
                old_coordinates = self._coordinates
                if old_coordinates not in self._opponent_coor:
                    self._opponent_coor.append(old_coordinates)

                niz, postoji_ruta = self.possible_routes(old_coordinates, current_player)
                if postoji_ruta == True: 
                    self._opponent_coor.remove(old_coordinates)
                    break
                # index += 1
                # self._coordinates = self._opponent_coor[index]

            niz_evaluations = []
            niz_objekata = []

            for coor in niz:
                #print("koordinate u petlji: " + coor)
                tree = Tree()
                ocena_poteza = Ocena_poteza()
                ocena_poteza._trenutne_koordinate = coor
                self.all_players_coordinates.append(coor)
                ocena_poteza._current_player = current_player
                ocena_poteza.evaluated_value = 0
                tree.root = TreeNode(ocena_poteza)
                self.tree_development("B", "W", 1, 1, self.all_players_coordinates, tree.root)
                
                start = time()
                ocena_poteza = self.minimax(tree.root, 2, current_player, 2)
                stop = time()
                print("vreme pretrage: ", end="")
                print(stop-start)

                ocena_poteza._trenutne_koordinate = coor
                niz_objekata.append(ocena_poteza)
                niz_evaluations.append(ocena_poteza.evaluated_value)
                #print("node_eval od itema: " + str(ocena_poteza._trenutne_koordinate))
                #print("vrednost od itema: " + str(ocena_poteza.evaluated_value))
                self.all_players_coordinates.remove(coor)         
            
            niz_evaluations.sort()
            #print(self._setup._taken_places)
            for vrednost in niz_evaluations:
                nadjen = False
                for item in niz_objekata:
                    if item.evaluated_value == vrednost:
                        niz_objekata[0] = item
                        nadjen = True
                        break
                if nadjen == True: break

                #input()
            self._coordinates = niz_objekata[0]._trenutne_koordinate
            self._opponent_coor.append(self._coordinates)        

        if current_player == "W":
            x_coor = int(input("Unesite koordinatu X: "))
            while x_coor > 6 or x_coor < 0:
                x_coor = int(input("Unesite koordinatu X: "))

            y_coor = int(input("Unesite koordinatu Y: "))
            while y_coor > 6 or y_coor < 0:
                y_coor = int(input("Unesite koordinatu Y: "))

            self._coordinates = str(x_coor) + str(y_coor)
            old_coordinates = self._coordinates
        else:
            print(self._coordinates)

        #provera ako je W ne moze da pomera crne i obrnuto
        legal = self.check_if_legal_move(current_player, old_coordinates)
        if legal == True:
            self.is_piece_blocked(current_player)
            if current_player == "W":
                self.possible_routes(self._coordinates, current_player)

                x_coor = int(input("Pomerite koordinatu X: "))
                while x_coor > 6 or x_coor < 0:
                    x_coor = int(input("Pomerite koordinatu X: "))

                y_coor = int(input("Pomerite koordinatu Y: "))
                while y_coor > 6 or y_coor < 0:
                    y_coor = int(input("Pomerite koordinatu Y: "))

                self._coordinates = str(x_coor) + str(y_coor)
                if self._setup._taken_places.get(self._coordinates) == True:
                    self.druga_faza(current_player)

            #if current_player == "W":
                self._player_coor.remove(old_coordinates)
                self.all_players_coordinates.remove(old_coordinates)
                if self._coordinates not in self._player_coor:
                    self._player_coor.append(self._coordinates)
                    self.all_players_coordinates.append(self._coordinates)
            else:
                if old_coordinates in self.all_players_coordinates:
                    self.all_players_coordinates.remove(old_coordinates)
                if self._coordinates not in self._opponent_coor:
                    self._opponent_coor.append(self._coordinates)
                    self.all_players_coordinates.append(self._coordinates)

            self.move_figure(old_coordinates, self._coordinates, current_player)

            if current_player == "W":
                print("self.player: " + str(self._player_coor))
                got_morris, self._outcome = self._state.is_closed_morris(self._coordinates, self._player_coor, current_player, True)
            else:
                print("self.opponent: " + str(self._opponent_coor))
                got_morris, self._outcome = self._state.is_closed_morris(self._coordinates, self._opponent_coor, current_player, True)

            if got_morris == True:
                self.take_away(current_player)

                if current_player == "W":
                   #self._opponent_coor.remove(oduzmi)
                    self._num_of_player_morrises += 1
                    self._opponent_pieces -= 1
                else: 
                    self._num_of_opponent_morrises += 1
                    self._player_pieces -= 1
                    #self._player_coor.remove(oduzmi)
                self._state.is_end(self._player_pieces, self._opponent_pieces)
                print(self._player_pieces, self._opponent_pieces)
            #self.calculate_path(self._coordinates)
            if current_player == "W":
                current_player = "B"
            else: current_player = "W"

            self.druga_faza(current_player)

        else: 
            print("Ne mozete pomerati tu figuru.")
            self.druga_faza(current_player)

    def check_if_legal_move(self, current_player, coordinates):
        for row in self._setup._tabela:
            for item in row:
                if isinstance(item, list) and item[0] == coordinates and item[1] == current_player:
                    return True
        return False

    def possible_routes(self, coordinates, player_turn):
        niz = []
        s = ""
        for item in self._setup._chained_next_hop[coordinates]:
            if self._setup._taken_places[item] == False:
                s += item + " "
                if player_turn == "B":
                    niz.append(item)

        if s == "":
            print("Nema ruta.")
            if player_turn == "B":
                return [], False
            self.druga_faza(player_turn)
        print("moguci smerovi kretanja: " + s)

        if player_turn == "B":
            return niz, True

    def move_figure(self, old_coordinates, coordinates, current_player):
        for row in self._setup._tabela:
            s = ""
            for item in row:
                if isinstance(item, str):
                    s += item
                else:
                    if current_player == "W" and item[0] == old_coordinates and item[1] == "W":
                        item[1] = "o"
                        self._setup._taken_places[old_coordinates] = False
                        s += "o"
                    elif current_player == "W" and item[0] == coordinates and item[1] == "o" and self._setup._taken_places.get(coordinates) == False: #pretpostavljam da je uracunao od possible routes da ne moze biti w/b
                        item[1] = "W"
                        self._setup._taken_places[coordinates] = True
                        s += "W"
                    elif current_player == "B" and item[0] == old_coordinates and item[1] == "B":
                        item[1] = "o"
                        self._setup._taken_places[old_coordinates] = False
                        s += "o"
                    elif current_player == "B" and item[0] == coordinates and item[1] == "o" and self._setup._taken_places.get(coordinates) == False:
                        item[1] = "B"
                        self._setup._taken_places[coordinates] = True
                        s += "B"
                    else: s += str(item[1])
            print(s)
    
    def tree_development(self, player1, player2, current_phase, depth, list_of_coordinates, new_root):

        #if current_phase == 1:
            if depth == 2:
                for item in self._setup._moves:
                    if item not in list_of_coordinates:
                        _ocena_poteza = Ocena_poteza()
                        _ocena_poteza._trenutne_koordinate = item
                        _ocena_poteza._current_player = player2
                        _ocena_poteza.evaluated_value = 0 #randrange(-50,50)
                        #_ocena_poteza.evaluated_value = _ocena_poteza.ocena_poteza_prva_faza()
                        cvor = TreeNode(_ocena_poteza)    
                        new_root.add_child(cvor)
                #        print(_ocena_poteza._trenutne_koordinate + "-" + str(depth))
               # print()
                return

            i = 0
            for item in self._setup._moves:
                if item not in list_of_coordinates:
                    _ocena_poteza = Ocena_poteza()
                    _ocena_poteza._trenutne_koordinate = item
                    _ocena_poteza._current_player = player2
                    _ocena_poteza.evaluated_value = 0 #randrange(-50,50)
                    cvor = TreeNode(_ocena_poteza)
                    new_root.add_child(cvor)
                    #print("novi cvor")
                    #print(_ocena_poteza._trenutne_koordinate + "-" + str(depth))
                    #print()

                    list_of_coordinates.append(_ocena_poteza._trenutne_koordinate)
                    self.tree_development(player2, player1, current_phase, depth+1, list_of_coordinates, new_root.children[i])
                    del list_of_coordinates[len(list_of_coordinates)-1]
                    i += 1
    

    def take_away(self, current_player):
        if current_player == "W":
            x_coor = int(input("Unesite koordinatu X za uklanjanje figure: "))
            while x_coor > 6 or x_coor < 0:
                x_coor = int(input("Unesite koordinatu X za uklanjanje figure: "))

            y_coor = int(input("Unesite koordinatu Y za uklanjanje figure: "))
            while y_coor > 6 or y_coor < 0:
                y_coor = int(input("Unesite koordinatu Y za uklanjanje figure: "))

            coordinates = str(x_coor) + str(y_coor)
        else:
        #proba za crnog
            #index = randrange(len(self._player_coor)-1)
            #coordinates = self._player_coor[index]
            coordinates = self.check_which_to_delete()
            print(coordinates)
            #print("ukloniti " + coordinates)
        ##############

        valid_key = False

        for key in self._setup._taken_places:
            if key == coordinates: 
                valid_key = True
                break
        if valid_key == True:
            print(coordinates)
            if current_player == "W":
                self._opponent_coor.remove(coordinates)
                self.all_players_coordinates.remove(coordinates)
            else:
                self._player_coor.remove(coordinates)
                self.all_players_coordinates.remove(coordinates)
            
            self._setup.setup_game(current_player, coordinates, True)
        else:
            print("Ne mozete odigrati taj potez.")
            self.take_away(current_player)

    def minimax(self, current_node, depth, current_player, current_phase):
        evaluation = Ocena_poteza()

        if depth == 0 or self._state.is_end(self._player_pieces, self._opponent_pieces):
            if current_phase == 1:
                #return current_node.data.ocena_poteza_prva_faza()
                # print("usao depth 0")
                # print(depth)
                # print(current_node.data._trenutne_koordinate)
                #return current_node.data.evaluated_value
                current_node.data.evaluated_value = self.ocena_poteza_prva_faza()#randrange(-50,50) // MOZDA JE BILO BOLJE DA SAM KOD DRVETA KOD LISTOVA DODELJIVAO VREDNOST!!
                return current_node.data
            else:
                current_node.data.evaluated_value = self.ocena_poteza_druga_faza()#randrange(-50,50)
                return current_node.data
                #return current_node.data.ocena_poteza_druga_faza() 
                #return current_node.data.evaluated_value

        if current_player == "W":
            max_eval = -inf
            for child in current_node.children:
                # print("usao W")
                # print(depth)
                # print(child.data._trenutne_koordinate)
                evaluation = self.minimax(child, depth-1, "B", current_phase)
                max_eval = max(max_eval, evaluation.evaluated_value)
                evaluation.evaluated_value = max_eval
            return evaluation
        else:
            min_eval = inf
            for child in current_node.children:
                # print("usao B")
                # print(depth)
                # print(child.data._trenutne_koordinate)
                evaluation = self.minimax(child, depth-1, "W", current_phase)
                min_eval = min(min_eval, evaluation.evaluated_value)
                evaluation.evaluated_value = min_eval
            return evaluation

    def check_which_to_delete(self):
        for item in self._setup._chained_morrises:
            #print("item = " + item)
            for niz in self._setup._chained_morrises[item]:
                #print("niz = " + str(niz))
                counter = 0
                for coor in self._player_coor:
                    #print(coor)
                    if coor in niz:
                        counter += 1
                if counter == 2: 
                    #print("nasao + " + coor)                       
                    return coor
        return self._player_coor[randrange(len(self._player_coor)-1)]

    def is_piece_blocked(self, current_player):
        for key in self._setup._taken_places:
            niz = []
            if self._setup._taken_places[key] == True:
                for coor in self._setup._chained_next_hop[key]:
                    if self._setup._taken_places[coor] == True:
                        niz.append(coor)
                if niz == self._setup._chained_next_hop[key]:
                    if current_player == "W":
                        self.number_of_player_blocked_pieces += 1
                    elif current_player == "B":
                        self.number_of_opponent_blocked_pieces += 1

    def two_piece_config(self, current_player, coordinate_list):
        #coor je key u self.setup.next_move
        for key in coordinate_list:
            counter = 0
            morris_counter = 0
            for coor in coordinate_list:
                if coor in self._setup._chained_next_hop[key]:            
                    ima, nebitno = self._state.is_closed_morris(coor, coordinate_list, current_player, False)
                    if ima == False:
                        counter += 1
                    else:
                        morris_counter += 1
            if current_player == "W":
                if counter == 2:
                    self.three_piece_config_player += counter
                else:
                    self.two_piece_config_player += counter
                if morris_counter == 2:
                    self.double_morris_config_player += 1
            else:
                if counter == 2:
                    self.three_piece_config_opponent += counter
                else:
                    self.two_piece_config_opponent += counter
                if morris_counter == 2:
                    self.double_morris_config_opponent += 1
            
    def ocena_poteza_prva_faza(self):
        jedan = self._outcome
        dva = self._state.number_of_morrises(self._num_of_player_morrises,self._num_of_opponent_morrises)
        tri = self._state.num_of_blocked_pieces(self.number_of_player_blocked_pieces, self.number_of_opponent_blocked_pieces)
        cetiri = self._state.num_of_pieces(self._player_pieces, self._opponent_pieces)
        pet = self._state.num_of_two_piece_config(self.two_piece_config_player, self.two_piece_config_opponent)
        sest = self._state.num_of_three_piece_config(self.two_piece_config_player, self.two_piece_config_opponent)

        return 18 * jedan + 26 * dva + 1 * tri + 9 * cetiri + 10 * pet + 7 * sest
    
    def ocena_poteza_druga_faza(self):
        jedan = self._outcome
        dva = self._state.number_of_morrises(self._num_of_player_morrises,self._num_of_opponent_morrises)
        tri = self._state.num_of_blocked_pieces(self.number_of_player_blocked_pieces, self.number_of_opponent_blocked_pieces)
        cetiri = self._state.num_of_pieces(self._player_pieces, self._opponent_pieces)
        sedam = self._state.num_double_morris(self.double_morris_config_player, self.double_morris_config_opponent)

        return 14 * jedan + 43 * dva + 10 * tri + 11 * cetiri + 8 * sedam


class Ocena_poteza(object):
    def __init__(self):
        self._trenutne_koordinate = ""
        self._current_player = ""
        self.evaluated_value = 0