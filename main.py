import discord
from discord.ext import commands
import json, botdb, aiosqlite
from datetime import datetime as dt


# - - - - - -
#   CASHEWBOT V4  ---  PHOENIX PROJECT
#       Another write-over inspired by the
#       rapid and wonderful new development of
#       Discord bot 'Geo', produced by DGTILL.
#
#       Uh oh, Natasha's 'robot.bd' is also getting
#       a reboot. This is a bot war. I'm doomed.
#
#       Sole developer:
#           Github  : https://github.com/casheww
#           Discord : @casheww#7881 [444857307843657739]
#
#           https://tse3.mm.bing.net/th?id=OIP.pr73nqt5kalqmB2ykQPmKwAAAA&pid=Api
# - - - - - -


with open('_keys.gitignore') as file:
    keys = json.load(file)
    bot_token = keys['discord']


async def get_prefix(clnt, message):
    default_prefix = '##'

    guild_info = await botdb.get_guild_data(clnt.db, message.guild.id)

    if message.guild:
        try:
            return guild_info['info']['prefix']
        except (KeyError, TypeError):
            pass

    return default_prefix


client = commands.Bot(command_prefix=get_prefix)

client.remove_command('help')


@client.event
async def on_ready():
    """
    The lack of the bot var 'db' is an indication that this is the start of the uptime.
    That's important to check for because on_ready can fire more than once during the uptime.
    The use of 'db' as a bot var prevents multiple concurrent db connections.
    """

    if not hasattr(client, 'db'):
        client.db = await aiosqlite.connect('db/cashewbot.db')
        client.start_time = dt.now()

    out = '========== READY ==========\n' \
        f'\tNAME :\t\t{str(client.user)}\n' \
        f'\tID :\t\t{client.user.id}\n' \
        f'\tDT :\t\t{dt.now()}\n' \
        '========== READY ==========\n'
    print(out)


@client.command()
@commands.is_owner()
async def load(ctx, ext_name):
    client.load_extension(ext_name)

    await ctx.message.add_reaction('\U00002705')
    with open('log.txt', 'a+') as f:
        f.write(f'--- Loaded {ext_name}')


@client.command()
@commands.is_owner()
async def reload(ctx, ext_name):
    client.reload_extension(ext_name)

    await ctx.message.add_reaction('\U00002705')
    with open('log.txt', 'a+') as f:
        f.write(f'--- Loaded {ext_name}')


@client.command()
@commands.is_owner()
async def unload(ctx, ext_name):
    client.unload_extension(ext_name)

    await ctx.message.add_reaction('\U00002705')
    with open('log.txt', 'a+') as f:
        f.write(f'--- Loaded {ext_name}')


extensions = ['eh', 'help', 'devtools', 'server', 'utilities']
for extension in extensions:
    try:
        client.load_extension(f'{extension}')
    except Exception as e:
        exc = "{}: {}".format(type(extension).__name__, e)
        print("Failed to load extension {}\n{}".format(extension, e))

client.run(bot_token)
