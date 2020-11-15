"""
Author: Konnor Klercke
File: framelessbot.py
Purpose: Discord bot for 2020 Frameless XR Symposium
"""

#####################################
                                    #
import os                           #
import discord                      #
from dotenv import load_dotenv      #
from discord.ext import commands    #
import logging                      #
import asyncio                      #
import string                       #
import time                         #
                                    #
#####################################


#################################################
                                                #
COMMAND_PREFIX = '-'                            #
VERSION = "v1.0.0"                              #
ACTIVITY = discord.Game("Frameless Symposium")  #
LOG_LEVEL = logging.INFO                        #
                                                #
#################################################


# Initialize bot object to use the COMMAND_PREFIX defined above
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_connect():
    """
    Prints a message with bot name and version when bot connects to Discord servers.
    Sets the bot activity to ACTIVITY.
    """

    logging.warning(f'{bot.user.name} {VERSION} has successfully connected to Discord.')
    await bot.change_presence(activity = ACTIVITY)


@bot.event 
async def on_ready():
    """
    Prints a list of guilds the bot is connected to when the bot is finished processing
    date from Discord servers. Also calls the initializing functions in activity.py.
    """

    logging.info('Bot loading complete. Current guilds: ')
    
    for guild in bot.guilds:
        label = guild.name + " (" + str(guild.id) + ")"
        logging.info(label)


@bot.event
async def on_disconnect():
    """
    Prints a message when bot disconnects from Discord. Usually this is temporary.
    """

    logging.warning('Lost connection to Discord.')


@bot.event
async def on_guild_join(guild):
    """
    Logs a message when bot joins a new guild and adds all users from that guild to the database.
    """

    logging.warning(f"Joined new guild: {guild.name + ' (' + str(guild.id) + ')'}")


@bot.event
async def on_error(event, *args, **kwargs):
    """
    Writes to err.log whenever a message triggers an error
    """

    if event == 'on_message':
        logging.error(f'Unhandled message: {args[0]}')
    else:
        logging.exception(event)


@bot.event
async def on_raw_reaction_add(payload):
    """
    Allows the bot to respond to user reactions
    """
    guild = discord.utils.get(bot.guilds, id = payload.guild_id)
    channel = discord.utils.get(guild.text_channels, id = payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = payload.member
    emoji = payload.emoji
    role = guild.get_role(775491115403051058)

    if (message.id == 775497910006579210):
        if (emoji.name == "🟧"):
            await member.add_roles(role)
    

@bot.event
async def on_message(message):
    """
    Allows the bot to respond to user messages rather than commands
    """

    if message.author.bot:
        """
        Tells the bot to ignore its own messages
        """

        return

    if 'happy birthday' in message.content.lower():
        """
        Lets the bot say happy birthday whenever a user says it
        """

        mentions = message.mentions
        author = message.author.name + "(" + str(message.author.id) + ")"
        logging.info(f"{author} wished happy birthday to {len(mentions)} user(s).")
        for recipient in mentions:
            await message.channel.send(f"Happy Birthday <@{recipient.id}>! 🎈🎉🎂")
    
    await bot.process_commands(message)


def main():
    # Load bot token from .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Generate timestamp of startup
    timestamp = time.strftime('%Y%m%d-%H%M%S')

    # Configure logging
    logging.basicConfig(
        level = LOG_LEVEL, 
        format = '%(asctime)s: [%(levelname)s] - %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S', 
        handlers = [
            logging.FileHandler('logs/{timestamp}.log', 'w', 'utf-8'), 
            logging.StreamHandler()
        ]
    )

    bot.run(TOKEN)

if __name__ == "__main__":
    main()
