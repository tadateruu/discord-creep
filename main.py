import discord
from discord.ext import commands, tasks
import os
import datetime

# id to receive join/leave logs
#notify_id = 

# ids to ignore logging
ignore_ids = {}

# separate verif channel media logging
verif_channel_id = 

# replace this with whatever
welcome_message = "Put your welcome message here."

# initialize dirs
os.makedirs('msg_logs', exist_ok=True)
os.makedirs('media_logs', exist_ok=True)
os.makedirs('verif_logs', exist_ok=True)
os.makedirs('join_logs', exist_ok=True)

def Latency():
    global latC
    latC = round(client.latency * 1000)

client = commands.Bot(command_prefix="ika do ", intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="Always"))
    print('Lurker is online :D')

@client.event
async def on_member_join(member):
    currenttime=str(datetime.datetime.now())
    join_log_dir = f'join_logs/join.log'
    with open(str(join_log_dir), 'a') as entry:
        entry.write(f'[{currenttime}]: {member.id} ({member})')
    await member.send(welcome_message)
    #notify_who = client.get_user(notify_id)
    #await notify_user.send(f':green_circle: `JOINED:{member.id} ({member})`')
@client.event
async def on_member_remove(member):
    currenttime=str(datetime.datetime.now())
    leave_log_dir = f'join_logs/leave.log'
    with open(str(leave_log_dir), 'a') as entry:
        entry.write(f'[{currenttime}]: {member.id} ({member})')
    #notify_who = client.get_user(notify_id)
    #await notify_user.send(f':red_circle: `LEFT:{member.id} ({member})`')

@client.event
async def on_message(message):
    currenttime=datetime.datetime.now()
    # ignore bot and admins
    if message.author.bot:
        return
    if message.author.id in ignore_ids:
        return

    if message.attachments:

        for attachment in message.attachments:
            formatdt = currenttime.strftime("%Y-%m-%d_%H-%M-%S").replace(':', '_').replace('.', '_')
            if message.channel.id == verif_channel_id:
                await attachment.save(f'verif_logs/{message.author.id}_{formatdt}_{attachment.filename}')
                print(f'Saved:{attachment.filename} from ID:{message.author.id} (verif)')
            else:
                await attachment.save(f'media_logs/{message.author.id}_{formatdt}_{attachment.filename}')
                print(f'Saved:{attachment.filename} from ID:{message.author.id}')

    # log all msgs
    msg_log_dir = f'msg_logs/{message.author.id}.log'
    with open(str(msg_log_dir), 'a') as entry:
        currenttime=str(currenttime)
        entry.write(f'[{currenttime}]{message.author}@{message.channel.id}: {message.content}\n')


@client.command(aliases = ['testing', 'test'])
async def _test(ctx):
    Latency()
    embed = discord.Embed(title = "Test Embed", description = "Test Run", color = 0x00dd99)
    embed.add_field(name = "This is a test field.", value = "Likely in a testing stage.")
    embed.add_field(name = "Response Time", value = str(latC)+ " ms")
    embed.set_image(url = "https://yourimage.here")
    await ctx.send(content = None, embed = embed)


client.run('')
