import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/amaterasu ", intents=intents)

@bot.event
async def on_ready():
    print(f"Đã đăng nhập: {bot.user}")

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} đã bị ban.")

@bot.command()
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"{member} đã bị mute.")

@bot.command()
@has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f"Đã thêm {role_name} cho {member}")
    else:
        await ctx.send(f"Role {role_name} không tồn tại.")

# Anti-spam đơn giản
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if len(message.content) > 200 or message.content.count("\n") > 10:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, đừng spam!")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
