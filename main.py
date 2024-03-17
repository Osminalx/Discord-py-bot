from typing import Final,Optional
import os
from rembg import remove
from dotenv import load_dotenv
from random import choice
from discord import Intents,sync,Attachment, Embed, File
from discord.ext import commands
import io
from poke_search import PokemonInfo
import chance_games


#load dotenv
load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_KEY')

#Intents and commands setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix='$',intents=intents)

#commands
@bot.command(name= 'test', description= 'Just a test command')
async def test(ctx, arg: str):
    await ctx.send(arg)

@bot.command(name='select', description='Se dan varias opciones y se elige una al azár')
async def select(ctx,*args):
    await ctx.send(f'La suerte eligió {choice(args)}')

@bot.command(name='flipc', description='se lanza una moneda y dice si ganó cara o cruz')
async def flipc(ctx):
    selection = chance_games.flip_a_coin()
    if selection == 1:
        await ctx.send("Ganó Cara")
    else:
        await ctx.send("Ganó Cruz")

@bot.command(name='poke', description= 'Se pasa un nombre o id y se devuelve una tarjeta con información de un pokemon')
async def poke(ctx,pokemon):
    poke_info = PokemonInfo()
    poke_data = poke_info.get_pokemon_info(pokemon)

    embed = Embed()

    sprite = poke_data['sprite']
    name =  poke_data['name']
    pkid = poke_data['id']

    embed.set_image(url=sprite)  
    embed.title = f"{name} # {pkid}"  
    embed.description = f"Types: {poke_data['types']} \n Abilities: {poke_data['abilities']} \n Weight: {poke_data['weight']} \n Weaknesses: {poke_data['weaknesses']} \n inmune to: {poke_data['inmune_to']}"

    await ctx.send(embed=embed)


@bot.command(name='rmbg', description='Se le pasa una imagen y devolverá la misma imagen sin fondo')
async def rmbg(ctx,img: Optional[Attachment]):
    if img is None:
        await ctx.send('You did not upload anything!')
    else:
        img_bytes = await img.read()
        output_bytes = remove(img_bytes)
        with io.BytesIO(output_bytes) as file:
            file.seek(0)
            await ctx.send(file=File(file, 'output.png'))






#login
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


def main() -> None:
    bot.run(token=TOKEN)



if __name__ == '__main__':
    main()