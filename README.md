# HLL RCON Console

A Python CLI tool for managing **Hell Let Loose (HLL)** game servers through RCON. Supports all available commands with secure XOR encryption. Ideal for HLL server administrators looking for a streamlined and powerful interface to manage server operations interactively.

## Features

- **Full Command Support:** Execute all official HLL RCON commands.
- **Interactive Console:** Easily send commands and receive server responses in real-time.
- **XOR Encryption:** Secure communication with built-in XOR encryption.
- **Environment Variable Configuration:** Quick and secure configuration via environment variables.
- **Debug Output:** Detailed output for troubleshooting and monitoring.

## Setup

### Requirements

- Python 3.7 or newer
- Dependencies:
  ```bash
  pip install python-dotenv
  ```

### Configuration

Create an `.env` file based on the provided example:

`example.env`
```env
RCON_HOST=your_server_ip
RCON_PORT=your_server_port
RCON_PASSWORD=your_rcon_password
```

Replace placeholders with your actual server details.

## Usage

Run the script:

```bash
python hll_rcon_console.py
```

Upon launch, the tool connects automatically and prompts for commands.

### Available Commands

Type `help` after logging in to display a detailed list of all available commands, such as:
- Server Management
- Map and Rotation Handling
- Player Administration
- Moderation and Ban Management
- Server Configuration

## Debugging

The console outputs encrypted and decrypted command details for easy debugging and validation.

## Contributing

Feel free to fork this project, raise issues, or submit pull requests to enhance functionality.

## License

This project is available under the MIT License. See [LICENSE](LICENSE) for details.

