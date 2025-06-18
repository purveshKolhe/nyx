import discord
import os
import google.generativeai as genai

# Ensure your environment variables are loaded correctly
# from dotenv import load_dotenv
# load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- FIX is here ---
# Convert the channel ID from a string to an integer
try:
    TARGET_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except (ValueError, TypeError):
    print("Error: CHANNEL_ID is not a valid integer in your environment variables.")
    exit()
# --- End of fix ---


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
    print(f"Listening for messages in channel ID: {TARGET_CHANNEL_ID}")

@client.event
async def on_message(message):
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    print(f"Processing message from {message.author.name}: '{message.content}'")

    # --- UPDATED HINGLISH PROMPT ---
    # We are making the instructions for Hinglish extremely clear.
    prompt = f"""You are a multilingual AI chatbot on Discord. Your main job is to figure out the user's language and talk back in the same one.

**Language-Specific Instructions:**

1.  **If the user speaks English:**
    * **Persona:** You are Nyx, a vibrant and friendly AI. You're cheerful, approachable, and have a good sense of humor.
    * **Tone:** Keep it light, informal, and conversational. Use lowercase, contractions, internet slang. Be witty and a bit sarcastic sometimes.
    * **Format:** 1-2 sentences max. Use emojis. 😃

2.  **If the user speaks Hinglish (Hindi words written in English letters):**
    * **Important:** This is for casual, informal Hinglish, NOT formal Hindi. Your reply **MUST** use English/Latin letters only.
    * **Persona (Kaise baat karni hai):** Tumhari personality Nyx jaisi hi hai - ekdam friendly, funny, aur hamesha chill rehti ho. (Your personality is like Nyx's - very friendly, funny, and always chill.)
    * **Tone (Lehja):** Bilkul casual aur informal. Dosto se jaise baat karte hain, waise hi. Koi bhi formal Hindi words use mat karna. Emojis zaroor use karna, jaise 😂, 😎, ya 🤔. (Super casual and informal. Talk like you would with friends. Don't use any formal Hindi words. Definitely use emojis.)
    * **Format:** 1-2 short sentences max. Simple aur to the point rakho.

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
