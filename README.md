
# Telegram iOS app signer bot.

iPAWiND is an iOS app signer bot for Telegram. It allows users to sign and install iOS applications directly through Telegram, making the sideloading process more accessible.

Telegram Bot: [@ipawind_bot](https://t.me/ipawind_bot)

## Features

- Sign iOS apps (.ipa files) directly through Telegram
- Automatic provisioning profile management
- Support for various signing certificates
- Easy installation and configuration
- Docker support for simple deployment

## Prerequisites

- Linux server (Ubuntu/Debian recommended)
- Python 3.8+
- Node.js and npm
- Docker and Docker Compose (optional, for containerized setup)
- Telegram Bot API token

## Installation

> Developing on Windows? See [LOCAL_SETUP.md](LOCAL_SETUP.md) for a WSL2 + conda setup.

### Step 1: Update and Install Essential Packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y zip unzip build-essential checkinstall zlib1g-dev libssl-dev git make g++ pkg-config  libminizip-dev  zlib1g-dev zip unzip nodejs
```

```bash
cd iPAWIND
```

```bash
npm install node-forge ocsp && nodejs tools/checker/resources.js
```

```bash
pip3 install -r requirements.txt
```


## Step 2: Install Docker
- Follow the Docker installation guide: https://docs.docker.com/engine/install/ubuntu/

```bash
docker compose up -d
```

## Step 3: setup cloudfalre worker shortner
- https://github.com/AppleEcosystem/ShortFlare



## Step 4: Configure storage and bot settings

- Storage defaults to the bundled RustFS container (S3 API on :9000, console on :9001). Buckets are created on startup.
- Then, edit the following configuration files:

- Copy `.env.example` to `.env` and set the Telegram API ID/hash and `S3_*` storage settings (RustFS runs in docker-compose; R2/MinIO also work)
- In bot/config.py, add your bot token and required API keys


## Step 5: Run the bot
```bash
python -m bot
```

```bash
screen -dmS bot python3 -m bot
```

# Setup Complete
# Your iPAWiND setup is now ready. If you encounter any issues, double-check the configuration files and ensure all packages are properly installed. or create issue on github


## License

ipawind is licensed under the terms of MIT License. See the [LICENSE](LICENSE) file. 
