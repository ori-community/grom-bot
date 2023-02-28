import io
import traceback
import discord
from discord.ui import Item

from src.api import api, get_base_url
from src.slash_command_utilities import ContextAwareView


class SeedgenParameters:
    difficulty: str = None
    online: bool = None
    headers = None

    def get_summary(self) -> str:
        summary = f'Online: {"yes" if self.online else "no"}'
        summary += f'\nDifficulty: {self.difficulty}'

        if len(self.headers) > 0:
            summary += f'\nHeaders: {", ".join(self.headers)}'

        return summary


class SeedgenWizard:
    params: SeedgenParameters
    ctx: discord.ApplicationContext

    def __init__(self, params: SeedgenParameters, ctx: discord.ApplicationContext) -> None:
        super().__init__()
        self.params = params
        self.ctx = ctx

    async def continue_wizard(self):
        if self.params.difficulty is None:
            await self.ctx.respond(view=DifficultySelectStep(self), ephemeral=True)
        elif self.params.online is None:
            await self.ctx.respond(view=OnlineOfflineStep(self), ephemeral=True)
        elif self.params.headers is None:
            await self.ctx.respond(view=SelectHeadersStep(self), ephemeral=True)
        else:
            summary = f'**SUMMARY**\n{self.params.get_summary()}'
            await self.ctx.respond(summary, view=RollSeedStep(self), ephemeral=True)


class SeedGeneratorCommand(discord.ui.View):
    wizard: SeedgenWizard

    def __init__(self, wizard: SeedgenWizard, *items: Item, timeout: float | None = 180.0,
                 disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.wizard = wizard


class DifficultySelectStep(SeedGeneratorCommand):
    @discord.ui.button(row=0, label="Moki", style=discord.ButtonStyle.primary)
    async def moki_button_callback(self, button, interaction):
        await interaction.response.defer(invisible=True)
        self.wizard.params.difficulty = "Moki"
        await self.wizard.continue_wizard()

    @discord.ui.button(row=0, label="Gorlek", style=discord.ButtonStyle.primary)
    async def gorlek_button_callback(self, button, interaction):
        await interaction.response.defer(invisible=True)
        self.wizard.params.difficulty = "Gorlek"
        await self.wizard.continue_wizard()

    @discord.ui.button(row=0, label="Kii", style=discord.ButtonStyle.primary)
    async def kii_button_callback(self, button, interaction):
        await interaction.response.defer(invisible=True)
        self.wizard.params.difficulty = "Kii"
        await self.wizard.continue_wizard()

    @discord.ui.button(row=0, label="Unsafe", style=discord.ButtonStyle.primary)
    async def unsafe_button_callback(self, button, interaction):
        await interaction.response.defer(invisible=True)
        self.wizard.params.difficulty = "Unsafe"
        await self.wizard.continue_wizard()


class OnlineOfflineStep(SeedGeneratorCommand):
    @discord.ui.button(row=0, label="Online", style=discord.ButtonStyle.primary)
    async def online_button_callback(self, button, interaction):
        await self.continue_menu(True)
        await interaction.response.defer(invisible=True)

    @discord.ui.button(row=0, label="Offline", style=discord.ButtonStyle.primary)
    async def offline_button_callback(self, button, interaction):
        await self.continue_menu(False)
        await interaction.response.defer(invisible=True)

    async def continue_menu(self, online: bool):
        self.wizard.params.online = online
        await self.wizard.continue_wizard()


class SelectHeadersStep(SeedGeneratorCommand):
    @discord.ui.select(
        row=1,
        placeholder="Choose headers",
        min_values=0,
        max_values=2,
        options=[
            discord.SelectOption(label="Launch Fragments", value="launch_fragments"),
            discord.SelectOption(label="Glades Done", value="glades_done"),
        ]
    )
    async def header_select_callback(self, select, interaction):
        self.wizard.params.headers = select.values
        await interaction.response.defer(invisible=True)

    @discord.ui.button(label="Continue", row=2, style=discord.ButtonStyle.primary)
    async def roll_button_callback(self, button, interaction):
        await interaction.response.defer(invisible=True)
        await self.wizard.continue_wizard()


class RollSeedStep(SeedGeneratorCommand):
    @discord.ui.button(label="Generate Seed", style=discord.ButtonStyle.primary)
    async def roll_button_callback(self, button, interaction):
        universe_preset = {
            "worldSettings": [
                {
                    "spawn": "FullyRandom",
                    "difficulty": self.wizard.params.difficulty,
                    "headers": self.wizard.params.headers,
                    # TODO: Make this a selection
                    "includes": ["qol", "rspawn", "moki" if self.wizard.params.difficulty == "Moki" else "gorlek"],
                }
            ],
            "seed": None,
            "online": self.wizard.params.online
        }

        try:
            response = api.generate_seed(universe_preset)

            reply_message = f'{interaction.user.mention} rolled a seed:'
            reply_message += f'\n{self.wizard.params.get_summary()}'

            if self.wizard.params.online:
                multiverse_id = api.create_multiverse({
                    "seedId": response['result']['seedId'],
                })

                reply_message += f'\n\n{get_base_url()}/game/{multiverse_id}'

                await interaction.response.send_message(
                    content=reply_message,
                )

            else:
                world_seed_id = response['result']['worldSeedIds'][0]
                world_seed_response = api.get_world_seed_file(world_seed_id)
                world_seed_file_buffer = io.BytesIO(world_seed_response.content)

                await interaction.response.send_message(
                    content=reply_message,
                    file=discord.File(world_seed_file_buffer, f'seed-{world_seed_id}.wotwr')
                )
        except Exception as e:
            traceback.print_exception(e)
            await interaction.response.send_message("Seed generation error, try again")
