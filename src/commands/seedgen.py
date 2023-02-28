import io
import traceback
import discord
from src.api import api


class SeedgenCommand(discord.ui.View):
    universe_preset = {
        "worldSettings": [
            {
                "spawn": "FullyRandom",
                "difficulty": "gorlek",
                "headers": []
            }
        ],
        "seed": None
    }

    def set_difficulty(self, difficulty):
        self.universe_preset["worldSettings"][0]["difficulty"] = difficulty

    @discord.ui.select(
        row=1,
        placeholder="Choose a header",
        min_values=0,
        max_values=2,
        options=[
            discord.SelectOption(label="Launch Fragments", value="launch_fragments"),
            discord.SelectOption(label="Glades Done", value="glades_done"),
        ]
    )
    async def preset_select_callback(self, select, interaction):
        self.universe_preset["worldSettings"][0]["headers"] = select.values
        await interaction.response.defer(invisible=True)

    @discord.ui.button(label="Roll", row=2, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        world_settings = self.universe_preset["worldSettings"][0]
        difficulty = world_settings["difficulty"]
        headers = world_settings["headers"]

        try:
            response = api.generate_seed(self.universe_preset)

            world_seed_id = response['result']['worldSeedIds'][0]
            world_seed_response = api.get_world_seed_file(world_seed_id)
            world_seed_file_buffer = io.BytesIO(world_seed_response.content)

            reply_message = f'{interaction.user.mention} Rolled a seed:'
            reply_message += f'\nDifficulty: {difficulty}'

            if len(headers) > 0:
                reply_message += f'\nHeaders: {", ".join(headers)}'

            await interaction.response.send_message(
                content=reply_message,
                file=discord.File(world_seed_file_buffer, f'seed-{world_seed_id}.wotwr')
            )
        except Exception as e:
            traceback.print_exception(e)
            await interaction.response.send_message("Seed generation error, try again")
