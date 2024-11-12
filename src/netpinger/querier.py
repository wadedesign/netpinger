import asyncio
from typing import Dict, Any
from .protocols.dayz import DayZProtocol
from .protocols.discord import DiscordProtocol
from .exceptions import QueryError

PROTOCOLS = {
    "dayz": DayZProtocol,
    "discord": DiscordProtocol
}

async def query_server(game: str, host: str, port: int, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Query a game server and return its information.
    
    Args:
        game: The game protocol to use
        host: Server hostname or IP (or guild ID for Discord)
        port: Server port (not used for Discord)
        timeout: Query timeout in seconds
    
    Returns:
        Dict containing server information
    
    Raises:
        QueryError: If the protocol is not supported or query fails
    """
    protocol_class = PROTOCOLS.get(game.lower())
    if not protocol_class:
        raise QueryError(f"Unsupported game protocol: {game}")
    
    protocol = protocol_class()
    return await protocol.query(host, port, timeout) 