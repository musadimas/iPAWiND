import os

from dotenv import load_dotenv

load_dotenv()

# S3-compatible storage (RustFS by default, see docker-compose.yml)
s3_endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000")
s3_region = os.getenv("S3_REGION", "us-east-1")
s3_access_key = os.getenv("S3_ACCESS_KEY", "rustfsadmin")
s3_secret_key = os.getenv("S3_SECRET_KEY", "rustfsadmin")
s3_bucket_ipa = os.getenv("S3_BUCKET_IPA", "ipa")
s3_bucket_plist = os.getenv("S3_BUCKET_PLIST", "plist")
# Public base urls the files are served from, must be HTTPS for iOS installs
s3_public_url_ipa = os.getenv("S3_PUBLIC_URL_IPA") or f"{s3_endpoint}/{s3_bucket_ipa}"
s3_public_url_plist = os.getenv("S3_PUBLIC_URL_PLIST") or f"{s3_endpoint}/{s3_bucket_plist}"

api_id = 8  # get this from my.telegram.org
api_hash = "7245de8e747a0d6fbe11f7cc14fcc0bb" # get this from my.telegram.org
bot_token = "Your Bot Token"  # get it from @botfather
server_address = "Your-url-shortner-api" # your url shortner api

PASSWORD = "1"
api_key = ""
api_urls = []

admin = [719363292] # add your telegram user ID
reseller = []

web_path = "/var/www/html"
template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>items</key>
    <array>
      <dict>
        <key>assets</key>
        <array>
          <dict>
            <key>kind</key>
            <string>software-package</string>
            <key>url</key>
            <string><![CDATA[{url}]]></string>
          </dict>
          <dict>
            <key>kind</key>
            <string>full-size-image</string>
            <key>url</key>
            <string><![CDATA[{redirect_url}]]></string>
          </dict>
          <dict>
            <key>kind</key>
            <string>display-image</string>
            <key>url</key>
            <string><![CDATA[{redirect_url}]]></string>
          </dict>
        </array>
        <key>metadata</key>
        <dict>
          <key>bundle-identifier</key>
          <string><![CDATA[{package_name}]]></string>
          <key>bundle-version</key>
          <string>1.0.0</string>
          <key>kind</key>
          <string>software</string>
          <key>title</key>
          <string>{appname}</string>
        </dict>
      </dict>
    </array>
  </dict>
</plist>"""


accounts = [
]

reseller_accounts = {
}


excluded_accounts = (

)
