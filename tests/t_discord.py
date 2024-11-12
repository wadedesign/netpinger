import pytest
from netpinger.protocols.discord import DiscordProtocol
from netpinger.exceptions import QueryError

# Use a public Discord server ID that has widgets enabled
SERVER_ID = "1279289370125275219"  # Discord.py server as an example

def pytest_configure(config):
    """Register the 'live' marker"""
    config.addinivalue_line(
        "markers", "live: mark test as requiring live internet connection"
    )

@pytest.mark.asyncio
@pytest.mark.live
async def test_live_discord_server():
    protocol = DiscordProtocol()
    try:
        result = await protocol.query(SERVER_ID)
    except QueryError as e:
        if "403" in str(e):
            pytest.skip("Discord API returned status 403, skipping test.")
        else:
            raise
    
    # Basic schema validation
    assert isinstance(result, dict)
    assert "name" in result
    assert "connect" in result
    assert "players" in result
    assert "maxplayers" in result
    assert "raw" in result

@pytest.mark.asyncio
@pytest.mark.live
async def test_discord_invalid_server():
    """Test handling of servers with disabled widgets"""
    protocol = DiscordProtocol()
    with pytest.raises(QueryError) as exc_info:
        await protocol.query("000000000000000000")  # Invalid server ID
    assert "404" in str(exc_info.value)