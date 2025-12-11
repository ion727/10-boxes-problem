from player import moves

class state:
    def __init__(self, parent=None, coin_pos:int=0):
        self.coin_pos:int = coin_pos
        
        if type(parent) is not tuple:
            self.parent:state = parent
            self.age:int = self.parent.age + 1
            self.hash:list = self.parent.hash + [coin_pos]
            self.size:int = parent.size
            self.max_moves:int = parent.max_moves
        else:
            self.age:int = 0
            self.hash:list = [coin_pos]
            size, max_moves = parent
            self.size:int = size
            self.max_moves:int = max_moves
        
        self.board:list = [0]*self.size
        self.board[coin_pos] = 1
        self.moves:list = self.generate_next()
        self.completed_hashes:list[list] = []
        if len(self.hash) == 10:
            self.completed_hashes.append(self.hash)
        self.completed_hashes.extend(hash_ for move in self.moves for hash_ in move.completed_hashes)
        

    def generate_next(self):
        moves:list = []
        if self.age < self.max_moves:
            coin_pos:int = self.board.index(1)
            if coin_pos != 0:
                moves.append(state(self, self.coin_pos-1))
            if coin_pos != len(self.board)-1:
                moves.append(state(self, self.coin_pos+1))
        return moves

        

class System:
    def __init__(self, size=10, max_moves=10, scope = 0):
        self.size=size
        self.max_moves=max_moves
        self.boards = [state((size,max_moves), coin_pos=i) for i in range(size)]
        self.all_completed_hashes:list = [hash_ for state in self.boards for hash_ in state.completed_hashes]
        self.solutions:list[list[int]] = []
        '''total = 0
        for _ in moves(self.size + scope -1):
            total += 1
            if total % 100000 == 0:
                print(total)
        print(total); quit()'''
        
        for k,move in enumerate(moves(self.size + scope)):
            if k % 100000 == 0:
                print(move)
            valid:bool = True
            for hash_ in self.all_completed_hashes:
                if not any(move[i] == hash_[i] for i in range(len(hash_))):
                    valid = False
                    break
            if valid:
                self.solutions.append(move)
                break



def main(size, moves):
    system = System(size,moves)
    """print(system.all_completed_hashes)
    print(f"Unique states detected: {len(system.all_completed_hashes)}\n")
    print(f"list of 1000 first possible moves: {system.all_possible_moves[:1000]}")"""
    return system

if __name__ == "__main__":
    system = main(size=10, moves=10)
    print(system.solutions)

