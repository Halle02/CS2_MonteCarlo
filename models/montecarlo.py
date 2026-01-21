import numpy as np

class MonteCarloSimulator:
    def __init__(self, p, simulations=1000):
        self.p = p
        self.simulations = simulations

    def run(self):
        results = np.random.binomial(n=1, p=self.p, size=self.simulations)
        return {
            "win_probability": results.mean(),
            "loss_probability": 1 - results.mean()
        }