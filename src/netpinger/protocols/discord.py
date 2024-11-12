import aiohttp
import logging
from typing import Dict, Any
from ..exceptions import QueryError

logger = logging.getLogger(__name__)

class DiscordProtocol:
    """Protocol for querying Discord guild information via the Discord API."""
    
    async def query(self, guild_id: str, port: int = None, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Query a Discord guild and return its information.
        
        Args:
            guild_id: The Discord guild ID (used instead of host)
            port: Not used for Discord protocol
            timeout: Query timeout in seconds
            
        Returns:
            Dict containing guild information
            
        Raises:
            QueryError: If the query fails
        """
        if not isinstance(guild_id, str):
            raise QueryError("Guild ID must be a string due to precision limitations")
            
        api_url = f"https://discord.com/api/guilds/{guild_id}/widget.json"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url, timeout=timeout) as response:
                    if response.status != 200:
                        logger.error(f"Discord API returned status {response.status} for guild ID {guild_id}")
                        raise QueryError(f"Discord API returned status {response.status}")
                    
                    data = await response.json()
                    
                    # Format response similar to other game servers
                    result = {
                        "name": data.get("name", "Unknown Server"),
                        "connect": data.get("instant_invite") or f"https://discord.com/channels/{guild_id}",
                        "players": [],
                        "maxplayers": 500000,  # Discord's theoretical limit
                        "raw": data.copy()
                    }
                    
                    # Process player list
                    members = data.get("members", [])
                    for member in members:
                        player = member.copy()
                        name = player.pop("username", "Unknown")
                        player["name"] = name
                        result["players"].append(player)
                        
                    # Remove members from raw data since we processed them
                    if "members" in result["raw"]:
                        del result["raw"]["members"]
                        
                    return result
                    
            except aiohttp.ClientError as e:
                logger.error(f"Failed to query Discord API: {str(e)}")
                raise QueryError(f"Failed to query Discord API: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error querying Discord: {str(e)}")
                raise QueryError(f"Unexpected error querying Discord: {str(e)}")
