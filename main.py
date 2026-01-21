import asyncio
from api.cs2_client import CS2Client
from models.montecarlo import MonteCarloSimulator

async def main():
    client = CS2Client()
    matches = await client.get_live_matches()

    p = 0.43

    sim = MonteCarloSimulator(p)
    result = sim.run()

    print("Simulated Win Probability: ", result["win_probability"])

asyncio.run(main())