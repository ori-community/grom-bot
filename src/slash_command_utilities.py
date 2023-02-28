import discord
from discord.ui import Item


class ContextAwareView(discord.ui.View):
    ctx: discord.ApplicationContext

    def __init__(self, ctx: discord.ApplicationContext, *items: Item, timeout: float | None = 180.0,
                 disable_on_timeout: bool = False):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.ctx = ctx
