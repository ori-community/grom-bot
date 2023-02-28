import math

import discord
import config
from discord import option
import asyncio
import schedule
import datetime

from commands.seedgen import SeedgenParameters, OnlineOfflineStep, SeedgenWizard

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    await weekly_reminder()


@bot.slash_command(name="roll", description="Roll a seed")
@option("difficulty", description="Choose seed difficulty", choices=["Moki", "Gorlek", "Kii", "Unsafe"], required=False)
@option("online_mode", description="Online or offline?", choices=["online", "offline"], required=False)
async def roll_seed(ctx: discord.ApplicationContext, difficulty: str, online_mode: str):
    params = SeedgenParameters()

    if difficulty is not None:
        params.difficulty = difficulty

    if online_mode is not None:
        params.online = online_mode == "online"

    wizard = SeedgenWizard(params, ctx)
    await wizard.continue_wizard()


async def weekly():
    return
    #schedule.every().saturday.at("12:00").do(await weekly_reminder())
    # schedule.every().saturday.at("20:00").do(weekly_message())
    # schedule.every().sunday.at("12:00").do(weekly_reminder())
    # schedule.every().sunday.at("20:00").do(weekly_message())

async def weekly_reminder():
    channel = bot.get_channel(1079926942456881204)
    weekly_time = datetime.datetime.today()
    weekly_time = weekly_time.replace(hour=20, minute=00, second=00)
    await channel.send(f"Weekly will be happening <t:{math.floor(weekly_time.timestamp())}:R> Don't forget to vote: *insert the vote link here*")

async def weekly_message():
    channel = bot.get_channel(1079926942456881204)
    await channel.send("Weekly will be ")
async def run_bot():
    try:
        await bot.start(config.TOKEN)
    except KeyboardInterrupt:
        await bot.close()


async def main():
    await asyncio.gather(weekly(), run_bot())


asyncio.run(main())
