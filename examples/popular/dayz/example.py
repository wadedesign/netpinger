import asyncio
from netpinger import query_server

async def main():
    result = await query_server("dayz", "172.111.51.154", 2303)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
    
    
# should return something like this:
# {'name': 'Rearmed US Main', 'map': 'ChernarusPlus', 'players': 38, 'maxPlayers': 127, 'gameDir': 'dayz', 'description': '', 'appId': 0, 'firstPerson': False, 'private': False, 'official': True, 'tags': ''}