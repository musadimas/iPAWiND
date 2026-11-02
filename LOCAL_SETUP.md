# Local setup (Windows + WSL2 + conda)

How to run iPAWiND on a Windows machine for development. The bot calls `tools/zsign`, a Linux x86-64 binary, so it must run inside WSL2 — not in native Windows Python.

## Requirements

| Tool | Version | Why |
|---|---|---|
| WSL2 + Ubuntu | 22.04 / 24.04 | Runs zsign and the bot |
| Miniforge (conda) | any | Provides Python 3.11 |
| Python | **3.11** (3.10 also works) | `aiogram==2.25.1` pins `aiohttp` 3.8.x, which does not build on Python 3.12+ |
| Node.js + npm | 18+ | Certificate checker in `tools/checker` |
| Docker Desktop | with WSL integration | Local Telegram Bot API server (port 81) |

## 1. WSL2

In PowerShell (admin):

```powershell
wsl --install -d Ubuntu
```

Reboot if asked, then open the **Ubuntu** terminal. All remaining commands run inside WSL.

> **Tip:** cloning into the WSL filesystem (`~/IPAWIND`) is much faster than working from `/mnt/c/...`, and `chmod +x` on `tools/zsign` is reliable there. Running from `/mnt/c` works, but if zsign fails with *permission denied*, move the repo.

```bash
cd ~
git clone <repo-url> IPAWIND
cd IPAWIND
```

## 2. System packages

```bash
sudo apt update
sudo apt install -y build-essential git zip unzip libssl-dev zlib1g-dev libminizip-dev nodejs npm
```

## 3. Miniforge + Python 3.11 env

Skip the install if `conda` already works.

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b
~/miniforge3/bin/conda init bash
exec bash
```

Create and activate the env:

```bash
conda create -n ipawind python=3.11 -y
conda activate ipawind
python --version   # must print 3.11.x
```

> Miniforge's `base` env may be Python 3.13/3.14. Always `conda activate ipawind` before running pip or the bot.

## 4. Python dependencies

```bash
pip install -r requirements.txt pyjwt cryptography pytz
```

`requirements.txt` lists `jwt`, but the code needs **PyJWT** (plus `cryptography` for ES256). `pytz` is imported but not listed.

## 5. Certificate checker (Node)

Run from the repo root — the checker looks for `CA-PEM/` in the current directory:

```bash
npm install node-forge ocsp
node tools/checker/resources.js
ls CA-PEM   # should contain Apple CA .pem files
```

## 6. zsign

```bash
chmod +x tools/zsign
./tools/zsign -v
```

If it complains about missing shared libraries, install them with `sudo apt install` (usually `libssl3` / `libminizip1`).

## 7. Docker (local Telegram Bot API server)

1. Install Docker Desktop on Windows.
2. Docker Desktop → **Settings → Resources → WSL integration** → enable your Ubuntu distro → **Apply & restart**.
3. Open a new WSL terminal and check: `docker version`.

Set your own `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` (from https://my.telegram.org) in `docker-compose.yml`, then:

```bash
docker compose up -d
curl -s http://localhost:81   # any HTTP response means nginx is up
```

## 8. Web folder

The bot creates per-user folders under `web_path` (`/var/www/html` by default):

```bash
sudo mkdir -p /var/www/html/uploads
sudo chown -R $USER /var/www/html/uploads
```

## 9. Configuration

### `bot/config.py`

| Setting | Value |
|---|---|
| `api_id`, `api_hash` | From https://my.telegram.org (used by Pyrogram) |
| `bot_token` | From @BotFather |
| `server_address` | URL of your [ShortFlare](https://github.com/AppleEcosystem/ShortFlare) worker — signing fails without it |
| `api_key`, `api_urls` | Shortener API key and redirect domains |
| `admin`, `reseller` | Telegram user IDs |
| `PASSWORD` | Password for exported `.p12` files |
| `web_path` | Keep `/var/www/html` unless you changed step 8 |
| `accounts` | `[{"name": "<name>", "id": "<id>"}]` — see below |

### `bot/loader.py`

Fill in the two storage clients `r2` (signed `.ipa` files) and `r2_plist` (manifests and logos): endpoint, access key, secret key, bucket, public URL.

### Apple developer accounts

Each entry in `accounts` needs a folder, or the bot will not start:

```
api/
├── README.txt                          # included in cert zips sent to users
└── <name> - <id>/
    ├── <id>.json                       # {"issuer_id": "...", "key_id": "..."}
    ├── AuthKey_<key_id>.p8             # App Store Connect API key
    └── <id>_PASSWORD.p12               # distribution certificate
```

`api/` is git-ignored — never commit it.

## 10. Run

```bash
conda activate ipawind
python -m bot
```

Logs go to the terminal and `bot.log`. Pyrogram creates `pyrobot.session` on first start.

## Notes

- **Installing on a device needs public HTTPS.** iOS only installs `itms-services://` links when the `.plist` and `.ipa` URLs are public HTTPS with a valid certificate. Signing works locally; installing from `localhost` does not.
- **Database:** `database.db` ships with the table schema. Back it up before experimenting — it holds users, redeem codes, and sessions.

## Troubleshooting

| Error | Fix |
|---|---|
| `Failed building wheel for aiohttp` / `'PyDictObject' has no member named 'ma_version_tag'` | Wrong Python. `conda activate ipawind` and check that `python --version` prints 3.11 |
| `ModuleNotFoundError: No module named 'apscheduler'` | The pip install failed partway (usually the aiohttp error above). Fix the Python version and re-run step 4 |
| `Command 'npm' not found` | `sudo apt install -y nodejs npm` |
| `The command 'docker' could not be found in this WSL 2 distro` | Turn on WSL integration in Docker Desktop (step 7) and open a new terminal |
| `NotADirectoryError: Account folder not found` | An entry in `accounts` has no matching `api/<name> - <id>/` folder |
| `Please run 'resources.js'` | Run `node tools/checker/resources.js` from the repo root |
| `./tools/zsign: Permission denied` | `chmod +x tools/zsign`; if you are on `/mnt/c`, move the repo into `~` |
| Bot can't connect to `localhost:81` | `docker compose ps`; both `api` and `nginx` must be running |
