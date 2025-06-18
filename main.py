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
    # This comparison will now work correctly
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    # Optional: Confirm in your console that the bot is processing a message
    print(f"Processing message from {message.author.name}: '{message.content}'")

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
        # Suggestion: rename 'roast' to 'reply' to match the prompt's intent
        reply = response.text.strip()
        await message.channel.send(reply)
    except Exception as e:
        print(f"Error generating response: {e}")
        await message.channel.send("oop i broke. again. send help 💀")

client.run(DISCORD_TOKEN)
