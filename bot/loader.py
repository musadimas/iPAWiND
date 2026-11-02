import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import (bot_token, accounts, reseller_accounts, api_id, api_hash,
                        s3_endpoint, s3_region, s3_access_key, s3_secret_key,
                        s3_bucket_ipa, s3_bucket_plist, s3_public_url_ipa, s3_public_url_plist)
from bot.utils.storage import S3Storage
from pyrogram import Client 

server = TelegramAPIServer.from_base("http://localhost:81")
bot = Bot(bot_token, server=server)
pyrogram_bot = Client(name="pyrobot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, no_updates=True, max_concurrent_transmissions=20)

dp = Dispatcher(bot, storage=MemoryStorage())

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

storage = S3Storage(s3_endpoint, s3_access_key, s3_secret_key,
                    s3_bucket_ipa, s3_public_url_ipa, s3_region)

plist_storage = S3Storage(s3_endpoint, s3_access_key, s3_secret_key,
                          s3_bucket_plist, s3_public_url_plist, s3_region)


from bot.utils.account_manager import AccountManager, ChineseApi

chinese_api = ChineseApi()
account_manager = AccountManager.from_list(accounts, reseller_accounts)
