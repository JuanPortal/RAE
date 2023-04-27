import discord
from discord.ext import commands
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.parse
import lxml
from dotenv import load_dotenv

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())  # this is the way
client.remove_command("help")


@client.event
async def on_ready():
    print("RAE ready!")


@client.command(pass_context=True,
                aliases=["buscar", "search", "b", "lookfor"])
async def busca(ctx, arg, arg2=""):
    try:
        palabra = urllib.parse.quote(arg.lower())
        if str(arg2) != "":
            palabra = urllib.parse.quote(str(arg) + " " + str(arg2))

        print(palabra)

        url = f"https://dle.rae.es/{palabra}/"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml")

        article = soup.find("article")

        word_to_show = article.find("header", class_="f").text

        textote = ""

        for x in article.find_all(
                "p",
            {"class": ["j", "j1", "j2", "j3", "j4", "j5", "j6", "l2"]}):

            if len(textote + x.text) < 2048:
                textote += x.text + "\n\n"

        em = discord.Embed(title=word_to_show,
                           description=textote,
                           color=0xFFFF00)
        await ctx.send(embed=em)

    except UnicodeEncodeError:
        await ctx.channel.send(
            f"Por el momento estamos teniendo problemas con las palabras con tilde. Pronto lanzaremos la actualización. ¡Gracias por la paciencia!"
        )

    except AttributeError as e:
        print(e)
        if str(arg2) == "":
            await ctx.channel.send(
                f"{palabra} no se encuentra en el diccionario")
        else:
            palabra = palabra.replace("%20", " ")
            await ctx.channel.send(
                f"{palabra} no se encuentra en el diccionario")


@client.command(pass_context=True, aliases=["pdd", "deldia"])
async def wotd(ctx):
    req2 = Request("https://dle.rae.es/",
                   headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req2).read()
    soup2 = BeautifulSoup(webpage, "lxml")

    article = soup2.find("div")

    wotd = article.find("div", class_="row").find(
        "div", class_="col-sm-4 bloqueIn").find("div", class_="").p.a.text

    em = discord.Embed(title="Palabra del día",
                       description=wotd,
                       color=0xFF5733)
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def help(ctx):
    em = discord.Embed(
        title="Help",
        description=
        "***$busca*** devuelve el significado de la palabra\n\n***$wotd*** retorna la palabra del día"
    )
    await ctx.send(embed=em)


load_dotenv()
client.run(os.getenv("TOKEN"))
