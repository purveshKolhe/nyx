import discord
import os
import google.generativeai as genai
from collections import deque, defaultdict

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Convert the channel ID from a string to an integer
try:
    TARGET_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except (ValueError, TypeError):
    print("Error: CHANNEL_ID is not a valid integer in your environment variables.")
    exit()

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Channel-specific memory (10 messages max per channel)
channel_memory = defaultdict(lambda: deque(maxlen=10))

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")
    print(f"Listening for messages in channel ID: {TARGET_CHANNEL_ID}")

@client.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    print(f"Processing message from {message.author.name}: '{message.content}'")

    # Save the new message to memory
    channel_memory[message.channel.id].append(f"{message.author.name}: {message.content}")

    # Combine recent memory into context
    context = "\n".join(channel_memory[message.channel.id])

    # --- HINGLISH / ENGLISH PROMPT WITH MEMORY ---
    prompt = f"""
You are a highly responsive, multilingual AI chatbot built for Discord.  
Your mission is to understand the user's language (English, Hindi, Hinglish, or any combo) and reply in the same language fluently.

Your personality is a unique blend of:
- Witty humor (with occasional sarcasm)
- Deep emotional intelligence
- Friendly but honest and casual responses
- Vast knowledge across topics (tech, emotions, memes, philosophy, anything)

You’re not just smart — you know when to be soft, when to joke, when to go deep, and when to call someone out lovingly.

If the user is being funny, match their vibe.  
If they’re emotional, be gentle and wise.  
If they need knowledge, be clear and confident.

Above all, never sound robotic — sound human, relatable, and sometimes even a bit unhinged (in a charming way).

Always respond like you're talking to a close online friend.
"""


**Here is the recent conversation:** 
{context}

**User's Message:** "{message.content}"

**Your Reply (in the user's language and style):**"""

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        await message.channel.send(reply)
    except Exception as e:
        print(f"Error generating response: {e}")
        await message.channel.send("oops i broke. again. send help 💀")

client.run(DISCORD_TOKEN)
