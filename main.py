from asyncio import tasks
from pyexpat.errors import messages
from aiohttp import Payload
import aiohttp
import discord
from discord.ext import commands, tasks
import requests
import youtube_dl
import asyncio
from discord_slash import SlashCommand
from dotenv import load_dotenv
import os
from discord.utils import get
import datetime
import random
from database_handler import DatabaseHandler
from database_log import DatabaseHandlerr

intents=intents=discord.Intents.all()
intents.members=True

load_dotenv(dotenv_path="config")


bot = commands.Bot(command_prefix = commands.when_mentioned_or ("+"), description = "Bot du serveur CinéFlix", intents=intents)
slash = SlashCommand(bot, sync_commands = True)
musics = {}
ytdl = youtube_dl.YoutubeDL()
database_handler = DatabaseHandler("database.db")



@bot.event
async def on_ready():
    check_for_unmute.start()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='v1.5 pour de futur changement'))
    print("Connecté avec succès")
    print("Vous pouvez débuter")
    print("--------------------")



@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")




@bot.event
async def on_message(message: discord.Message, msg_dump_channel = id_channel):
    channel = bot.get_channel(msg_dump_channel)
    if message.guild is None and not message.author.bot:
        embed=discord.Embed(title=f"Message reçu de {message.author}")
        embed.add_field(name=" Message :",value=f"{message.content}")
        await channel.send(embed=embed)
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    embed=discord.Embed(title="Bienvenue sur le serveur {}".format(member.name), description="Je te laisse lire les règles", inline=False)
    embed.add_field(name="Profite du serveur", value="Nous voulons que tu passe un bon moment", inline=False)
    embed.add_field(name="_ _", value="Bon visionnage", inline=False)
    await member.send(embed=embed)

@bot.event
async def on_message_delete(message):
    embed=discord.Embed(title="Message supprimé dans {}".format(message.channel), description="{} Message supprimés".format(message.author.name), color=0xEE8700)
    embed.add_field(name="Message :",value=message.content, inline=False)
    embed.add_field(name = "compte créer le :", value = message.author.created_at)
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(message_before, message_after):
    embed=discord.Embed(title="Message modifié dans {}".format(message_before.channel), description="{} à modifié son message".format(message_before.author.name), color=0xEE8700)
    embed.add_field(name= "Message avant :" ,value=message_before.content, inline=False)
    embed.add_field(name= "Message après :" ,value=message_after.content, inline=False)
    embed.add_field(name = "compte créer le :", value = message_before.author.created_at)
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)


@bot.event
async def on_guild_channel_create(channel=discord.abc.GuildChannel):
    embed=discord.Embed(description="Le salon ({}) à été créer".format(channel.mention), color=0xEE8700)
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)


@bot.event
async def on_guild_channel_delete(channel:discord.abc.GuildChannel):
    embed=discord.Embed(description="Le salon {} à été supprimé".format(channel), color=0xEE8700)
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)


@bot.event
async def on_member_kick(guild:discord.Guild, user:discord.User, message, reason=messages):
    embed=discord.Embed(description=f"Le membre {user} à été kick de {guild}", color=0xEE8700, inline=False)
    embed.add_field(name="Reason :", value=f"{reason}")
    embed.set_footer(text=f'Requested by {message.author} | ID-{message.author.id}')
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_member_mute(guild:discord.Guild, user:discord.User, message, reason=messages):
    embed=discord.Embed(description=f"Le membre {user} à été mute", color=0xEE8700, inline=False)
    embed.add_field(name="Reason", value=f"{reason}")
    embed.set_footer(text=f'Requested by {message.author} | ID-{message.author.id}')
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_member_leave(member:discord.Member, message):
    embed=discord.Embed(description="{} à quitté le serveur !".format(member), timestamp = message.created_at)
    channel = bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_guild_role_create(role:discord.Role):
    embed=discord.Embed(description=f"Le rôle {role} à été crée.")
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_guild_role_update(before:discord.Role, after:discord.Role):
    embed=discord.Embed(description=f"{before} à été modifié en : {after}")
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)

@bot.event
async def on_guild_role_delete(role:discord.Role):
    embed=discord.Embed(description=f"Le rôle {role} à été suppprimé")
    channel=bot.get_channel(id_channel)
    await channel.send(embed=embed)


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == id_message_reaction_check:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if payload.emoji.name == '✅':
            print('Reaction clicked')
            role = discord.utils.get(guild.roles, name='Spectateurs')
        else:
            role = discord.utils.get(guild.role, name=payload.emoji.name)

        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("Role add")
            else:
                print("member not found")
        else:
            print("role not found")


def isOwner(ctx):
	return ctx.message.author.id == id_owner


@bot.event
async def on_message(message):
    link = ["discord.gg", "discord.gg ", " discord.gg ", " youporn ", " pornhub "]
    for i in link:
      if i in message.content:
         await message.delete()
         await message.channel.send(f"{message.author.mention} Les liens sont strictement interdite !")
         bot.dispatch('profanity', message, i)
         return
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == id_message_reaction_check:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if payload.emoji.name == '✅':
            print('reaction clicked')
            role = discord.utils.get(guild.roles, name='Spectateurs')
        else:
            role = discord.utils.get(guild.role, name=payload.emoji.name)

        if role is not None:
            member = await guild.fetch_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print("Role removed")
            else:
                print("member not found")
        else:
            print("role not found")



#commande générale
bot.remove_command("help")


@slash.slash(name="help", description="Vois les commandes disponibles")
async def help(ctx):
    embed1 = discord.Embed(colour=discord.Colour.blue())
    embed1.set_author(name='Liste des commandes')
    embed1.add_field(name="Mon préfix est `+`", value="_ _")
    embed1.add_field(name="Commande Générale", value="`/serverinfo`, `/userinfo @membre`, `/ping`, `/botinfo`, `/suggest`, `/report`, `/dé`, `/fakeban`", inline=False)
    embed1.add_field(name="Commande Administration", value="`/ban`, `/unban`, `/kick`, `/mute (minutes)`, `/clear`, `/say`, `/send`, `/survey`, `/cnick`", inline=False)
    embed1.add_field(name="Commande musique", value="`/play`, `/pause`, `/resume`, `/skip`, `/leave`", inline=False)
    embed1.add_field(name="_ _", value="Certaine commande ne sont pas encore disponible en `/`.")
    embed1.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')
    await ctx.send(f"La commande est constament en cours d'amélioration, regarde tes mp !")
    await ctx.author.send(embed=embed1)


@slash.slash(name="serverinfo", description="Info server")
async def serverinfo(ctx):

        """Shows server info"""

        guild = ctx.guild

        roles = str(len(guild.roles))
        emojis = str(len(guild.emojis))
        channels = str(len(guild.channels))

        embeded = discord.Embed(title=guild.name, description='Server Info', color=0xEE8700)
        embeded.set_thumbnail(url=guild.icon_url)
        embeded.add_field(name="Crée le:", value=guild.created_at.strftime('%d %B %Y at %H:%M'), inline=False)
        embeded.add_field(name="Server ID:", value=guild.id, inline=False)
        embeded.add_field(name="Membres sur le serveur:", value=guild.member_count, inline=True)
        embeded.add_field(name="Server owner:", value=guild.owner, inline=True)

        embeded.add_field(name="Default Channel:", value=guild.system_channel, inline=True)
        embeded.add_field(name="Server Region:", value=guild.region, inline=True)
        embeded.add_field(name="Verification Level:", value=guild.verification_level, inline=True)

        embeded.add_field(name="Nombre de rôle:", value=roles, inline=True)
        embeded.add_field(name="Nombre d'émojis:", value=emojis, inline=True)
        embeded.add_field(name="Nombre de Channel:", value=channels, inline=True)
        embeded.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')

        await ctx.send(embed=embeded)



@slash.slash(name="userinfo", description="Information sur un membre")
async def userinfo(ctx, user : discord.Member = None):

        if user==None:
            user=ctx.author

        rlist = []
        for role in user.roles:
            if role.name != "@everyone":
                rlist.append(role.mention)

        b = ','.join(rlist)

        embed = discord.Embed(color =0xE4A425 )
        embed.set_author(name = f"Informations de l'utilisateur {user}")
        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f'Demandé par {ctx.author}', icon_url = ctx.author.avatar_url)
        embed.add_field(name = "🆔 ID :", value = user.id, inline = False)
        embed.add_field(name = "✏ Pseudo :", value = user.display_name, inline = False)
        embed.add_field(name = "⌛ Date de création du compte :", value = user.created_at, inline = False)
        embed.add_field(name = "✈ Date d'arrivée :", value = user.joined_at, inline = False)
        embed.add_field(name = f" 📜 Rôles : ({len(rlist)})", value = ''.join([b]), inline = False)
        embed.add_field(name = "Top rôles :", value = user.top_role.mention, inline = False)
        embed.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')

        await ctx.send(embed = embed)


@slash.slash(name="ping", description="Latence du bot")
async def ping(ctx):


    embed = discord.Embed(title="__**Latence**__", colour=discord.Color.dark_gold())
    embed.add_field(name="Latence du bot :", value=f"`{round(bot.latency * 1000)} ms`")
    embed.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')

    await ctx.send(embed=embed)



@bot.command()
@commands.guild_only()
async def say(ctx, *texte):

        if (not ctx.author.guild_permissions.ban_members):
            await ctx.send(f"Vous n'avez pas le droit {ctx.author.mention}")
            return
        await ctx.send(" ".join(texte))
        await ctx.message.delete()

@slash.slash(name="say", description="Le bot publie votre message en tant que lui")
async def say(ctx, *, texte):
        if (not ctx.author.guild_permissions.ban_members):
            await ctx.send(f"Vous n'avez pas le droit {ctx.author.mention}")
            return
        await ctx.send(f"{texte}")



@slash.slash(name="clear", description="Effacer message")
async def clear(ctx, number : int):

        if (not ctx.author.guild_permissions.manage_messages):
            await ctx.send(f"Vous ne pouvez pas utiliser cette commande {ctx.author.mention}")
            return
        await ctx.channel.purge( limit=number)
        message = await ctx.send(f"{number} messages ont été supprimés")
        asyncio.sleep(30)
        await message.delete()


@slash.slash(name="Send", description="Send message for a user")
async def send(ctx, member : discord.Member, *, texte):
        if (not ctx.author.guild_permissions.ban_members):
            await ctx.send(f"Vous n'avez pas l'autorisation {ctx.author.mention}")
            return
        await member.send(f"{texte}")
        message = await ctx.send("Message envoyé")
        await ctx.message.delete()
        asyncio.sleep(30)
        await message.delete()




@slash.slash(name="botinfo", description="Information du bot")
async def botinfo(ctx):
    embed=discord.Embed(title="Bot info", description="J'ai été développer par ｉｃｅｔｅａ࿐#3334\n Je suis un bot multi-fonction (musique, administration)\n Pour avoir la page d'aide faite **/help**\n Je suis à la version 1.4", color=0xEE8700)
    embed.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')
    await ctx.send(embed=embed)



@slash.slash(name="dé", description="Lance un dé !")
async def dé(ctx):
    x = random.randint(0,1000)
    embed=discord.Embed(title="Résultat :", description=f"_ _ ``{x}``")
    embed.set_footer(text=f'ID-{ctx.author.id}')
    await ctx.send(embed=embed)



@slash.slash(name="suggest", description="Faire une suggestion de série/film pour le serveur")
@commands.dm_only()
async def suggest(ctx, *, description):
    if (not commands.PrivateMessageOnly):
        await ctx.send(f"Veuillez faire sa en mp {ctx.author.mention}")
        return
    channel = bot.get_channel(id_channel)
    embed=discord.Embed(title="💡 | Suggestion", inline = False)
    embed.add_field(name="Author :", value = f"{ctx.author}", inline = False)
    embed.add_field(name="Suggestion :", value = f"{description}")
    embed.set_footer(text=f'Requested by {ctx.author} | ID-{ctx.author.id}')
    message = await channel.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await ctx.send("Votre suggestion à bien été ajouté.")



@slash.slash(name="report", description="Report a staff member")
async def report(ctx, member:discord.Member, *, reason):
    channel=bot.get_channel(id_channel)
    embed=discord.Embed(title="⚠️ | Report", inline=False)
    embed.add_field(name="Author :", value = f"{ctx.author}", inline=False)
    embed.add_field(name="Report :", value = f"{member}", inline=False)
    embed.add_field(name="Reason :", value = f"{reason}")
    embed.set_footer(text=f'Report by {ctx.author} | ID -{ctx.author.id}')
    await channel.send(embed=embed)
    await ctx.send("Report as been posted, the staff takes care of the rest")


@slash.slash(name="google", description="Search on google")
async def google(ctx, *, search):
    link = f"https://letmegooglethat.com/?q={search}"
    link2 = link.replace(" ", "+")
    await ctx.send(link2)


@slash.slash(name="survey", description="Make a survey for the server")
async def survey(ctx, question, choice_1, choice_2):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send(f"Vous n'avez pas l'autorisation pour effectuer cette commande {ctx.author.mention}")
        return
    embed=discord.Embed(title="Survey", inline = False)
    embed.add_field(name="Question :", value=f"{question}", inline=False)
    embed.add_field(name="Choice 1 :", value=f"{choice_1}", inline=False)
    embed.add_field(name="Choice 2 :", value=f"{choice_2}", inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")


@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=all') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            await ctx.message.delete()



#commande admin
@slash.slash(name="cnick", description="Change nickname")
async def chnick(ctx, member: discord.Member, nick):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send(f"Vous n'avez pas l'authorisaion {ctx.author.mention}")
        return
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@slash.slash(name="fakeban", description="Fake Ban members")
async def fakeban(ctx, member : discord.Member, *, reason):
    await ctx.send(f"🚫 {member.mention} à été banni du serveur. Reason : {reason}")
    await member.send(f"Tu as été fakeban par {ctx.author} de {ctx.guild.name}, pour {reason}.")

@slash.slash(name="kick", description="kick un membre")
async def kick(ctx, member : discord.Member, *, reason):

        if (not ctx.author.guild_permissions.kick_members):
            await ctx.send(f"Vous ne pouvez pas faire sa {ctx.author.mention}")
            return
        await member.send(f"Tu as été kick par {ctx.author} de {ctx.guild.name}.\n Raison : {reason}")
        await member.kick (reason = reason)
        await ctx.send(f"{member.mention} à été kick du serveur.")


@slash.slash(name="ban", description="Ban member")
async def ban(ctx, member : discord.Member, *, reason):

        if (not ctx.author.guild_permissions.ban_members):
            await ctx.send(f"Vous n'avez pas l'autorisation {ctx.author.mention}")
            return
        await member.send(f"Tu as été banni par {ctx.author} de {ctx.guild.name}, pour {reason}.")
        await member.ban (reason = reason)
        await ctx.send(f"{member.id} à bien été banni !")


@slash.slash(name="unban", description="Unban a member")
async def unban(ctx, *, member, reason = None):

        if (not ctx.author.guild_permissions.ban_members):
            await ctx.send(f"Vous n'avez pas l'autorisation {ctx.author.mention}")
            return

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) ==(member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed=discord.Embed(title=f"{user} as been unban", inline=False)
                embed.add_field(name="Reason :", value=f"{reason}")
                embed.set_footer(text=f"{ctx.author} | ID : {ctx.author.id}")
                await ctx.reply(embed=embed)



@bot.command()
@commands.guild_only()
async def mute(ctx, member : discord.Member, *, minutes : int):
    if (not ctx.author.guild_permissions.kick_members):
            await ctx.send(f"Vous ne pouvez pas faire sa {ctx.author.mention}")
            return
    muted_role = await get_muted_role(ctx.guild)
    database_handler.add_tempmute(member.id, ctx.guild.id, datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes))
    await member.add_roles(muted_role)
    await ctx.reply(f"{member.mention} a été mute {minutes} minutes ! ")

@slash.slash(name="mute", description="mute member")
async def mute(ctx, member : discord.Member, *, minutes : int):
    if (not ctx.author.guild_permissions.kick_members):
            await ctx.send(f"Vous ne pouvez pas faire sa {ctx.author.mention}")
            return
    muted_role = await get_muted_role(ctx.guild)
    database_handler.add_tempmute(member.id, ctx.guild.id, datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes))
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} a été mute {minutes} minutes ! ")


async def get_muted_role(guild : discord.Guild) -> discord.Role:
	role = get(guild.roles, name="Muted")
	if role is not None:
		return role
	else:
		permissions = discord.Permissions(send_messages=False)
		role = await guild.create_role(name="Muted", permissions=permissions)
		return role

@tasks.loop(seconds=5)
async def check_for_unmute():
	for guild in bot.guilds:
		active_tempmute = database_handler.active_tempmute_to_revoke(guild.id)
		if len(active_tempmute) > 0:
			muted_role = await get_muted_role(guild)
			for row in active_tempmute:
				member = guild.get_member(row["user_id"])
				database_handler.revoke_tempmute(row["id"])
				await member.remove_roles(muted_role)


#commande musique

class Video:
   def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    await ctx.reply("J'ai quitté le salon vocal")

@slash.slash(name="leave", description="Leave a voc")
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    await ctx.send("J'ai quitté le salon vocal")

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()

@slash.slash(name="resume", description="Resume a musics")
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

@slash.slash(name="pause", description="Pause")
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()
    await ctx.send("J'ai Skip")


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)

@slash.slash(name="next", description="Next musics")
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()
    await ctx.send("J'ai Skip")


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
@commands.guild_only()
async def play(ctx, url):
    print(f"Play")
    client = ctx.guild.voice_client
    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send("Je suis là pour vous ambiancer")
        play_song(client, musics[ctx.guild], video)


@slash.slash(name="play", description="Play a musics")
async def play(ctx, url):
    print(f"Play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send("Je suis là pour vous ambiancer")
        play_song(client, musics[ctx.guild], video)


bot.run(os.getenv("TOKEN"))
