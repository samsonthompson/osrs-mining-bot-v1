# OSRS Mining Bot

## Description
This project is an automated bot for Old School RuneScape (OSRS) designed to perform mining tasks. The bot utilizes OpenCV for image detection to identify and interact with in-game elements, automating the mining process.

## Features
- Automated mining of ores in OSRS.
- Image detection using OpenCV to identify rocks and other game elements.
- Customizable settings for different mining locations and ore types.

## Installation

### Prerequisites
- Python 3.x
- OpenCV
- NumPy

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/osrs-mining-bot.git
   cd osrs-mining-bot
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot settings in `config.json` to match your desired mining location and ore type.

## Usage
1. Start the OSRS client and log in to your account.
2. Position your character at the desired mining location.
3. Run the bot:
   ```bash
   python main.py
   ```

4. The bot will begin mining automatically. Monitor the console for any messages or errors.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Disclaimer
This bot is intended for educational purposes only. Use of automated bots in OSRS is against the game's terms of service and can result in account bans. Use at your own risk.
