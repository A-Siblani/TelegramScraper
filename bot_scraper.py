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

    try:
        await client(JoinChannelRequest(channel_link))
        print(f'Successfully joined the channel {channel_link}')
    except Exception as e:
        print(e)

async def scrape_messages(client, channel_link, limit=100):

    try:
        entity = await client.get_entity(channel_link)
        messages = await client.get_messages(entity, limit=limit)
        print(f'Scraped {len(messages)} messages from {channel_link}')
        
        for message in messages:
            print(message.text) 
    except Exception as e:
        print(f"Error scraping messages: {e}")

async def main():
    channel_link = 'https://t.me/Hackingbotprooo'
    await join_channel(client, channel_link)
    await scrape_messages(client, channel_link, limit=100)
with client:
    client.loop.run_until_complete(main())
