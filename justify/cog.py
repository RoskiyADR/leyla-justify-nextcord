import time
from typing import Union
import sys

import nextcord
from .services.utils import JustifyUtils
from nextcord.ext import commands


class JustifyCog(commands.Cog):
    """Loads justify cog."""
    def  __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]) -> None:
        self.bot = bot
        self.justify = JustifyUtils(bot)
    
    @commands.is_owner()
    @commands.group(name='justify', aliases=['jst'], invoke_without_command=True)
    async def justify_main_command(self, ctx: commands.Context):
        text = [
            f'`{self.justify.__version__}, nextcord-{nextcord.__version__}, {sys.version}.`\n',
            f'Серверов: **{len(self.bot.guilds)}**, users: **{len(self.bot.users)}**',
            f'Кэша: **{len(self.bot.cached_messages)}**',
            f'```py\nВключённые интенты: {", ".join([i[0] for i in self.bot.intents if i[-1]])}```'
        ]

        if isinstance(self.bot, commands.AutoShardedBot):
            text.append(f'Шардов:\n' + '```py\n' + '\n'.join(list(f"{i[0]} - {i[-1]*1000}" for i in self.bot.latencies)) + '```')

        await ctx.reply('\n'.join(text))

    @justify_main_command.command(name='eval', aliases=['py'])
    @commands.is_owner()
    async def justify_eval(self, ctx: commands.Context, *, text: str):
        code = text.strip("\n").strip("```").lstrip("\n").lstrip("py") if text.startswith("```py") else text # Колбаска ^-^

        try:
            result = str(await self.justify.eval_code(ctx, code))

        except Exception as exception:
            result = f"# Произошла ошибка при выполнении кода: \n```py\n{exception.__class__}: {exception}```" 
        
        finally:
            await self.justify.python_handler_result(ctx, result)

    @justify_main_command.command(name='debug', aliases=['dbg'])
    @commands.is_owner()
    async def justify_debug(self, ctx: commands.Context, *, cmd: str):
        command = self.bot.get_command(cmd)

        if command is None:
            return await ctx.reply('Команда не найдена...')
        

        start = time.perf_counter()

        await ctx.invoke(command)

        end = time.perf_counter()
        await ctx.reply(f"Команда `{command}` была исполнена за `{end - start:.3f}` секунд")

def setup(bot):
    bot.add_cog(JustifyCog(bot=bot))
