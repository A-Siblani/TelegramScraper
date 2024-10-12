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

def sanitize_channel_name(channel_name):
    """
    Sanitizes the channel name by removing special characters and spaces.
    """
    return re.sub(r'[^\w]', '_', channel_name)

def clean_message(text):
    """
    Cleans the message by removing unwanted elements like emojis, links, and certain phrases.
    """
    # Remove emojis using regex pattern for emoji ranges
    emoji_pattern = re.compile("[" u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"  # Enclosed characters
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove URLs and phrases related to links
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = url_pattern.sub(r'', text)

    # Remove unwanted phrases
    unwanted_phrases = [
        "للاشتراك في اخبارنا السريعة",
        "عبر تلغرام",
        "انقر هنا",
        " على قناة {يَسْتَبشِرُونَ} :",
    ]
    for phrase in unwanted_phrases:
        text = text.replace(phrase, '')

    # Clean up extra whitespace
    text = text.strip()

    return text

async def scrape_message(client, channel_name, limit=100):
    """
    Scrapes text messages from a Telegram channel and returns them in a list.
    """
    messages = []

    try:
        async for message in client.iter_messages(channel_name, limit=limit):
            if message.text:
                # Clean the message before appending
                clean_text = clean_message(message.text)
                if clean_text:  # Only append if there's meaningful content after cleaning
                    # Append the cleaned message with a separator
                    messages.append(f"Message: {clean_text}\n------------------------------------------------------------------------------------------")
        return messages
    except Exception as e:
        print(f"Error scraping messages from {channel_name}: {e}")
        return []

async def main():
    """
    Joins each channel listed in the CHANNELS environment variable and scrapes text messages.
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
        
        # Scrape messages from the channel (only text)
        messages = await scrape_message(client, channel_name, limit=10)  # Adjust the limit as needed
        
        # Save the messages to a file named after the channel in the channel_messages directory
        output_file = os.path.join(channel_messages_dir, f'{sanitize_channel_name(channel_name)}_messages.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines("\n".join(messages) + "\n")
        
        print(f"Scraped messages from {channel_name} saved to {output_file}")

# Run the script
with client:
    client.loop.run_until_complete(main())
