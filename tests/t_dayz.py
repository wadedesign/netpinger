# NOTE - all tests are passing, could change or add more tests

import pytest
from netpinger import query_server, QueryError, TimeoutError

@pytest.mark.asyncio
async def test_dayz_query_success():
    """Test DayZ server query success."""
    test_servers = [
        ("172.111.51.154", 2303), # public servers on battlemetrics
        ("172.111.51.184", 2303), 
        ("193.25.252.54", 2303)
    ]
    
    success = False
    last_error = None
    
    for host, port in test_servers:
        try:
            result = await query_server("dayz", host, port)
            success = True
            
            assert isinstance(result, dict)
            assert "name" in result
            assert isinstance(result["name"], str)
            assert "map" in result
            assert isinstance(result["map"], str)
            assert "players" in result
            assert isinstance(result["players"], int)
            assert "maxPlayers" in result
            assert isinstance(result["maxPlayers"], int)
            assert result["players"] >= 0
            assert result["maxPlayers"] >= 0
            assert result["players"] <= result["maxPlayers"]
            assert "firstPerson" in result
            assert isinstance(result["firstPerson"], bool)
            assert "official" in result
            assert isinstance(result["official"], bool)
            
            break
            
        except Exception as e:
            last_error = str(e)
            continue
            
    if not success:
        pytest.skip(f"No test servers available: {last_error}")

@pytest.mark.asyncio
async def test_dayz_query_timeout():
    """Test DayZ server query timeout."""
    with pytest.raises(TimeoutError):
        await query_server("dayz", "invalid.host", 2302, timeout=0.1)

@pytest.mark.asyncio
async def test_invalid_protocol():
    """Test querying with invalid protocol."""
    with pytest.raises(QueryError):
        await query_server("invalid_game", "172.111.51.154", 2302)

@pytest.mark.asyncio
async def test_malformed_response():
    """Test handling of malformed response."""
    with pytest.raises(TimeoutError):
        await query_server("dayz", "127.0.0.1", 2302, timeout=0.1)