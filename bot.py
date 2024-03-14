import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Determine the configuration module
config_module = "sample_config" if bool(os.environ.get("WEBHOOK", False)) else "config"

# Import the configuration
import importlib
Config = importlib.import_module(config_module).Config

# Ensure the download location exists
download_location = Config.DOWNLOAD_LOCATION
if not os.path.isdir(download_location):
    os.makedirs(download_location)

# Initialize Pyrogram client with plugins
plugins = {"root": "plugins"}
app = pyrogram.Client(
    "RenameBot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

# Add the admin user to the authorized users list
Config.AUTH_USERS.add(861055237)

if __name__ == "__main__":
    app.run()
