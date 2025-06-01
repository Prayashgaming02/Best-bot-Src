import os
os.system("pip install discord.py==1.7.3 asyncio aiohttp") 
import discord

import aiohttp
import os
import asyncio

TOKEN = "Enter your user token"  
COMMAND_PREFIX = "&"

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user} (ID: {client.user.id})")

@client.event
async def on_message(message):
    
    if message.author.id != client.user.id:
        return

    if message.content.lower().strip() == f"{COMMAND_PREFIX}steal":
        guild = message.guild

        if not guild:
            await message.channel.send("❌ This command must be used inside a server.")
            return

        await message.channel.send(f"📥 Saving emojis from **{guild.name}**...")

        # Create folder for the guild
        folder_path = os.path.join("assets", str(guild.id))
        os.makedirs(folder_path, exist_ok=True)

        saved_count = 0

        async with aiohttp.ClientSession() as session:
            for emoji in guild.emojis:
                emoji_url = str(emoji.url)
                extension = "gif" if emoji.animated else "png"
                filename = f"{emoji.name}_{emoji.id}.{extension}"
                filepath = os.path.join(folder_path, filename)

                try:
                    async with session.get(emoji_url) as resp:
                        if resp.status == 200:
                            with open(filepath, "wb") as f:
                                f.write(await resp.read())
                            saved_count += 1
                except Exception as e:
                    print(f"❌ Error saving {emoji.name}: {e}")

        await message.channel.send(f"✅ Saved `{saved_count}` emojis to `assets/{guild.id}/`")


client.run(TOKEN, bot=False)
