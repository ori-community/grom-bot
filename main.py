import discord
import json
import requests
import io

ori_url = "https://wotw.orirando.com/api/seeds"
settings = {"worldSettings":[{"spawn":"FullyRandom","difficulty":"gorlek","headers": []}],
            "seed":None}

data = json.load(open("config.json"))
bot = discord.Bot()

class SeedgenView(discord.ui.View):
    @discord.ui.select(
        row=0,
        placeholder="Choose a difficulty",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Moki",
                value="Moki"
            ),
            discord.SelectOption(
                label="Gorlek",
                value="Gorlek"
            ),
            discord.SelectOption(
                label="Kii",
                value="Kii"
            ),
            discord.SelectOption(
                label="Unsafe",
                value="Unsafe"
            )
        ]
    )
    async def difficulty_select_callback(self, select, interaction):
        settings["worldSettings"][0]["difficulty"] = select.values[0]
        await interaction.response.defer(invisible=True)

    @discord.ui.select(
        row=1,
        placeholder="Choose a header",
        min_values=0,
        max_values=2,
        options=[
            discord.SelectOption(
                label="Launch Fragments",
                value="launch_fragments"
            ),
            discord.SelectOption(
                label="Glades Done",
                value="glades_done"
            ),
            # discord.SelectOption(
            #     label="Glitches"
            # ),
            # discord.SelectOption(
            #     label="FullBonus"
            # )
        ]
    )
    async def preset_select_callback(self, select, interaction):
        settings["worldSettings"][0]["headers"] = select.values
        await interaction.response.defer(invisible=True)

    @discord.ui.button(label="Roll", row=2, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        difficulty = settings["worldSettings"][0]["difficulty"]
        headers = settings["worldSettings"][0]["headers"]
        response = requests.post(ori_url, json=settings)
        if response.status_code == 201:
            response_json = json.loads(response.text)
            get_response = requests.get(f"https://wotw.orirando.com/api/world-seeds/" + str(response_json["result"]["worldSeedIds"][0])+"/file")
            seed_buffer = io.BytesIO(get_response.content)
            await interaction.response.send_message(content=f"{interaction.user.mention} Rolled a seed with difficulty: { difficulty }"+(f", headers: {headers} " if len(headers)>0 else ""), file=discord.File(seed_buffer, "Seed.wotwr"))
        else:
            await interaction.response.send_message("Seed generation error, try again")


@bot.event
async def on_ready():
    print(f"{bot.user} is online")

@bot.slash_command(name="roll", description="Roll a seed")
async def roll_seed(ctx):
    await ctx.respond("Rolling a seed", view=SeedgenView(), ephemeral=True)

bot.run(data["token"])