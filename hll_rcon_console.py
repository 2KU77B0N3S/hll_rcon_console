import socket
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

class XOR_RCON:
    def __init__(self, host, port, password, timeout=10):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.socket = None
        self.xor_key = None

    def connect(self):
        """Establish TCP connection and retrieve XOR key."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))
        self.xor_key = self.socket.recv(4096)
        print(f"Connected. Received XOR key: {self.xor_key.hex()}")

    def xor_crypt(self, data):
        """Encrypt or decrypt data using XOR with the key."""
        if not self.xor_key:
            raise ValueError("XOR key not received yet.")
        if isinstance(data, str):
            data = data.encode('utf-8')
        key_len = len(self.xor_key)
        return bytes(a ^ b for a, b in zip(data, self.xor_key * (len(data) // key_len + 1)))

    def send(self, command):
        """Send an XOR-encrypted command to the server."""
        encrypted_command = self.xor_crypt(command)
        print(f"Sending: '{command}' | Encrypted: {encrypted_command.hex()}")
        self.socket.send(encrypted_command)
        return self.receive()

    def receive(self):
        """Receive and decrypt response from the server."""
        raw_response = self.socket.recv(4096)
        print(f"Raw response: {raw_response.hex()}")
        if not raw_response:
            return ""
        decrypted_response = self.xor_crypt(raw_response)
        return decrypted_response.decode('utf-8', errors='ignore')

    def close(self):
        """Close the connection."""
        if self.socket:
            self.socket.close()
            print("Connection closed.")

def display_help():
    """Display available commands based on HLL RCON documentation."""
    commands = """
Available Commands (case-insensitive):
  General:
    help                              - List all commands
    Login <password>                  - Authorize the connection
    RconPassword <old> <new>          - Change RCON password

  Server:
    Get Name                         - Get server name
    Get Slots                        - Get current/max players
    Get GameState                    - Get match info
    Get MaxQueuedPlayers             - Get max queue size
    Get NumVipSlots                  - Get VIP reserved slots
    SetMaxQueuedPlayers <size>       - Set queue size (max 6)
    SetNumVipSlots <amount>          - Set VIP slots
    Say <message>                    - Set welcome message
    Broadcast <message>              - Broadcast message (empty to clear)
    ShowLog <timespan> ["filter"]    - Get logs from <timespan> minutes ago

  Maps:
    Get Map                          - Get current map
    Get MapsForRotation              - List all available maps
    Get ObjectiveRow_[0-4]           - List objectives for row 0-4
    RotList                          - List current rotation
    RotAdd <map> [after] [ordinal]   - Add map to rotation
    RotDel <map> [ordinal]           - Remove map from rotation
    Map <map> [ordinal]              - Switch to map
    GameLayout <obj0> ... <obj4>     - Restart with specific objectives
    QueryMapShuffle                  - Check if shuffling is enabled
    ToggleMapShuffle                 - Toggle map shuffling
    ListCurrentMapSequence           - List shuffled rotation

  Players:
    Get Players                      - List player names
    Get PlayerIds                    - List names and UIDs
    Get AdminIds                     - List admins with roles
    Get AdminGroups                  - List available roles
    Get VipIds                       - List VIPs
    PlayerInfo <name>                - Get player details
    AdminAdd <"uid"> <"role"> ["name"] - Add admin
    AdminDel <uid>                   - Remove admin
    VipAdd <"uid"> <"name">          - Add VIP
    VipDel <uid>                     - Remove VIP

  Moderation:
    Get TempBans                     - List temp bans
    Get PermaBans                    - List permanent bans
    Message <"player"> <"message">   - Message a player
    Punish <"player"> ["reason"]     - Kill a player
    SwitchTeamOnDeath <player>       - Switch team on death
    SwitchTeamNow <player>           - Switch team immediately
    Kick <"player"> ["reason"]       - Kick a player
    TempBan <"uid"> [hours] ["reason"] ["admin"] - Temp ban
    PermaBan <"uid"> ["reason"] ["admin"] - Permanent ban
    PardonTempBan <ban_log>          - Remove temp ban
    PardonPermaPan <ban_log>         - Remove permanent ban (note: typo in docs as 'PardonPermaPan')

  Configuration:
    Get Idletime                     - Get idle kick time
    Get HighPing                     - Get ping threshold
    Get TeamSwitchCooldown           - Get team switch cooldown
    Get AutoBalanceEnabled           - Check auto-balance status
    Get AutoBalanceThreshold         - Get balance threshold
    Get VoteKickEnabled              - Check vote kick status
    Get VoteKickThreshold            - Get vote kick threshold
    Get Profanity                    - List censored words
    SetKickIdleTime <minutes>        - Set idle kick time
    SetHighPing <ms>                 - Set ping threshold
    SetTeamSwitchCooldown <minutes>  - Set team switch cooldown
    SetAutoBalanceEnabled <on/off>   - Toggle auto-balance
    SetAutoBalanceThreshold <num>    - Set balance threshold
    SetVoteKickEnabled <on/off>      - Toggle vote kick
    SetVoteKickThreshold <pairs>     - Set vote kick thresholds (e.g., "0,5,25,10")
    ResetVoteKickThreshold           - Reset vote kick thresholds
    BanProfanity <words>             - Add profanities (comma-separated)
    UnbanProfanity <words>           - Remove profanities (comma-separated)

  Extra:
    exit                             - Close the connection and quit
    """
    print(commands)

def main():
    # Retrieve values from environment variables
    host = os.getenv("RCON_HOST")
    port = os.getenv("RCON_PORT")
    password = os.getenv("RCON_PASSWORD")

    # Validate environment variables
    if not host or not port or not password:
        print("Error: Missing required environment variables: RCON_HOST, RCON_PORT, or RCON_PASSWORD")
        print("Set them in a .env file or as system environment variables.")
        return

    # Convert port to integer
    try:
        port = int(port)
    except ValueError:
        print("Error: RCON_PORT must be an integer")
        return

    rcon = XOR_RCON(host, port, password)
    try:
        rcon.connect()

        # Attempt login
        login_response = rcon.send(f"Login {rcon.password}")
        print(f"Login response: '{login_response}'")

        if login_response != "SUCCESS":
            print("Login failed. Check your password and try again.")
            return

        print("Logged in successfully. Type 'help' for commands or 'exit' to quit.")
        time.sleep(1)  # Small delay after login

        while True:
            command = input("> ").strip()
            if not command:
                continue
            if command.lower() == "exit":
                break
            elif command.lower() == "help":
                display_help()
            else:
                response = rcon.send(command)
                print(f"Response: '{response}'")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        rcon.close()

if __name__ == "__main__":
    main()
