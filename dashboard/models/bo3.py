import numpy as np

class BO3Simulator:
    def __init__(self, p1, p2, p3, simulations=10000):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.simulations = simulations

    def run(self):
        bo3_wins = 0
        win2_0 = 0
        win2_1 = 0
        loss1_2 = 0
        loss0_2 = 0

        cumulative_winrate = []

        for i in range(self.simulations):
            m1 = np.random.random() < self.p1
            m2 = np.random.random() < self.p2
            if m1 and m2:
                win2_0 += 1
                bo3_wins += 1
                continue
            if not m1 and not m2:
                loss0_2 += 1
                continue

            m3 = np.random.random() < self.p3
            if m3:
                win2_1 += 1
                bo3_wins += 1
            else:
                loss1_2 += 1

            cumulative_winrate.append(bo3_wins / (i + 1))


        return {
                "bo3_winrate": round(bo3_wins * 100 / self.simulations, 2),
                "win_2_0": round(win2_0 * 100 / self.simulations, 2),
                "win_2_1": round(win2_1 * 100/ self.simulations, 2),
                "loss_1_2": round(loss1_2 * 100 / self.simulations, 2),
                "loss_0_2": round(loss0_2 * 100 / self.simulations, 2),
                "convergence": cumulative_winrate
            }

