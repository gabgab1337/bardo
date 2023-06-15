import os
import pickle
import copy
import random
import operator
import re
import hikari
import lightbulb
from required import TOKEN

bot = lightbulb.BotApp(
    token = TOKEN,
    #default_enabled_guilds =
    )


#bot.load_extensions_from("./bot/extensions")

### PICKLE LOADS ###
mainDir = os.path.dirname(__file__)
spellsDict = {}
with open(os.path.join(mainDir, 'spells/spellsDict.pkl'), 'rb') as file:
    spellsDict = pickle.load(file)
spellsList = {}
with open(os.path.join(mainDir, 'spells/spellsList.pkl'), 'rb') as file:
    spellsList = pickle.load(file)
### hit dice ###
classDie = {'artificer':8
           ,'barbarian':12
           ,'bard':8
           ,'cleric':8
           ,'druid':8
           ,'fighter':10
           ,'monk':8
           ,'paladin':10
           ,'ranger':10
           ,'rogue':8
           ,'sorcerer':6
           ,'warlock':8
           ,'wizard':6
           ,'bloodhunter':10}
### class names ###
className = {'artificer':'Artificer'
             ,'barbarian':'Barbarian'
             ,'bard':'Bard'
             ,'cleric':'Cleric'
             ,'druid':'Druid'
             ,'fighter':'Fighter'
             ,'monk':'Monk'
             ,'paladin':'Paladin'
             ,'ranger':'Ranger'
             ,'rogue':'Rogue'
             ,'sorcerer':'Sorcerer'
             ,'warlock':'Warlock'
             ,'wizard':'Wizard'
             ,'bloodhunter':'Blood Hunter'}

#############
### ROLLS ###
#############
@bot.command
@lightbulb.option('dice', 'ex: "3d20 + 3"', type = str)
@lightbulb.command('roll', 'Roll a dice!')
@lightbulb.implements(lightbulb.SlashCommand)
async def roll(ctx):
    
    ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv}

    user = ctx.author
    userInput = ctx.options.dice.upper().replace(" ", "")
    slicedInput = userInput.split('D')
    
    if slicedInput[0] == '':
            slicedInput[0] = '1'

    if (not slicedInput[0].isdigit()) or len(slicedInput) != 2:
        await ctx.respond('Error: Wrong amount of dice, or missing \'d\'')
        return

    count = int(slicedInput[0])
    dice = 0
    total = 0
    oper = ''

    if not slicedInput[1].isdigit():
        for i in slicedInput[1]:
            if i in ops:
                oper = i
                break

        if oper != '':
            slicedInput = slicedInput[1].split(oper)
        dice = int(slicedInput[0])

    else:
        dice = int(slicedInput[1]) 

    if (not slicedInput[0].isdigit()) or (not slicedInput[1].isdigit()) or len(slicedInput) != 2:
        await ctx.respond('Error: Wrong die or modifier')
        return

    if count > 100 or dice > 1000000 or int(slicedInput[1]) > 1000000:
        await ctx.respond('Error: Try smaller numbers')
        return

    throws = [random.randrange(dice) + 1 for i in range(count)]

    if oper != '':
        total = ops[oper](sum(throws), int(slicedInput[1]))
    else:
        total = sum(throws)
    
    ###NAT 1 or NAT 20###
    if len(throws) == 1 and dice == 20 and (throws[0] == 20 or throws[0] == 1):
        ###NAT 20###
        if throws[0] == 20:
            await ctx.respond(f'`{user}` rolls `{userInput}`. Roll result: `{throws}` Total: `{total}` :partying_face: ***A NATURAL 20*** :partying_face:')
        ###NAT 1###
        else:
            await ctx.respond(f'`{user}` rolls `{userInput}`. Roll results: `{throws}` Total: `{total}` :skull: ***A NATURAL 1*** :skull:')
    ###REGULAR RESPONSE###
    else:
        await ctx.respond(f'`{user}` rolls `{userInput}`. Roll result: `{throws}`. Total: `{total}`')


@bot.command
@lightbulb.option('dice', 'ex: "3d20 + 3" or "stats" for stat rolls', type = str)
@lightbulb.command('r', 'Roll a dice!')
@lightbulb.implements(lightbulb.SlashCommand)
async def r(ctx):
    
    ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv}

    user = ctx.author
    userInput = ctx.options.dice.upper().replace(" ", "")
    slicedInput = userInput.split('D')
    
    if slicedInput[0] == '':
            slicedInput[0] = '1'

    if (not slicedInput[0].isdigit()) or len(slicedInput) != 2:
        await ctx.respond('Error: Wrong amount of dice, or missing \'d\'')
        return

    count = int(slicedInput[0])
    dice = 0
    total = 0
    oper = ''

    if not slicedInput[1].isdigit():
        for i in slicedInput[1]:
            if i in ops:
                oper = i
                break

        if oper != '':
            slicedInput = slicedInput[1].split(oper)
        dice = int(slicedInput[0])

    else:
        dice = int(slicedInput[1]) 

    if (not slicedInput[0].isdigit()) or (not slicedInput[1].isdigit()) or len(slicedInput) != 2:
        await ctx.respond('Error: Wrong die or modifier')
        return

    if count > 100 or dice > 1000000 or int(slicedInput[1]) > 1000000:
        await ctx.respond('Error: Try smaller numbers')
        return

    throws = [random.randrange(dice) + 1 for i in range(count)]

    if oper != '':
        total = ops[oper](sum(throws), int(slicedInput[1]))
    else:
        total = sum(throws)
    
    ###NAT 1 or NAT 20###
    if len(throws) == 1 and dice == 20 and (throws[0] == 20 or throws[0] == 1):
        ###NAT 20###
        if throws[0] == 20:
            await ctx.respond(f'`{user}` rolls `{userInput}`. Roll result: `{throws}` Total: `{total}` :partying_face: ***A NATURAL 20*** :partying_face:')
        ###NAT 1###
        else:
            await ctx.respond(f'`{user}` rolls `{userInput}`. Roll results: `{throws}` Total: `{total}` :skull: ***A NATURAL 1*** :skull:')
    ###REGULAR RESPONSE###
    else:
        await ctx.respond(f'`{user}` rolls `{userInput}`. Roll result: `{throws}`. Total: `{total}`')

##############
### SPELLS ###
##############
@bot.command
@lightbulb.option('name', 'Spell name (it is not case sensetive)', type = str)
@lightbulb.command('spell', '(BETA) Find a spell and its info')
@lightbulb.implements(lightbulb.SlashCommand)
async def spell(ctx):
    input = ctx.options.name
    inputAdjusted = input.lower().replace(' ', '')
    spellsData = ''

    if inputAdjusted not in spellsDict:
        if len(inputAdjusted) > 3:
            similar = []
            for i in spellsDict:
                if re.search("^"+inputAdjusted, i):
                    similar.append(spellsList[i])
            if len(similar) != 0:
                await ctx.respond(f'Error: **No such spell as** `{input}` \nDid you mean any of these? \n`{similar}`')
                return
        await ctx.respond(f'Error: **No such spell as** `{input}`')
        return

    with open(os.path.join(mainDir, 'spells/spellsFormated.txt'), 'r', encoding='UTF-8') as file:
        spellsData = file.read().split('$$$')
    spellsData.pop(0)
    spellsData = spellsData[spellsDict[inputAdjusted]]
        
    await ctx.respond(spellsData)

##############
### STATS ###
##############
@bot.command
@lightbulb.command('stats', 'Roll for stats!')
@lightbulb.implements(lightbulb.SlashCommand)
async def stats(ctx):
    user = ctx.author

    throws = [[random.randrange(6) + 1 for _ in range(4)] for _ in range(6)]

    throwsRemoved = copy.deepcopy(throws)
    
    for i in range(6):
        throwsRemoved[i].remove(min(throwsRemoved[i]))
    
    await ctx.respond(f'`{user}` rolls for stats!  :sparkles:\nResult:\n1. `{throws[0]}` Total: **{sum(throwsRemoved[0])}**\n2. `{throws[1]}` Total: **{sum(throwsRemoved[1])}**\n3. `{throws[2]}` Total: **{sum(throwsRemoved[2])}**\n4. `{throws[3]}` Total: **{sum(throwsRemoved[3])}**\n5. `{throws[4]}` Total: **{sum(throwsRemoved[4])}**\n6. `{throws[5]}` Total: **{sum(throwsRemoved[5])}**')

##############
##### HP #####
##############
@bot.command
@lightbulb.option('classname', 'Class (it is not case sensetive)', type = str)
@lightbulb.command('hp', 'Roll for hit points!')
@lightbulb.implements(lightbulb.SlashCommand)
async def hp(ctx):
    userInput = ctx.options.classname
    user = ctx.author
    userInputStripped = userInput.lower().replace(' ', '')

    if (userInputStripped not in className) and (userInputStripped != 'help'):
        similar = []
        for i in className:
            if re.search('^'+userInputStripped, i):
                similar.append(className[i])
        if similar:
            await ctx.respond(f'Error: Class not found. Did you mean any of these?\n `{similar}`')
            return
        await ctx.respond(f'Error: Class not found. Aviable classes: `{", ".join(className.values())}`\nType `/hp help` for more info on hit dice.')
        return

    if userInputStripped == "help":
        await ctx.respond(f'*Hit Dice determines amount of Hit Points you can gain with every level, and recover with every short rest :sleeping:. *\n**d6** - `[\'Sorcerer\', \'Wizard\']`\n**d8** - `[\'Artificer\', \'Bard\', \'Cleric\', \'Druid\', \'Monk\', \'Rogue\', \'Warlock\']`\n**d10** - `[\'Fighter\', \'Paladin\', \'Ranger\', \'Blood Hunter\']`\n**d12** - `[\'Barbarian\']`')
        return
    dice = classDie[userInputStripped]

    await ctx.respond(f'`{user}`rolls for :sparkling_heart:  as **{className[userInputStripped]}** (d{dice}). Result: **{random.randrange(dice) + 1}**')

bot.run()