import discord
import functions
import json
import os.path
import random
import pickle
from discord.ext import commands,tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

#Insert token and guild_id prior to building the app
token = ''
guild_id = 0
client = commands.Bot(command_prefix = "!")
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("Bot is ready")

@tasks.loop(seconds=100)
async def consistentcheck_onprices():

    #Get the data
    openPickle = open("save.pickle","rb")
    saveList = pickle.load(openPickle)
    
    for enum,i in len(saveList):
        
        coinToCheck = i["coin"]
        member = i["name"]

        #Get the current price
        priceGet = functions.checkBitrue(coinToCheck+"USDT")
        price = round(float(json.loads(priceGet)["price"]),2)

        #Check if goal is met
        if i["priceIndicator"] >= price:
            print("Goal is met")

            #Inform user if goal is met
            if member is not None:
                channel = member.dm_channel
                if channel is None:
                    channel = await member.create_dm()
                
                await channel.send("Your goal of {} for {} has been reached!".format(str(price), coinToCheck))


            #Delist goal if reached
            del saveList[enum]

            #Repickle the list
            pickleSave = open("save.pik", "wb")
            pickle.dump(saveList, pickleSave)
            pickleSave.close()


@client.event
async def on_member_join(member):
    print(f'Hello unnamed creature, I mean {member}. Welcome to the cave! ')

@client.event
async def on_member_remove(member):
    print(f'{member} has checked out.')

@client.command()
async def pog(ctx):
    await ctx.send('No u')

@client.command()
async def pingme(ctx):
    await ctx.send(ctx.author.mention + " , No horny")

@slash.slash(
    name="hello",
    description="Send a random owo or uwu",
    guild_ids=[guild_id]
)
async def _hello(ctx):
    num = random.randint(1,3)
    if num == 1:
        await ctx.send("Uh, hi there")
    elif num == 2:
        await ctx.send("Welcome to the server!")
    elif num == 3:
        await ctx.send("*cricket noises*")
    else:
        await ctx.send("Invalid Input")

@slash.slash(
    name = "checkprice",
    description = "Gets the price of crypto in USD/USDT", 
    guild_ids=[guild_id],
    options = [
        {
            "name": "coin",
            "description": "choice of coin to check (Ex.: XRP)",
            "required": True,
            "type": 3
        }
    ]
)
async def priceChecker(ctx, coin):
    try:
        priceGet = functions.checkBitrue(coin+"USDT")
        price = round(float(json.loads(priceGet)["price"]),2)
        await ctx.send(f'The price of 1 {coin} is {price} USD')

    except:
        await ctx.send("Price not found, does this coin exist?")

@slash.slash(
    name = "remindprice",
    description = "Reminds user when the price reaches a limit",
    guild_ids = [guild_id],
    options = [
        create_option(
            name= "coin",
            description= "choice of coin to check (Ex.: XRP)",
            required= True,
            option_type = 3
        )
    ]
)
async def remind_price(ctx,coin):

    embed = discord.Embed(
        title="Please set the price goal you want to be reminded of. ",
        description = "||Timeout in 30 seconds||"
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await client.wait_for("message", check=lambda user: user.author == ctx.author and user.channel == ctx.channel, timeout=30)
        priceDeterminor = float(msg.content)
        try:
            await sent.delete()

            #Proceed to save
            saveFileStatus = functions.pickleToFile({
                "name" : ctx.author,
                "coin" : coin,
                "priceIndicator": str(priceDeterminor)
            })

            await ctx.send("Reminder sucessfully saved.")

        except:
            await ctx.send("Input invalid, please try again. ")

    except:
        
        await ctx.send("Request has been cancelled")

    

client.run(token)
