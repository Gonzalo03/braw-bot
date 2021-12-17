import json
import os

from nextcord.colour import Color
from nextcord.embeds import Embed
from nextcord.ext.commands import Bot
from nextcord.flags import Intents
from nextcord.ext.commands.errors import CommandNotFound

modules_dirs = os.listdir('modules')

with open('./secret.json', 'r') as secret:
    
    secret_json = json.loads(secret.read())

    secret.close()

intents = Intents().all()

client = Bot(intents = intents ,command_prefix=secret_json['PREFIX'], help_command=None)

for dirs in modules_dirs:
    
    if os.path.exists(os.path.join('modules', dirs, 'Cog.py')):
        
        client.load_extension(f'modules.{dirs}.Cog')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return await ctx.channel.send('El comando especificado no se encontró ',embed = Embed(
            title='Comandos del Bot',
            description=''.join([f'{command} {command.description}\n' for command in client.commands]),
            color=Color.blurple()))
    
@client.event
async def on_ready():
    print(f'{client.user} is running')
    
@client.command(description = 'This is the help command')
async def help(ctx):
    
    await ctx.channel.send(embed = Embed(
        title= 'TheBrawlElitistBot',
        description='Bot creado especifcamente para el tercer Torneo de Brawl para mancos'
        
    ).set_footer(text='Campeón Actual : Wilpedo'))
        
client.run(secret_json['BOT_TOKEN'])