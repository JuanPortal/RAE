import discord
from discord.ext import commands
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.parse


client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    print("RAE ready!")


@client.command(pass_context=True, aliases=["buscar", "busca", "b"])
async def definition(ctx, *args):
    if not args:
        await ctx.send("Debes escribir una palabra.")
        return

    url = f"https://dle.rae.es/{urllib.parse.quote(' '.join(args).lower())}/"
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": "https://www.google.com/"
        }
    )

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    article = soup.find("article")

    word = article.find("h1", class_="c-page-header__title") if article else None

    if word is None:
        await ctx.send(f"**{' '.join(args)}** no se encuentra en el diccionario o está mal escrito.")
        return

    word = word.get_text(strip=True)

    definitions = []

    for definition in article.find_all(
        "li",
        class_=["j", "j1", "j2", "j3", "j4", "j5", "j6"]
    ):
        definitions.append(
            definition.find(
                "div",
                class_="c-definitions__item"
            ).get_text(" ", strip=True)
        )

    description = "\n\n".join(definitions)

    embedded = discord.Embed(
        title=word,
        description=description,
        color=0x2596BE
    )

    await ctx.send(embed=embedded)


@client.command(pass_context=True, aliases=["dia", "día", "pdd"])
async def wotd(ctx):
    req = Request( "https://dle.rae.es/", headers={ "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8", "Referer": "https://www.google.com/"})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    wotd = soup.find("span", class_="c-word-day__word").text.strip()
    embedded = discord.Embed( title="Palabra del día", description=wotd, color=0x2596BE)
    await ctx.send(embed=embedded)


@client.command(aliases=["ayuda"])
async def help(ctx):

    embedded = discord.Embed(
        title="📖 Ayuda",
        description="Comandos disponibles:",
        color=0x2596BE
    )

    embedded.add_field(
        name="🔎 `$buscar <palabra>`",
        value="Busca una palabra en el Diccionario de la RAE.\n",
        inline=False
    )

    embedded.add_field(
        name="📅 `$dia`",
        value="Muestra la palabra del día de la RAE.\n",
        inline=False
    )

    await ctx.send(embed=embedded)


client.run(os.environ["TOKEN"])

