import discord
from discord.ext import commands, tasks
from functions import *

prefix = "!"
token = ''

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
current_board = []
ongoing_game = {}
'''

'''


async def print_board(channel, cur_board):
    x = 1
    for _x in cur_board:
        _ = ""
        _ += nums.get(f"number_{x}")
        x += 1
        for square in _x:
            _ += square.icon_id if isinstance(square, ChessPiece) else square
        await channel.send(_)
    await channel.send(''.join(j for j in blank))


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title=f"{bot.user.name}'s ping",
                          description=f'Ping/Latency is {round(bot.latency * 1000)}ms!',
                          color=discord.Color.dark_red())
    await ctx.send(embed=embed)


@bot.command()
async def board(ctx):
    channel = await ctx.guild.create_text_channel(f"{ctx.author.name}s Game")
    ongoing_game[ctx.author.id] = channel
    for i in range(1, 9):
        row = []
        _ = ''
        color = 'black' if i in (1, 2) else 'white' if i in (7, 8) else False
        if color:
            row = boardRows(i, color)
        else:
            first = True if i % 2 == 1 else False
            for x in range(1, 9):
                row.append(white_square if first else black_square)
                first = not first
        current_board.append(row)
    await print_board(channel, current_board)
    await ctx.send(f"Proceed to {channel.mention} for your game!")


@bot.command()
async def play(ctx, to_move, where):
    channel = ongoing_game[ctx.author.id]
    if current_board:
        col = letters_dict[to_move[0]] - 1
        row = 8 - int(to_move[1])
        chosen_col = letters_dict[where[0]] - 1
        chosen_row = 8 - int(where[1])
        chosen_piece = current_board[row][col]
        chosen_square = current_board[chosen_row][chosen_col]

        if not legal_move(chosen_piece, current_board, (row, col, to_move), (chosen_row, chosen_col, where)):
            await channel.send("Illegal Move!")
        else:
            current_board[chosen_row][chosen_col] = chosen_piece
            current_board[row][col] = white_square if ((row % 2 == 1 and col % 2 == 1) or
                                                       (row % 2 == 0 and col % 2 == 0)) else black_square
            await channel.purge()
            await print_board(channel, current_board)
    else:
        await channel.send("Board not yet generated!!")


@bot.command()
async def check(ctx, square):
    row = 8 - int(square[1])
    col = letters_dict[square[0]] - 1
    await ctx.send(current_board[row][col].color if isinstance(current_board[row][col], ChessPiece)
                   else current_board[row][col])


@bot.command()
async def remove(ctx, square):
    channel = ongoing_game[ctx.author.id]
    col = letters_dict[square[0]] - 1
    row = 8 - int(square[1])
    current_board[row][col] = white_square if ((row % 2 == 1 and col % 2 == 1) or
                                               (row % 2 == 0 and col % 2 == 0)) else black_square
    await channel.purge()
    await print_board(channel, current_board)


@bot.command()
async def mot(ctx, s):
    await ctx.send(current_board[int(s[1]) - 1][letters_dict[s[0]] - 1].position)


@bot.command()
async def end(ctx):
    channel = ongoing_game[ctx.author.id]
    await channel.delete()


bot.run(token)

'''
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜

a8 b8 c8 d8 e8 f8 g8 h8
a7 b7 c7 d7 e7 f7 g7 h7
a6 b6 c6 d6 e6 f6 g6 h6
a5 b5 c5 d5 e5 f5 g5 h5
a4 b4 c4 d4 e4 f4 g4 h4
a3 b3 c3 d3 e3 f3 g3 h3
a2 b2 c2 d2 e2 f2 g2 h2
a1 b1 c1 d1 e1 f1 g1 h1

a8 - h8 is (0, 0) - (0, 7)
a1 - h1 is (7, 0) - (7, 7)

'''
