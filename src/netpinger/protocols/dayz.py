import asyncio
import socket
import struct
from typing import Dict, Any, Tuple
from ..exceptions import QueryError, TimeoutError

class DayZProtocol:
    """Implementation of the DayZ server query protocol (based on Valve protocol)."""
    
    A2S_INFO = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'
    DAYZ_INFO = b'\xFF\xFF\xFF\xFFTDayZ Server Query\x00'
    
    A2S_INFO_RESPONSE = 0x49  # 'I'
    A2S_PLAYER = b'\xFF\xFF\xFF\xFF\x55'  # 'U'
    A2S_RULES = b'\xFF\xFF\xFF\xFF\x56'   # 'V'
    
    # im guessing these are the ports that dayz uses
    QUERY_PORT_OFFSETS = [24, 123, 23, 0]  
    MAX_RETRIES = 3
    
    async def query(self, host: str, port: int, timeout: float) -> Dict[str, Any]:
        """Query a DayZ server."""
        retry_timeout = timeout / self.MAX_RETRIES
        last_error = None

        # fuck we need to try multiple ports
        for offset in self.QUERY_PORT_OFFSETS:
            query_port = port + offset
            
            for query_packet in [self.A2S_INFO, self.DAYZ_INFO]:
                for attempt in range(self.MAX_RETRIES):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.settimeout(retry_timeout)
                        
                        try:
                            sock.sendto(query_packet, (host, query_port))
                            
                            data, _ = sock.recvfrom(4096)
                            
                            if not data:
                                continue
                                
                            if data.startswith(b'\xFE'):
                                # Handle split packets
                                full_data = await self._handle_split_packets(sock, data)
                                return self._parse_response(full_data)
                            
                            return self._parse_response(data)
                            
                        finally:
                            sock.close()
                            
                    except socket.timeout:
                        last_error = f"Attempt {attempt + 1} timed out"
                        continue
                    except ConnectionRefusedError:
                        last_error = "Connection refused"
                        continue
                    except Exception as e:
                        last_error = str(e)
                        continue

        raise TimeoutError(f"Query to {host}:{port} failed after trying multiple ports. Last error: {last_error}")

    async def _handle_split_packets(self, sock: socket.socket, first_packet: bytes) -> bytes:
        """Handle split packet responses."""
        try:
            packet_id = struct.unpack('<l', first_packet[4:8])[0]
            total_packets = first_packet[8]
            packet_num = first_packet[9]
            
            packets = {packet_num: first_packet[10:]}
            
            while len(packets) < total_packets:
                data, _ = sock.recvfrom(4096)
                if not data.startswith(b'\xFE'):
                    raise QueryError("Invalid split packet format")
                    
                num = data[9]
                packets[num] = data[10:]
                
            return b''.join(packets[i] for i in range(total_packets))
            
        except Exception as e:
            raise QueryError(f"Failed to handle split packets: {str(e)}")
    
    def _parse_response(self, data: bytes) -> Dict[str, Any]:
        """Parse the server response."""
        try:
            if len(data) < 5:
                raise QueryError("Response too short")
                
            if data[0:4] != b'\xFF\xFF\xFF\xFF':
                raise QueryError("Invalid response header")
                
            if data[4] != self.A2S_INFO_RESPONSE:
                raise QueryError("Invalid response type")
                
            # we skip the first 6 bytes as they are not needed
            offset = 6
            
            name, offset = self._read_string(data, offset)
            map_name, offset = self._read_string(data, offset)
            game_dir, offset = self._read_string(data, offset)
            game_desc, offset = self._read_string(data, offset)
            
            app_id = struct.unpack('<H', data[offset:offset+2])[0]
            offset += 2
            players = data[offset]
            offset += 1
            max_players = data[offset]
            offset += 1
            
            tags = ""
            try:
                if offset < len(data):
                    tags, _ = self._read_string(data, offset)
            except:
                pass
                
            server_info = {
                "name": name,
                "map": map_name,
                "players": players,
                "maxPlayers": max_players,
                "gameDir": game_dir,
                "description": game_desc,
                "appId": app_id,
                "firstPerson": "no3rd" in tags,
                "private": "privHive" in tags,
                "official": not ("external" in tags or "privHive" in tags),
                "tags": tags
            }
            
            # Extract time if present
            for tag in tags.split(','):
                if ':' in tag:
                    server_info['time'] = tag.strip()
                elif tag.startswith('lqs'):
                    try:
                        server_info['queue'] = int(tag[3:])
                    except:
                        pass
                        
            return server_info
            
        except Exception as e:
            raise QueryError(f"Failed to parse server response: {str(e)}")
    
    def _read_string(self, data: bytes, offset: int) -> Tuple[str, int]:
        """Read a null-terminated string from the data."""
        try:
            end = data.index(b'\x00', offset)
            string = data[offset:end].decode('utf-8', errors='ignore')
            return string, end + 1
        except ValueError:
            raise QueryError("Malformed string in response")