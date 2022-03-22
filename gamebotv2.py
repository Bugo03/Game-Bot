import discord
from discord.ext import commands
import random
import pickle
from datetime import datetime
import threading

bot = commands.Bot(command_prefix = '!')

#General variables
players = ['Carter Haws', 'Serpent']
playermoney = [250, 250]
nameinlist = False

#Slot machine variables
sm_run = False
sm_currentplayer = ''
sm_currentmoney = ''
sm_1 = ''
sm_2 = ''
sm_3 = ''
sm_1options = [':skull:', ':poop:', ':money_mouth:', ':cherries:', ':smiling_face_with_3_hearts:', ':partying_face:', ':rage:', ':exploding_head:', ':face_vomiting:', ':monkey_face:', ':dog:', ':cat:', ':bear:', ':tangerine:', ':pear:', ':apple:', ':lemon:', ':peach:', ':mango:', ':star2:']
sm_2options = [':skull:', ':poop:', ':money_mouth:', ':cherries:', ':smiling_face_with_3_hearts:', ':partying_face:', ':rage:', ':exploding_head:', ':face_vomiting:', ':monkey_face:', ':dog:', ':cat:', ':bear:', ':tangerine:', ':pear:', ':apple:', ':lemon:', ':peach:', ':mango:', ':star2:']
sm_3options = [':skull:', ':poop:', ':money_mouth:', ':cherries:', ':smiling_face_with_3_hearts:', ':partying_face:', ':rage:', ':exploding_head:', ':face_vomiting:', ':monkey_face:', ':dog:', ':cat:', ':bear:', ':tangerine:', ':pear:', ':apple:', ':lemon:', ':peach:', ':mango:', ':star2:']
sm_commentaries = ['Here we go!', 'Let\'s go!', 'Hope you\'re feeling lucky today!', 'Chkskskcksk...', 'Let\'s make some money!']
sm_lose = ['Uh oh...', 'Oh no...', 'Bad luck...', 'Sorry...', 'That\'s too bad...', 'Whoops']
sm_win = ['Woo-hoo!', 'Yeah!', 'Great luck!', 'Yes!', 'You win!', 'Wow!', 'Yay!']

#Guess the number variables
gn_playerguesses = [0, 5]
gn_run = False
gn_currentplayer = ''
gn_currentguesses = 0
gn_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
gn_todaysnumber = random.choice(gn_possibilities)

#Song writer variables
sw_notelist = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
sw_song = []
sw_notecounter = 1
sw_shuffle = True

#Madlibs variables
ml_players = []
ml_currentplayer = ''
ml_run = False
ml_readyfornextmessage = False
ml_wordsetsrand = ['brainstorm', 'spooky stuff']
ml_brainstormwords = ['**body organ**', '**adjective**', '**verb**', '**plural noun**', '**plural noun**', '**plural noun**', '**adjective**', '**adjective**', '**plural noun**', '**container**', '**adjective**', '**noun**', '**adjective**', '**adjective**', '**number**', '**adjective**', '**adverb** (verb ending in -ly)', '**noun**', '**verb**', '**adjective**', '**event**', '**verb**', '**adjective**', '**exclamation**']
ml_spookystuffwords = ['**adjective**', '**plural noun**', '**plural noun**', '**silly word**', '**type of liquid**', '**adjective**', '**noun**', '**verb**', '**plural noun**', '**verb ending in \'ing\'**', '**number**', '**verb ending in \'ing\'**', '**plural noun**', '**noun**']

ml_currentstory = ''
ml_words = []
ml_onword = 0
ml_givenwords = []

#Maintenance
@bot.event
async def on_ready(): 
    global playermoney
    global players
    global gn_playerguesses

    print('Bot is ready')

    #Slots data loader
    sm_moneydata = open('moneydata.dat', 'rb')
    playermoney = pickle.load(sm_moneydata)
    sm_moneydata.close()
    sm_playerdata = open('playerdata.dat', 'rb')
    players = pickle.load(sm_playerdata)
    sm_playerdata.close()

    #Guess the number data loader
    gn_guessdata = open('guessdata.dat', 'rb')
    gn_playerguesses = pickle.load(gn_guessdata)
    gn_guessdata.close()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#Slots give money
@bot.command()
async def givemoney(ctx, password, player, amount):
    global sm_currentmoney
    global sm_currentplayer
    global players
    global playermoney
    await ctx.message.delete()
    if password == 'slotcash':
        for x in players:
            if x == player:
                playermoney[players.index(x)] += int(amount)
                await ctx.send('Gave $' + str(amount) + ' to ' + str(player))
                return
    else:
        await ctx.send("WRONG PASSWORD")


#Stop game
@bot.command()
async def stop(ctx, game):
    global sm_run
    if game == 'slots':
        if sm_run:
            global sm_currentmoney
            global sm_currentplayer
            global players
            global playermoney
            for x in players:
                if x == sm_currentplayer:
                    playermoney[players.index(x)] = sm_currentmoney
                    sm_currentmoney = ''
                    sm_currentplayer = ''
                    await ctx.send('Slots game ended.')
                    sm_moneydatahandler = open('moneydata.dat', 'wb')
                    pickle.dump(playermoney, sm_moneydatahandler)
                    sm_moneydatahandler.close()
                    sm_playerdatahandler = open('playerdata.dat', 'wb')
                    pickle.dump(players, sm_playerdatahandler)
                    sm_playerdatahandler.close()
                    gn_guessdatahandler = open('guessdata.dat', 'wb')
                    pickle.dump(gn_playerguesses, gn_guessdatahandler)
                    gn_guessdatahandler.close()
                    sm_run = False
                    return
        else:
            await ctx.send('You can\'t stop a game if it never started in the first place.')
    else:
        await ctx.send('Please choose an existing game.')

#Slot machine placeholder command
@bot.command()
async def slots(ctx):
    return

#Slot machine crank
@bot.command()
async def crank(ctx):
    global sm_currentmoney
    global sm_run
    global sm_1
    global sm_2
    global sm_3
    if sm_run:
        if sm_currentmoney > 0:
            sm_1 = random.choice(sm_1options)
            sm_2 = random.choice(sm_2options)
            sm_3 = random.choice(sm_3options)
            await ctx.send(random.choice(sm_commentaries))
            await ctx.send(sm_1 + '  ' + sm_2 + '  ' + sm_3)
            if sm_1 == sm_2 and sm_2 == sm_3:
                if sm_1 == ':star2:':
                    sm_currentmoney += 1000
                    await ctx.send('JACKPOT!\n+$1000\nYour total is now $' + str(sm_currentmoney))
                else:
                    sm_currentmoney += 300
                    await ctx.send(random.choice(sm_win) + '\n+$300\nYour total is now $' + str(sm_currentmoney))
            else:
                sm_currentmoney -= 5
                await ctx.send(random.choice(sm_lose) + '\n-$5\nYour total is now $' + str(sm_currentmoney))
        else:
            await ctx.send("You do not have enough money to crank the slot machine again.")
    else:
        await ctx.send("Start a slot machine game to use this command.")

#Guess the number timer
def checkTime():
    global gn_todaysnumber
    global gn_playerguesses
    threading.Timer(1, checkTime).start()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if(current_time == '23:59:59'):
        for x in gn_playerguesses:
            gn_playerguesses[gn_playerguesses.index(x)] = 5
        gn_todaysnumber = random.choice(gn_possibilities)
        gn_guessdatahandler = open('guessdata.dat', 'wb')
        pickle.dump(gn_playerguesses, gn_guessdatahandler)
        gn_guessdatahandler.close()
checkTime()

#Guess the number placeholder command
@bot.command()
async def guess(ctx):
    pass


#Song writer command
@bot.command()
async def songwrite(ctx, notes : int):
    global sw_notelist
    global sw_song
    global sw_notecounter
    global sw_shuffle
    if sw_shuffle == True and notes < 51:
        sw_notecounter = 1
        while sw_notecounter <= notes:
            sw_song.append(random.choice(sw_notelist))
            sw_notecounter += 1
        await ctx.send(sw_song)
        sw_shuffle = False
    elif sw_shuffle == True and notes > 50:
        await ctx.send("Maximum number of notes is 50.")
    else:
        await ctx.send("Finish this song with *!songfinish* before starting a new one.")

#Song writer shuffle
@bot.command()
async def songshuffle(ctx, shufflednote : int):
    global sw_song
    global sw_notelist
    if sw_shuffle == False and shufflednote <= len(sw_song):
        sw_song.pop(shufflednote - 1)
        sw_song.insert(shufflednote - 1, random.choice(sw_notelist))
        await ctx.send(sw_song)
    elif sw_shuffle == False and shufflednote > len(sw_song):
        await ctx.send("Must choose a number within range of the number of notes in song.")
    else:
        await ctx.send("Start a new song with *!songwrite <numberofnotes>* in order to use this command.")

#Song writer finish
@bot.command()
async def songfinish(ctx):
    global sw_song
    global sw_shuffle
    if sw_shuffle == False:
        await ctx.send("Song finished!")
        await ctx.send(str(sw_song) + ' by ' + str(ctx.message.author))
        sw_shuffle = True
        sw_song = []
    else:
        await ctx.send("Start a new song with *!songwrite <numberofnotes>* in order to use this command.")

#Madlibs choose story
def chooseStory():
    global ml_wordsetsrand
    global ml_words
    global ml_brainstormwords
    global ml_spookystuffwords
    global ml_currentstory
    ml_currentstory = random.choice(ml_wordsetsrand)
    if ml_currentstory == 'brainstorm':
        ml_words = ml_brainstormwords
    elif ml_currentstory == 'spooky stuff':
        ml_words = ml_spookystuffwords

#Madlibs start
@bot.command()
async def madlibs(ctx, *args):
    global ml_run
    global ml_players
    global ml_currentplayer
    global ml_onword
    global ml_givenwords
    global ml_readyfornextmessage
    if not ml_run and not gn_run and not sm_run:
        ml_players = []
        ml_onword = 0
        ml_givenwords = []
        chooseStory()
        for arg in args:
            ml_players.append(arg)
        if len(ml_players) >= 1:
            ml_currentplayer = ml_players[0]
            await ctx.send('Starting a game with: ' + str(ml_players))
            ml_run = True
            await ctx.send(str(ml_currentplayer) + ', give me a(n) ' + str(ml_words[ml_onword]))
            ml_readyfornextmessage = True
        else:
            await ctx.send('You need to list at least 1 player.')


#On message
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = message.content
    global sm_run
    global gn_run
    global sm_currentplayer
    global players
    global sm_currentmoney
    global playermoney
    global nameinlist
    global gn_playerguesses
    global gn_currentguesses
    global gn_currentplayer
    global gn_todaysnumber
    global ml_run
    global ml_readyfornextmessage
    global ml_givenwords
    global ml_words
    global ml_players
    global ml_currentplayer
    global ml_onword
    #Slot machine
    if msg == '!slots':
        if not sm_run and not gn_run and not ml_run:
            sm_run = True
            await message.channel.send('Starting slot machine game with ' + str(message.author.name))
            nameinlist = False
            for x in players:
                if x == str(message.author.name):
                    sm_currentplayer = str(message.author.name)
                    sm_currentmoney = playermoney[players.index(x)]
                    gn_currentguesses = gn_playerguesses[players.index(x)]
                    nameinlist = True
                    await message.channel.send('You have $' + str(sm_currentmoney) + ' remaining. Use *!crank* to crank the slot machine.')
                    return
            if not nameinlist:
                if len(players) == 1:
                    players[0] = str(message.author.name)
                    sm_currentplayer = str(message.author.name)
                    gn_playerguesses[0] = 0
                    gn_currentguesses = gn_playerguesses[0]
                    playermoney[0] = 250
                    sm_currentmoney = 250
                    await message.channel.send('You have $' + str(sm_currentmoney) + ' remaining. Use *!crank* to crank the slot machine.')
                else:
                    players.append(str(message.author.name))
                    sm_currentplayer = str(message.author.name)
                    gn_playerguesses.append(0)
                    gn_currentguesses = 0
                    playermoney.append(250)
                    sm_currentmoney = 250
                    await message.channel.send('You have $' + str(sm_currentmoney) + ' remaining. Use *!crank* to crank the slot machine.')
        else:
            await message.channel.send("Another game is currently running.")
    #Guess the number
    if msg == '!guess':
        if not sm_run and not gn_run and not ml_run:
            await message.channel.send('Hello, ' + str(message.author.name))
            gn_run = True
            nameinlist = False
            for x in players:
                if x == str(message.author.name):
                    gn_currentplayer = str(message.author.name)
                    gn_currentguesses = int(gn_playerguesses[players.index(x)])
                    sm_currentmoney = playermoney[players.index(x)]
                    nameinlist = True
                    if gn_currentguesses >= 1:
                        await message.channel.send('You have ' + str(gn_currentguesses) + ' guesses remaining. Guess a number between 1 and 20.')
                    else:
                        await message.channel.send('You are out of guesses. Come back tomorrow for more.')
                        gn_run = False
            if not nameinlist:
                if len(players) == 1:
                    players[0] = str(message.author.name)
                    gn_currentplayer = str(message.author.name)
                    gn_playerguesses[0] = 0
                    gn_currentguesses = 0
                    playermoney[0] = 250
                    sm_currentmoney = 250
                    if gn_currentguesses >= 1:
                        await message.channel.send('You have ' + str(gn_currentguesses) + ' guesses remaining. Guess a number between 1 and 20.')
                    else:
                        await message.channel.send('You are out of guesses. Come back tomorrow for more.')
                        gn_run = False
                else:
                    players.append(str(message.author.name))
                    gn_currentplayer = str(message.author.name)
                    gn_playerguesses.append(0)
                    gn_currentguesses = 0
                    playermoney.append(250)
                    sm_currentmoney = 250
                    await message.channel.send('You are out of guesses. Come back tomorrow for more.')
                    gn_run = False
        else:
            await message.channel.send('Another game is currently running.')

    if not sm_run and not ml_run:
        if gn_run:
            if gn_currentguesses >= 1:
                if not '!' in msg:
                    if int(msg) in gn_possibilities:
                        if int(msg) == gn_todaysnumber:
                            gn_currentguesses = 0
                            await message.channel.send('Congratulations! You guessed today\'s number! You win $100!')
                            for x in players:
                                if gn_currentplayer == x:
                                    playermoney[players.index(x)] += 100
                                    gn_playerguesses[players.index(x)] = 0
                            sm_moneydatahandler = open('moneydata.dat', 'wb')
                            pickle.dump(playermoney, sm_moneydatahandler)
                            sm_moneydatahandler.close()
                            sm_playerdatahandler = open('playerdata.dat', 'wb')
                            pickle.dump(players, sm_playerdatahandler)
                            sm_playerdatahandler.close()
                            gn_guessdatahandler = open('guessdata.dat', 'wb')
                            pickle.dump(gn_playerguesses, gn_guessdatahandler)
                            gn_guessdatahandler.close()
                            gn_currentplayer = ''
                            gn_currentguesses = 0
                            gn_run = False
                        else:
                            gn_currentguesses -= 1
                            await message.channel.send('That\'s not my number. You can use !guess ' + str(gn_currentguesses) + ' more times.')
                            for x in players:
                                if gn_currentplayer == x:
                                    gn_playerguesses[players.index(x)] -= 1
                            sm_playerdatahandler = open('playerdata.dat', 'wb')
                            pickle.dump(players, sm_playerdatahandler)
                            sm_playerdatahandler.close()
                            gn_guessdatahandler = open('guessdata.dat', 'wb')
                            pickle.dump(gn_playerguesses, gn_guessdatahandler)
                            gn_guessdatahandler.close()
                            gn_currentplayer = ''
                            gn_currentguesses = 0
                            gn_run = False
                    else:
                        await message.channel.send("Please choose an integer between 1 and 20 (inclusive).")
            else:
                gn_run = False
        else:
            gn_run = False
    else:
        gn_run = False

    #Madlibs
    if ml_run:
        if ml_readyfornextmessage:
            if ml_onword < len(ml_words):
                ml_givenwords.append(msg)
                ml_readyfornextmessage = False
                for player in ml_players:
                    if ml_currentplayer == player:
                        if ml_players.index(player) + 1 == len(ml_players):
                            ml_currentplayer = ml_players[0]
                        else:
                            ml_currentplayer = ml_players[ml_players.index(player) + 1]
                ml_onword += 1
                if ml_onword < len(ml_words):
                    await message.channel.send(str(ml_currentplayer) + ', give me a(n) ' + str(ml_words[ml_onword]))
                else:
                    ml_readyfornextmessage = False
                    await message.channel.send('Madlibs finished! Sending story now.')
                    if ml_currentstory == 'brainstorm':
                        await message.channel.send('**Brainstorming**\nMany say that ' + str(ml_givenwords[0]) + ' storming is ' + str(ml_givenwords[1]) + ' and does not ' + str(ml_givenwords[2]) + '. However, with the combination of the right ' + str(ml_givenwords[3]) + ', ' + str(ml_givenwords[4]) + ', and ' + str(ml_givenwords[5]) + ' anyone can lead a ' + str(ml_givenwords[6]) + ' session. When you have pulled together a ' + str(ml_givenwords[7]) + ' group of ' + str(ml_givenwords[8]) + ', brought together in a ' + str(ml_givenwords[9]) + ' that is ' + str(ml_givenwords[10]) + ', and have a ' + str(ml_givenwords[11]) + ' that is ' + str(ml_givenwords[12]) + ' for the participants to suggest ' + str(ml_givenwords[13]) + ' ideas, you will yield ' + str(ml_givenwords[14]) + ' more ' + str(ml_givenwords[15]) + ' ideas. Next time you need ' + str(ml_givenwords[16]) + ' thought-up ideas for a ' + str(ml_givenwords[17]) + ', a way to ' + str(ml_givenwords[18]) + ' sales for your business, or even ' + str(ml_givenwords[19]) + ' ideas for activities for the company ' + str(ml_givenwords[20]) + ' put these suggestion to work and let the ideas ' + str(ml_givenwords[21]) + '. With so many ' + str(ml_givenwords[22]) + ' ideas you\'ll have the boss declaring ' + str(ml_givenwords[23]) + ' in no time!')
                    elif ml_currentstory == 'spooky stuff':
                        await message.channel.send('**Spooky Stuff**\nAmerican children are fascinated by ' + str(ml_givenwords[0]) + ' stuff - like stories that scared the ' + str(ml_givenwords[1]) + ' off them or make their ' + str(ml_givenwords[2]) + ' stand on end. Scientists say this is because being frightened causes the ' + str(ml_givenwords[3]) + ' gland to function and puts ' + str(ml_givenwords[4]) + ' into their blood. And everyone knows that makes kids feel ' + str(ml_givenwords[5]) + '. When they are scared by a movie or a/an ' + str(ml_givenwords[6]) + ', boys laugh and holler and '  + str(ml_givenwords[7]) + '. But girls cover their eyes with their ' + str(ml_givenwords[8]) + ' and keep screaming and ' + str(ml_givenwords[9]) + '. Most kids get over this by the time they are ' + str(ml_givenwords[10]) + '. Then they like movies about cars ' + str(ml_givenwords[11]) + ' or cops shooting ' + str(ml_givenwords[12]) + ', or, if they are girls, they like movies about a boy meeting a/an ' + str(ml_givenwords[13]) + ' and falling in love. Of course, that can be scary, too.')
                    ml_run = False
                ml_readyfornextmessage = True
            else:
                print(ml_givenwords)

    await bot.process_commands(message)

#Command Errors
@givemoney.error
async def givemoney_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("The format of this command should be *!givemoney <password> <player> <amount>*.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Make sure to put names with multiple words in quotation marks.")

@songwrite.error
async def songwrite_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("The format of this command should be *!songwrite <numberofnotes>*.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Make sure to use an integer for the number of notes.")

@songshuffle.error
async def songshuffle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("The format of this command should be *!songshuffle <shufflednote>*.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Make sure to use an integer for the shuffled note.")

bot.run('TOKEN')