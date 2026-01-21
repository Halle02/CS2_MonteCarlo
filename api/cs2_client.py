from cs2api import CS2
import asyncio

class CS2Client:
    async def get_live_matches(self):
        async with CS2() as cs2:
            return await cs2.get_live_matches()


# Test
if __name__ == "__main__":
    async def test():
        client = CS2Client()
        matches = await client.get_live_matches()
        print(matches)
    asyncio.run(test())