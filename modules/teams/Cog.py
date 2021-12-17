import random

from nextcord.ext.commands import Bot, Cog, command

from nextcord.embeds import Embed

from nextcord.ext.commands.errors import MissingRequiredArgument 


class Teams(Cog):
    
    def __init__(self, bot: Bot) -> None:
        
        self.bot = bot
        
        self.match_conditions = {
            '0' : 'L',
            '1' : 'V'
        }
        
    @staticmethod  
    def set_teams(members, length):
                
        try:
            
            list_teams = []
            
            total_teams = int(len(members)/length)
        
        
            for _ in range(total_teams):
                
                team = random.sample(members, length)
            
                list_teams.append(team)
                
                members = list( set(members) - set(team) )
                
            return list_teams
                   
        except Exception as e:
            print(e)
            return 
        
    @command(description='This command is for create teams randomly')   
    async def teams(self, ctx, channel_name, length):
        
        try:
            
            channel = next(filter((lambda c : c if c.name == channel_name else None), ctx.guild.channels)) or None
                
            members = [m.name for m in channel.members]
        
            list_teams = self.set_teams(members ,int(length))
            
            if not list_teams: return await ctx.channel.send('No se puede formar equipos por falta de participantes') 

            for index, team in enumerate(list_teams):
                
              
                await ctx.channel.send(embed = Embed(
                    title=f'Group {index+1}',
                    description=''.join(
                        [f'{self.match_conditions[str(index_name)]}: {name}\n'
                         if len(team) == 2 else f'{name}\n' 
                         for index_name, name in enumerate(team)])
                ))    
        
        except:
            await ctx.channel.send('El canal de voz especificado no existe')

    @teams.error
    async def teams_error(self, ctx, error):
        
        if isinstance(error, MissingRequiredArgument):
            
            return await ctx.channel.send('Es necesario especificar como argumento un canal de voz activo\n```yaml\n.teams <canal de voz> <equipos>```')
        
        
        
def setup(bot : Bot):
    bot.add_cog(Teams(bot))
    
    
    

