import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from models.bo3 import BO3Simulator
from models.odds import Odds
from models.maplogic import calculate_map_probabilities
from models.ev import EVCalculator


st.title("CS2 - BO3 Monte Carlo Simulator")
st.markdown('<a href="https://hltv.org/matches" target="_blank">HLTV <--- get stats for input values</a>', unsafe_allow_html=True)


#--------------------------------------------------------------------------------------------------------------------
st.subheader("Map 1              (you are always team1)")
map1t1wr, map1t2wr, map1t1g, map1t2g = st.columns(4)
with map1t1wr:
    map1_team1_wr = st.slider("Team1 Winrate:", 0.0, 1.0, 0.50, key="map1_team1_wr")
with map1t2wr:
    map1_team2_wr = st.slider("Team2 Winrate:", 0.0, 1.0, 0.50, key="map1_team2_wr")
with map1t1g:
    map1_team1_games = st.number_input("Team1 Map Played:", min_value=1, key="map1_team1_games")
with map1t2g:
    map1_team2_games = st.number_input("Team2 Map Played:", min_value=1, key="map1_team2_games")

st.subheader("Map 2")
map2t1wr, map2t2wr, map2t1g, map2t2g = st.columns(4)
with map2t1wr:
    map2_team1_wr = st.slider("Team1 Winrate:", 0.0, 1.0, 0.50, key="map2_team1_wr")
with map2t2wr:
    map2_team2_wr = st.slider("Team2 Winrate:", 0.0, 1.0, 0.50, key="map2_team2_wr")
with map2t1g:
    map2_team1_games = st.number_input("Team1 Map Played:", min_value=1, key="map2_team1_games")
with map2t2g:
    map2_team2_games = st.number_input("Team2 Map Played:", min_value=1, key="map2_team2_games")

st.subheader("Map 3")
map3t1wr, map3t2wr, map3t1g, map3t2g = st.columns(4)
with map3t1wr:
    map3_team1_wr = st.slider("Team1 Winrate:", 0.0, 1.0, 0.50, key="map3_team1_wr")
with map3t2wr:
    map3_team2_wr = st.slider("Team2 Winrate:", 0.0, 1.0, 0.50, key="map3_team2_wr")
with map3t1g:
    map3_team1_games = st.number_input("Team1 Map Played:", min_value=1, key="map3_team1_games")
with map3t2g:
    map3_team2_games = st.number_input("Team2 Map Played:", min_value=1, key="map3_team2_games")
#--------------------------------------------------------------------------------------------------------------------



# Bruker logikken i maplogic for å korrigere og hente ut bedre winrate verdier.
p1, p2, p3 = calculate_map_probabilities(
    map1_team1_wr, map1_team2_wr, map1_team1_games, map1_team2_games,
    map2_team1_wr, map2_team2_wr, map2_team1_games, map2_team2_games,
    map3_team1_wr, map3_team2_wr, map3_team1_games, map3_team2_games
)

#gamle winrate inputs
#p1 = st.slider("Map 1 winrate", 0.0, 1.0, 0.55)
#p2 = st.slider("Map 2 winrate", 0.0, 1.0, 0.60)
#p3 = st.slider("Decider winrate", 0.0, 1.0, 0.50)
sims = st.number_input("Simulations", 1, 100000, 10000)

sim = BO3Simulator(p1, p2, p3, sims)
result = sim.run()

odds1 = st.number_input("Bookmakers Odds - Team1 (your team): ", 1.02, 20.00, 2.00)
odds2 = st.number_input("Bookmakers Odds - Team2 (their team): ", 1.02, 20.00, 2.00)
o = Odds(odds1, odds2)


#visualisering
convergence = result["convergence"]
n = len(convergence)

df = pd.DataFrame({
    "Simulation": range(1, n + 1),
    "Winrate": convergence
})
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Simulation"],
    y=df["Winrate"],
    mode="lines",
    line=dict(color="#4A90E2", width=2),
    name="Winrate"
))
fig.update_layout(
    title="Monte Carlo Visualization",
    xaxis_title="Simulation number",
    yaxis_title="Winrate",
    template="plotly_white",
    height=400,
    margin=dict(l=40, r=40, t=60, b=40)
)
st.plotly_chart(fig, use_container_width=True)




left, right = st.columns(2)
with left:
    st.markdown("### Simulation Results")
    st.write("BO3 Winrate:", result["bo3_winrate"], "%")
    st.write("2–0 Win:", result["win_2_0"], "%")
    st.write("2–1 Win:", result["win_2_1"], "%")
    st.write("1–2 Loss:", result["loss_1_2"], "%")
    st.write("0–2 Loss:", result["loss_0_2"], "%")
with right:
    st.markdown("### Bookmaker Analysis")
    st.write("Team 1 (you):", round(o.chance_team1 * 100, 2), "%")
    st.write("Team 2:", round(o.chance_team2 * 100, 2), "%")

    st.write("Fair odds:")
    st.write("Team 1 (you):", round(o.fair_odds1, 2))
    st.write("Team 2:", round(o.fair_odds2, 2))

def copy_sim_values():
    st.session_state.ev_winrate = result["bo3_winrate"]
    st.session_state.ev_odds = odds1
    st.session_state.trigger_rerun = True


st.subheader("EV Calculator")
stake, odds, winrate, bets = st.columns(4)
with stake:
    ev_stake = st.number_input("Stake per bet:", 1.00, 99999999.00, 100.00, key="ev_stake")
with odds:
    ev_odds = st.number_input("Odds:", 1.01, 100.00, 1.86, key="ev_odds")
with winrate:
    ev_winrate = st.number_input("Winrate %:", 0.01, 100.00, 50.00, key="ev_winrate")
with bets:
    ev_bets = st.number_input("Number of bets to simulate:", 1, 100000, 1000, key="ev_bets")


ev = EVCalculator(
    stake = ev_stake,
    odds = ev_odds,
    winrate_percent = ev_winrate,
    bets = ev_bets
)


ev_left, ev_right = st.columns(2)
with ev_left:
    st.write("EV per bet:", round(ev.ev_per_bet, 2), "$     (How much you on avg. win or lose per bet)")
    st.write("Total EV:", round(ev.total_ev, 2), "$     (EV after all simulated bets)")
with ev_right:
    st.write("Break even winrate:", round(ev.break_even_winrate * 100, 2), "%   (How many bets need to go in for you to break even)")
    st.write("ROI per bet:", round(ev.roi_per_bet * 100, 2), "%     (How much you on avg. win or lose per bet)")
#Knapp for å kopiere verdier
st.button("Use simulation + bookmaker values", on_click=copy_sim_values)
if st.session_state.get("trigger_rerun", False):
    st.session_state.trigger_rerun = False
    st.rerun()





