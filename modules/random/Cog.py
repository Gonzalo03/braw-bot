from datetime import datetime
from nextcord.role import R
import requests, random


from nextcord.ext.commands.errors import MissingRequiredArgument
from nextcord.ext.commands import Bot, Cog, command
from nextcord.colour import Color
from nextcord.embeds import Embed

from ..utils import from_hex


class Random(Cog):
    
    def __init__(self, bot : Bot) -> None:
        self.bot = bot
        self.uri = 'https://api.brawlapi.com/v1/'
        self.excludes_modes = ['Training','Showdown', 'Solo-Showdown', 'Duo-Showdown', 'Lone-Star', 'Trophy-Thieves', 'Takedown', 'Basket-Brawl', 'Volley-Brawl', 'Big-Game']


        
    @staticmethod
    def get_resource(url : str):

        res = requests.get(url)

        data = res.json()['list']
        
        return data
    
    @staticmethod
    def get_color(hex_code : str) -> Color:
        
        color_rgb = from_hex(hex_code)
        
        return Color.from_rgb(*color_rgb)
    
    @command(description='This command is search a map or maps randomly')
    async def rmap(self, ctx, num_map):
         
        maps = self.get_resource(self.uri + 'maps')
        
        maps = filter(lambda m: all(
        [m['gameMode']['hash'] not in self.excludes_modes ,
        not m['disabled'],
        ])
        , maps)

        maps = random.sample(list(maps), int(num_map))

        for i,m in enumerate(maps): 
            
            embed = Embed(
            title=m['name'],
            url=m['link'],
            color=self.get_color(m['gameMode']['color']),
            timestamp=datetime.now())
            
            embed.set_image(url=m['imageUrl'])
                
            embed.set_thumbnail(url=m['gameMode']['imageUrl'])
                
            embed.set_footer(text=ctx.author)
             
            await ctx.channel.send('Random Map # {}\n'.format(i+1), embed = embed)
            
            
    @command(description='This command is search a map or maps by a game mode')
    async def map_by_mode(self, ctx, num_map, game_mode):
         
        maps = self.get_resource(self.uri + 'maps')
        
        maps = filter(lambda m: all(
        [m['gameMode']['hash'] not in self.excludes_modes ,
        not m['disabled'],
        m['gameMode']['hash'].lower() == game_mode
        ])
        , maps)

        maps = random.sample(list(maps), int(num_map))

        for i,m in enumerate(maps): 
            
            embed = Embed(
            title=m['name'],
            url=m['link'],
            color=self.get_color(m['gameMode']['color']),
            timestamp=datetime.now())
            
            embed.set_image(url=m['imageUrl'])
                
            embed.set_thumbnail(url=m['gameMode']['imageUrl'])
                
            embed.set_footer(text=ctx.author)
             
            await ctx.channel.send('Random Map # {}\n'.format(i+1), embed = embed)
            
            
    @rmap.error
    async def rmap_error(self, ctx, error):
        
        if isinstance(error, MissingRequiredArgument):
            return await ctx.channel.send('Es necesario especificar una cantidad de mapas aleatorios\n```yaml\n.rmap <cantidad de mapas>```')
   
    @map_by_mode.error
    async def rmap_error(self, ctx, error):
        
        if isinstance(error, MissingRequiredArgument):
            return await ctx.channel.send('Es necesario especificar una cantidad de mapas aleatorios y un modo de juego\n```yaml\n.map_by_mode <cantidad de mapas> <modo de juego>```')
  
        
    @command(description='This command is search a brawler randomly')
    async def rbrawl(self, ctx):
            
        brawl = self.get_resource(self.uri + 'brawlers')
            
        brawl = random.sample(list(brawl), 1)[0]
        
        embed = Embed(
        title=brawl['name'],
        url=brawl['link'],
        color=self.get_color(brawl['rarity']['color']),
        timestamp=datetime.now())
        
        embed.set_image(url=brawl['imageUrl'])
        
        embed.set_thumbnail(url=brawl['imageUrl3'])
        
        embed.set_footer(text=ctx.author)
        
        await ctx.channel.send(embed = embed)
   
    @command(description='This command is search a brawler by rarity randomly')
    async def brawl_by_rarity(self, ctx, rarity):
            
            
        brawls = self.get_resource(self.uri + 'brawlers')
        
        brawls_by_rarity = list(filter(lambda b : b['rarity']['name'].lower() == rarity, brawls))

        brawl = random.sample(brawls_by_rarity, 1)[0]      
        
        
        embed = Embed(
        title=brawl['name'],
        url=brawl['link'],
        color=self.get_color(brawl['rarity']['color']),
        timestamp=datetime.now())
        
        embed.set_image(url=brawl['imageUrl'])
        
        embed.set_thumbnail(url=brawl['imageUrl3'])
        
        embed.set_footer(text=ctx.author)
        
        await ctx.channel.send(embed = embed)
        
    @brawl_by_rarity.error
    async def brawl_by_rarity_error(self, ctx, error):
        
        if isinstance(error, MissingRequiredArgument):
            return await ctx.channel.send('Es necesario especificar una rareza del brawler\n```yaml\n.brawl_by_rarity <rareza>```')
  
        
    

    
def setup(bot : Bot):
    bot.add_cog(Random(bot))