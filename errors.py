from discord import Embed, Color


async def same_move(channel, pos1, pos2):
    msg = Embed(title="Same Move", description=f"Move is invalid because {pos1} is the same with {pos2}.",
                color=Color.dark_red())
    await channel.send(msg)
