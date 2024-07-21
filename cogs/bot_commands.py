import datetime
import sys
from typing import Optional

import asqlite
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values

utc = datetime.timezone.utc
config = dotenv_values(".env")
if config["DATABASE"]:
    db_name = config["DATABASE"]
else:
    print("Please set the DATABASE value in the .env file and restart the bot.")
    sys.exit(0)

class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name='setup', description='Basic setup command for the bot')
    @app_commands.describe(output_channel="The text channel you want notifications in.")
    @app_commands.describe(role_to_mention="The role you want mentioned in the alert. Blank = None")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    @app_commands.checks.has_permissions(administrator=True)
    async def output_setup(self, interaction: discord.Interaction, output_channel: discord.TextChannel, role_to_mention: Optional[discord.Role] = None):
        async with asqlite.connect(db_name) as conn:
            async with conn.cursor() as cursor:
                data = {
                    "guild_id": interaction.guild_id,
                    "channel_id": output_channel.id,
                }
                await cursor.execute("INSERT OR IGNORE INTO channels (guild_id,channel_id) VALUES (:guild_id, :channel_id);", data)
                await cursor.execute("UPDATE channels SET channel_id=:channel_id WHERE guild_id=:guild_id;", data)
                if role_to_mention is not None:
                    data = {"guild_id": interaction.guild_id,"role_id": role_to_mention.id}
                    await cursor.execute("UPDATE channels SET role_id=:role_id WHERE guild_id=:guild_id;", data)
                elif role_to_mention is None:
                    data = {"guild_id": interaction.guild_id,"role_id": None}
                    await cursor.execute("UPDATE channels SET role_id=:role_id WHERE guild_id=:guild_id;", data)
                await conn.commit()
        await interaction.response.send_message(f"Your output channel has been set to {output_channel.mention}!\nThe role that will be mentioned is {role_to_mention.mention if role_to_mention else '`None`'}.", ephemeral=True, delete_after=30)
        await output_channel.send("This channel is where respawn alerts will be sent!")


async def setup(bot: commands.Bot):
    await bot.add_cog(CommandsCog(bot))
    print(f"{__name__[5:].upper()} loaded")


async def teardown(bot: commands.Bot):
    await bot.remove_cog(CommandsCog(bot))  # type: ignore
    print(f"{__name__[5:].upper()} unloaded")