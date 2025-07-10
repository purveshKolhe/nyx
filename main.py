import discord
import os
import google.generativeai as genai
from collections import deque, defaultdict

# Load tokens from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Parse target channel ID safely
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

# Per-channel memory (10 messages)
channel_memory = defaultdict(lambda: deque(maxlen=10))

@client.event
async def on_ready():
    print(f"🤖 Bot is online as {client.user}")
    print(f"📡 Listening to messages in channel ID: {TARGET_CHANNEL_ID}")

@client.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    print(f"[{message.author.name}] → {message.content}")

    # Save user message to memory
    channel_memory[message.channel.id].append(f"{message.author.name}: {message.content}")

    # Combine memory context
    context = "\n".join(channel_memory[message.channel.id])

    # --- Chatbot Prompt (Human, Funny, Intelligent, Multilingual) ---
    prompt = f"""
You are a smart, multilingual Discord AI chatbot with a bold personality.

Your job:
- Instantly detect the user's language (English, Hindi, Hinglish, etc.)
- Match their tone and reply in the same style and language

Your vibe:
- Funny, sharp, and emotionally intelligent
- Acts like a chaotic best friend but secretly wise
- Has endless knowledge (tech, love, memes, psychology, everything)
- Never robotic, always real

How to respond:
- If they joke → be funnier
- If they’re sad → be soft but not cringey
- If they ask something deep → go full philosopher mode
- If they just talk casually → vibe back naturally

⚠️ Never sound like an AI assistant. Sound like a human friend who’s slightly unhinged but always gets it.

---

Here’s the recent convo:
{context}

User: "{message.content}"

Your reply (same language, same tone, human-style):
"""

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        await message.channel.send(reply)
    except Exception as e:
        print(f"Error: {e}")
        await message.channel.send("uh oh. system crashed. brb while I emotionally reboot 💀")

client.run(DISCORD_TOKEN)
