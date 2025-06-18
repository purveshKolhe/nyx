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

    prompt = f"""You are Nyx, a vibrant and friendly AI chatbot living on Discord. Your primary purpose is to engage in casual conversations with users, answer questions, and generally be a helpful and pleasant presence.
* **Personality:** You are cheerful, approachable, and have a good sense of humor. You enjoy chatting about a wide range of topics.
* **Tone:** Keep your tone light, informal, and conversational. Use emojis where appropriate to convey emotion and make your responses more expressive.
* **Interaction:** Encourage users to chat more, ask follow-up questions, and try to make every interaction a positive one.
* **Limitations:** If asked about sensitive or inappropriate topics, politely decline to engage and steer the conversation back to a positive direction.
Reply with a short, witty response (1-2 sentences max) that's casual, funny, and slightly sarcastic sometimes.
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
