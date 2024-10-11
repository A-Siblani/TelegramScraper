from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import os
import re
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
channels = os.getenv('CHANNELS', '').split(',')

if not api_id or not api_hash or not channels:
    raise ValueError("API ID, Hash, or Channel Names are missing. Check your .env file.")

client = TelegramClient('anon', api_id, api_hash)

async def join_channel(client, channel_name):
    """
    Joins a Telegram channel using the provided client and channel name.
    """
    try:
        await client(JoinChannelRequest(channel_name))
        print(f'Successfully joined the channel {channel_name}')
    except Exception as e:
        print(f"Error joining channel {channel_name}: {e}")

async def scrape_message(client, channel_name, limit=100):
    """
    Scrapes messages, photos, and videos from a Telegram channel and returns them in a list.
    Downloads media (photos and videos) and saves them in a channel-specific subdirectory.
    """
    messages = []
    
    # Create a folder for the current channel under the media directory
    media_folder = os.path.join('media', sanitize_channel_name(channel_name))
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    try:
        async for message in client.iter_messages(channel_name, limit=limit):
            if message.text:
                messages.append(f"Message: {message.text}")
            
            # Download media if available (photos, videos)
            if message.media:
                file_path = await client.download_media(message.media, media_folder)
                if file_path:
                    messages.append(f"Downloaded media: {file_path}")
            
        return messages
    except Exception as e:
        print(f"Error scraping messages from {channel_name}: {e}")
        return []

def sanitize_channel_name(channel_name):
    """
    Sanitizes the channel name by removing special characters and spaces.
    """
    # Replace any character that is not alphanumeric or underscore with an underscore
    return re.sub(r'[^\w]', '_', channel_name)

async def main():
    """
    Joins each channel listed in the CHANNELS environment variable and scrapes messages.
    Downloads media (photos, videos) and saves them to a local folder.
    Saves the messages for each channel in a separate file named after the channel in the channel_messages directory.
    """
    
    # Create the channel_messages directory if it does not exist
    channel_messages_dir = 'channel_messages'
    if not os.path.exists(channel_messages_dir):
        os.makedirs(channel_messages_dir)

    # Scrape each channel and save messages to a separate file in the channel_messages directory
    for channel_name in channels:
        channel_name = channel_name.strip()  # Clean up any leading/trailing whitespace
        if not channel_name:
            continue
        
        await join_channel(client, channel_name)
        
        # Scrape messages and media from the channel
        messages = await scrape_message(client, channel_name, limit=10)  # Adjust the limit as needed
        
        # Save the messages to a file named after the channel in the channel_messages directory
        output_file = os.path.join(channel_messages_dir, f'{sanitize_channel_name(channel_name)}_messages.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines("\n".join(messages) + "\n" + "-"*40 + "\n")
        
        print(f"Scraped messages from {channel_name} saved to {output_file}")

# Run the script
with client:
    client.loop.run_until_complete(main())
