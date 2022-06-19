from datetime import datetime
import discord
from h11 import SERVER
from Token_reader import read_token
from Prefix_Commands import *
from discord import Embed, Guild, app_commands
import sqlite3
from youtubesearchpython import VideosSearch
from discord.ext import commands
from discord.utils import get
from DiscordUtils import Music
from Defines import *

db,intents,MY_GUILD,command = sqlite3.connect("bot_database.db"),discord.Intents.all(),discord.Object(id=839639743771836456),app_commands.CommandTree
intents.members = True
intents.message_content = True
client,cr,music = commands.Bot(command_prefix='!',intents=intents),db.cursor(),Music()

users = get_users_from_db()
Blocked_Words = get_bad_words()



"""EVENTS"""
@client.event
async def on_message_delete(message):
    datetest = int(message.created_at.strftime("%I"))+2
    date = message.created_at.strftime("%Y/%m/%d, " + str(datetest) +":%M:%S")
    date_now = datetime.today().strftime("%Y/%m/%d, %I:%M:%S")
    emb = discord.Embed(title = (f"Message deletion"),description = f"A message was deleted in <#{message.channel.id}>",color = 0x6B5B95)
    emb.add_field(name = "Message Content", inline = False, value = message.content)
    emb.add_field(name = "Message Author", inline = False, value = message.author)
    emb.add_field(name = "Sent at", inline = False, value = date)
    emb.add_field(name = "Deleted at", inline = False, value = date_now)
    emb.set_footer(text=" ================\n🔥SECRET 101⚡SCR🔥")
    await client.get_channel(958072130598219847).send(embed=emb)
    await client.get_channel(958072130598219847).send('===============================================================')

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
        cr.execute(f"INSERT INTO users (user_name,id,roles) VALUES ('{member}','{member.id}','Bystanders')")
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
    await ctx.response.send_message(f"Hello! {name}")


"""Music Commands"""
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

#leave
@client.command()
async def leave(ctx) :
	if (ctx.voice_client) :
		await ctx.guild.voice_client.disconnect()
		await ctx.send("I left the voice channel")
	else :
		await ctx.send("I am not in a voice channel")
@client.tree.command(name="leave",description="Leave the voice channel", guild=MY_GUILD)
async def leave(ctx:discord.Interaction):
    if (ctx.guild.voice_client):
        await ctx.response.send_message("**LEFT**")
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.response.send_message("I am not in a voice channel")
#leave
@client.tree.command(name="play",description="Play some Music",guild=MY_GUILD)
async def play(ctx:discord.Interaction,url:str):
    if not (ctx.user.voice):
        voice_client = get(ctx.bot.voice_client,guild=MY_GUILD)
        if voice_client == None:
            channel = ctx.message.author.voice.channnel
            await channel.connect()
    player = music.get_player(guild_id = ctx.guild.id)
    if "https:" in url:
        url = url
    else:
        video = VideosSearch(url,limit = 1)
        url = video.result()['result'][0]['link']

    if not player:
        player = music.create_player(ctx,ffmmpeg_error_betterfix=True)
    if not ctx.user.voice.is_playing():
        await player.queue(url,search=True)
        song = await player.play()
        await ctx.response.send_message(f"Playing: {song.name}")
    else:
        song = await player.queue(url,search=True)
        await ctx.response.send_message(f"Queued: {song.name}")

@client.command()
async def play(ctx,*,url):
    if not (ctx.voice_client):
        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client == None :
            channel = ctx.message.author.voice.channel
            await channel.connect()
    player = music.get_player(guild_id = ctx.guild.id)
    if "https:" in url:
        url = url
    else:
        l = url
        video = VideosSearch(l,limit = 1)
        url = video.result()['result'][0]['link']
        
    if not player:
        player = music.create_player(ctx,fmmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url , search=True)
        song = await player.play()
        await ctx.send(f"Playing: {song.name}")
    else:
        song = await player.queue(url,search=True)
        await ctx.send(f"Queud: {song.name}")

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send("Paused")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send("Resumed")

@client.command()
async def stop(ctx):
    if (ctx.voice_client) :
        player = music.get_player(guild_id=ctx.guild.id)
        await ctx.guild.voice_client.disconnect()
        await player.stop()
        await ctx.send("Stopped")
    else :
        await ctx.send("I am not Playing")


@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{' ,'.join([song.name for song in player.current_queue()])}")

@client.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    playr = player.current_queue()
    await ctx.send(f"Skipped from {playr[0].name} to {playr[1].name}")

@client.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {int(volume*100)}%")
    
@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")
""""Music Commands"""


@client.tree.command(name='kick',description='Kick a specific member',guild=MY_GUILD)
async def Kick(ctx:discord.Interaction, member: discord.Member, reason: str):
    if "Admin" in str(ctx.user.roles):
        await ctx.guild.kick(member)
        await ctx.response.send_message(f"{member},{reason}")
        dm = await member.create_dm()
        await dm.send(embed=discord.Embed(title='Kick Warning',description=f"You Have been Kicked From the Server\nBecause of: {reason}"))
    else:
        await ctx.response.send_message(f"sent to admin")
        await client.get_channel(839642523722055691).send(embed=discord.Embed(title= "Kick Request", color = discord.Color.red(), description= f"{ctx.user} want's to kick {member}\nReason: {reason}")) ##in warn

@client.tree.command(name="say", description="say message in channel",guild=discord.Object(id = 839639743771836456))
async def Say(ctx:discord.Interaction, channel: discord.TextChannel, message: str):
    if "Admin" in str(ctx.user.roles):
        async with channel.typing():
            await client.get_channel(channel.id).send(message)
            await ctx.response.send_message("Message sent")
    else :
        ctx.response.send_message("You MUST be an Admin to Announce")

@client.tree.command(name="warn",description='Warn Someone',guild=MY_GUILD)
async def warn(ctx:discord.Interaction,member:discord.Member,reason:str):
    if "Admin" in str(ctx.user.roles):
        cr.execute(f"SELECT warns FROM violations WHERE id = '{member.id}'")
        newno = int(cr.fetchone()[0])+1
        cr.execute(f"UPDATE violations SET warns = '{newno}' WHERE id = '{member.id}'")
        db.commit()
        await ctx.response.send_message(
            f'"{member}" has been warned\n'
            # f'Reason : {Reason}'
              f'Now he has {newno} warns')
        dm = await member.create_dm()
        await dm.send(embed=discord.Embed(title='You are warned',description=f"Reason : {reason} \nYou have {newno} Warns NOW!"))

    else:
        await ctx.response.send_message("Waiting For Admin Approval")
        await client.get_channel(839642523722055691).send(f"Author : {ctx.user.mention} \nWant's to warn {member.mention}\nBecause of : {reason}")


@client.tree.command(name="stats",description='Shows Some Stats Of the server',guild=MY_GUILD)
async def STATS(ctx):
    cr.execute("SELECT value FROM STATS WHERE item = 'no_bad_words'")
    nobd = cr.fetchone()
    cr.execute("SELECT value FROM STATS WHERE item = 'messages'")
    msg = cr.fetchone()
    cr.execute("SELECT value FROM STATS WHERE item = 'no_users'")
    nousr = cr.fetchone() 
    await ctx.response.send_message(f"no. of bad words : {nobd[0]} , no. msg : {msg[0]} , usr : {nousr[0]}")

@client.tree.command(name="give_role",description='Give Someone a specific role',guild=MY_GUILD)
async def give_role(ctx:discord.Interaction,member:discord.Member,role:discord.Role):
    users = get_users_from_db()
    if role in member.roles:
        await ctx.response.send_message("The user has this role already")
    else:
        if member.id in users:
            cr.execute(f"SELECT roles FROM users WHERE id = '{member.id}'")
            rls = cr.fetchone()[0]
            if rls == None or rls == '':
                cr.execute(f"UPDATE users SET roles ='{role}' WHERE id = '{member.id}'")
            else:
                new_rls = f"{rls},{role}"
                cr.execute(f"UPDATE users SET roles ='{new_rls}' WHERE id = '{member.id}'")
            db.commit()
            await member.add_roles(role)
            await client.get_channel(958072130598219847).send(f"{member.mention} has been given {role} Role")
        else:
            cr.execute(f"INSERT INTO users (user_name,id,no_of_BD) VALUES ('{member}','{member.id}','0')")
            cr.execute(f"INSERT INTO ranks (id,XP,lvl) VALUES ('{member.id}','0','0')")
            cr.execute(f"UPDATE users SET roles = '{role}' WHERE id = '{member.id}'")
            db.commit()
            await member.add_roles(role)
            await client.get_channel(958072130598219847).send(f"{member.mention} has been given {role} Role")
        await ctx.response.send_message("Done")


@client.tree.command(name='remove_role',description='Remove a specific Role from Someone',guild=MY_GUILD)
async def remove_role(ctx:discord.Interaction,member:discord.Member,role:discord.Role):
    if role not in member.roles:
        await ctx.response.send_message("The user doesn't have this role already")
    else:
        cr.execute(f"SELECT roles FROM users WHERE id = '{member.id}'")
        roles = cr.fetchone()[0]
        new_roles = roles.replace(f"{role}",'')
        llrls = new_roles.replace(',,',',')
        if llrls[0] == ",":
            llrls = llrls[1:]
        elif llrls[-1] == ",":
            llrls = llrls[:-1]
        cr.execute(f"UPDATE users SET roles = '{llrls}' WHERE id = '{member.id}'")
        db.commit()
        await member.remove_roles(role)
        await ctx.response.send_message("Done")

@client.tree.command(name='check',description="check if Someone is in the DataBase",guild=MY_GUILD)
async def check(ctx:discord.Interaction,member:discord.Member):
    if member.id in users:
        await ctx.response.send_message("safe and sound")
    else:
        await ctx.response.send_message("not Found")

@client.tree.command(name='top',description="Find the Top 10 Ranks On the server",guild=MY_GUILD)
async def top(ctx:discord.Interaction):
    cr.execute(f"SELECT XP,lvl,id FROM ranks ORDER BY lvl DESC LIMIT 10")
    r = cr.fetchall()
    ha = []
    for i in range(len(r)):
        if r[i][1] > 0:
            ha.append(f"#{i+1} | [{get_user_name(r[i][2])}] | [lvl : {r[i][1]}]")
    await ctx.response.send_message(embed=discord.Embed(title="Top-10-Ranks",description="\n".join(ha),color=0x00FF00))


@client.tree.command(name='add_bad_word',description='Add Bad Word in DataBase',guild=MY_GUILD)
async def addbdword(ctx:discord.Interaction,word:str):
    global Blocked_Words
    if word in Blocked_Words:
        await ctx.response.send_message(f"Already Exists")
    else:
        xp = get_user_XP_LVL(ctx.user.id)[0]
        lvl = get_user_XP_LVL(ctx.user.id)[1]
        newxp = int(xp)+5
        tg_XP = int(lvl)*100
        if newxp >= tg_XP and "BOT" not in str(message.author.roles):
            lvl +=1
            cr.execute(f"UPDATE ranks SET XP = '0', lvl = {lvl} WHERE id = '{ctx.user.id}'")
            await message.channel.send(f"Good Job {ctx.user.mention} for advancing to level: {lvl}")
        else:
            cr.execute(f"UPDATE ranks SET XP = '{newxp}' WHERE id = '{ctx.user.id}'")
        cr.execute(f"INSERT INTO bad_words (bad_word) VALUES ('{word}')")
        db.commit()
        await ctx.response.send_message(f"Word added ||{word}||")
        Blocked_Words = get_bad_words()

@client.command()
async def صباحو(message):
    await message.channel.send("ميتين دي اصطباحه قوم نام يلا")

@client.tree.command(name='avatar',description="Show the avatar of a user",guild=MY_GUILD)
async def avatar(ctx:discord.Interaction,*,member:discord.Member=None):
    if member == None :
        member = ctx.user
        UserAvatar = member.avatar
        emb = discord.Embed(title = f"{member.name}'s Avatar", description="Look , He's so SEXY")
        emb.set_image(url = UserAvatar)
        await ctx.response.send_message(embed = emb)

    elif member != None :
        UserAvatar = member.avatar
        emb = discord.Embed(title = f"{member.name}'s Avatar", description="Look , He's so SEXY")
        emb.set_image(url = UserAvatar)
        await ctx.response.send_message(embed = emb)

@client.tree.command(name="spam",description="spam",guild=MY_GUILD)
async def spam(ctx:discord.Interaction, member:discord.Member=None):
    count = 5
    if member != None :
        while count > 0 :
            await ctx.response.send_message(member.mention)
            count = count - 1
    elif member == None :
        while count > 0 :
            await ctx.response.send_message(count)
            count = count - 1


client.run(read_token())
