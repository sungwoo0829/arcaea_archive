import datetime
import json
from dis import disco
from http import client
from pydoc import cli
from ssl import CHANNEL_BINDING_TYPES
from typing import Any
from discord.ext.commands.core import Command
import requests

import discord
from discord import app_commands
from discord.ext import commands

import io



intents=discord.Intents.all()
intents.message_content=True
bot=discord.Client(intents=intents)


bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1007625110083076146))
    print(f"logged in as {bot.user}")

@bot.tree.command(
    name="ping",
    description="Check bot's response latency",
    guild=discord.Object(id=1007625110083076146)
)
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title="Pong!", description=f"Delay: {round(bot.latency*1000)} ms", color=0xFFFFFF)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(
    name="push",
    description="push score data to your google sheet",
    guild=discord.Object(id=1007625110083076146)
)
async def push(interaction: discord.Interaction):
    embed = discord.Embed(title="Pushed!", description=f"Your score data is pushed on your google sheet", color=0xFFFFFF)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
    if message.content.startswith("<@1211203828335247410>"):

        data=[]
        for attach in message.attachments:
            data.append(await attach.to_file())
        await message.channel.send(files = data)


with open("config.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data["token"]
bot.run(token)