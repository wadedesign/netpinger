import pytest
from netpinger.protocols.discord import DiscordProtocol
from netpinger.exceptions import QueryError

# Replace this with your Discord server ID
SERVER_ID = "1279289370125275219"  # Example: "123456789012345678"

@pytest.mark.asyncio
@pytest.mark.live  # This marker helps separate live tests from unit tests
async def test_live_discord_server():
    protocol = DiscordProtocol()
    result = await protocol.query(SERVER_ID)
    
    # Basic structure checks
    assert isinstance(result, dict)
    assert "name" in result
    assert "connect" in result
    assert "players" in result
    assert "maxplayers" in result
    assert "raw" in result
    
    # Type checks
    assert isinstance(result["name"], str)
    assert isinstance(result["connect"], str)
    assert isinstance(result["players"], list)
    assert isinstance(result["maxplayers"], int)
    assert isinstance(result["raw"], dict)
    
    # Player data checks
    for player in result["players"]:
        assert "name" in player
        assert "status" in player
        assert isinstance(player["name"], str)
        assert isinstance(player["status"], str)
    
    print("\nLive Discord Server Results:")
    print(f"Server Name: {result['name']}")
    print(f"Connect URL: {result['connect']}")
    print(f"Online Players: {len(result['players'])}")
    print(f"Player List: {[p['name'] for p in result['players']]}")

@pytest.mark.asyncio
@pytest.mark.live
async def test_live_invalid_server():
    protocol = DiscordProtocol()
    with pytest.raises(QueryError):
        await protocol.query("000000000000000000")  # Non-existent server ID 