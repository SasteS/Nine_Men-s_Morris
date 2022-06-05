from hashmap import ChainedHashMap


class Setup(object):
    def __init__(self):
        self._chained_next_hop = ChainedHashMap()
        self._chained_morrises = ChainedHashMap()
        # self._polja = {'00': 'O', '03': 'O', '06': 'O', '11': 'O', '13': 'O', '15': 'O', '22': 'O', '23': 'O', '24': 'O',
        #             '30': 'O', '31': 'O', '32': 'O', '34': 'O', '35': 'O', '36': 'O', '42': 'O', '43': 'O', '44': 'O',
        #             '51': 'O', '53': 'O', '55': 'O', '60': 'O', '63': 'O', '66': 'O'}

        self._next_hop = {'00': ['30', '03'], '03': ['00', '13', '06'], '06': ['03', '36'], '11': ['31', '13'],
                        '13': ['03', '11', '23', '15'], '15': ['13', '35'], '22': ['32', '23'],
                        '23': ['13', '22', '24'], '24': ['23', '34'], '30': ['00', '60', '31'],
                        '31': ['11', '30', '51', '32'], '32': ['22', '31', '42'], '34': ['24', '44', '35'],
                        '35': ['15', '34', '55', '36'], '36': ['06', '35', '66'], '42': ['32', '43'],
                        '43': ['42', '53', '44'], '44': ['34', '43'], '51': ['31', '53'],
                        '53': ['43', '51', '63', '55'], '55': ['35', '53'], '60': ['30', '63'],
                        '63': ['53', '60', '66'], '66': ['36', '63']}

        
        self._chained_next_hop['00'] = ['30', '03']
        self._chained_next_hop['03'] = ['00', '13', '06']
        self._chained_next_hop['06'] = ['03', '36']
        self._chained_next_hop['11'] = ['31', '13']
        self._chained_next_hop['13'] = ['03', '11', '23', '15']
        self._chained_next_hop['15'] = ['13', '35']
        self._chained_next_hop['22'] = ['32', '23']
        self._chained_next_hop['23'] = ['13', '22', '24']
        self._chained_next_hop['24'] = ['23', '34']
        self._chained_next_hop['30'] = ['00', '60', '31']
        self._chained_next_hop['31'] = ['11', '30', '51', '32']
        self._chained_next_hop['32'] = ['22', '31', '42']
        self._chained_next_hop['34'] = ['24', '44', '35']
        self._chained_next_hop['35'] = ['15', '34', '55', '36']
        self._chained_next_hop['36'] = ['06', '35', '66']
        self._chained_next_hop['42'] = ['32', '43']
        self._chained_next_hop['43'] = ['42', '53', '44']
        self._chained_next_hop['44'] = ['34', '43']
        self._chained_next_hop['51'] = ['31', '53']
        self._chained_next_hop['53'] = ['43', '51', '63', '55']
        self._chained_next_hop['55'] = ['35', '53']
        self._chained_next_hop['60'] = ['30', '63']
        self._chained_next_hop['63'] = ['53', '60', '66']
        self._chained_next_hop['66'] = ['36', '63']


        self._taken_places = {'00': False, "03": False, "06": False,
                            "11": False, "13": False, "15": False,
                            "22": False, "23": False, "24": False,
                            "30": False, "31": False, "32": False, "34": False, "35": False, "36": False,
                            "42": False, "43": False, "44": False,
                            "51": False, "53": False, "55": False,
                            "60": False, "63": False, "66": False }
                    
        self._morrises = {'00': [['03', '06'], ['30', '60']], '03': [['00', '06'], ['13', '23']],
                        '06': [['00', '03'], ['36', '66']], '11': [['13', '15'], ['31', '51']],
                        '13': [['11', '15'], ['03', '23']], '15': [['11', '13'], ['35', '55']],
                        '22': [['23', '24'], ['32', '42']], '23': [['22', '24'], ['03', '13']],
                        '24': [['22', '23'], ['34', '44']], '30': [['00', '60'], ['31', '32']],
                        '31': [['30', '32'], ['11', '51']], '32': [['30', '31'], ['22', '42']],
                        '34': [['24', '44'], ['35', '36']], '35': [['34', '36'], ['15', '55']],
                        '36': [['34', '35'], ['06', '66']], '42': [['43', '44'], ['22', '32']],
                        '43': [['42', '44'], ['53', '63']], '44': [['42', '43'], ['24', '34']],
                        '51': [['53', '55'], ['11', '31']], '53': [['51', '55'], ['43', '63']],
                        '55': [['51', '53'], ['15', '35']], '60': [['00', '30'], ['63', '66']],
                        '63': [['60', '66'], ['43', '53']], '66': [['60', '63'], ['06', '36']]}


        self._chained_morrises['00'] = [['03', '06'], ['30', '60']]
        self._chained_morrises['03'] = [['00', '06'], ['13', '23']]
        self._chained_morrises['06'] = [['00', '03'], ['36', '66']]
        self._chained_morrises['11'] = [['13', '15'], ['31', '51']]
        self._chained_morrises['13'] = [['11', '15'], ['03', '23']]
        self._chained_morrises['15'] = [['11', '13'], ['35', '55']]
        self._chained_morrises['22'] = [['23', '24'], ['32', '42']]
        self._chained_morrises['23'] = [['22', '24'], ['03', '13']]
        self._chained_morrises['24'] = [['22', '23'], ['34', '44']]
        self._chained_morrises['30'] = [['00', '60'], ['31', '32']]
        self._chained_morrises['31'] = [['30', '32'], ['11', '51']]
        self._chained_morrises['32'] = [['30', '31'], ['22', '42']]
        self._chained_morrises['34'] = [['24', '44'], ['35', '36']]
        self._chained_morrises['35'] = [['34', '36'], ['15', '55']]
        self._chained_morrises['36'] = [['34', '35'], ['06', '66']]
        self._chained_morrises['42'] = [['43', '44'], ['22', '32']]
        self._chained_morrises['43'] = [['42', '44'], ['53', '63']]
        self._chained_morrises['44'] = [['42', '43'], ['24', '34']]
        self._chained_morrises['51'] = [['53', '55'], ['11', '31']]
        self._chained_morrises['53'] = [['51', '55'], ['43', '63']]
        self._chained_morrises['55'] = [['51', '53'], ['15', '35']]
        self._chained_morrises['60'] = [['00', '30'], ['63', '66']]
        self._chained_morrises['63'] = [['60', '66'], ['43', '53']]
        self._chained_morrises['66'] = [['60', '63'], ['06', '36']]


        self._moves = {"00": 0, "03": 1, "06": 2,
                    "11": 3, "13": 4, "15": 5,
                    "22": 6, "23": 7, "24": 8,
                    "30": 9, "31": 10, "32": 11, "34": 12, "35": 13, "36": 14,
                    "42": 15, "43": 16, "44": 17,
                    "51": 18, "53": 19, "55": 20,
                    "60": 21, "63": 22, "66": 23,}

        self._tabela = [["0   ", ["00", "o"], "--------------------", ["03", "o"], "--------------------", ["06", "o"]],
                ["    |", "                    ", "|", "                    ", "|"],   
                ["    |", "                    ", "|", "                    ", "|"],
                ["1   |      ", ["11", "o"],"-------------", ["13", "o"], "-------------", ["15", "o"], "      |"],
                ["    |", "      |             ", "|", "             |      ", "|"],  
                ["    |", "      |             ", "|", "             |      ", "|"],
                ["2   |      |     ", ["22", "o"], "-------", ["23", "o"], "-------", ["24", "o"], "     |      |"], 
                ["    |      |     |               |     |      |"], 
                ["    |      |     |               |     |      |"],    
                ["3   ", ["30", "o"], "------", ["31", "o"],"-----", ["32", "o"], "               ", ["34", "o"], "-----", ["35", "o"], "------", ["36", "o"]],           
                ["    |      |     |               |     |      |"], 
                ["    |      |     |               |     |      |"], 
                ["4   |      |     ", ["42", "o"], "-------", ["43", "o"], "-------", ["44", "o"], "     |      |"], 
                ["    |", "      |             ", "|", "             |      ", "|"],  
                ["    |", "      |             ", "|", "             |      ", "|"],   
                ["5   |      ", ["51", "o"],"-------------", ["53", "o"], "-------------", ["55", "o"], "      |"],
                ["    |", "                    ", "|", "                    ", "|"],   
                ["    |", "                    ", "|", "                    ", "|"],                
                ["6   ", ["60", "o"], "--------------------", ["63", "o"], "--------------------", ["66", "o"]],
                ["                                                                   "],
                ["    0      1     2       3       4     5      6"]]

    def setup_game(self, player_turn, coordinates, deleting):
        print("\n\n")
        for row in self._tabela:
            ponovi = False
            s = ""
            for item in row:
                if deleting == False:
                    if isinstance(item, str):
                        s += item
                    else:
                        if player_turn == "W" and item[0] == coordinates:
                            s += "W"
                            item[1] = "W"
                        elif player_turn == "B" and item[0] == coordinates:
                            s += "B"
                            item[1] = "B"
                        elif item[1] != "W" and item[1] != "B":
                            s += "o"
                        else: s+= item[1]

            
                if deleting == True:
                    if isinstance(item, str):
                        s += item
                    else: 
                        if player_turn == "W" and item[0] == coordinates and item[1] == "B":
                            s += "o"
                            item[1] = "o"
                            self._taken_places[coordinates] = False
                        elif player_turn == "W" and item[0] == coordinates and item[1] == "W":
                            ponovi = True

                        elif player_turn == "B" and item[0] == coordinates and item[1] == "W":
                            s += "o"
                            item[1] = "o"
                            self._taken_places[coordinates] = False
                        elif player_turn == "B" and item[0] == coordinates and item[1] == "B":
                            ponovi = True

                        else: s += item[1]
            print(s)
        print("")
        if ponovi == True:    
            print("Ne moze se uklanjati.")
            self.take_away(player_turn)

# setup = Setup()

# for item in setup._chained_morrises:
#     print(item)
#     # print(setup._chained_morrises[item])