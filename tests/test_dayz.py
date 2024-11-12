import pytest
import asyncio
from netpinger import query_server, QueryError, TimeoutError

@pytest.mark.asyncio
async def test_dayz_query_success():
    """Test successful DayZ server query."""
    # Mock server response
    result = await query_server("dayz", "127.0.0.1", 2302)
    
    assert isinstance(result, dict)
    assert "name" in result
    assert "map" in result
    assert "players" in result
    assert "maxPlayers" in result

@pytest.mark.asyncio
async def test_dayz_query_timeout():
    """Test DayZ server query timeout."""
    with pytest.raises(TimeoutError):
        await query_server("dayz", "invalid.host", 2302, timeout=0.1)

@pytest.mark.asyncio
async def test_invalid_protocol():
    """Test querying with invalid protocol."""
    with pytest.raises(QueryError):
        await query_server("invalid_game", "127.0.0.1", 2302) 