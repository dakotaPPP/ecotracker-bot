# Eco Kill Tracker Bot

## Overview

This Discord bot is designed to track "eco kills" for specified players in an online game. It interacts with Riot Games' API to retrieve in-game statistics, coding in Python and utilizing SQLite for database operations. The bot logs recent game data in JSON format, providing a comprehensive tracking mechanism.

## Features

- **Unofficial Valorant API Integration:** Makes requests to the [Unofficial Valorant API](https://github.com/Henrik-3/unofficial-valorant-api) to gather detailed information about players' in-game stats.
- **Python and SQLite:** Coded in Python, the bot utilizes SQLite for seamless interaction with its database.
- **Game Logging:** Logs recent game information in JSON format, ensuring a comprehensive record of player performance.
- **Collaborative Development:** Developed in collaboration with a Rice University student and a fellow Texas A&M University student.

## Getting Started

To get the bot up and running:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/eco-kill-tracker-bot.git
   ```

2. Open the main.py file and replace the line bot.run(os.getenv("TOKEN")) with your bot's actual token.

3. If you don't want our preset users in the user_data.db table, feel free to delete them.

4. Run the bot:

   ```bash
   python main.py
   ```

## Contributors

- [Dakota Pound](https://github.com/dakotaPPP) - requesta.py, main.py, and SQLite database (table_formatting.py)  
- [Johnnie Chen](https://github.com/chenjohnnie) - requesta.py, main.py, and discord bot initalization
- [Mac Tucker](https://github.com/Mac-Tucker) - request.py, main.py, and image manipulation and creation

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to the contributors of the [Unofficial Valorant API](https://github.com/Henrik-3/unofficial-valorant-api) for providing valuable data and to the community for contributing to the development of this bot.

---
