import generate as gen

import discord
from discord import Intents
from discord.ext import commands, tasks
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import json
import random
import time
from threading import Timer
import asyncio
intents = Intents.default()
intents.members = True

config = json.load(open('config.json'))

client = commands.Bot(command_prefix = config['prefix'], intents = intents)

botKey = config['bot_key']



bot_id = int(config['bot_id'])



depositChannelID = int(config['deposit_channel'])
withdrawChannelID = int(config['withdraw_channel'])

commandChannelID = int(config['command_channel'])

coinflipChannelID = int(config['coinflip_channel'])
coinflipLogChannelID = int(config['coinflip_log_channel'])


dealerRoleID = int(config['dealer_role_id'])

def easyEmbed(titleText, descriptionText):
	embed = discord.Embed(title = titleText,color = 0xFFD700, description = descriptionText)
	return embed


invites = {}
@client.event
async def on_ready():
    print('Bot is ready.')
    backup.start()

def dataLoad():
    global data
    try:
        data = json.load(open("data.json"))
    except:
        print('data json empty')
        data = {}


def dataUpdate():
    global data
    j = json.dumps(data)
    with open("data.json", "w") as f:
        f.write(j)
        f.close()

dataLoad()
print(data)

@tasks.loop(minutes = 30)
async def backup():
    j = json.dumps(data)
    print('backing Up')
    string = f'backups\\{str(datetime.now())}data.json'
    string = string.replace(':', '')
    with open(string, 'w+') as f:
        f.write(j)
        f.close()



async def createKey(id, level_ = 0, kr_ = 10, gems_ = 0, inventory_ = []):
    global data
    id = str(id)
    if id in data:
        return False
    print(f'adding new id {id}')
    data[id] = {'level':level_, 'kr':kr_, 'gems':gems_, 'ref':False, 'inventory':{}}
    dataUpdate()

@client.event
async def on_member_join(member):
    global data
    await createKey(str(member.id))
    data[str(member.id)]['ref'] = True


@commands.has_permissions(administrator=True)
@client.command()
async def refcheck(ctx, id):
    await ctx.send(data[id]['ref'])


@commands.has_permissions(administrator=True)
@client.command()
async def balancereset(ctx, user, confirm):
    if confirm == 'confirm':
        idPayee = str(ctx.message.mentions[0].id)
        data[idPayee] = {'level':0, 'kr':0, 'gems':0, 'ref':True}


@client.command(aliases = ['b', 'bal'])
async def balance(ctx, id = None):
    if ctx.message.channel.id not in [coinflipChannelID, withdrawChannelID, depositChannelID, commandChannelID]:
        return
    global data
    if id == None: 
        id = str(ctx.message.author.id)
    else:
        id = str(ctx.message.mentions[0].id)

    try:
        embed = easyEmbed('BALANCE', f'<@{id}> has {data[id]["kr"]} KR in their balance')
        embed.add_field(name = 'GEMS', value = f'<@{id}> has {data[id]["gems"]} gems :gem: in their balance')
        embed.add_field(name = 'LEVEL', value = f'<@{id}> is level {data[id]["level"]}')
        await ctx.send(embed = embed)
    except:
        await createKey(id)

@client.command(aliases = ['d', 'dep'])
async def deposit(ctx, amount, ign):
    if ctx.message.channel.id != depositChannelID:
        return
    id = str(ctx.message.author.id)
    try:
        int(amount)
        embed = easyEmbed('DEPOSIT', f'<@{id}> would like to deposit {amount} KR to their balance from https://krunker.io/social.html?p=profile&q={ign}')
        embed.add_field(name = 'INFO', value = f'Somebody with the <@&{dealerRoleID}> Role will assist you shortly, please be patient :). Do not send KR to anyone without the <@&{dealerRoleID}> role')
    except:
        embed = easyEmbed('ERROR', 'Please use the format .depost <amount> <krunker ign>')
    await ctx.send(embed = embed)

@client.command(aliases = ['w', 'with'])
async def withdraw(ctx, amount, ign):
    try:
         int(amount)
    except:
        embed = easyEmbed('ERROR', 'Please use the format .withdraw <amount> <krunker ign>')
        await ctx.send(embed = embed)
        return
    if ctx.message.channel.id != withdrawChannelID:
        return
    id = str(ctx.message.author.id)
    if int(amount) > data[id]['kr']:
        embed = easyEmbed('ERROR', f'You requested to withdraw {amount} KR, but you only have {data[id]["kr"]} in your balance')
    elif int(amount) < 50:
        embed = easyEmbed('ERROR', f'You requested to withdraw {amount} KR, but the minimum amount to withdraw is 50 KR ')
    else:
        gift = round(int(amount)/1.1)
        embed = easyEmbed('WITHDRAW', f'<@{id}> would like to withdraw {amount} KR to their account https://krunker.io/social.html?p=profile&q={ign} from their balance, too account for fees gift them {gift} KR')
        embed.add_field(name = 'INFO', value = f'Somebody with the <@&{dealerRoleID}> Role will assist you shortly, please be patient :). Make sure to double check your account IGN as KR sent to the wrong account will not be refunded.')
    await ctx.send(embed = embed)
@client.command()

async def link(ctx, profile):
    await ctx.send(f'https://krunker.io/social.html?p=profile&q={profile}')

@commands.has_role(dealerRoleID)
@client.command()
async def add(ctx, amount, user, type_ = 'kr'):
    global data
    id = str(ctx.message.mentions[0].id)
    if id in data:
        data[id][type_] += int(amount)
        dataUpdate()
        embed = easyEmbed('BALANCE CHANGE', f'<@{ctx.message.author.id}> added {amount} {type_.upper()} to <@{id}>\'s balance')
        embed.add_field(name = 'BALANCE', value = f'<@{id}> has {data[id]["kr"]} KR in their balance')
        embed.add_field(name = 'GEMS', value = f'<@{id}> has {data[id]["gems"]} gems :gem: in their balance')
        embed.add_field(name = 'LEVEL', value = f'<@{id}> is level {data[id]["level"]}')
    else:
        await createKey(id)
        embed = easyEmbed('NO ACCOUNT', f'<@{id}> didn\'t have an account, an account has been made for them.')
    await ctx.send(embed = embed)
 

@commands.has_permissions(administrator=True)
@client.command()
async def datacmd(ctx, choice):
    global data
    if choice in ['l', 'load']:
        print('loading')
        dataLoad()
    elif choice in ['u', 'update']:
        dataUpdate()
        print('updating')
    print(data)

@commands.has_permissions(administrator=True)
@client.command()
async def stop(ctx):
    await ctx.send('Stopping')
    await client.logout()





coinflips = {}
@client.command(aliases = ['cf', 'c', 'coin'])
async def coinflip(ctx, action = 'list', arg = None):
    global coinflips
    global data
    channel = client.get_channel(coinflipLogChannelID)
    if ctx.message.channel.id != coinflipChannelID:
        return
    id = str(ctx.message.author.id)
    if action in ['l', 'list']:
        embed = easyEmbed('COINFLIP LIST', 'Here is a list of active coinflips, use .cf join <@user> to join or do .cf create <amount> to create your own!')
        for coinflip in coinflips:
            embed.add_field(name = f'{coinflips[coinflip]} KR', value = f'<@{coinflip}> has a bet of **{coinflips[coinflip]} KR** on heads, do .cf j <@{coinflip}> to join')
        await ctx.send(embed = embed)

    elif action in ['c', 'create']:
        try:
            amount = int(arg)
        except:
            embed = easyEmbed('COINFLIP ERROR', 'Please enter integer value for amount. Correct syntax is .coinflip create <amount>')
            await ctx.send(embed = embed)
            return
        if id in coinflips:
            embed = easyEmbed('COINFLIP ERROR', f'<@{id}> already has a bet of {coinflips[id]} KR on heads') 
        elif amount > data[id]['kr']:
            embed = easyEmbed('COINFLIP ERROR', f'Bet of {amount} KR is greater than user balance of {data[id]["kr"]} KR')
        elif amount < 5:
            embed = easyEmbed('COINFLIP ERROR', f'Bet of {amount} KR is less than minimum bet of 5 KR')
        else:
            embed = easyEmbed('COINFLIP CREATE', f'<@{id}> created a bet of {amount} KR on heads, do .coinflip join <@{id}> to join')
            embed.add_field(name = 'INFO', value = f'{amount} KR has been removed from your balance, you will get it back when you win your coinflip or if you do .coinflip cancel')
            data[id]['kr'] -= amount
            coinflips[id] = amount
            dataUpdate()
            channel = client.get_channel(coinflipLogChannelID)
            await channel.send(embed = embed)
        await ctx.send(embed = embed)
    elif action in ['j', 'join']:
        try:
            idJoin = str(ctx.message.mentions[0].id)
        except:
            embed = easyEmbed('COINFLIP ERROR', f'{arg} is an invalid value for user. Correct syntax is .coinflip join <@user>. Do .cf for a list of active coinflips')
            await ctx.send(embed = embed)
            return
        if idJoin == id:
            embed = easyEmbed('COINFLIP ERROR', f'Cant join yourself, lol...')
        elif coinflips[idJoin] > data[id]["kr"]:
            embed = easyEmbed('COINFLIP ERROR', f'bet to meet of {coinflips[idJoin]} KR is greater than user balance of {data[id]["kr"]} KR')
        else:
            data[id]['kr'] -= coinflips[idJoin]
            if await gen.coinflip():
                embed = easyEmbed('COINFLIP', f'The coinflip between <@{id}> and <@{idJoin}> landed on **heads** so <@{idJoin}> won {int(coinflips[idJoin] * 2 * 0.9)} KR')
                data[idJoin]['kr'] += int(coinflips[idJoin] * 2 * 0.9)
                embed.set_image(url = 'https://cutt.ly/krheads')
            else:
                embed = easyEmbed('COINFLIP', f'The coinflip between <@{id}> and <@{idJoin}> landed on **tails** so <@{id}> won {int(coinflips[idJoin] * 2 * 0.9)} KR')
                data[id]['kr'] += int(coinflips[idJoin] * 2 * 0.9)
                embed.set_image(url = 'https://cutt.ly/krtails')
            if coinflips[idJoin] >= 10:
                gems = int(coinflips[idJoin] / 10)
                embed.add_field(name = 'GEMS', value = f'Because of the size of the bet both users have been awarded {gems} :gem: ') 
                data[id]['gems'] += gems
                data [idJoin]['gems'] += gems
            channel = client.get_channel(coinflipLogChannelID)
            await channel.send(embed = embed)
            dataUpdate()
            coinflips.pop(idJoin)
        await ctx.send(embed = embed)
    elif action in ['d', 'delete', 'cancel']:

        if id in coinflips:
            embed = easyEmbed('COINFLIP DELETE', f'<@{id}>\'s coinflip of {coinflips[id]} KR on heads has been deleted. KR has been returned. Do .cf to see the new coinflip list.')
            data[id]['kr'] += coinflips[id]
            coinflips.pop(id)
            await channel.send(embed = embed)
        else:
            embed = easyEmbed('COINFLIP ERROR', f'<@{id}> does not have an active coinflip.')
        await ctx.send(embed = embed)

@client.command(aliases = ['lb'])
async def leaderboard(ctx):
    if ctx.message.channel.id not in [commandChannelID, coinflipChannelID]:
        return
    choice = 'kr'
    sortedData = sorted(data, key=lambda x: (data[x][choice]), reverse=True)
    if choice == 'kr':
        text = 'KR in their balance'

    embed = easyEmbed('LEADERBOARD', f'Highest {choice}')
    n = 0
    for leader in sortedData:
        embed.add_field(name = f'#{n+1}', value = f'<@{leader}> has {data[leader][choice]} {text}')
        n+=1
        if n >9:
            break
    await ctx.send(embed = embed)

client.run(botKey)