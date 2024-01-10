import discord
from discord.ext import commands, tasks
from functions import *
from errors import *
import os
from dotenv import load_dotenv

# Load the dotenv file
load_dotenv()

prefix = "!"

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
ongoing_game = {}
roles_id = []


async def print_board(channel, cur_board, moves):
    if moves % 2 == 0:
        x = 8
        for _x in cur_board:
            _ = ""
            _ += nums.get(f"number_{x}")
            x -= 1
            for square in _x:
                _ += square.icon_id if isinstance(square, ChessPiece) else square
            await channel.send(_)
    else:
        x = 1
        for _x in reversed(cur_board):
            _ = ""
            _ += nums.get(f"number_{x}")
            x += 1
            for square in _x:
                _ += square.icon_id if isinstance(square, ChessPiece) else square
            await channel.send(_)
    await channel.send(''.join(j for j in blank))
    await channel.send("Use !move <from> <to>")


async def get_info(ctx):
    for i in roles_id:
        role: discord.Role = discord.utils.get(ctx.guild.roles, id=i)
        if role in ctx.author.roles:
            return i


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title=f"{bot.user.name}'s ping",
                          description=f'Ping/Latency is {round(bot.latency * 1000)}ms!',
                          color=discord.Color.dark_red())
    await ctx.send(embed=embed)


@bot.command()
async def chess(ctx, player2: discord.Member, private: bool = False, player_color: str = 'White'):
    current_board = []
    for i in range(1, 9):
        row = []
        _ = ''
        color = 'white' if i in (1, 2) else 'black' if i in (7, 8) else False
        if color:
            row = boardRows(i, color)
        else:
            first = True if i % 2 == 1 else False
            for x in range(1, 9):
                row.append(white_square if first else black_square)
                first = not first
        current_board.append(row)

    role: discord.Role = await ctx.guild.create_role(name=f"Chess: {ctx.author.name} vs {player2.name}")
    channel: discord.TextChannel = await ctx.guild.create_text_channel(f"chess {ctx.author.name} vs {player2.name}")
    if private:
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await channel.set_permissions(role, view_channel=True)
    await player2.add_roles(role)
    await ctx.author.add_roles(role)
    ongoing_game[role.id] = {
        ctx.author.id: player_color,
        player2.id: 'Black' if player_color == 'White' else 'White',
        'moves': 0,
        'channel': channel.id,
        'board': current_board,
        'private': private,
        'status': 'ongoing'
    }
    roles_id.append(role.id)

    await print_board(channel, current_board, 0)
    await ctx.send(f"Proceed to {channel.mention} for your game!")


@bot.command()
async def move(ctx, to_move, where):
    x = await get_info(ctx)
    channel, current_board = bot.get_channel(ongoing_game[x]['channel']), ongoing_game[x]['board']
    turn = 'White' if ongoing_game[x]['moves'] % 2 == 0 else 'Black'
    if ctx.author.id not in ongoing_game[x]:
        await channel.send("You are not a player of this game!")
        return

    elif ongoing_game[x][ctx.author.id] != turn:
        await channel.send("It is not your turn yet!")

    elif current_board and ongoing_game[x][ctx.author.id] == turn:
        col = letters_dict[to_move[0]] - 1
        row = 8 - int(to_move[1])
        chosen_col = letters_dict[where[0]] - 1
        chosen_row = 8 - int(where[1])
        chosen_piece = current_board[row][col]
        if to_move == where:
            await same_move(channel, to_move, where)

        elif not legal_move(chosen_piece, current_board, (row, col, to_move), (chosen_row, chosen_col, where)):
            await channel.send("Illegal Move!")
        else:
            ongoing_game[x]['moves'] += 1
            current_board[chosen_row][chosen_col] = chosen_piece
            current_board[row][col] = white_square if ((row % 2 == 1 and col % 2 == 1) or
                                                       (row % 2 == 0 and col % 2 == 0)) else black_square
            await print_board(channel, current_board, ongoing_game[x]['moves'])
    else:
        await channel.send("Board not yet generated!!")


@bot.command()
async def remove(ctx, square):
    x = await get_info(ctx)
    channel, current_board = bot.get_channel(ongoing_game[x]['channel']), ongoing_game[x]['board']
    col = letters_dict[square[0]] - 1
    row = 8 - int(square[1])
    current_board[row][col] = white_square if ((row % 2 == 1 and col % 2 == 1) or
                                               (row % 2 == 0 and col % 2 == 0)) else black_square
    await print_board(channel, current_board, 0)


@bot.command()
async def finish(ctx):
    _ = await get_info(ctx)
    channel = bot.get_channel(ongoing_game[_]['channel'])
    role: discord.Role = discord.utils.get(ctx.guild.roles, id=_)
    ongoing_game.pop(_)

    await role.delete()
    await channel.delete()


@bot.command()
async def test(ctx):
    x = await get_info(ctx)
    current_board = ongoing_game[x]['board']
    print(current_board[0][0])

    await ctx.send("XXX")

bot.run(os.getenv('TOKEN'))
