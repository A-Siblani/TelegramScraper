from telethon import TelegramClient
import os
from dotenv import load_dotenv
from telethon.tl.functions.channels import JoinChannelRequest

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

if not api_id or not api_hash or not bot_token:
    raise ValueError("API ID, Hash, or Bot Token is missing. Check your .env file.")

client = TelegramClient('anno', api_id=api_id, api_hash=api_hash).start(bot_token=bot_token)

async def join_channel(client, channel_link):
    
    
    """
    Joins a Telegram channel using the provided client and channel link.

    Args:
        client (TelegramClient): The TelegramClient instance to use for joining the channel.
        channel_link (str): The link to the Telegram channel to join.

    Raises:
        Exception: An error occurred while joining the channel.

    Returns:
        None
    """
    try:
        await client(JoinChannelRequest(channel_link))
        print(f'Successfully joined the channel {channel_link}')
    except Exception as e:
        print(e)

async def main():
    
    """
    Main entry point of the script. Joins a Telegram channel using the provided client and channel link.

    Raises:
        Exception: An error occurred while joining the channel.

    Returns:
        None
    """


    channel_link = 'https://t.me/Hackingbotprooo'
    await join_channel(client, channel_link) 
    

# async def main():
#     await client.send_message('@Kjlk123', 'Hello from Python!')

with client:
    client.loop.run_until_complete(main())
