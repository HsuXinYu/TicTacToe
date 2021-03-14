from models import TicTac, TicTacAgent

if __name__ == "__main__":
    # TicTac.get_finishing_states_win_count()
    # ticTac = TicTac()
    # ticTac.play()
    tictacAgent = TicTacAgent()
    # tictacAgent.explore(30000)
    tictacAgent.monitor()
    # count = TicTac.calc_all_states(-np.ones(9,dtype=np.int))
    # count = TicTac.calc_all_states()
    # print(count)
    print(len(tictacAgent.STATES))