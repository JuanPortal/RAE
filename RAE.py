import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix="$")
client.remove_command("help")


@client.event
async def on_ready():
    print("RAE ready!")


@client.command(pass_context=True)
async def busca(ctx, arg):
    try:
        palabra = arg.lower()

        source = requests.get('https://dle.rae.es/' + palabra + '/').text

        soup = BeautifulSoup(source, "lxml")

        article = soup.find("article")

        word_to_show = article.find("header", class_="f").text

        textote = ""

        for x in article.find_all(
                "p", {"class": ["j", "j1", "j2", "j3", "j4", "j5", "j6", "l2"]}):

            if len(textote + x.text) < 2048:
                textote += x.text + "\n\n"

        em = discord.Embed(title=word_to_show, description=textote, color=0xFFFF00)
        await ctx.send(embed=em)

    except (ValueError, Exception):
        await ctx.channel.send(f"{palabra} no se encuentra en el diccionario")


@client.command(pass_context=True)
async def wotd(ctx):
    source = requests.get('https://dle.rae.es/').text

    soup = BeautifulSoup(source, "lxml")

    article = soup.find("div")

    pdd = article.find("div", class_="row").find("div", class_="col-sm-4 bloqueIn").find("div", class_="").p.a.text

    em = discord.Embed(title="Palabra del día", description=pdd, color=0xFF5733)
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def help(ctx):
    em = discord.Embed(
        title="Help",
        description=
        "***$busca*** devuelve el significado de la palabra\n\n***$wotd*** retorna la palabra del día"
    )
    await ctx.send(embed=em)


client.run("TOKEN")
