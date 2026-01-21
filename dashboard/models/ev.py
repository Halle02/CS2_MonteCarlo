import numpy as np

class EVCalculator:
    def __init__(self, stake: float, odds: float, winrate_percent: float, bets: int):
        self.stake = stake
        self.odds = odds
        self.winrate_percent = winrate_percent
        self.winrate = winrate_percent / 100.00
        self.bets = bets

    @property
    def profit_if_win(self ):
        return self.stake * (self.odds -1)

    @property
    def profit_if_lose(self):
        return self.stake

    @property
    def ev_per_bet(self):
        return self.winrate * self.profit_if_win - (1-self.winrate) * self.profit_if_lose

    @property
    def total_ev(self):
        return self.ev_per_bet * self.bets

    @property
    def break_even_winrate(self):
        return 1 / self.odds

    @property
    def roi_per_bet(self): # EV per bet / innsats
        return self.ev_per_bet / self.stake


    # For visualisering
    def ev_convergence(self):
        cumulative = []
        total = 0

        for i in range(self.bets):
            # 1 = win        0 = loss
            win = np.random.random() < (self.winrate_percent / 100)
            if win:
                total += (self.stake * (self.odds - 1))
            else:
                total -= self.stake

            cumulative.append(total)
        return cumulative
