import math
import discord
import config
from discord import option
import datetime
import aiocron

from controllers.seedgen import SeedgenParameters, OnlineOfflineStep, SeedgenWizard
from controllers.weekly import WeeklyVoteController

bot = discord.Bot()

SERVER_ID = 909423614108008448
WEEKLY_CHANNEL_ID = 1079926942456881204

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

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
@aiocron.crontab("0 16 * * sat,sun")
async def weekly_reminder():
    print("the weekly message should be sent now")
    if bot.is_ready():
        channel = bot.get_guild(SERVER_ID).get_channel_or_thread(WEEKLY_CHANNEL_ID)
        await WeeklyVoteController.weeklyReminderMessage(channel)



@aiocron.crontab("0 20 * * sat,sun")
async def weekly_message():
    channel = bot.get_guild(SERVER_ID).get_channel_or_thread(WEEKLY_CHANNEL_ID)
    await channel.send("Weekly will be ")

bot.run(config.TOKEN)

