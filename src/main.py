import discord
import config

from commands.seedgen import SeedgenCommand

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.slash_command(name="roll", description="Roll a seed")
async def roll_seed(ctx):
    await ctx.respond("Rolling a seed", view=SeedgenCommand(), ephemeral=True)


bot.run(config.TOKEN)
