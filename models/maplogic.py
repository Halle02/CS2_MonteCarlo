

def adjusted_winrate(winrate, games, k=20):
    weight = games / (games + k)
    return 0.5 + (winrate - 0.5) * weight


def head_to_head_p(wA, wB):
    sA = wA / (1 - wA)
    sB = wB / (1 - wB)
    return sA / (sA + sB)


def calculate_map_probabilities(
    m1_t1_wr, m1_t2_wr, m1_t1_games, m1_t2_games,
    m2_t1_wr, m2_t2_wr, m2_t1_games, m2_t2_games,
    m3_t1_wr, m3_t2_wr, m3_t1_games, m3_t2_games):
    # Map 1
    m1_t1_adj = adjusted_winrate(m1_t1_wr, m1_t1_games)
    m1_t2_adj = adjusted_winrate(m1_t2_wr, m1_t2_games)
    p1 = head_to_head_p(m1_t1_adj, m1_t2_adj)

    # Map 2
    m2_t1_adj = adjusted_winrate(m2_t1_wr, m2_t1_games)
    m2_t2_adj = adjusted_winrate(m2_t2_wr, m2_t2_games)
    p2 = head_to_head_p(m2_t1_adj, m2_t2_adj)

    # Map 3 (decider)
    m3_t1_adj = adjusted_winrate(m3_t1_wr, m3_t1_games)
    m3_t2_adj = adjusted_winrate(m3_t2_wr, m3_t2_games)
    p3 = head_to_head_p(m3_t1_adj, m3_t2_adj)

    return p1, p2, p3
