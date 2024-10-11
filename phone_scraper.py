from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('anon', api_id, api_hash)


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
        
async def scrape_message(client,channel,limit=100):
    """
    Scrapes messages from a Telegram channel.

    Args:
        client (TelegramClient): The TelegramClient instance to use for scraping messages.
        channel (str): The link to the Telegram channel to scrape messages from.
        limit (int, optional): The maximum number of messages to scrape from the channel. Defaults to 100.

    Raises:
        Exception: An error occurred while scraping messages.

    Returns:
        None
    """
    async for message in client.iter_messages(channel,limit):
        if message.text:
            print(message.text)
            print("---"*40)
    
async def main():
    """
    Main entry point of the script. Joins a Telegram channel and scrapes messages from it.

    The channel to join and scrape is specified by the `channel_link` variable. The number of messages to scrape is specified by the `limit` variable.

    Raises:
        Exception: An error occurred while joining the channel or scraping messages.

    Returns:
        None
    """

    channel_link = 'https://t.me/Hackingbotprooo'
    await join_channel(client, channel_link) 
    
    await scrape_message(client,channel_link,10)
    
with client:
    client.loop.run_until_complete(main())