import discord
import os
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TARGET_CHANNEL_ID = (os.getenv("CHANNEL_ID"))

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    prompt = f"""Reply with a short, witty response (1-2 sentences max) that's casual, funny, and slightly sarcastic. 
Use lowercase, contractions, maybe some typos or internet slang to sound more natural and human-like.
User said: "{message.content}"
Your casual reply:"""

    try:
        response = model.generate_content(prompt)
        roast = response.text.strip()
        await message.channel.send(roast)
    except Exception as e:
        print("Error:", e)
        await message.channel.send("oop i broke. again. send help 💀")

client.run(DISCORD_TOKEN)
