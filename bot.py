import discord
from Token_reader import read_token
from Prefix_Commands import *
from discord import app_commands
import sqlite3
from youtubesearchpython import VideosSearch
from discord.ext import commands
from discord.utils import get
from DiscordUtils import Music

db,intents,MY_GUILD,command = sqlite3.connect("bot_database.db"),discord.Intents.all(),discord.Object(id=839639743771836456),app_commands.CommandTree
intents.members = True
intents.message_content = True
client,cr,music = commands.Bot(command_prefix='!',intents=intents),db.cursor(),Music()



def get_bad_words():
    global Blocked_Words
    cr.execute("SELECT bad_word FROM bad_words")
    data = cr.fetchall()
    Blocked_Words = []
    for i in range(len(data)):
        Blocked_Words.append(data[i][0])
get_bad_words()

def get_id(user_name):
    cr.execute(f"SELECT id FROM users WHERE user_name = '{user_name}'")
    it = cr.fetchone()
    id = it[0]
    return id

def get_user_name(id):
    cr.execute(f"SELECT user_name FROM users WHERE id = '{id}'")
    user_ame = cr.fetchone()
    user_name = user_ame[0]
    return user_name

def get_users_from_db():
    global users
    cr.execute("SELECT id FROM users")
    lol = cr.fetchall()
    users = []
    for i in range(len(lol)):
        users.append(lol[i][0])
get_users_from_db()

def get_user_XP_LVL(ig):
    cr.execute(f"SELECT XP,lvl FROM ranks WHERE id = '{ig}'")
    xpdata = cr.fetchone()
    return xpdata

"""EVENTS"""
@client.event
async def on_ready():
    await client.tree.sync(guild=MY_GUILD)
    print('Sucessfully synced applications commands')
    print(f'Connected as {client.user}')
    print('------')

@client.event
async def on_member_remove(member):
    await client.get_channel(958072130598219847).send(embed=discord.Embed(title="Member Left",description=f"{member.mention} left the server"))

@client.event
async def on_member_join(member):
    if member.id not in users:
        cr.execute(f"INSERT INTO users (user_name,id,no_of_BD,roles) VALUES ('{member}','{member.id}','0','Bystanders')")
        cr.execute(f"INSERT INTO ranks (id,XP,lvl) VALUES ('{member.id}','{int(0)}','{int(0)}')")
        db.commit()
    await client.get_channel(839671710856773632).send(embed=discord.Embed(title="NEW MEMBER",description=f"Thanks {member.name} for joining!"))
    await member.add_roles(get(member.guild.roles, id=958038471656763422))

@client.listen('on_message')
async def BadWords(message):
    if "BOT" not in str(message.author.roles):
        cr.execute("SELECT value FROM STATS WHERE item = 'messages'")
        mes = cr.fetchone()
        new_mes = int(mes[0])+1
        cr.execute(f"UPDATE STATS SET value ='{new_mes}' WHERE item = 'messages'")
        db.commit()
    id = message.author.id
    username = message.author
    get_users_from_db()
    if id in users:
        cr.execute(f"SELECT XP,lvl FROM ranks WHERE id = '{id}'")
        DBxp = cr.fetchone()
        XP,lvl = DBxp[0],DBxp[1]
        new_xp,tg_XP = int(XP) + 10,int(lvl)*100
        if new_xp >= tg_XP and "BOT" not in str(message.author.roles) and tg_XP != 0:
            cr.execute(f"UPDATE ranks SET XP = '0', lvl = {lvl+1} WHERE id = '{id}'")
            db.commit()
            await message.channel.send(embed=discord.Embed(title="Congrats",description=f"Good Job {username.mention} for advancing to level: {lvl+1}"))
        else:
            cr.execute(f"UPDATE ranks SET XP = '{new_xp}' WHERE id = '{id}'")
            db.commit()
    elif id not in users and "BOT" not in str(message.author.roles):
        cr.execute(f"INSERT INTO users (user_name,id) VALUES ('{username}','{id}')")
        cr.execute(f"INSERT INTO ranks (id,XP,lvl) VALUES ('{id}','{int(0)}','{int(0)}')")
        db.commit()
    for txt in Blocked_Words:
        if txt in str(message.content.lower()) and "Admin" not in str(message.author.roles) and "BOT" not in str(message.author.roles):
            cr.execute(f"SELECT bad_words FROM violations where id = '{id}'")
            BD = cr.fetchone()
            new_BD = int(BD[0])+1
            cr.execute(f"UPDATE violations SET bad_words = '{new_BD}' WHERE id = '{id}'")
            await message.delete()
            await message.channel.send("اخلاقك يا برو ")
            cr.execute("SELECT value FROM STATS WHERE item = 'no_bad_words'")
            badwrd = cr.fetchone()
            cr.execute(f"UPDATE STATS SET value ='{int(badwrd[0])+1}' WHERE item = 'no_bad_words'")
            db.commit()



"""RANK Commmand"""
@client.tree.command(name="rank",description='Get The Rank Of a User In The Server',guild=MY_GUILD)
async def rank(ctx:discord.Interaction,user:discord.Member=None):
    if user==None:
        user=ctx.user
    r =get_user_XP_LVL(user.id)
    await ctx.response.send_message(embed=discord.Embed(title="",description=f"XP : {r[0]} / {int(r[1])*100} , LVL : {r[1]}"))
@client.command()
async def rank(ctx,user:discord.Member=None):
    if user==None:
        user=ctx.message.author
    r = get_user_XP_LVL(user.id)
    await ctx.send(embed=discord.Embed(title="",description=f"XP : {r[0]} / {int(r[1])*100} , LVL : {r[1]}"))
"""RANK Commmand"""



"""CALCULATOR"""
@client.command() 
async def calc(ctx,equation:str):
    await ctx.send(eval(equation))
@client.tree.command(name='calc',description='Do some Math', guild=discord.Object(id = 839639743771836456))
async def calc(ctx,equation:str):
    await ctx.response.send_message(eval(equation))
"""CALCULATOR"""

"""PING COMMAND"""
@client.tree.command(name="ping",description="Test The Ping of The Bot", guild=discord.Object(id = 839639743771836456))
async def ping(ctx:discord.Interaction):
    await ctx.response.send_message(f"Pong in! {round(client.latency*1000)}ms")
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong in! {round(client.latency*1000)}ms")
"""PING COMMAND"""

@client.tree.command(name= "welcome", description= "say hi", guild=discord.Object(id = 839639743771836456))
async def self(ctx: discord.Interaction, name: str):
    await ctx.response.send_message(f"Hello {name}!")


"""Music commands"""
@client.command()
async def join(ctx):
    if (ctx.author.voice):
        #if bot isnt in ANY channels
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client == None :
            channel = ctx.message.author.voice.channel
            await channel.connect()
        #if bot in channel
        else :
            #if in the SAME channel
            if (ctx.voice_client.channel.id) == (ctx.message.author.voice.channel.id) :
                await ctx.send("I am in the same voice channel")
            #if in ANOTHER channel
            elif (ctx.voice_client.channel.id) != (ctx.message.author.voice.channel.id) :
                await ctx.guild.voice_client.disconnect()
                channel = ctx.message.author.voice.channel
                await channel.connect()
    #if author isnt in ANY channels
    else :
        await ctx.send("You are not in a voice channel, you must be in a voice channnel to run this command!")

@client.tree.command(name='join',description='Join the Voice Channel', guild=discord.Object(id = 839639743771836456))
async def join(ctx:discord.Interaction):
    if (ctx.user.voice):
        #if bot isnt in ANY channels
        voice_client = get(ctx.client.voice_clients, guild=ctx.guild)
        if voice_client == None :
            channel = ctx.user.voice.channel
            await channel.connect()
            await ctx.response.send_message("**JOINED**")
        #if bot in channel
        else :
            #if in the SAME channel
            if (ctx.guild.voice_client.channel.id) == (ctx.user.voice.channel.id) :
                await ctx.response.send_message("I am in the same voice channel")
            #if in ANOTHER channel
            elif (ctx.guild.voice_client.channel.id) != (ctx.user.voice.channel.id) :
                await ctx.guild.voice_client.disconnect()
                channel = ctx.user.voice.channel
                await channel.connect()
    #if author isnt in ANY channels
    else :
        await ctx.response.send_message("You are not in a voice channel, you must be in a voice channnel to run this command!")



client.run(read_token())