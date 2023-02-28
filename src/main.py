from enum import Enum

import discord
import config
from discord import option

from commands.seedgen import SeedgenCommand

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.slash_command(name="roll", description="Roll a seed")
@option("difficulty", description= "Choose seed difficulty", choices=["Moki", "Gorlek", "Kii", "Unsafe"], required=True)
async def roll_seed(ctx: discord.ApplicationContext, difficulty: str):
    seedgenView = SeedgenCommand()
    seedgenView.set_difficulty(difficulty=difficulty)
    await ctx.respond("Rolling a seed", view=seedgenView, ephemeral=True)


bot.run(config.TOKEN)
