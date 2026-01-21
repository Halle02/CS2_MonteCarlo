# For å normalisere tallene (fjerne bookmakers cut fra oddsene og statistikken)
class Odds:
    def __init__(self, odds1, odds2):
        self.odds1 = odds1
        self.odds2 = odds2

        self.chance_team1_raw = 1 / odds1
        self.chance_team2_raw = 1 / odds2

        self.total = self.chance_team1_raw + self.chance_team2_raw

        self.chance_team1 = self.chance_team1_raw / self.total
        self.chance_team2 = self.chance_team2_raw / self.total

        self.fair_odds1 = 1 / self.chance_team1
        self.fair_odds2 = 1 / self.chance_team2

        self.bookmakers_cut = self.total - 1

