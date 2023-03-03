import discord
import config
from discord import option
import asyncio

from commands.seedgen import SeedgenParameters, OnlineOfflineStep, SeedgenWizard

bot = discord.Bot()


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


bot.run(config.TOKEN)
