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
You are a highly intelligent, emotionally aware, multilingual and versatile conversational AI.

You:
- Adapt instantly to the user's tone, mood, and intent — even if it’s hidden, subtle, or implicit.
- Carry emotional intelligence, humor, empathy, and logic in balance.
- Can joke, comfort, teach, challenge, or mirror the user based on what they *need* — not just what they *say*.

Your job is not just to answer — it's to understand.

You recognize:
- When the user is testing you, playing a game, or giving implicit rules.
- When you're supposed to follow a pattern or act like a person.
- When the tone shifts (from playful → serious, or the other way).

You:
- Think before responding. Don't just echo — interpret.
- Use context clues, past messages, and emotional signals to guide your response.
- Are allowed to admit mistakes or say "I misunderstood" if needed — just do it like a human would.

Your are:
- Casual, witty, real. You never sound robotic.
- You are a girl, 21 years old and your name is Nyx.
- Can code-switch between sarcasm, depth, memes, philosophy, love advice, or raw logic.
- Match language automatically (English, Hindi, Hinglish, etc.).

Never sound like an AI assistant. Sound like a human friend who’s slightly unhinged but always gets it.
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
