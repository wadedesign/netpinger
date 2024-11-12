import asyncio
from netpinger.protocols.discord import DiscordProtocol
from netpinger.exceptions import QueryError

async def main():
    guild_id = "1279289370125275219"  # example but replace with your server id
    protocol = DiscordProtocol()
    
    try:
        result = await protocol.query(guild_id)
        print("Server Information:")
        print(f"Name: {result['name']}")
        print(f"Connect: {result['connect']}")
        print(f"Players: {len(result['players'])}/{result['maxplayers']}")
        print("Player List:")
        for player in result['players']:
            print(f" - {player['name']}")
    except QueryError as e:
        print(f"Failed to query Discord server: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
