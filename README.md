# Uta-Chan Bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Discord](https://img.shields.io/badge/Discord.py-7289DA?style=for-the-badge&logo=discord&logoColor=white)

## About
Uta-Chan is a Discord music bot that allows users to play music directly from YouTube. This is the V2 version of a previous music bot project, improving performance and adding new features.

## Incoming Features
- [x] Play songs from YouTube (priority)
- [ ] Queues
- [ ] Skip songs
- [x] Pause Song
- [X] Resume Song
- [X] Leave channel
- [ ] Spotify compatibility
- [ ] SoundCloud compatibility
- [ ] Deezer compatibility

## Prerequisites
Ensure you have the following installed before proceeding:
- Python 3.10+
- `ffmpeg` (required for audio processing)
- A Discord bot token

## Installation Guide
### 1. Create a Virtual Environment
Open a terminal or command prompt and navigate to the bot's directory:
```sh
python -m venv venv
```
Activate the virtual environment:
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```sh
  source venv/bin/activate
  ```

### 2. Install Dependencies
Once the virtual environment is activated, install the required dependencies:
```sh
pip install -r requirements.txt
```

### 3. Install `ffmpeg`
#### Windows
1. Download `ffmpeg` from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
2. Extract the contents to a desired location (e.g., `C:\ffmpeg`).
3. Add the `bin` folder to your system's PATH:
   - Open *System Properties* > *Environment Variables*.
   - Under *System Variables*, find `Path`, edit it, and add `C:\ffmpeg\bin`.
4. Restart your terminal and verify installation:
   ```sh
   ffmpeg -version
   ```

#### Linux
```sh
sudo apt update && sudo apt install ffmpeg -y
```
Verify installation:
```sh
ffmpeg -version
```

#### macOS
```sh
brew install ffmpeg
```
Verify installation:
```sh
ffmpeg -version
```

## Running the Bot
To start Uta-Chan, simply run the following command inside the project directory:
```sh
python ./main.py
```
Ensure your Discord bot token is properly configured before running the bot.
Please create a .env file on the root of the project before run this command.

## License
This project is licensed under the MIT License.

---
Feel free to contribute or report issues in the repository!

Happy listening! 🎵

