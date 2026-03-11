import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("BOT_A_TOKEN")
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    keep_in_vc.start()


@tasks.loop(seconds=10)
async def keep_in_vc():
    channel = await bot.fetch_channel(VOICE_CHANNEL_ID)
    vc = channel.guild.voice_client

    try:
        # bot not in VC
        if vc is None:
            await channel.connect(reconnect=True)
            print("Joined VC")

        # stale voice connection
        elif not vc.is_connected():
            await vc.disconnect(force=True)
            await channel.connect(reconnect=True)
            print("Reconnected VC")

        # dragged to another VC
        elif vc.channel.id != VOICE_CHANNEL_ID:
            await vc.move_to(channel)
            print("Moved back to correct VC")

    except Exception as e:
        print("Voice error:", e)


bot.run(TOKEN)