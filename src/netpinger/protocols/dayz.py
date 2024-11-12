import asyncio
import struct
from typing import Dict, Any, Tuple
from ..exceptions import QueryError, TimeoutError

class DayZProtocol:
    """Implementation of the DayZ server query protocol."""
    
    CHALLENGE_PACKET = b'\xff\xff\xff\xffTSource Engine Query\x00'
    
    async def query(self, host: str, port: int, timeout: float) -> Dict[str, Any]:
        """
        Query a DayZ server.
        
        Args:
            host: Server hostname or IP
            port: Server port
            timeout: Query timeout in seconds
        
        Returns:
            Dict containing server information
        """
        try:
            reader, writer = await asyncio.open_connection(host, port)
            
            # Send challenge request
            writer.write(self.CHALLENGE_PACKET)
            await writer.drain()
            
            # Read response
            data = await asyncio.wait_for(reader.read(4096), timeout=timeout)
            
            # Parse response
            result = self._parse_response(data)
            
            writer.close()
            await writer.wait_closed()
            
            return result
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"Query to {host}:{port} timed out")
        except Exception as e:
            raise QueryError(f"Failed to query {host}:{port}: {str(e)}")
    
    def _parse_response(self, data: bytes) -> Dict[str, Any]:
        """Parse the server response."""
        try:
            # Skip header and protocol version
            offset = 6
            
            # Read server name
            name, offset = self._read_string(data, offset)
            
            # Read map name
            map_name, offset = self._read_string(data, offset)
            
            # Read game directory
            game_dir, offset = self._read_string(data, offset)
            
            # Read game description
            description, offset = self._read_string(data, offset)
            
            # Read player counts
            players = struct.unpack('B', data[offset:offset+1])[0]
            max_players = struct.unpack('B', data[offset+1:offset+2])[0]
            
            return {
                "name": name,
                "map": map_name,
                "players": players,
                "maxPlayers": max_players,
                "gameDir": game_dir,
                "description": description
            }
            
        except Exception as e:
            raise QueryError(f"Failed to parse server response: {str(e)}")
    
    def _read_string(self, data: bytes, offset: int) -> Tuple[str, int]:
        """Read a null-terminated string from the data."""
        end = data.index(b'\x00', offset)
        string = data[offset:end].decode('utf-8', errors='ignore')
        return string, end + 1 