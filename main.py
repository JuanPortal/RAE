import discord
from discord.ext import commands
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.parse
import lxml
# from keep_alive import keep_alive

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    print("RAE ready!")


@client.command(pass_context=True, aliases=["busca", "b"])
async def buscar(ctx, arg, arg2=""):
    try:
        palabra = urllib.parse.quote(arg.lower())
        if str(arg2) != "":
            palabra = urllib.parse.quote(str(arg) + " " + str(arg2))

        url = f"https://dle.rae.es/{palabra}/"

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml")
        article = soup.find("article")

        palabra_a_mostrar = article.find("header", class_="f").text

        significados = ""

        for significado in article.find_all("p", {"class": ["j", "j1", "j2", "j3", "j4", "j5", "j6", "l2"]}):
            if len(significados + significado.text) < 2048:
                significados += significado.text + "\n\n"

        mostrar = discord.Embed(title=palabra_a_mostrar, description=significados, color=0xFFFF00)
        await ctx.send(embed=mostrar)

    except UnicodeEncodeError:
        await ctx.channel.send(f"Por el momento estamos teniendo problemas con las palabras con tilde; pronto lanzaremos la actualización. ¡Gracias por la paciencia!")

    except AttributeError as e:
        print(e)
        if str(arg2) == "":
            await ctx.channel.send(f"{palabra} no se encuentra en el diccionario")
        else:
            palabra = palabra.replace("%20", " ")
            await ctx.channel.send(f"{palabra} no se encuentra en el diccionario")


@client.command(pass_context=True, aliases=["pdd", "wotd", "deldia", "día"])
async def dia(ctx):
    req = Request("https://dle.rae.es/", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    article = soup.find("div")
    palabra = article.find("div", class_="row").find("div", class_="col-sm-4 bloqueIn").find("div", class_="").p.a.text
    # palabra.replace('1','').replace('2','')

    if palabra.endswith('1'):
        palabra = palabra[:len(palabra)-1]

    mostrar = discord.Embed(title="Palabra del día", description=palabra, color=0xFF5733)
    await ctx.send(embed=mostrar)


@client.command(pass_context=True)
async def help(ctx):
    mostrar = discord.Embed(title="Help", description="***$buscar*** *palabra*\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0devuelve el significado de la palabra\n\n***$dia***\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0retorna la palabra del día")
    await ctx.send(embed=mostrar)


client.run(os.environ["TOKEN"])
# client.run('TOKEN')
