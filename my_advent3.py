#####################################################
# my_advent.py   350 point adventure  Python 3.x port
# Python program runs on Windows, Linux or a Mac
# includes IDLE incompatible function getch
# run from cmd / shell with 'python my_advent.py'
######################################################
import random                  # witts end
import sys                     # my_input, attack, detonate, getch
from random import randrange   # bedquilt paths, dwarf attack, bear on bridge
import time                    # playmove
import pickle                  # savegame, loadgame
import select                  # forest door cave test
import platform                # support Windows in getch
import os                      # support Windows clear screen in playmove
#
# messages are sentences using a sublist in my_list
# all commands get mylist,mysent,myvars
# clear screen with each room now controlled by debug
#
# main service loop for the game
#  announce_room -
#    room description long first, subsequently short
#    inlist show description of objects in the room
#    display current room number (debug)
#  my_input -
#    getch loop for action word and object word collection
#    mycmd dispatch to individual action word functions
#    mycmd uses playmove function for the subset of action words for moves
#  playmove -
#    moves returns new room number for valid moves, same room if no cave path
#    playmove announces any puzzles that block a move from the room
#      grate,snake,dragon,rusty door,crossover
#    playmove announces a randomized move failure if no cave path when no puzzle blocking
#    playmove announces magic activity for a new room
#      magic status of grate, troll, crystalline bridge,rickety bridge,snake
#      magic status of dragon,bear,beanstalk,rusty door,lamp,dwarf,pirate
#      enter end game, player move counter
#
def main_loop(mylist,mysent,myvars):
    print("")
    mysentence(mysent[1])
    try:
        yn = getch()
        print(yn,flush=True)
    except:
        print("Please run me on the command line, not in IDLE.")
        sys.exit()
    if yn == "y":
        mysentence(mysent[347])
    print("")
    while True:
        myvars = announce_room(mysent,myvars)
        if myvars[193] == 1:     # auto map display enabled?
            myvars[126] = "zzz"
            myvars[128] = "map"
            myvars[129] = "zzz"
            myvars = mapp(mylist,mysent,myvars)
        myvars = my_input(mylist,mysent,myvars)
#
# displays a sentence using a sublist in my_list
#
def mysentence(my_sent_list):
    b = ''
    colflag = 0
    for i in my_sent_list:
        b += str(i)      # add a word
        b += chr(32)     # follow with space
        if len(b) > 73:  # print if more than 73 chars
            print(b)
            b = ''
    if len(b) > 0:       # print any leftovers
        print(b) 
    return
# 
# take game commands with a getch loop that matches actword and collects the objword
#
def my_input(mylist,mysent,myvars):
    actwords = {'about': info, 'f': forward,'b': back,'quit': quit_this,'west': playmove,'east': playmove,'north': playmove,'south': playmove,'sw': playmove,'nw': playmove,'se': playmove,'ne': playmove, 'news': news, 'map': mapp, \
                'up': playmove,'down': playmove,'take': take, 'drop': drop, 'inven': inven,'look': look,'n': playmove,'s': playmove,'e': playmove,'w': playmove,'u': playmove,'d': playmove,'help': helpme, 'inventory': inven, \
                'building': building, 'forest': forest,'enter': enter, 'exit': exitt, 'downstream': downstream,'xyzzy': xyzzy,'y2': y2,'unlock': unlock,'lock': lock,'score': score,'wave': wave,'variables':variables, 'cheat':cheat, \
                'get': take,'open': openn,'free': freee,'on': lampon,'off': lampoff,'kill': attack,'attack': attack,'plugh': plugh,'throw': throw,'room': mapp,'feed': feed,'water': pour, 'showrooms': mapp, \
                'fee': feefiefoefoo,'fie': feefiefoefoo,'foe': feefiefoefoo,'foo': feefiefoefoo,'fill': fillbottle,'cross': cross,'plover': plover,'info': info,'words': words,'save': savegame,'load': loadgame,'blast': detonate, \
                'detonate': detonate,'jump': jump, 'walk': gowhere,'run': gowhere,'go': gowhere,'climb': climb,'light': light,'grate': grate,'pour':pour,'pit':pit,'bedquilt':bedquilt,'slab':slab,'reservoir':canyon}
    movewords = ['e','east','w','west','s','south','n','north','ne','nw','se','sw','up','down','u','d']
    print("Adventure>",end=" ",flush=True)
    firstword = []
    secondword = []
    while True:
        yn = getch()
        if yn == chr(32):
            sys.stdout.write(chr(32))  # space between echoed words
            sys.stdout.flush()         # echo buffer with space between words
            break
        elif yn == chr(127):           # del is backspace & rewrite line
            firstword = firstword[0:-1]
            sys.stdout.write(chr(32))  # overwrite to erase
            sys.stdout.write(chr(13))  # start the line over
            print("Adventure>",end=" ",flush=True)
            for cc in firstword:
                sys.stdout.write(cc)
        elif yn == chr(47):            # / is the adventure command cancel
            firstword = []
            count = 0
            print(chr(13,end=""))
            while count < 10:
                print(chr(32),end="")
                count += 1
            print(chr(13),"Adventure> ",end="",flush=True)
        elif yn == chr(13):            # if only one word entered
            secondword = "noword"
            break
        elif yn == chr(9) and len(firstword) == 1: # Linux style autocomplete?
            addword = []
            mywords = ["building","forest","grate","downstream","inventory","quit","reservoir","variables"]
            for oneword in mywords:
                if firstword[0] == oneword[0]:
                    addword += oneword[1:]
            if len(addword) > 0:
                for cc in addword:
                    firstword.extend(cc)
            sys.stdout.write(chr(32))  # overwrite to erase
            sys.stdout.write(chr(13))  # start the line over
            print("ADVenture>",end=" ",flush=True)  # redisplay the prompt
            for cc in firstword:
                sys.stdout.write(cc)   # display the expanded command
                sys.stdout.flush()     # force python3 to show the I/O buffered command 
            break
        else:
            sys.stdout.write(yn)
            sys.stdout.flush()
            firstword.append(yn)
    while secondword != "noword":
        yn = getch()
        if yn == chr(13):
            break
        elif yn == chr(127):
            secondword = secondword[0:-1]
            sys.stdout.write(chr(32))  # overwrite to erase
            sys.stdout.write(chr(13))  # start the line over
            print("Adventure> ",end="",flush=True) # rewrite entire line sans 1 char
            for cc in firstword:
                sys.stdout.write(cc)
            sys.stdout.write(chr(32))  # space between words
            for cc in secondword:
                sys.stdout.write(cc)            
                sys.stdout.flush()
        else:
            sys.stdout.write(yn)
            sys.stdout.flush()
            secondword.append(yn)
#
# if there is an action word, it must be the first word unless take inventory
#
    thefirstword = ("".join(firstword))   # player provided first word
    thesecondword = ("".join(secondword)) # player provided second word
    myvars[128] = thefirstword.lower()    # action word lower case
    myvars[129] = thesecondword.lower()   # object word lower case
    foundit = 0
    for check in actwords:
        if myvars[128] == check and myvars[129] != "inventory":
            foundit = 1
            break
        else:
            for check in actwords:
                if myvars[129] == check:       # if reversed, flip em around
                    myvars[129] = myvars[128]  # second word is action word
                    myvars[128] = check        # now good to go
                    foundit = 1
                    break
#
# run any supported command entered by player
# for playmove commands, include the direction of the move in myvars[126]
#
    myvars[126] = "zzz"    # not a move by default if no action words
    if check in movewords and foundit == 1:
        myvars[126] = check
    if check in actwords:
        mycmd = actwords[check]
        print("")
        if foundit == 1:
            myvars = mycmd(mylist,mysent,myvars)
        else:
            mysentence(mysent[352])           # Huh?
    return myvars
#
# game command handlers
#
def quit_this(mylist,mysent,myvars):
    print("Are you sure you want to quit? ",end="",flush=True)
    yn = getch()
    print(yn,flush=True)
    if yn == "y":
        print("")
        the_score = scoreit(myvars)
        rating = [389,390,391,392,393,394,395,396]
        ratelevel = [464,463,462,461,460,459,458]
        levels = [0,25,75,130,200,270,340,350]
        leveloop = 0
        while leveloop < 8:
            if the_score <= levels[leveloop]:
                mysentence(mysent[ratelevel[leveloop - 1]])
                mysentence(mysent[rating[leveloop]])
                break
            leveloop += 1
        sys.exit()
    else:
        print("")
        return myvars
#
# save game
#
def savegame(mylist,mysent,myvars):
    with open('myadvent.sav', 'wb') as fp:
        pickle.dump(myvars, fp)
    print("Your current game has been saved.")
    return myvars
#
# load saved game
#
def loadgame(mylist,mysent,myvars):
    try:
        with open ('myadvent.sav', 'rb') as fp:
            myvars = pickle.load(fp)
            mysentence(mysent[419])  # poof!        
    except:
        print("Previous game not loaded.")
    return myvars
#
# if the endgame conditions are met, proceed to repository
# In Witts End, Lamp is off, Cave is closing and one magic magazine dropped
#
def endgame(mylist,mysent,myvars):
    if myvars[0] == 59 and myvars[158] > 0 and myvars[171] > 0:
        copies = [178,179,180,181,182,183,184,185,186,187,188,189]
        for copy in copies:
            if myvars[copy] == 59:            # found a magazine, any edition?
                myvars[0] = 123               # proceed to endgame rooms
                mysentence(mysent[470])       # cave is closed announcement
                print("")                     # blank line, big event
                myvars[158] = 0               # turn lamp back on
                myvars[151] = 130             # put bear away, if present
                myvars[177] = 0               # bear stops following if present
                myvars[144] = 1               # put the player's magazine in building
                magazines = [178,179,180,181,182,183,184,185,186,187,188,189]
                for edition in magazines:
                    myvars[edition] = 130     # suppress magazine magic
                myvars[171] = 0               # suppress cave closing message
                myvars[175] = 1               # repository entered
    return myvars
#
# score   add points for solved puzzles
#
def score(mylist,mysent,myvars):
    the_score = scoreit(myvars)
    return myvars
#
# scoring  used by score command and at game exit
#
def scoreit(myvars):
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    r = 1
    while r < 126:
        if myvars[r] == 1:
            score1 += 1 # one point for each room visited
        r += 1
    treasures = [142,143,144,145,146,147,148,149,150,152,153,154,155,156,157]
    for trophy in treasures:
        if myvars[int(trophy)] == 1:
            score2 += 8 # eight points for each treasure in room 1
    magazines = [178,179,180,181,182,183,184,185,186,187,188,189]
    for edition in magazines:
        if myvars[int(edition)] == 1:
            score2 += 8 # eight points for any one magic magazine
            break
# puzzles
# grate,bridge,snake,dragon,plugh,beanstalk,door,shell,eggs,rickety bridge
#
    puzzles = [127,161,167,166,173,168,169,176,176,166]  # myvars puzzle flags
    for trophy in puzzles:
        if myvars[int(trophy)] > 0:
            score3 += 10        # ten points for each puzzle
    if myvars[175] > 0:         # repository entered if gt 0
        score4 = 5              # five final points for endgame entry
    score = score1 + score2 + score3 + score4
    print("Your current score is", str(score), "out of 350 after",str(myvars[159]), "moves.")
    print("Rooms=",str(score1)+"/125  Treasures= "+str(score2)+"/120  Puzzles= "+str(score3)+"/100  Endgame= "+str(score4)+"/5")
    return score
#
# detonate same as blast
#
def detonate(mylist,mysent,myvars):
    if myvars[175] == 1:                # in the repository?
        if myvars[136] == 124:          # rod dropped in ne corner?
            if myvars[0] == 123:        # player in sw corner?
                print("")
                mysentence(mysent[475]) # final game sentence
                print("")
                the_score = scoreit(myvars)
                print("")
                sys.exit()              # game over
            if myvars[0] == 124:
                print("It is not safe to blast here.")
        else:
            mysentence(mysent[476])     # I see no dynamite here        
    else:
        print("Nothing Happens...Yet.")
    return myvars
#
# the player requests a move, make a move if allowed in moves
#   
def playmove(mylist,mysent,myvars):    
    newroom = moves(myvars[126],myvars[0])
#
# Hall of Mists Crossover has an extra info message in one direction
#
    if myvars[0] == 17:
        if myvars[126] == "n" or myvars[126] == "north":
            mysentence(mysent[465])
#
# for all other cases where move blocked the move request..
#
    if newroom == myvars[0]:          # true when moves blocks the request
        one_msg = 0
#
# lost in the forest
#
        if myvars[0] == 4:
            lost_list = ["n","north","w","west","se","ne","sw","sw","u","up","d","down"]
            for ImLost in lost_list:
                if myvars[126] == ImLost:
                    print("You are wandering aimlessly.",end="")
                    one_msg = 1
#
# snake blocks
#
        if myvars[0] == 40 and myvars[167] == 0:
            mysentence(mysent[358])   # cannot get past snake
            one_msg = 1
#
# dragon blocks
#
        if myvars[0] == 46 and myvars[166] == 0:
            mysentence(mysent[362])   # cannot get past dragon
            one_msg = 1
#
# door rusted shut
#
        if myvars[0] == 96 and myvars[169] == 0:
            if myvars[126] == "n" or myvars[126] == "north":
                mysentence(mysent[316])
                one_msg = 1
#
# narrow passage to Plover
#
        if myvars[0] == 82 and myvars[190] == 0: # in the Alcove with objects?
            if myvars[126] == "e" or myvars[126] == "east":
                mysentence(mysent[262])   # tunnel is too tight
                one_msg = 1           
#
# dark room
#
        if myvars[0] == 83:
            if myvars[126] == "n" or myvars[126] == "north":            
                mysentence(mysent[416])
                one_msg = 1                     
#
# troll blocks rickety bridge
#
        if myvars[165] == 0: # rickety bridge toll not paid?
            if (myvars[0] == 64 and myvars[126] == "ne") or (myvars[0] == 65 and myvars[126] == "sw"):
                one_msg = 1  # troll announces the blockade           
#
# a move that is never permitted
#
        if one_msg == 0:
            mykey = random.randint(0, 2)
            if mykey == 0:
                print("You cannot go that direction from here.")
            if mykey == 1:
                print("There is no way to proceed in that direction!")
            if mykey == 2:
                print("Sorry. Please try some other direction.")
    else:
        myvars[0] = newroom         # all other cases, move to another room
        if myvars[191] == 0:        # debug mode is off
            if 'Windows' == platform.system():
                os.system('cls')
            else:
                 print("\n")
#                print(chr(27) + "[2J")  # clear the screen in a new room
#
# bear activity based on myvars[177]
#
    if myvars[177] == 3 :     # bear in tow, crossing bridge, toll paid?
        if myvars[151] == 64 and myvars[126] == "ne" and myvars[165] == 1:
            myvars[177] = 0   # block bear msg and bear goes away
            myvars[194] = 1   # block future bridge access
        elif myvars[151] == 65 and myvars[126] == "sw" and myvars[165] == 1:
            myvars[177] = 0   # block bear msg and bear goes away
            myvars[194] = 1   # block future bridge access
        else:
            myvars[151] = newroom         # bear on the move
            mysentence(mysent[295])
    if myvars[0] == 70:
        if myvars[177] == 0:
            mysentence(mysent[483])   # first bear encounter warning
            myvars[177] += 1
#
# if next to rickety bridge, announce it
#
    if newroom == 64 or newroom == 65:
        if myvars[194] == 0:
            mysentence(mysent[248])     # rickety bridge in the mist
        if myvars[194] == 1:
            print("The wreckage of a bridge (and a dead bear) can be seen at the bottom of the chasm.")
        if myvars[165] == 0:
            mysentence(mysent[249]) # a sign says pay troll until paid
#
# troll toll activity
#
    if (myvars[0] == 64 and myvars[128] == "ne") or (myvars[0] == 65 and myvars[128] == "sw"):
        if myvars[165] == 0:
            mysentence(mysent[251])  # troll demands a treasure
#
# if in the dark room, announce it
#
    if myvars[0] == 84:
        mysentence(mysent[363])   # massive stone tablet reads congrats
#
# if snake in the room, announce it
#
    if myvars[0] == 40 and myvars[167] == 0:
        mysentence(mysent[303])      # fierce snake bars the way
#
# if dragon in the room, announce it
#
    if myvars[0] == 46 and myvars[166] == 0:
        mysentence(mysent[441])      # dragon in the way
#
# announce beanstalk status
# 364 = tiny mumur, 367 = bellowing, 370 = full grown
#
    if myvars[0] == 92:             # west pit.  add up to hole to 94
        if myvars[168] == 0:
            mysentence(mysent[364]) # plant mumur
        if myvars[168] == 1:
            mysentence(mysent[366]) # 12 foot beanstalk
            mysentence(mysent[367]) # plant is now bellowing
    if myvars[0] == 90 and myvars[168] == 2:      # 168 = plant lifecycle
        mysentence(mysent[370])     # huge beanstalk
#
# if in Immense N/S Passage, announce massive rusty door
#
    if myvars[0] == 96:
        if myvars[169] == 0:
            mysentence(mysent[315])
        else:
            mysentence(mysent[317])
#
# if lamp is off, fall into a pit and die
#
    if myvars[0] > 11 and myvars[158] > 3:
        myvars = death(mylist,mysent,myvars)
        return myvars
    elif myvars[0] > 11 and myvars[158] > 0 and myvars[158] < 4:
        mysentence(mysent[359])  # dark and there are pits
        myvars[158] += 1
#
# dwarf activity
#
    myvars[162] = randrange(40, 46)
    if newroom == myvars[162]:
        if myvars[164] > 0:
            myvars[164] -= 1        # dwarf encounter counter
        if myvars[164] > 0:
            mysentence(mysent[468]) # dwarf nearby
        if myvars[164] == 0:
            mysentence(mysent[310]) # dwarf throws axe
            irand = randrange(0,5)
            if irand < 2:
                myvars[163] = 0     # player dead
                mysentence(mysent[309]) # axe hits announcement
                myvars = death(mylist,mysent,myvars) # game starts over
                return myvars
            else:
                mysentence(mysent[311]) # axe missed
                myvars[139] = newroom   # leave axe in room
                myvars[164] = 7         # reset encounter counter
#
# pirate activity  pirate robbery if 170 > 1, add nw to 122 from room 48
#
    if myvars[170] == 1:                       # second encounter
        if myvars[172] == newroom:
            mysentence(mysent[266])            # robbery
            myvars[170] = 2                    # pirate work is finished
            myvars[172] = 130                  # pirate disappears
            grabit = 142                       # first treasure is coins
            while grabit < 158:
                if myvars[grabit] == 126:      # player has this object?
                    if grabit != 151:          # bear in middle of treasures
                        myvars[grabit] = 48    # treasure to lair
                grabit += 1
    if myvars[170] == 0:                       # first encounter
        if myvars[172] == newroom:
            mysentence(mysent[439])            # pirate hasty exit
            myvars[170] = 1                    # next time is a bad encounter
        else:
            if newroom >= 50 and newroom < 60: # pirate neighborhood
                mysentence(mysent[265])        # faint rustling noise
    if myvars[170] < 2:                        # pirate moves until robbery
        irand = randrange(0,10)
        myvars[172] = 50 + irand               # pirate moves every turn
#
# lamp life test
#
    if myvars[159] == 230:                        # 230 turns taken
        mysentence(mysent[436])                   # lamp getting dim
    if myvars[159] == 265:                        # 265 turns taken
        mysentence(mysent[437])                   # lamp is almost dead
    if myvars[159] > 300 and myvars[142] != 130:  # 300 turns, no coins used?
        mysentence(mysent[438])                   # lamp is now dead
        myvars[158] = 4                           # lamp set to dark
#
# cave closure test for 12 found treasures in Well House, magazine does not count
#
    count = 0
    treasures = [142,143,144,145,146,147,148,149,150,152,153,154,155,156,157]
    for trophy in treasures:
        if myvars[int(trophy)] == 1:  # this treasure found?
            count += 1 
    if count >= 12:                   # 12 treasures in well house?
        myvars[171] += 1              # indicate cave is closing
    if myvars[171] > 9:               # every ten turns, announce closure
        myvars[171] = 1               # reset counter
        mysentence(mysent[469])       # cave is closing
#
# move complete
#
    myvars[159] += 1                    # count game moves here
    return myvars         
#
# warning the getch function does not work in idle, use shell
# idle has its own psuedo terminal, does not include file ops
# separate getch code for Linux/Mac versus Windows
#
def getch():
    if 'Windows' == platform.system():
        ch = msvcrt.getch()
        return ch
    else:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
#
# set of flags used to operate the game
#
def myvars_init():
    myvars = []
    myvars.append(0)          # player current room in the cave, starts outside well house
    myvars.extend([0] * 125)  # room visit flag, 1 per room
    myvars.append('e')        # player requested move direction string [126]
    myvars.append(0)          # grate locked between room 8 and room 9 [127]
    myvars.append('action')   # player provided action word [128]
    myvars.append('objword')  # player provided object word [129]
    myvars.append(1) # 0.keys [130]
    myvars.append(1) # 1.lamp [131]
    myvars.append(1) # 2.food [132]
    myvars.append(1) # 3.empty bottle [133]
    myvars.append(10) # 4.empty cage [134]
    myvars.append(13) # 5.bird nearby [135]
    myvars.append(11) # 6.rod [136]
    myvars.append(130) # 7.bird in cage [137]
    myvars.append(130) # 8.bottle with water [138]
    myvars.append(130) # 9.axe [139]
    myvars.append(76) # 10.pillow [140]
    myvars.append(91) # 11.oil [141]
    myvars.append(41) # 12.coins [142]
    myvars.append(130) # 13.gold chain [143]
    myvars.append(58) # 14.magazine [144]
    myvars.append(130) # 15.pearl [145]
    myvars.append(83) # 16.emerald [146]
    myvars.append(74) # 17.vase [147]
    myvars.append(46) # 18.rug [148]
    myvars.append(84) # 19.pyramid [149]
    myvars.append(17) # 20.diamonds [150]
    myvars.append(130) # 21.bear [151]
    myvars.append(94) # 22.golden eggs [152]
    myvars.append(97) # 23.trident [153]
    myvars.append(18) # 24.gold nugget [154]
    myvars.append(39) # 25.bars of silver [155]
    myvars.append(42) # 26.jewelry [156]
    myvars.append(72) # 27.spices [157]
    myvars.append(1)  # lamp on=0 lamp off>0 goto pit>4 [158]
    myvars.append(0)  # player game turns counter [159]
    myvars.append(0)  # fee fie foe foo counter [160]
    myvars.append(0)  # crystalline bridge visibility [161]
    myvars.append(130) # dwarf location [162]
    myvars.append(1)  # player is dead if 0 [163]
    myvars.append(7)  # dwarf encounter counter [164]
    myvars.append(0)  # 1 = rickety bridge toll paid [165]
    myvars.append(0)  # 1 = dragon dead rug can be taken [166]
    myvars.append(0)  # 1 - snake dead [167]
    myvars.append(0)  # 1 = beanstalk growing 2 = beanstalk to room 94 [168]
    myvars.append(0)  # 1 = rusted door opens [169]
    myvars.append(0)  # 1 = pirate seen 2 = robbery [170]
    myvars.append(0)  # 1-10 = cave is closing counter [171]
    myvars.append(50) # pirate random room [172]
    myvars.append(0)  # plugh puzzle [173]
    myvars.append(0)  # clam / shell opened [174]
    myvars.append(0)  # repository entered [175]
    myvars.append(0)  # eggs recovered [176]
    myvars.append(0)  # bear state [177]
    myvars.append(130) # Spelunker Today January edition [178]
    myvars.append(130) # Spelunker Today February edition [179]
    myvars.append(130) # Spelunker Today March edition [180]
    myvars.append(130) # Spelunker Today April edition [181]
    myvars.append(130) # Spelunker Today May edition [182]
    myvars.append(130) # Spelunker Today June edition [183]
    myvars.append(130) # Spelunker Today July edition [184]
    myvars.append(130) # Spelunker Today August edition [185]
    myvars.append(130) # Spelunker Today September edition [186]
    myvars.append(130) # Spelunker Today October edition [187]
    myvars.append(130) # Spelunker Today November edition [188]
    myvars.append(130) # Spelunker Today December edition [189]
    myvars.append(0)   # Player drops everything for Plover [190]
    myvars.append(0)   # 0=normal game, 1=cheat commands enabled [191]
    myvars.append(0)   # 0=player moves 1=map calling moves [192]
    myvars.append(0)   # 0=regular display 1=auto map with every move [193]
    myvars.append(0)   # 1 = rickety bridge destroyed [194]
    return myvars
#
# this is the set of move dictionaries with from-room and to-room elements
# if room has a valid move in the list, return new room else return same room
# solved puzzles have myvars flags that add moves
# [168] room 92 beanstalk grew UP to room 93
# room 60 bedquilt N,S,UP,DOWN randomized to four of 49,58,61,86,88
# room 59 witts end all directions back to 59 except 3 randomly set to room 58
# room 59 witts end, [158] lamp off and [144] magazine dropped, [171] cave closed
# then player goes to room 123
#
def moves(direction,room):
    newroom = room     # unless changed below, blocked move returns same number
#
# moves by compass directions, west & east
#
    if direction == "w" or direction == "west":
        mylist = {1:0,0:2,2:3,3:4,6:5,9:10,10:11,11:12,12:13,13:14,15:16,17:19,19:20,20:23,22:20,24:31,25:24,26:25,27:26,28:27,29:28,30:29,31:30,36:37,38:86,41:22,43:46,50:49,51:50,53:60,58:60,60:75,66:65,67:66,72:71,74:61,75:89,76:75,77:78,81:82,83:82,89:90,90:88,97:98,121:120,122:121,69:68,70:69,93:94,100:100,99:100,102:99,101:99,106:109,105:108,107:106,108:107,119:105,109:106,110:109,111:100,113:102,117:110}   
        if myvars[161] == 1:
            mylist[16] = 17  # crystalline bridge now visible to the west
        if myvars[167] == 1:
            mylist[40] = 41  # snake is gone now, permit travel west
    if direction == "e" or direction == "east":
        mylist = {15:14,14:13,13:12,12:11,11:10,10:9,6:5,5:4,4:6,3:2,2:0,0:1,16:15,19:17,20:19,22:41,23:20,24:25,25:26,26:27,27:28,28:29,29:30,30:31,31:24,36:35,37:36,41:40,43:40,46:43,49:50,50:51,53:58,58:59,60:53,66:67,71:72,63:61,75:76,77:79,89:75,90:89,94:95,68:69,69:70,98:97,99:101,101:102,104:101,106:107,107:104,108:109,109:108,119:122,121:122,105:119,100:111,112:102,102:113,118:119,120:121}
        if myvars[161] == 1:
            mylist[17] = 16  # crystalline bridge visible to the east
        if myvars[167] == 1:
            mylist[40] = 15  # snake is gone now, permit travel east
        if myvars[166] == 1:
            mylist[46] = 43  # dragon is gone, permit travel east
#
# plover room east entry test 
#
        my_index = 130            # things to carry 130-157
        myvars[190] = 1           # permit move through tight passage
        while my_index < 158:
            if myvars[my_index] == 126 and my_index != 144: # magazine ok
                myvars[190] = 0   # got to drop it all before proceeding
                break             # stop looking
            my_index += 1
        if myvars[190] == 1:
            mylist[82] = 83  # enable tight tunnel to plover room
#
# moves by compass directions, besides west and east
#
    if direction == "n" or direction == "north":
        mylist = {2:5,5:4,7:6,60:61,6:2,8:7,15:40,17:19,19:17,20:22,23:22,22:21,24:31,25:24,26:25,27:26,28:27,29:28,30:29,31:30,34:33,33:32,35:15,39:36,42:40,44:45,45:47,46:44,53:54,54:55,61:62,68:67,71:73,74:81,77:75,79:77,80:79,85:86,86:38,87:85,88:60,94:96,100:99,99:99,102:101,110:108,108:105,119:121,122:119,104:114,18:15}
        if myvars[167] == 1:
            mylist[40] = 39  # snake is gone, permit travel north
        if myvars[166] == 1:
            mylist[46] = 44  # dragon is gone, permit travel north
        if myvars[158] > 0:
            mylist[83] = 84  # permit entry to dark room with lamp off
        if myvars[169] == 1:
            mylist[96] = 97  # rusty door is open, permit travel north
    if direction == "s" or direction == "south":
        mylist ={2:6,3:5,60:88,4:5,6:7,7:8,14:15,15:18,19:99,21:22,22:23,23:24,24:25,25:26,26:27,27:28,28:29,29:30,30:31,31:24,33:34,36:39,39:40,44:46,45:44,47:45,54:53,62:61,71:67,73:71,75:77,78:77,79:80,81:74,84:83,85:87,86:85,88:90,94:93,95:94,96:94,97:96,121:119,19:99,99:102,100:100,101:104,104:107,107:108,108:108,109:110,102:112,114:104,110:117,119:118}
        if myvars[167] == 1: # snake is gone?
            mylist[40] = 42  # permit travel south
    if direction == "ne":
        mylist = {65:66,67:71,75:60,32:24,124:123}
        if myvars[165] == 1: # rickety bridge toll paid?
            mylist[64] = 65  # troll is gone, good to cross
    if direction == "se":
        mylist = {61:74,67:68,24:23,25:23,26:23,27:23,28:23,29:23,30:23,31:23,32:33,74:75,86:60,48:122}	
    if direction == "nw":
        mylist = {60:85,82:81,75:74}  # bedquilt 60 to be randomized
        if myvars[172] == 130:        # pirate goes into hiding after robbery
            mylist[122] = 48          # permit travel into pirate lair
    if direction == "sw":
        mylist = {24:32,61:63,25:32,26:32,27:32,28:32,29:32,30:32,31:32,123:124}
        if myvars[165] == 1: # rickety bridge toll paid?
            mylist[65] = 64  # troll is gone, good to cross
        if myvars[167] == 1: # snake is gone?
            mylist[40] = 43  # permit travel sw to ew canyon
    if direction == "u" or direction == "up":
        mylist = {11:12,60:69,15:14,35:15,40:15,41:22,50:39,52:51,53:49,54:55,56:54,57:56,58:53,63:64,74:81,88:44,91:89,92:90,2:3,99:19,102:103,103:102,109:107,108:110,115:104,116:108}
        if myvars[127] == 1:
            mylist[9] = 8
        if myvars[168] == 2: # beanstalk status 2 = full grown
            mylist[90] = 93  # can now climb beanstalk to E/W corridor
    if direction == "d" or direction == "down":
        mylist = {14:15,15:40,24:23,60:58,35:36,39:50,43:79,44:88,49:53,51:52,54:56,55:54,56:57,64:63,85:60,87:107,89:91,90:92,93:90,98:61,102:103,103:102,119:13,104:115,107:109,108:116}
        if myvars[127] == 1:
            mylist[8] = 9
    if room == 59:       # Witts End
        wittroom = [58,58,58,59,59,59,59,59,59,59]
        wittkey = random.randint(0, 9)
        mylist[59] = wittroom[wittkey]   # 3 in 10 chance that player gets out
        if myvars[191] == 1 and myvars[192] == 0:
            print("WittsEnd=",str(wittkey),end="")
#
# move data is in dictionaries, appended by puzzle flags
#
    for room_now in mylist:
        if room_now == room:
            newroom = mylist.get(room_now)
            break
    return newroom
#
# room descriptions for first visit and subsequent visits
# the first 111 rooms have almost calculable sentence numbers, then it is a mess
# myvars[0] = room number  myvars[1-125] = room visited flags
#
def announce_room(mysent,myvars):
    room = myvars[0]
    my_room1 = room + 2   # first room = 0 first description = 2
    my_room2 = room + 125
    if room == 15:        # Hall of Mists east
        my_room2 = 145
    if room == 20:        # Long Hall east end
        my_room2 = 146
    if room == 21:        # Dead End passage
        my_room1 = 220
        my_room2 = 220    
    if room == 22:        # High N/S Crossover
        my_room1 = 147
    if int(room) > 98:
        add1 = [101,101,101,101,101,101,101,101,101,101,101,101,101,113,113,113,113,113,113,113,113,121,113,101,101,471,472,113]
        my_room1 = add1[(int(room) - 98)]
        add2 = [101,101,101,101,101,101,101,101,101,101,101,101,101,113,113,113,113,113,113,113,113,244,113,101,101,473,474,113]
        my_room2 = add2[(int(room) - 98)]
    if myvars[room+1] == 0:
        mysentence(mysent[int(my_room1)])
        myvars[room+1] = 1
    else:
        mysentence(mysent[int(my_room2)])
    myvars = inlist(mysent,myvars)     # announce any object in the room
#
# if in debug mode, show current room number
#
    if myvars[191] == 1:               # in debug mode?
        print("current room=",str(myvars[0]))
#
# if grate nearby, report locked or unlocked
#
    if myvars[0] == 8 or myvars[0] == 9:
        if myvars[127] == 0:
            mysentence(mysent[354])  # grate locked
        if myvars[127] == 1:
            mysentence(mysent[355])  # grate unlocked
#
# if crystalline bridge is visible, announce it
#
    if myvars[0] == 16 or myvars[0] == 17:
        if myvars[161] == 1:  # crystalline bridge visible
            mysentence(mysent[356])
#
# in debug mode show Dwarf movements
#
    if myvars[191] == 1 and myvars[0] >= 40 and myvars[0] < 46:   # dwarf radar report
        print("Dwarf presently in room",str(myvars[162]),"attack downcounter=",str(myvars[164]))
#
# in debug mode show Pirate movements
#
    if myvars[0] >= 50 and myvars[0] < 60 and myvars[191] == 1:
        print("Pirate presently in room",str(myvars[172]),end="")
        pstatus = (["Pirate not yet seen.","Robbery with next encounter.","Player has been robbed."])
        print(pstatus[myvars[170]])
    return myvars
#
# objects found in the cave, report if room has an object
# Inlist has the current room number, object sentence number
# S_Index3  list of sentences for objects found in the cave
# S_Index4 list of sentences for objects carried by player
# Use myvars[130] through [157] to announce an object
# since myvars can be updated, this supports object take and drop
# had to exclude sentence 289 for the bear, conflicts with bear logic
#
def inlist(mysent,myvars):
    S_Index3 = [267,268,269,275,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,288,289,290,291,292,293,294,480]
    room = myvars[0]
    x = 130
    while x < 158:
        if room == myvars[x] and S_Index3[x-130] != 289:
            mysentence(mysent[S_Index3[x-130]])
        x += 1
#
# bear activity based on myvars[177]
#  0= bear chained, dangerous  sent485 room 70 and sent483 once
#  1= bear chained, dangerous  sent485 room 70
#  2= bear chained, fed        sent289 room 70 very large brown bear here
#  3= bear unchained           sent486 room 70 contented bear wandering nearby
#  bear following              sent295 any room
#
    if myvars[0] == 70:
        if myvars[177] < 3:           # fourth bear state in moves
            bears = [485,485,289,486] # 1 of 4 bear states
            mysentence(mysent[bears[myvars[177]]])
#
# magazine magic
# edition of Spelunker Today here 1417-1428 == Jan through Dec
# myvars 178-189 are the locations
#
    magazines = [1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428]
    copies = [178,179,180,181,182,183,184,185,186,187,188,189]
    for mindex, copy in enumerate(copies):
        if myvars[copy] == myvars[0]:
            print("I see the",end="")
            print(mylist[magazines[mindex]],end="")
            mysentence(mysent[443])
            break
    return myvars
#
# enable debug commands
#
def cheat(mylist,mysent,myvars):
    if myvars[191] == 0:
        myvars[191] = 1        # enable debug commands
        print("Debugging commands are on.  Same commmand turns them off.")
    elif myvars[191] == 1:
        myvars[191] = 0        # disable debug commands
        print("No longer cheating, debug commands are off.")
    return myvars          
#
# climb beanstalk
#
def climb(mylist,mysent,myvars):
    if myvars[0] == 92:        # in bottom of west pit?
        if myvars[168] == 2:   # beanstalk full grown?
            myvars[0] = 93     # climb up to E/W narrow corridor
        elif myvars[168] == 1: # 12 foot beanstalk?
            myvars[0] = 90     # climb up to western Two Pit room
        elif myvars[168] == 0: # still a tiny plant?
            print("You cannot climb a tiny plant!")
    else:
        print("Nothing to climb here.")
    return myvars    
#
# move forward by room number
#
def forward(mylist,mysent,myvars):
    if myvars[191] == 1:          # debug command enabled?
        if myvars[0] < 125:
            myvars[0] += 1
    else:
        print("Cheat?")
    return myvars
#
# move backward by room number
#
def back(mylist,mysent,myvars):
    if myvars[191] == 1:          # debug command enabled?
        if myvars[0] > 0:
            myvars[0] -= 1
    else:
        print("Cheat?")
    return myvars         
#
# free bear
#
def freee(mylist,mysent,myvars):
    if myvars[129] == "bear" and myvars[0] == 70:
        myvars = unlock(mylist,mysent,myvars)
    else:
        print("That is not free.")
    return myvars
#
# unlock command for bear, chain, door
#
def unlock(mylist,mysent,myvars):
    if myvars[130] == 126:               # player has keys?
        if myvars[129] == "door":
            if myvars[0] == 96:          # in room 96?
                mysentence(mysent[371])  # door needs oil to open
            else:
                print("I do not see a door here.")  # no door to open here
        elif myvars[129] == "grate" or myvars[128] == "grate":
            if int(myvars[0]) == 8 or int(myvars[0]) == 9:  # grate location
                if myvars[127] == 0:
                    myvars[127] = 1          # grate unlocked flag
                else:
                    mysentence(mysent[478])  # I see nothing to unlock here
            else:
                mysentence(mysent[477])     # I see no grate here
        elif myvars[0] == 70 and (myvars[129] == "bear" or myvars[129] == "chain"):
            if myvars[177] == 2:
                myvars[151] = 70            # bear in room, now following
                myvars[143] = 70            # gold chain now in room 70
                myvars[177] = 3             # bear flag = unchained
                mysentence(mysent[486])     # bear unchained
            elif myvars[177] == 3:
                print("The",myvars[129],"is already unlocked.")
            else:
                if myvars[177] < 2:
                    print("Unlock a hungry bear that sees you as food?")
        elif myvars[0] == 70 and (myvars[129] == "chain" or myvars[129] == "bear"):
            print("I see no", str(myvars[129]), "here.")
        else:
            print("Is something locked?")     # no unlockable object cited     
    else:
        mysentence(mysent[353])              # no keys 
    return myvars
#
# lock command  needs test for grate, bear, chain and keys
#
def lock(mylist,mysent,myvars):
    if myvars[129] == "grate":
        if int(myvars[0]) == 8 or int(myvars[0]) == 9:  # grate location
            if myvars[127] == 1:
                myvars[127] = 0          # grate locked flag
            else:
                mysentence(mysent[300])  # Nothing happens
        else:
            mysentence(mysent[477])      # I see no grate here
    elif myvars[129] == "bear":
        print("The bear becomes ferocious when locked up.")
    else:
        mysentence(mysent[300])         # Huh?
    return myvars
#
# magic pit
#
def pit(mylist,mysent,myvars):
    if myvars[0] == 10:
        myvars[0] = 14              # go to top of pit
    else:
        mysentence(mysent[300])     # Nothing happens
    return myvars
#
# magic bedquilt
#
def bedquilt(mylist,mysent,myvars):
    if myvars[0] == 50:             # in Dirty Broken Passage?
        myvars[0] = 60              # go to Bedquilt
    else:
        mysentence(mysent[300])     # Nothing happens
    return myvars
#
# magic slab room
#
def slab(mylist,mysent,myvars):
    if myvars[0] == 60:             # in Bedquilt?
        myvars[0] = 88              # go to Slab Room
    else:
        mysentence(mysent[300])     # Nothing happens
    return myvars
#
# magic N/S Canyon
#
def canyon(mylist,mysent,myvars):
    if myvars[0] == 44:             # in N/S Canyon?
        myvars[0] = 47              # go to Reservoir
    else:
        mysentence(mysent[300])     # Nothing happens
    return myvars
#
# magic with xyzzy
#
def xyzzy(mylist,mysent,myvars):
    if int(myvars[0]) == 1:          # magic room
        myvars[0] = 11
    elif int(myvars[0]) == 11:       # magic room
        myvars[0] = 1
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# magic with downstream
#
def downstream(mylist,mysent,myvars):
    if int(myvars[0]) < 8:           # only works above ground
        myvars[0] = 8
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# magic with y2
#
def y2(mylist,mysent,myvars):
    if myvars[0] == 1:               # magic room
        myvars[0] = 36
    elif myvars[0] == 36:            # magic room
        myvars[0] = 1
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# plugh please lift up gold here or jump between Y2 and building
#
def plugh(mylist,mysent,myvars):
    if myvars[0] == 18 and int(myvars[154]) == 18:
        myvars[154] = 15         # move the gold
        myvars[173] = 1          # flag for plugh puzzle scoring
        mysentence(mysent[412])  # gold went north
    elif myvars[0] == 36:        # in room Y2?
        myvars[0] = 1            # then back to building
    elif myvars[0] == 1:         # in building?
        myvars[0] = 36           # then out to room Y2
    else:
        mysentence(mysent[300])  # Nothing happens
    return myvars            
#
# magic with building except when lost in forest or underground
#
def building(mylist,mysent,myvars):
    if int(myvars[0]) <= 9 and int(myvars[0]) != 4:
        myvars[0] = 1
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# magic with grate except when lost in forest or underground
#
def grate(mylist,mysent,myvars):
    if myvars[129] == "open" or myvars[129] == "unlock":
           myvars = unlock(mylist,mysent,myvars)
           return myvars          
    if int(myvars[0]) <= 9 and int(myvars[0]) != 4:
        myvars[0] = 8
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# magic with plover
#
def plover(mylist,mysent,myvars):
    if myvars[146] == 126:          # player has emerald?
        if myvars[0] == 36:         # in room y2?
            myvars[0] = 83          # go to plover room
        elif myvars[0] == 83:       # in plover room
            myvars[0] = 36          # go to y2
        else:
            mysentence(mysent[300]) # nothing happens
    else:
        mysentence(mysent[300])     # nothing happens
    return myvars
#
# exit building
#
def exitt(mylist,mysent,myvars):
    if int(myvars[0]) == 1:
        myvars[0] = 0
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# enter building
#
def enter(mylist,mysent,myvars):
    if int(myvars[0]) == 0:
        myvars[0] = 1
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# open cage, door, grate, clam
#
def openn(mylist,mysent,myvars):
    if myvars[129] == "cage":
        myvars = drop(mylist,mysent,myvars)
    elif myvars[129] == "grate":
        myvars = unlock(mylist,mysent,myvars)
    elif myvars[129] == "clam" or myvars[129] == "shell":  
        if myvars[0] == 54:                 # in room 54?
            if myvars[153] == 126:          # have trident?
                if myvars[145] == 130:      # clam has pearl?
                    myvars[145] = 57        # pearl appears in room 57
                    myvars[174] = 1         # shell opened
                    mysentence(mysent[406]) # pearl rolls away
                else:
                    mysentence(mysent[407]) # no pearl in shell
            else:
                mysentence(mysent[263])     # need the trident
        else:
            mysentence(mysent[405])         # nothing here to open
    elif myvars[129] == "noword":
        print("Open what?")
    elif myvars[129] == "door":
        if myvars[0] == 96:                 # in room 96?
            if myvars[141] == 126:          # player has oil?
                myvars[169] = 1             # door open
                mysentence(mysent[317])     # door is now open
            else:
                mysentence(mysent[371])     # door needs oil to open
        else:
            print("I see no door here.")
    else:
        mysentence(mysent[405])             # nothing here to open
    return myvars
#
# go run walk
#
def gowhere(mylist,mysent,myvars):
    mysentence(mysent[482])          # go where?
    return myvars
#
# detect a keystroke to interrupt forest door
# Returns True if a keypress is waiting to be read in stdin, False otherwise.
# code runs on Linux, Windows support ripped out https://stackoverflow.com/questions/292095/polling-the-keyboard-detect-a-keypress-in-python
#
def kbhit():
    dr,dw,de = select.select([sys.stdin], [], [], 0)
    return dr != []
#
# forest only works above ground
# forest door is a test script for moves and actions
# when [126]="zzz" = not a directional move
#
def forest(mylist,mysent,myvars):
    if myvars[129] == "door":
        print("#" * 55)
        z = input("Start Cave Testing. Hit Enter/Return to start or stop.")
        myvars[0] = 0  # must start in room 0
        mypath = ['e', 'getone', 'lampon', 'w', 'w', 'w', 's', 'e', 'e', 's', 's', \
                   'grate', 'comment1', 'd', 'w', 'cage', 'w', 'rod', 'w', 'w', 'rodd', 'bird', \
                   'rod', 'w', 's', 's', 'plugh', 'n', 'gold', 'w', 'wave', 'w', 'diamonds', \
                   'w', 'w', 'n', 'n', 's', 's', 's', 's','s', 's', 's', 's', 's', 's', \
                   'sw', 'se', 's', 'n', 'n', 'ne', 'se', 'n', 'n', 's', 'e', 'coins', \
                   'e', 'birdd', 's', 'jewelry', 'n', 'n', 'silver', 'n', 'w', 'e', 'e', \
                   'd', 'plugh', 'diamondsd', 'goldd', 'silverd', 'coinsd', 'jewelryd', 'rodd', 'comment2', \
                   'plugh', 's', 's', 'sw', 'w', 'dragon', 'rug', 'n', 'n', 'n', 'bottlef', \
                   's', 's', 'd', 's', 'd', 'waterp', 'u', 'w', 'u', 'n', 'n', 'bottlef', \
                   's', 's', 'd', 's', 'd', 'waterp', 'u', 'e', 'd', 'oil', 'u', 'e', 's', \
                   'w', 's','e','s','n','n','n', 'e', 'pillow', 'w', 'w', 'w', 'u', 'w', \
                   'eggs', 'e', 's', 'n', 'door', 'n', 'trident', 'w','d','n','s','se','vase', \
                   'u','w','nw','s','se','ne','nw','n','n','w','s','s','n','d','e','u','e','u','n', \
                   'plugh','pillowd','vased','rugd','eggsd', 'comment3','xyzzy','w','w','w','d','w','w','w','s', \
                   'w', 'e', 'w', 'n', 'e', 'e', 's', 'e', 'e', 'w', 'd', 'd', 'n', 's', 'n', 's', 'd', 'u', 's', 'w', \
                   'w', 's', 's', 'w', 'n', 'd', 'u', 'n', 'e', 's', 'e', 'n', 'w', 'e', 'e', 'n', \
                   'd', 'w', 'd', 'd', 'n', 'd', 'e', 'd', 'u', 'w', 'w', 'd', 'e', 'magazine', 'u', \
                   'n', 'u', 'd', 'clam', 'd', 'd', 'pearl', 'u', 'u', 's', 'u', 'e', 'u', 'n', 'plugh','tridentd','pearld','comment4', \
                   'eggs', 'plugh', 's', 'd', 'w', 'd', 'w', 'w', 'nw', 'w', 'sw', 'u', 'eggst', 'cross', 'ne', 'e', 'ne', 'n', 's', 'e', \
                   'spices', 'w', 's', 'se', 'e', 'e', 'feed', 'chainu', 'chain', 'w', 'w', 'n', 'w', 'w', 'beard', 'cross', 'd', 'e', 'se', 'se', \
                   'ne', 'e', 'u', 'e', 'u', 'n',  'magazined', 'plugh', 'chaind', 'spicesd', 'comment5', 'keysd', 'bottled', 'caged', 'oild', \
                   'magazined', 'plugh', 'magazined','s', 'magazined', 'd', 'magazined', 'w', 'magazined', 'd', 'magazined', 'w', 'magazined', \
                   'w', 'magazined', 'nw', 'magazined', 'u', 'magazined', 'w', 'magazined', 'lampd', 'e', 'emerald', 'w', 'lamp', 'nw', 's', \
                   'se', 'ne', 'e', 'u', 'e', 'u', 'n', 'plover', 'lampoff', 'n', 'pyramid', 's', 'lampon', 'w', 'nw', 's', 'se', 'w', 'w', 'u', 'w', \
                   'fee', 'fie', 'foe', 'foo', 'eggs', 's', 'd', 'e', 'e', 'ne', 'e', 'u', 'e', 'u', 'n', 'plugh','emeraldd','pyramidd','eggsd','magazined', \
                   'comment6', 'rod', 'plugh', 's', 'd', 'w', 'd', 'e', 'e', 'magazined', 'lampoff', 'sw', 'rodd', 'ne']
#
        mycmds = {"e":"east","w":"west","n":"north","s":"south","ne":"northeast","nw":"northwest","se":"southeast","sw":"southwest", "chainu":"unlock chain", "emeraldd": "drop emerald", \
                  "u":"up","d":"down","getone":"get keys, lamp, food, bottle","xyzzy":"xyzzy","lampon":"lamp on","cage":"take cage","caged":"drop cage", "chaind":"drop chain", \
                  "pit":"go to pit","bird":"get bird","birdd":"drop bird","dragon":"kill dragon","unlock":"unlock grate","door":"open door", "feed":"feed bear", "magazined":"drop a magic magazine", \
                  "plugh":"magic word plugh","wave":"wave rod","waterp":"water plant","bottlef":"fill bottle","grate":"unlock grate", "clam": "open shell", "spicesd":"drop spices", \
                  "rod":"take rod","bird":"take bird","oil":"take oil","rug":"take rug", "vase":"take vase", "pillow":"take pillow", "pearl":"take pearl", "lampd":"drop lamp", "lamp":"take lamp", "lampoff":"lamp off", \
                  "gold":"take gold","jewelry":"take jewelry","diamonds":"take diamonds","coins":"take coins","pyramid":"take pyramid","silver":"take silver", \
                  "eggs":"take eggs","trident":"take trident","oild":"oil for door", "magazine": "take magazine, no subscription required", "pearld":"drop pearl", \
                  "goldd":"drop gold","jewelryd":"drop jewelry","coinsd":"drop coins","pyramidd":"drop pyramid","diamondsd":"drop diamonds", "spices": "take spices", \
                  "silverd":"drop silver bars","rodd":"drop rod",'pillowd':"drop pillow",'vased':"drop vase on pillow",'rugd':"drop rug",'eggsd':"drop eggs", \
                  "tridentd":"drop trident","comment1": "First cave excursion.","comment2": "Second cave excursion.","comment3": "Third cave excursion.", "chain":"take chain", \
                  "comment4": "Fourth cave excursion", "emerald": "take emerald","plover":"plover","cross":"cross bridge","eggst":"throw eggs", "spicesd": "drop spices", \
                  "beard":"drop bear", "comment5": "Fifth cave excursion", "fee":"fee","fie":"fie","foe":"foe","foo":"foo","keysd":"drop keys","bottled":"drop bottle", \
                  "comment6": "Endgame cave excursion"}
#
        takes = ["gold","jewelry","diamonds","coins","pyramid","silver","eggs","trident","vase","emerald", \
                 "rod", "bird", "oil", "rug", "pillow", "magazine", "pearl", "spices", "chain", "lamp"]
#
        drops = ["goldd", "jewelryd", "coinsd", "pyramidd", "diamondsd", "silverd", "rodd", "chaind", "bottled", "oild", "magazined", \
                 "pillowd", "vased", "rugd", "eggsd", "tridentd", "pearld", "spicesd", "beard", "keysd", "lampd", "emeraldd"]
#
        test = 0   # displayed test numbers
        for testit in mypath:
            print("\ntest number",str(test),"command=",mycmds[testit])  # count and show test number
# handle moves
            moves = ["e","w","n","s","ne","nw","se","sw","u","d"]
            if testit in moves:
                myvars[126] = testit
                myvars[128] = testit
                myvars[129] = "noword"
                myvars = playmove(mylist,mysent,myvars)
                myvars = announce_room(mysent,myvars)
# handle commands  myvars = mycmd(mylist,mysent,myvars)
            else:
                if testit == "getone":
                    myvars[130] = 126 # keys
                    myvars[131] = 126 # lamp
                    myvars[132] = 126 # food
                    myvars[133] = 126 # bottle
                    myvars = inven(mylist,mysent,myvars)
                elif testit == "xyzzy":
                    myvars[126] = "zzz"
                    myvars[128] = testit
                    myvars[129] = "noword"
                    myvars = xyzzy(mylist,mysent,myvars)
                    print("xyzzy to room 11")
                elif testit == "lampon":
                    myvars[126] = "zzz"
                    myvars[128] = "on"
                    myvars[129] = "lamp"
                    myvars = lampon(mylist,mysent,myvars)
                elif testit == "lampoff":
                    myvars[126] = "zzz"
                    myvars[128] = "off"
                    myvars[129] = "lamp"
                    myvars = lampoff(mylist,mysent,myvars)
                elif testit == "cage":
                    myvars[126] = "zzz"
                    myvars[128] = "take"
                    myvars[129] = "cage"
                    myvars = take(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)
                elif testit == "caged":
                    myvars[126] = "zzz"
                    myvars[128] = "drop"
                    myvars[129] = "cage"
                    myvars = drop(mylist,mysent,myvars)
                elif testit == "pit":
                    myvars[126] = "zzz"
                    myvars[128] = testit
                    myvars[129] = "noword"
                    myvars = pit(mylist,mysent,myvars)
                elif testit == "bird":
                    myvars[126] = "zzz"
                    myvars[128] = "take"
                    myvars[129] = testit
                    myvars = take(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)
                elif testit == "birdd":
                    myvars[126] = "zzz"
                    myvars[128] = "drop"
                    myvars[129] = "bird"
                    myvars = drop(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)
                elif testit == "dragon":
                    myvars[166] = 1
                    print("The dragon is now dead.")
                elif testit == "unlock":
                    myvars[126] = "zzz"
                    myvars[128] = testit
                    myvars[129] = "noword"
                    myvars = unlock(mylist,mysent,myvars)
                elif testit == "grate":
                    myvars[126] = "zzz"
                    myvars[128] = "unlock"
                    myvars[129] = testit
                    myvars = unlock(mylist,mysent,myvars)
                elif testit == "door" or testit == "clam":
                    myvars[126] = "zzz"
                    myvars[128] = "open"
                    myvars[129] = testit
                    myvars = openn(mylist,mysent,myvars)                    
                elif testit == "plugh":
                    myvars = plugh(mylist,mysent,myvars)
                    if myvars[0] == 1 :           # back to building?
                        print("Poof! At Building now.")
                    if myvars[0] == 36:           # back to Y2?
                        print("Poof! At Y2 now.")
                elif testit == "plover":
                    myvars = plover(mylist,mysent,myvars)
                    if myvars[0] == 83 :          # in Plover Room?
                        print("Poof! In Plover Room now.")
                    if myvars[0] == 36:           # back to Y2?
                        print("Poof! At Y2 now.")
                elif testit == "wave":
                    myvars[126] = "zzz"
                    myvars[128] = testit
                    myvars[129] = "rod"
                    myvars = wave(mylist,mysent,myvars)                    
                elif testit == "waterp":
                    myvars[126] = "zzz"
                    myvars[128] = "water"
                    myvars[129] = "plant"
                    myvars = pour(mylist,mysent,myvars)
                elif testit == "bottlef":
                    myvars[126] = "zzz"
                    myvars[128] = "fill"
                    myvars[129] = "bottle"
                    myvars = fillbottle(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)                    
                elif testit == "cross":
                    myvars[126] = "zzz"
                    myvars[128] = "cross"
                    myvars[129] = "bridge"
                    myvars = cross(mylist,mysent,myvars)
                elif testit == "eggst":
                    myvars[126] = "zzz"
                    myvars[128] = "throw"
                    myvars[129] = "eggs"
                    myvars = throw(mylist,mysent,myvars)
                elif testit == "feed":
                    myvars[126] = "zzz"
                    myvars[128] = "feed"
                    myvars[129] = "bear"
                    myvars = feed(mylist,mysent,myvars)
                elif testit == "chainu":
                    myvars[126] = "zzz"
                    myvars[128] = "unlock"
                    myvars[129] = "chain"
                    myvars = unlock(mylist,mysent,myvars)
                elif testit in takes:
                    myvars[126] = "zzz"
                    myvars[128] = "take"
                    myvars[129] = testit
                    myvars = take(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)                         
                elif testit in drops:
                    myvars[126] = "zzz"
                    myvars[128] = "drop"
                    myvars[129] = testit[:-1]
                    myvars = drop(mylist,mysent,myvars)
                    myvars = inven(mylist,mysent,myvars)
                elif testit == "fee" or testit == "fie" or testit == "foe" or testit == "foo":
                    myvars[126] = "zzz"
                    myvars[128] = testit
                    myvars[129] = "zzz"
                    myvars = feefiefoefoo(mylist,mysent,myvars)
            test += 1
#            if True == kbhit():
#                break
            myvars[170] = 0    # suppress pirate while testing
#            time.sleep(2)
        print("Cave Test Complete.")
        print("#" * 55)
        return myvars              
#
# forest takes player to forest if above ground
#
    if myvars[0] <= 9:
        myvars[0] = 4
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# three commands that share the maps information
# -room       show moves from current room
# -showrooms  show rooms not yet visited
# -map        show cave map
#  three boxes per row, each box is 26 spaces inside
#  append third field of data using getmoves and room command
#
def mapp(mylist,mysent,myvars):
    if myvars[129] == "enable":
        myvars[193] = 1   # automatically show a map with each turn
        print("ok")
        return myvars
    if myvars[129] == "disable":
        myvars[193] = 0    # turn off automatic map display
        print("ok")
        return myvars
    room = myvars[0]
    map1 = [["2","End of Road"],["0","Outside Building"],["1","Inside Building"]]
    map2 = [["4","Forest near Road"],["5","Open Forest"],["3","Hill in Road"]]
    map3 = [["6","Valley"],["7","Slit in Streambed"],["8","Outside Grate"]]
    map4 = [["11","Debris Room"],["10","Cobble Crawl"],["9","Below Grate"]]
    map5 = [["14","Top of Small Pit"],["13","Bird Chamber"],["12","Sloping Canyon"]]
    map6 = [["17","Fissure West Bank"],["16","Fissure East Bank"],["15","Hall of Mists"]]
    map7 = [["18","Gold Nugget Room"],["19","Hall of Mists West"],["20","Long Hall East"]]
    map8 = [["21","dead end"],["22","Crossover"],["23","Long Hall West"]]
    map9 = [["24","all different maze"],["25","all different maze"],["26","all different maze"]]
    map10 = [["27","all different maze"],["28","all different maze"],["29","all different maze"]]
    map11 = [["30","all different maze"],["31","all different maze"],["32","all different maze"]]
    map12 = [["33","all different maze"],["34","Vending Machine"],["35","Jumble of Rocks"]]
    map13 = [["36","Y2"],["37","Window on Pit right"],["38","Window on Pit left"]]
    map14 = [["39","Low N/S Passage"],["40","Hall of Mtn King"],["41","West Side Chamber"]]
    map15 = [["42","South Side Chamber"],["43","Secret E/W Canyon"],["44","Secret N/S Canyon"]]
    map16 = [["45","Mirror Canyon"],["46","Secret N/E Canyon"],["47","Reservoir"]]
    map17 = [["48","Pirate Lair"],["49","Dusty Rock room"],["50","Dirty Passage"]]
    map18 = [["51","Top of Pit"],["52","Pit near Stream"],["53","Complex Junction"]]
    map19 = [["54","Shell Room"],["55","Arched Hall"],["56","Sloping Corridor"]]
    map20 = [["57","Cul-De-Sac"],["58","Anteroom"],["59","Witt's End"]]
    map21 = [["60","Bedquilt"],["61","Large Low Room"],["62","dead end crawl"]]
    map22 = [["63","Winding Corridor"],["64","SW Side of Chasm"],["65","NE Side of Chasm"]]
    map23 = [["66","Long E/W Corridor"],["67","Fork in Path"],["68","Limestone Passage"]]
    map24 = [["69","Barren Entrance"],["70","Barren room"],["71","Warm Walls Junction"]]
    map25 = [["72","Chamber of Boulders"],["73","Breath Taking View"],["74","Oriental Room"]]
    map26 = [["75","Swiss Cheese room"],["76","Soft Room"],["77","Tall E/W Canyon"]]
    map27 = [["78","dead end"],["79","Tight N/S Canyon"],["80","Too tight here"]]
    map28 = [["81","Large Misty cavern"],["82","Alcove"],["83","Plover Room"]]
    map29 = [["84","Dark room"],["85","Secret N/S Canyon"],["86","Three Secret Canyons"]]
    map30 = [["87","Stalactite Room"],["88","Slab Room"],["89","Two Pit Room east"]]
    map31 = [["90","Two Pit Room west"],["91","East Pit"],["92","West Pit"]]
    map32 = [["93","Narrow Corridor"],["94","Giant Room"],["95","dead end"]]
    map33 = [["96","Immense Passage"],["97","Magnificent Cavern"],["98","Steep Incline"]]
    map34 = [["99","all alike maze"],["100","all alike maze"],["101","all alike maze"]]
    map35 = [["102","all alike maze"],["103","all alike maze"],["104","all alike maze"]]
    map36 = [["105","all alike maze"],["106","all alike maze"],["107","all alike maze"]]
    map37 = [["108","all alike maze"],["109","all alike maze"],["110","all alike maze"]]
    map38 = [["111","dead end"],["112","dead end"],["113","dead end"]]
    map39 = [["114","dead end"],["115","dead end"],["116","dead end"]]
    map40 = [["117","dead end"],["118","dead end"],["119","Brink of Pit"]]
    map41 = [["120","dead end","e 121"],["121","all alike maze"],["122","all alike maze"]]
    map42 = [["123","Repository NE"],["124","Repository SW"],["125","Game Over"]]
    maps = [map1,map2,map3,map4,map5,map6,map7,map8,map9,map10,map11,map12,map13,map14, \
            map15,map16,map17,map18,map19,map20,map21,map22,map23,map24,map25,map26,map27,map28, \
            map29,map30,map31,map32,map33,map34,map35,map36,map37,map38,map39,map40,map41,map42]
    moves1 = []
    moves2 = []
    moves3 = []
#
# show the moves from the current room not blocked by magic
#
    if myvars[128] == "room":      # this is the room command?
        msn = myvars[0]
        print("Moves=",end="")
        movewords = ['east','west','south','north','ne','nw','se','sw','up','down']
        for mydirection in movewords:
            move_result = moves(mydirection,msn)
            if msn != int(move_result):
                z = 0
                room_name = "room name error."
                while z < 42:
                    zz = 0
                    while zz < 3:
                        if int(maps[z][zz][0]) == int(move_result):
                            room_name = maps[z][zz][1] + chr(32)
                            break
                        zz += 1
                    z += 1
                print(mydirection.capitalize()+" to "+ room_name,end="")
        print("")
        return myvars
#
# show the rooms not yet visited, room 0-124 myvars[1-125]
#
    if myvars[128] == "showrooms":
        if myvars[191] == 1:         # debug command enabled?
            print("List of rooms not yet visited.")
            print("-" * 30)
            r = 0
            while r < 125:           # scan all rooms for visits
                if myvars[r+1] == 0: # is this room unvisited?
                    found_flag = 0   # look for room name, quit when found
                    z = 0
                    room_name = "room name error."
                    while z < 42:
                        zz = 0
                        while zz < 3:
                            if int(maps[z][zz][0]) == int(r): # this entry = room number?
                                room_name = maps[z][zz][1]
                                found_flag = 1
                                break
                            zz += 1
                            if found_flag == 1:
                                break
                        z += 1
                        if found_flag == 1:
                            break
                    print("room"+str(r)+room_name)
                r += 1
        else:
            print("Cheat?")           # no command if not debugging
        return myvars            
#
# display all map rows with three columns of rooms on each line
#
    print(chr(45) * 82)        # top line of table
    if myvars[129] == "all":
        for myline in maps:
            moves1a = get_moves(myvars,myline[0][0])
            moves1 = ','.join(moves1a)
            moves2a = get_moves(myvars,myline[1][0])
            moves2 = ','.join(moves2a)
            moves3a = get_moves(myvars,myline[2][0])            
            moves3 = ','.join(moves3a)            
            mappp(myline,moves1,moves2,moves3,room)
#
# display first three rows of table with three rooms on each line
# based on current player location
#
    elif myvars[0] < 3:
        maplist = [maps[0],maps[1],maps[2]]
        for myline in maplist:
            moves1a = get_moves(myvars,myline[0][0])
            moves1 = ','.join(moves1a)
            moves2a = get_moves(myvars,myline[1][0])
            moves2 = ','.join(moves2a)
            moves3a = get_moves(myvars,myline[2][0])            
            moves3 = ','.join(moves3a)            
            mappp(myline,moves1,moves2,moves3,room)
#
# display three rows in the middle of the table with three rooms on each line
# based on current player location
#
    elif myvars[0] >= 3:
        x = int(myvars[0]/3)
        if x > 40:         # bottom of map table limit switch
            x = 40         # show last three map rows 40,41,42
        maplist = [maps[x-1],maps[x],maps[x+1]]
        for myline in maplist:
            moves1a = get_moves(myvars,myline[0][0])
            moves1 = ','.join(moves1a)
            moves2a = get_moves(myvars,myline[1][0])
            moves2 = ','.join(moves2a)
            moves3a = get_moves(myvars,myline[2][0])            
            moves3 = ','.join(moves3a)            
            mappp(myline,moves1,moves2,moves3,room)
    return myvars
#
# display three table columns for three table rows
# current map line chars  chr(124) = |  chr(32) = (space)  chr(45) = hyphen
# uses data from moves function
# future- create three row entries if there are too many items
#
def mappp(mapx,moves1,moves2,moves3,room):
    s1 = 22 - (len(mapx[0][0]) + len(mapx[0][1]))
    s2 = 22 - (len(mapx[1][0]) + len(mapx[1][1]))
    s3 = 22 - (len(mapx[2][0]) + len(mapx[2][1]))
    s4 = 25 - len(moves1)    # padding space count, column 1
    s5 = 25 - len(moves2)    # padding space count, column 2
    s6 = 25 - len(moves3)    # padding space count, column 3
#
# highlight current room with # around the box
#
    if int(mapx[0][0]) == room:
        md = [chr(42),chr(42),chr(124),chr(124),chr(42),chr(42),chr(124),chr(124)]
    elif int(mapx[1][0]) == room:
        md = [chr(124),chr(42),chr(42),chr(124),chr(124),chr(42),chr(42),chr(124)]
    elif int(mapx[2][0]) == room:
        md = [chr(124),chr(124),chr(42),chr(42),chr(124),chr(124),chr(42),chr(42)]
    else:
        md = [chr(124),chr(124),chr(124),chr(124),chr(124),chr(124),chr(124),chr(124)]
    print(md[0],str(mapx[0][0]),mapx[0][1],(chr(32)*s1),md[1],str(mapx[1][0]),mapx[1][1],(chr(32)*s2),md[2],str(mapx[2][0]),mapx[2][1],(chr(32)*s3),md[3])
#
# when list of moves fits in one line, s4,s5,s6 are correct
#
    if s4 >= 0 and s5 >= 0 and s6 >= 0:  
        print(md[4],moves1+(chr(32)*s4)+md[5],moves2+(chr(32)*s5)+md[6],moves3+(chr(32)*s6)+md[7])
#
# list is too long, bust move list into two rows and recalc pad space counts
# t1,t3,t5 = end of first row, always a comma
# t2,t4,t6 = beginning of second row
# s4,s5,s6 = pad character (space) counts for first row, three columns
# s7,s8,s9 = pad character (space) counts for second row, three columns
#
    else:               
        t1,t2,s4,s7 = findcomma5(moves1) # moves1[0:t1] moves1[t2:] 
        t3,t4,s5,s8 = findcomma5(moves2) # row 1 pad1=s4,s5,s6
        t5,t6,s6,s9 = findcomma5(moves3) # row 2 pad2=s7,s8,s9
        print(md[4],moves1[0:t1]+(chr(32)*s4)+md[5],moves2[0:t3]+(chr(32)*s5)+md[6],moves3[0:t5]+(chr(32)*s6)+md[7])
        print(md[4],moves1[t2:]+(chr(32)*s7)+md[5],moves2[t4:]+(chr(32)*s8)+md[6],moves3[t6:]+(chr(32)*s9)+md[7])    
    if int(mapx[0][0]) == room:
        print((chr(42)*28)+(chr(45)*54))
    elif int(mapx[1][0]) == room:
        print((chr(45)*27)+(chr(42)*28)+(chr(45)*27))
    elif int(mapx[2][0]) == room:
        print((chr(45)*54)+(chr(42)*28))
    else:
        print(chr(45) * 82)                 # default table row divider
    return
#
# in the long lists, always break after the 4th comma
# t1= end of #1, t2= start of #2, s1= #1 padded spaces s2= #2 padded spaces
#
def findcomma5(movesx):
    x = 0
    c = 0
    while x < len(movesx):
        if movesx[x] == chr(44):
            c += 1
            if c >= 5:
                break
        x += 1        
    t1 = x
    t2 = x + 1
    s1 = 25 - x                 # pad for first row of moves in this column
    s2 = 25 -(len(movesx)-t2)   # pad for second row of moves in this column
    if c < 5:                   # not all columns need two rows, handle short lists
        t2 = x
        s2 = 25
    return t1,t2,s1,s2
#
# fetch possible move data for one room
# return in a list, show only single letter directions, table space limited
# 0=player moves 1=map calling moves [192]
#
def get_moves(myvars,room):
        myvars[192] = 1   # disable Witts End cheat display
        move_list = []
        movewords = ['east','west','south','north','ne','nw','se','sw','up','down']
        movedisplay = {'east':'E','west':'W','south':'S','north':'N','ne':'NE','nw':'NW','se':'SE','sw':'SW','up':'U','down':'D'}
        for mydirection in movewords:
            move_result = moves(mydirection,int(room))
            if int(room) != int(move_result):
                mydirectiondisplay = movedisplay.get(mydirection)
                move_list.append(mydirectiondisplay+str(move_result))
        myvars[192] = 0   # re-enable Witts End cheat display
        return move_list      
#
# show all rooms for debugging using mapp command  dead code, not in commands
#
def showallrooms(mylist,mysent,myvars):
    if myvars[191] == 1:          # debug command enabled?
        realroom = myvars[0]
        x = 0
        while x < 126:
            myvars[0] = x
            print("room=",str(x),end="")
            myvars[128] = "room"   # room command buried in mapp command
            mapp(mylist,mysent,myvars)
            x += 1
        myvars[0] = realroom
    else:
        print("Cheat?")           # no command if not debugging
    return myvars      
#
# cross bridge
# 248 A rickety wooden bridge extends across the chasm, vanishing into the mist.  A sign posted on the bridge reads, "STOP! Pay troll!"$
# 249 The wreckage of a bridge (and a dead bear) can be seen at the bottom of the chasm.$
# 250 The charred remains of a wooden bridge can be seen at the bottom of the chasm.$
# 251 A burly troll stands by the bridge and insists you throw him a treasure before you may cross.$
# 252 The troll catches the $
# 253 and scurries away out of sight.$
# 254 The rickety bridge, with you and an 800 pound bear, collapses into the chasm.$
# "Just as you reach the other side, the bridge buckles beneath the weight of the bear, which was still following you around.  You scrabble desperately for support, but as the bridge collapses you stumble back and fall into the chasm."
# look for rickety bridge test in moves
#
def cross(mylist,mysent,myvars):
    if myvars[129] == "bridge":                # crossing a bridge?
        if myvars[0] == 17 or myvars[0] == 16: # next to crystalline bridge?
            if myvars[161] == 1: # bridge visible?
                if myvars[0] == 17:
                    myvars[0] = 16             # cross crystalline bridge
                    mysentence(mysent[356])
                elif myvars[0] == 16:
                    myvars[0] = 17             # cross crystalline bridge
                    mysentence(mysent[356])
                else:
                    mysentence(mysent[300])    # Nothing happens
            else:
                mysentence(mysent[426])        # see no bridge
        elif myvars[0] == 64 or myvars[0] == 65:  # rickety bridge?
            if myvars[165] == 1 and myvars[194] == 0: # toll paid, bridge intact?
                if myvars[0] == 64:            # cross rickety bridge
                     myvars[0] = 65
                elif myvars[0] == 65:          # or cross back
                     myvars[0] = 64
            else:
                if myvars[194] == 0:
                    mysentence(mysent[251])    # troll demands a treasure
                else:
                    mysentence(mysent[426])    # see no bridge
        else:
            mysentence(mysent[300])            # not near bridge, nothing happens
        if myvars[0] == 64 or myvars[0] == 65:  # rickety bridge?
            if myvars[165] == 1 and myvars[177] == 3: # toll paid, bear follows?
                irand = randrange(0, 1)        # expand to 0-3 after testing
                if irand == 0:                 # bear on rickety bridge?
                    print("Just as you reach the other side, the bridge buckles beneath the weight of the bear,")
                    print("which was still following you around.  You scrabble desperately for support, but as")
                    print("the bridge collapses, you stumble back and fall into the chasm.")
                    myvars = death(mylist,mysent,myvars)
                else:
                    mysentence(mysent[249])    # bridge collapsed
    elif myvars[129] == "noword":
        print("Cross what?")
    else:
        mysentence(mysent[300])                # Nothing happens
    return myvars
#
# attack snake, dragon, dwarf, (anything else), (no object)
#
def attack(mylist,mysent,myvars):
    if myvars[129] == "bear" and myvars[151] == myvars[0]:
        print("Not a good idea.")        
    elif myvars[129] == "snake":
        if myvars[0] == 40 and myvars[167] == 0: # in snake room, snake there
            mysentence(mysent[304])              # snake very dangerous
        else:
            mysentence(mysent[411])              # no snake here
    elif myvars[129] == "dragon":
        if myvars[0] == 46:      # dragon in room 46?
            if myvars[166] == 0: # dragon is on the rug?
                print("What, kill the dragon with your bare hands?")
                yn = getch()
                sys.stdout.write(yn)
                if yn == "y":
                    yn = getch()
                    sys.stdout.write(yn)
                    if yn == "e":
                        yn = getch()
                        sys.stdout.write(yn)
                        if yn == "s":
                            sys.stdout.write(chr(32))
                            myvars[166] = 1
                            mysentence(mysent[422])  # dragon vanquished
                        else:
                            mysentence(mysent[421])  # dragon still dangerous
                    else:
                        mysentence(mysent[421])  # dragon still dangerous
                else:
                    mysentence(mysent[421])      # dragon still dangerous
            else:
                mysentence(mysent[420])  # no dragon here
        else:
            mysentence(mysent[420])      # no dragon here
    elif myvars[129] == "dwarf":
        mysentence(mysent[357])  # no dwarf here
    elif myvars[129] == "noword":
        print("What am I hunting?")
    else:
        mysentence(mysent[302])  # nothing to attack
    return myvars
#
# variables  debug show all vars
# first entry = 130 last entry = 189
#
def variables(mylist,mysent,myvars):
    names = ["keys","lamp","food","empty bottle","empty cage","bird nearby","rod", \
             "bird in cage","bottle with water","axe","pillow","oil","coins","gold chain", \
             "magazine","pearl","emerald","vase","rug","pyramid","diamonds","bear", \
             "golden eggs","trident","gold nugget","bars of silver","jewelry","spices", \
             "lamp state","player game turns","fee fie foe foo counter","crystalline bridge visibility", \
             "dwarf location","player is dead if 0","dwarf encounter counter","rickety bridge toll paid", \
             "dragon dead","snake dead","beanstalk growth","rusted door opened","pirate", \
             "cave is closing","pirate random room","plugh puzzle","clam/shell opened","repository entered", \
             "eggs have been recovered","bear state","Spelunker Today January edition", \
             "Spelunker Today February edition","Spelunker Today March edition", \
             "Spelunker Today April edition","Spelunker Today May edition", \
             "Spelunker Today June edition","Spelunker Today July edition", \
             "Spelunker Today August edition","Spelunker Today September edition", \
             "Spelunker Today October edition","Spelunker Today November edition", \
             "Spelunker Today December edition","inventory"]
    x = 0
    while x < len(names):
        print(names[x]," = ",str(myvars[x + 130]))
        x += 1
    print("grate unlocked = ",str(myvars[127]))
    print("debug commands enabled = ",str(myvars[191]))
    print("automatic map display enabled = ",str(myvars[193]))
    print("########################")
    return myvars
#
# words offer some usage help
#
def words(mylist,mysent,myvars):
    if myvars[191] == 1:
        mysentence(mysent[433])
        mypoint = 3
        while mypoint < 60:
            print(mylist[mypoint],end="")
            mypoint += 1
        print("\n")
        mysentence(mysent[434])
        objwords = ['all','axe','bear','blast','bottle','bird','bridge','cage','chain','clam','coins','detonate', \
            'diamonds','door','dragon','dwarf','eggs','emerald','food','fill','gold','grate','help','info','inven','inventory', \
            'jewelry','keys','lamp','lantern','magazine','news','nugget','oil','pearl','pillow','plant','pour','pyramid','rod', \
            'rug','score','shell','silver','snake','spices','trident','vase','water']
        for oneword in objwords:
            print(oneword,end="")
            mypoint += 1
        print("\n")
        print("Magic Words")
        print("bedquilt- Dirty Broken Passage to Bedquilt")
        print("building- Anywhere Above Ground (except forest) to Building")
        print("canyon- Secret N/S Canyon to Tall E/W Canyon")
        print("downstream- Anywhere Above Ground to Stream Above Grate")
        print("enter- Outside Building to Inside Building")
        print("exit- Inside Building to Outside Building")
        print("forest- Anywhere Above Ground to Forest")
        print("grate- Anywhere Above Ground (except forest) to Grate")
        print("pit- Cobble Crawl to Top of Small Pit")
        print("plugh- Building to Room with Y2 (both ways)")
        print("plover- Room with Y2 to Plover Room (both ways)")
        print("slab- Bedquilt Room to Slab Room")
        print("xyzzy- Building to Debris Room (both ways)")
        print("y2- Building to Room with Y2 (both ways)")
        print("")
    else:
        print("Cheat?")   # no command if not debugging
    return myvars
#
# bear activity
#  0= bear chained, dangerous  sent485 room 70 and sent483 once
#  1= bear chained, dangerous  sent485 room 70
#  2= bear chained, fed        sent289 room 70
#  3= bear unchained           sent486 room 70
# 376 The bear is hungry.  Without food, you are the food. The bear remains chained.$
# 376a There is nothing here it wants to eat (except perhaps you).$
# 377 The hungry bear eats your food.$
# 378 The gold chain is released from the bear and is unlocked from the cave wall.$
# 379 You want the food for another purpose.$
# 380 One only feeds a bear when there is a barren room.$
#
def feed(mylist,mysent,myvars):
    if myvars[129] == "bear":        # feeding a bear?
        if myvars[132] == 126:       # have food?
            if myvars[0] == 70:      # in barren room?
                myvars[132] = 130    # consume food
                myvars[177] = 2      # bear now fed
                mysentence(mysent[377]) # announce feeding
                mysentence(mysent[289]) # new bear description
            else:
                mysentence(mysent[380]) # no bear to feed here
        else:
            print("There is nothing here it wants to eat (except perhaps you).")
    else:
        mysentence(mysent[379])         # the food is for the bear only
    return myvars
#
# jump command can be deadly but not in cheat mode used for debugging
#
def jump(mylist,mysent,myvars):
    if myvars[191] == 0:
        if myvars[0] == 16 or myvars[0] == 17:
            if myvars[161] == 0:            # next to fissure with no bridge?
                myvars = death(mylist,mysent,myvars)
        elif myvars[0] == 64 or myvars[0] == 65:
            if myvars[165] == 0:            # next to rickety bridge w/o toll paid?
                myvars = death(mylist,mysent,myvars)
        elif myvars[0] == 73:               # at breathtaking view?
            myvars = death(mylist,mysent,myvars)
        elif myvars[191] == 0:
            print("Nothing happens")
    if myvars[191] == 1:
        if myvars[129].isdigit() and myvars[191] == 1:
            new_room = myvars[129]
            myvars[0] = int(new_room)
        elif myvars[191] == 1:
            new_room = raw_input("new room number ") or 1
            myvars[0] = int(new_room)
    return myvars
#
# death happens for several mistakes, jumps and dark moves in the cave
#
def death(mylist,mysent,myvars):
    falling = [0,1,2,3,4,5,5,5,5,5]
    for fall in falling:
        print(" " * int(fall)+"X")
        time.sleep(0.5)
    print("    XXXXX")
    mysentence(mysent[417])  # falling
    mysentence(mysent[418])  # player breaks it all
    mysentence(mysent[419])  # poof!
    time.sleep(2)
    myvars = myvars_init()  # game starts over
    return myvars    
#
# help for player
#
def helpme(mylist,mysent,myvars):
    mysentence(mysent[348])  # I know of...
    mysentence(mysent[487])  # For mistakes
    print("Commands for more game information: 'info' and 'news’")
    print("\n")
    return myvars 
#
# info about
#
def info(mylist,mysent,myvars):
    info_sents = [489,427,428,429,432]
    for myinfo in info_sents:
        mysentence(mysent[myinfo])
    print("\n")
    return myvars
#
# news
#
def news(mylist,mysent,myvars):
    print("This is a python 3.x based Colossal Cave Adventure.")
    print("It was tested on MacOS 10.15.7 Catalina and Windows 10")
    print("’forest door' runs the automated cave test")
    print("\nSpecial notes in this version:")
    print(" 'load' restores the game state from a game 'save’")
    print(" 'look' shows the current room long description without admonishment")
    print(" 'map' shows the nearby room map moves.")
    print(" 'map enable' displays a map with every move.")
    print(" 'map disable' turns off automatic map display.")
    print(" 'map all' shows moves for all rooms.")
    print(" 'room' lists all possible moves not blocked by magic for the current room")
    print(" 'save' preserves the current game state in a file named 'myadvent.sav’")
    print(" 'jump' might be deadly in some rooms with pits.")
    print("Magazine magic can map the All Alike maze. Get one magazine, drop 12 monthly editions.")
    print("TAB autocompletes (b)uilding, (d)ownstream, (f)orest, (g)rate, (i)nventory, (r)eservoir, (v)ariables, (q)uit")
    print("\n’cheat' enables and disables commands for game design study.")
    print("Enter 'y' to see more about the 'cheat' commands.")
    yn = getch()
    print(yn)
    if yn == chr(121):
        print("\nCommands that are available in 'cheat' mode.")
        print(" 'f' moves forward one room by internal room number.")
        print(" 'b' moves back one room by internal room number")
        print(" 'jump' moves to a specific room number. Jump is dangerous when not in debug mode.")
        print(" 'words' lists all action and object words")
        print(" 'variables' lists most internal game variables")
        print(" 'showrooms' lists all unvisted rooms with room numbers.")
        print("Cheat mode adds these room displays:")
        print("- The internal map room number with every move.")
        print("- Pirate movements when in rooms 50-59.")
        print("- Dwarf movements and attack countdown when in rooms 40-45.")
    print("\n")
    return myvars
#
# lamp on
#
def lampon(mylist,mysent,myvars):
    if myvars[129] != "lamp" and myvars[129] != "lantern":
        mysentence(mysent[352])    # object not lamp
    elif myvars[131] == 126:       # player has lamp?
        myvars[158] = 0            # lamp on flag
        mysentence(mysent[296])    # lamp on message
    else:
        mysentence(mysent[410])    # player lacks lamp
    return myvars
#
# lamp off
#
def lampoff(mylist,mysent,myvars):
    if myvars[129] != "lamp" and myvars[129] != "lantern":
        mysentence(mysent[352])    # object not lamp
    elif myvars[131] == 126:
        myvars[158] = 1            # lamp off flag, 3 to the pit
        mysentence(mysent[297])    # lamp off, darkness warning on
    else:
        mysentence(mysent[410])    # player lacks lamp
    myvars = endgame(mylist,mysent,myvars) # check for endgame
    return myvars
#
# lamp lantern status
#
def light(mylist,mysent,myvars):
    if myvars[131] == 126:           # player has the lamp?
        if myvars[158] == 0:
            mysentence(mysent[296])  # lamp off
        else:
            mysentence(mysent[297])  # lamp on
    else:
        mysentence(mysent[410])      # player does not have lamp
    return myvars        
#
# look  shows full description of current room
#
def look(mylist,mysent,myvars):
    room = myvars[0] + 1
    myvars[room] = 0
    return myvars
#
# wave rod, crystalline bridge appears and vanishes
#
def wave(mylist,mysent,myvars):
    if myvars[129] == "rod":         # waving a rod?
        if myvars[136] == 126:       # got the rod
            if myvars[0] == 17 or myvars[0] == 16: # next to chasm
                if myvars[161] == 0: # bridge not visible
                    myvars[161] = 1  # crystalline bridge appears
                else:
                    myvars[161] = 0  # bridge vanishes
                    mysentence(mysent[399])
            else:
                mysentence(mysent[300]) # not near chasm, nothing happens
        else:
            mysentence(mysent[398])   # need a rod to wave one
    else:
        mysentence(mysent[400])       # wave what?
    return myvars
#
# pour water beanstalk only
#  mysentence(mysent[365]) # furious growth
#  mysentence(mysent[366]) # 12 foot beanstalk room above pit
#  mysentence(mysent[368]) # explosive growth
#  mysentence(mysent[369]) # over watered
#
def pour(mylist,mysent,myvars):
    if myvars[129] == "plants":
        myvars[129] = "plant"
    if myvars[129] == "water" or (myvars[128] == "water" and myvars[129] == "plant"):
        if myvars[138] == 126:    # got bottle with water?
            if myvars[0] == 92:   # in pit with beanstalk?
                myvars[138] = 130 # bottle with water disappears
                myvars[133] = 126 # empty bottle with player
                beans = [365,366,368,369]
                myvars[168] += 1  # beanstalk grows
                mysentence(mysent[beans[myvars[168]]]) # show plant new state
                if myvars[168] == 3: # overwatered?
                    myvars[168] = 0  # beanstalk dead
            else:
                mysentence(mysent[382])  # don't see a plant
        else:
            mysentence(mysent[384])  # no bottle with water
    elif myvars[128] == "water" and myvars[129] != "plant":
        mysentence(mysent[381])      # do not waste water
    else:
        print("I only pour water.")
    return myvars

#
# magic phrase fee fie foe foo for golden eggs recovery in the Giant Room
#
def feefiefoefoo(mylist,mysent,myvars):
    if myvars[128] == "fee" and myvars[160] == 0 and myvars[0] == 94:
        myvars[160] += 1
    elif myvars[128] == "fie" and myvars[160] == 1 and myvars[0] == 94:
        myvars[160] += 1
    elif myvars[128] == "foe" and myvars[160] == 2 and myvars[0] == 94:
        myvars[160] += 1
    elif myvars[128] == "foo" and myvars[160] == 3 and myvars[0] == 94:
        myvars[160] = 0    # reset for further requests
        myvars[176] = 1    # eggs puzzle, eggs recovered
        myvars[152] = 94   # eggs now back in Giant Room
    else:
        mysentence(mysent[300])      # Nothing happens
    return myvars
#
# show what the player is carrying based on myvars[130] through [157]
#
def inven(mylist,mysent,myvars):
    S_Index4 = [321,322,324,325,326,328,327,488,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,435,481]	
    found_something = 0
    my_index = 130
    while my_index < 158:
        if myvars[my_index] == 126:
            if found_something == 0:
                mysentence(mysent[255])  # announce prefix if something found
                found_something = 1      # announce prefix only once
            mysentence(mysent[S_Index4[my_index - 130]])
        my_index += 1
    if found_something == 0:
        mysentence(mysent[256])          # found nothing
    return myvars
#
# take some object from a room in the cave
# objdict shows myvars index to location for an object
#
def take(mylist,mysent,myvars):
    room = myvars[0]
    object_word = myvars[129]
    objdict = {'keys':130,'lamp':131,'food':132,'bottle':133,'cage':134,'bird':135,'rod':136,'birdcage':137,'bottle':138,'axe':139,'pillow':140,'oil':141, \
            'coins':142,'chain':143,'magazine':144,'pearl':145,'emerald':146,'vase':147,'rug':148,'pyramid':149,'diamonds':150,'bear':151,'eggs':152, \
            'trident':153,'gold':154,'silver':155,'jewelry':156,'spices':157,'nugget':154,'lantern':131}
#
# special case take all, need to add more puzzle restrictions
#
    if object_word == "all":
        my_index = 130
        while my_index < 158:
            if room == myvars[my_index]:   # this room has this object
                myvars[my_index] = 126     # this object now held by player
            my_index += 1
        if myvars[135] == 126 and myvars[134] == 126:  # got both cage and bird?
            myvars[134] = 130               # hide the empty cage
            myvars[135] = 130               # hide the cageless bird
            myvars[137] = 126               # show bird in cage
        return myvars
#
# take specific object if it is in the room
#
    block_not_found = 0
    if object_word in objdict:
        if myvars[objdict.get(object_word)] == room:   # object in room?
            my_index = objdict.get(object_word)        # if in room, take it
        else:
            my_index = 158            # object exists but not here
    else:
        my_index = 158                # object does not exist anywhere
#
# items taken only if puzzles are solved
#
# gold
    if int(myvars[0]) == 18 and int(myvars[154]) == 18 and object_word == "gold":
        mysentence(mysent[414])       # gold nugget stuck in room 18
# bird with cage
    elif object_word == "bird":
        if int(myvars[136]) == 126:   # rod held by player
            mysentence(mysent[307])   # bird afraid
            block_not_found = 1       # suppress not found message
        elif int(myvars[134]) != 126: # cage not held by player
            mysentence(mysent[401])   # no cage to hold bird
            block_not_found = 1       # suppress not found message
        else:
            myvars[135] = 130         # hide the free bird
            myvars[134] = 130         # hide the empty cage
            myvars[137] = 126         # show bird in cage
            mysentence(mysent[274])   # bird now in cage
            block_not_found = 1       # suppress not found message
# dragon & rug
    elif object_word == "dragon" and int(myvars[0]) == 46 and myvars[166] == 0:
        mysentence(mysent[421])       # dragon too dangerous to take
        block_not_found = 1            
    elif object_word == "rug":
        if int(myvars[0]) == 46 and myvars[166] == 0:
            mysentence(mysent[421])   # dragon puzzle
            block_not_found = 1
        if int(myvars[0]) == 46 and myvars[166] == 1:
            myvars[my_index] = 126
            print("rug taken.")
            block_not_found = 1
# inventory
    elif object_word == "inven" or object_word == "inventory":
        inven(mylist,mysent,myvars)
        block_not_found = 1        
# water
    elif object_word == "water":
        myvars = fillbottle(mylist,mysent,myvars)
        block_not_found = 1       
# bear
    elif object_word == "bear":
        if myvars[0] == 70:
            if myvars[177] < 2:
                print("A ferocious hungry bear is hard to take.")
            elif myvars[177] == 2:
                mysentence(mysent[483])  # bear is locked with chain
            else:
                print("This bear weighs 800 pounds.  You cannot carry it.")
        else:
            if myvars[151] == room:    # bear in this room?
                print("Not even bearly a good idea.")
            else:
                print("No bear here.")
        block_not_found = 1          
# magic magazines
    elif object_word == "magazine":   # player wants top pickup magic magazine?
        if myvars[144] == 58:
            myvars[144] = 126
            print(object_word, "taken.")           
            return myvars
        else:
            copies = [178,179,180,181,182,183,184,185,186,187,188,189]
            magazines = [1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428]
            for theindex,copy in enumerate(copies):
                if myvars[copy] == room:           # is there a mag here?
                    myvars[copy] = 130             # grab whatever edition
                    print("The"+mylist[magazines[theindex]]+"edition has been taken.")
                    return myvars
            else:
                print("I don't see a magazine here.")
                return myvars
#
# bottle which is confusing with empty and full
#
    elif object_word == "bottle":
        if myvars[133] == room:   # empty bottle in room?
            myvars[133] = 126
            print(object_word, "taken.")           
            return myvars
        elif myvars[138] == room:   # full bottle in room?
            myvars[138] = 126
            print(object_word, "taken.")          
            return myvars
        else:
            print("I do not see a bottle here.")
            return myvars
# everything else
    else:
        if my_index < 158:
            myvars[my_index] = 126
            print(object_word, "taken.")
        else:
            if block_not_found == 0:
                if object_word != "noword":
                    print("I do not see",object_word,"here.")
                else:
                    print("What exactly do you want?")
    return myvars   
#
# drop some object in a room
#
def drop(mylist,mysent,myvars):
    room = int(myvars[0])
    object_word = myvars[129]
    objwords = ['keys','lamp','food','bottle','cage','bird','rod','bird','bottle','axe','pillow','oil', \
            'coins','chain','magazine','pearl','emerald','vase','rug','pyramid','diamonds','bear','eggs', \
            'trident','gold','silver','jewelry','spices','grate','snake','shell','all','plant','dragon','inven', \
            'bridge','nugget','door','dwarf','inventory','lantern']
#
# drop bird in room for snake, if snake gone, bird flies away
#
    if object_word == "bird" and myvars[167] == 0 and myvars[0] == 40:
        if myvars[137] == 126:      # have bird in cage?
            myvars[167] = 1         # snake now gone
            myvars[134] = 126       # empty cage with player
            myvars[135] = 40        # bird nearby
            myvars[137] = 130       # bird in cage hidden
            mysentence(mysent[308]) # bird kills snake
        else:
            mysentence(mysent[402]) # no bird
        return myvars
#
# drop cage with bird in snake room, does not attack snake
#
    if object_word == "cage" and myvars[167] == 0 and myvars[0] == 40:
        if myvars[137] == 126:      # have bird in cage?
            myvars[134] = 40        # empty cage in room
            myvars[135] = 40        # bird nearby
            myvars[137] = 130       # bird in cage hidden
        else:
            print("You do not have a bird in the cage.")
        return myvars            
#
# drop bird in room for dragon
#
    if object_word == "bird" or object_word == "cage":
        if myvars[166] == 0 and myvars[0] == 46:  # if dragon exists in room 46
            if myvars[137] == 126:      # have bird in cage?
                myvars[134] = 126       # empty cage with player
                myvars[135] = 130       # bird disappears
                myvars[137] = 130       # bird in cage hidden
                mysentence(mysent[479]) # bird dies in flames
            else:
                mysentence(mysent[402]) # no bird
#
# prepare to drop bird or cage anywhere else
#
        else:
            if myvars[137] == 126:         # have bird in cage?
                if object_word == "bird":
                    myvars[134] = 126      # leave cage with player
                    myvars[135] = room     # bird dropped
                    myvars[137] = 130      # bird in cage now hidden
                if object_word == "cage": 
                    myvars[134] = room     # cage in room
                    myvars[135] = room     # bird now in room
                    myvars[137] = 130      # bird in cage now hidden
            elif object_word == "cage":    # drop empty cage?
                if myvars[134] == 126:     # have cage, no bird?
                    myvars[134] = room     # empty cage in room
            else:
                print("You don't have a",object_word,"to drop.")
        return myvars      
#
# drop vase not safe without pillow dropped in the room
#
    if object_word == "vase" and myvars[147] == 126: # player has vase?
        if myvars[140] != room:                      # non pillow landing?
            mysentence(mysent[373])                  # vase is smashed
            mysentence(mysent[374])                  # pieces go poof
            myvars[147] = 130                        # vase leaves inventory
            return myvars
#
# drop a bear in some cases
#
    if object_word == "bear":
        if myvars[177] == 3:        # friendly fed bear following player?
            myvars[177] = 0         # not anymore
            myvars[151] = 130       # put bear away
            print("The bear gets the hint and wanders away.")
        else:
            print("One cannot lift an 800 pound bear.")
        return myvars
#
# drop coins in vending machine, otherwise coins hit the floor in later code
#
    if object_word == "coins":
        if myvars[142] == 126:      # player has coins?
            if myvars[0] == 34:     # player with vending machine?
                myvars[142] = 130   # coins disappear into the vending machine
                mysentence(mysent[423]) # dim lamp is shining bright
                return myvars
#
# drop a magazine found in room 58
#
    if object_word == "magazine":                  # player has magic magazines?
        if myvars[144] == 126:
            copies = [178,179,180,181,182,183,184,185,186,187,188,189]
            magazines = [1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428]
            for theindex,copy in enumerate(copies):
                if myvars[copy] == room:           # already have a mag?
                    print("I already see the",mylist[magazines[theindex]],"edition here.")
                    return myvars
                else:
                    if myvars[copy] == 130:            # is this copy available?
                        myvars[copy] = room            # drop next available edition
                        print("The", mylist[magazines[theindex]], "edition has been dropped.")
                        myvars = endgame(mylist,mysent,myvars)  # check for endgame
                        return myvars
            else:
                print("You have dropped all of the magazine copies.")
                return myvars
        else:
            print("You do not have a magazine.")
            return myvars
#
# special case drop all
#
    if object_word == "all":
        my_index = 130
        while my_index < 158:
            if myvars[my_index] == 126:
                myvars[my_index] = room  # now dumped in room
            my_index += 1
        if myvars[137] == room:          # dropped bird in cage?
            myvars[137] = 130
            myvars[134] = room           # split up cage and bird
            myvars[135] = room
        return myvars
#
# lamp and lantern are synonyms
#
    if object_word == "lamp" or object_word == "lantern":
        if myvars[131] == 126:         # does the player have the lamp?
            myvars[131] = room         # drop lantern or lamp
        else:
            print("You do not have a",object_word,"to drop.")
        return myvars
#
# drop specific object if the player has it
#
    my_index = 130
    while my_index < 158:
        if object_word == objwords[my_index - 130] and myvars[my_index] == 126:
            myvars[my_index] = room
            print(object_word, "dropped.")
            break
        else:
            my_index += 1
#
# objword not found, player does not have it
#
    if my_index >= 158:
        if object_word != "noword" and len(object_word) > 1:
            if object_word[-1] == "s":
                plural = "have"
            elif object_word[0] in ('a', 'e', 'i', 'o', 'u'):
                plural = "have an"
            else:
                plural = "have a"
            print("You don't",plural,object_word,"to drop.")
        else:
            print("What exactly do you want to drop?")
    return myvars   
#
# fill bottle with water
#
def fillbottle(mylist,mysent,myvars):
    if myvars[129] == "bottle":
        waterplace = [0,1,6,7,47,52,97]
        if myvars[0] in waterplace:
            if myvars[133] == 126:
                myvars[133] = 130
                myvars[138] = 126
                print("Ok")
            elif myvars[138] == 126:
                print("The bottle already has water!")
            else:
                mysentence(mysent[387])    # player lacks bottle
        else:
            mysentence(mysent[385])        # no water here
    else:
        mysentence(mysent[386])            # bottle only
    return myvars
#
# throw axe, different than drop axe, dwarf is the target
#
def throw(mylist,mysent,myvars):
    room = int(myvars[0])
    object_word = myvars[129]
    if myvars[129] == "axe":        # axe is the action word?
        if myvars[139] == 126:      # player has axe?
            if myvars[162] == room: # dwarf in the same room?
                
                if irand == 0:
                    myvars[164] = 500 # dwarf dead, clear encounter counter
                if irand == 2:
                    mvyars[163] = 0  # player is dead
                else:
                    myvars[129] = room # drop the axe now
            else:
                print("I don't see a dwarf here.")
        else:
            print("You do not have an axe to throw.")
    elif myvars[0] == 64 or myvars[0] == 65:  # at rickety bridge
        if myvars[165] == 0:                  # need to pay toll
            not_held = 0                      # thwart player throwing trash
            treasures = ['coins','chain','pearl','emerald','vase','rug','pyramid', \
                         'diamonds','eggs','trident','gold','silver','jewelry','spices']
            the_index = [142,143,145,146,147,148,149,150,152,153,154,155,156,157]
            for idx, item in enumerate(treasures):
                if item == myvars[129]:          # player throwing a treasure?
                    if myvars[the_index[idx]] == 126: # player has this treasure?
                        myvars[the_index[idx]] = 130  # treasure thrown away
                        myvars[165] = 1          # toll paid
                        print("The troll catches the",treasures[idx],"and scurries away.")
                        not_held = 1
                        break
                    else:
                        print("You do not have that treasure to throw!")
                        not_held = 1
                        break
            if not_held == 0:
                print("The Troll does not accept",myvars[129],"!")
        else:
            myvars = drop(mylist,mysent,myvars)  # troll gone, throw becomes drop
        #    mysentence(mysent[300])
    else:
        myvars = drop(mylist,mysent,myvars)
    return myvars
#
# this list is the game word database
#
def mylist_init():
    mylist =  [' ','f', 'b', 'quit', 'west', 'east', 'north', 'south', 'sw', 'nw', 'se'] + \
    ['ne', 'up', 'down', 'take', 'drop', 'inven', 'look', 'n', 's', 'e'] + \
    ['w', 'u', 'd', 'help', 'inventory', 'building', 'forest', 'enter', 'exit', 'downstream'] + \
    ['xyzzy', 'y2', 'unlock', 'lock', 'score', 'wave', 'get', 'open', 'free', 'on'] + \
    ['off', 'kill', 'attack', 'plugh', 'throw', 'room', 'feed', 'water', 'fee', 'fie'] + \
    ['foe', 'foo', 'fill', 'cross', 'plover', 'info', 'words', 'save', 'load', 'Welcome'] + \
    ['to', 'Adventure!', ' ', 'Would', 'you', 'like', 'instructions?', 'You', 'are', 'standing'] + \
    ['at', 'the', 'end', 'of', 'a', 'road', 'before', 'small', 'brick', 'building.'] + \
    ['Around', 'is', 'forest.', 'A', 'stream', 'flows', 'out', 'and', 'gully.', 'inside'] + \
    ['building,', 'well', 'house', 'for', 'large', 'spring.', 'roads', 'end.', 'The', 'rises'] + \
    ['hill', 'behind', 'you.', 'have', 'walked', 'hill,', 'still', 'in', 'slopes', 'back'] + \
    ['other', 'side', 'hill.', 'There', 'distance.', 'near', 'both', 'valley', 'road.', 'forest,'] + \
    ['with', 'deep', 'one', 'side.', 'beside', 'tumbling', 'along', 'rocky', 'bed.', 'At'] + \
    ['your', 'feet', 'all', 'splashes', 'into', '2-inch', 'slit', 'rock.', 'Downstream', 'stream'] + \
    ['bare', '20-foot', 'depression', 'floored', 'dirt.', 'Set', 'dirt', 'strong', 'steel'] + \
    ['grate', 'mounted', 'concrete.', 'dry', 'leads', 'depression.', 'chamber', 'beneath', '3x3', 'surface.'] + \
    ['low', 'crawl', 'over', 'cobbles', 'inward', 'west.', 'wide', 'passage', 'becomes', 'plugged'] + \
    ['mud', 'debris', 'here,', 'but', 'an', 'awkward', 'canyon', 'upward', 'filled', 'stuff'] + \
    ['washed', 'from', 'path', 'sloping', 'awkwardly', 'east.', 'splendid', 'thirty', 'high.', 'walls'] + \
    ['frozen', 'rivers', 'orange', 'stone.', 'An', 'good', 'sides', 'chamber.', 'bird', 'has'] + \
    ['been', 'nesting', 'here.', 'You are', 'top', 'pit.', 'pit', 'breathing', 'traces', 'white'] + \
    ['mist.', 'ends', 'here', 'except', 'crack', 'leading', 'on.', 'Rough', 'stone', 'steps'] + \
    ['lead', 'vast', 'hall', 'mists', 'stretching', 'forward', 'sight', 'west,', 'wisps', 'mist'] + \
    ['that', 'sway', 'fro', 'almost', 'as', 'if', 'alive.', 'dome', 'above', 'staircase'] + \
    ['runs', 'downward', 'darkness;', 'chill', 'wind', 'blows', 'below.', 'passages', 'south,', 'bank'] + \
    ['fissure.', 'quite', 'thick', 'fissure', 'too', 'jump.', 'Hall', 'Mists.', 'crude', 'note'] + \
    ['wall.', 'says,', '"You', 'will not', 'it', 'steps".', 'continues', 'another', 'goes', 'north.'] + \
    ['To', 'little', '6', 'floor.', 'very', 'long', 'hall,', 'apparently', 'without', 'chambers.'] + \
    ['east,', 'slants', 'up.', 'around', 'two', 'foot', 'hole', 'down.', 'not used', 'crossover', 'high'] + \
    ['N/S', 'E/W', 'one.', 'featureless', 'hall.', 'joins', 'narrow', 'north/south', 'passage.'] + \
    ['maze', 'twisting', 'passages,', 'different.', 'twisty', 'In', 'this', 'enormous', 'vending', 'machine'] + \
    ['not used','not used','not used','not used','not used','not used','not used','not used'] + \
    ['coins', 'not used', '$', 'next', 'not used', 'not used', 'it.', 'jumble', 'rocks,', 'cracks', 'everywhere.', 'room,', 'wall'] + \
    ['broken', 'rock', '"Y2"', 'rooms', 'center.', 'window', 'overlooking', 'huge', 'pit,', 'which'] + \
    ['extends', 'sight.', 'floor', 'indistinctly', 'visible', '50', 'Traces', 'cover', 'becoming', 'thicker'] + \
    ['right.', 'Marks', 'dust', 'would', 'seem', 'indicate', 'someone', 'recently.', 'Directly', 'across'] + \
    ['25', 'away', 'there', 'similar', 'looking', 'lighted', 'room.', 'shadowy', 'figure', 'can'] + \
    ['be', 'seen', 'peering', 'left.', 'Mountain', 'King,', 'directions.', 'King.', 'secret', 'E/W.'] + \
    ['It', 'crosses', 'tight', '15', 'If', 'go', 'may', 'not', 'able', 'about'] + \
    ['across.', 'covered', 'by', 'seeping', 'extend', '100', 'feet.', 'Suspended', 'some', 'unseen'] + \
    ['point', 'far', 'you,', 'two-sided', 'mirror', 'hanging', 'parallel', 'midway', 'between', 'walls.'] + \
    ['(The', 'obviously', 'provided', 'use', 'dwarves,', 'who', 'know,', 'extremely', 'vain).', 'either'] + \
    ['wall,', 'fifty', 'N/E', 'southern', 'edge', 'underground', 'reservoir.', 'cloud', 'fills', 'rising'] + \
    ['surface', 'drifting', 'rapidly', 'upwards.', 'lake', 'fed', 'stream,', 'tumbles', '10', 'overhead'] + \
    ['noisily', 'reservoi', 'northern', 'dimly-seen', 'exits', 'through', 'cannot', 'Another', 'Pirate', 'Lair.'] + \
    ['treasure', 'chest', 'half-hidden', 'rock!', 'full', 'dusty', 'rocks.', 'big', 'everywhere,', 'dirty'] + \
    ['crawl.', 'Above', 'brink', 'clean', 'climbable', 'bottom', 'enters', 'tiny', 'slits.', 'complex'] + \
    ['junction.', 'hands', 'knees', 'higher', 'make', 'walking', 'going', 'also', 'above.', 'air'] + \
    ['damp', 'shell,', 'tightly', 'shut.', 'arched', 'corridor', 'ragged', 'sharp', 'cul-de-sac', 'eight'] + \
    ['anteroom', 'Small', 'remnants', 'recent', 'digging', 'evident.', 'sign', 'midair', 'says', '"Cave'] + \
    ['under', 'construction', 'beyond', 'point.', 'Proceed', 'own', 'risk.', '{Witt', 'Construction', 'Company}.'] + \
    ['Witts', 'End.', 'Passages', '*all*', 'Bedquilt,', 'east/west', 'holes', 'explore', 'random', 'select'] + \
    ['NORTH,', 'SOUTH,', 'UP,', 'or', 'DOWN.', 'Crawls', 'north,', 'SE,', 'SW.', 'dead'] + \
    ['winding', 'large,', 'chasm.', 'heavy', 'below', 'obscures', 'view', 'SW', 'chasm', 'corridor.'] + \
    ['NE', 'long,', 'faint', 'rumbling', 'noise', 'heard', 'forks', 'left', 'fork', 'northeast.'] + \
    ['dull', 'seems', 'louder', 'direction.', 'right', 'southeast', 'gentle', 'slope.', 'main', 'gently'] + \
    ['lined', 'oddly', 'shaped', 'limestone', 'formations.', 'entrance', 'barren', 'posted', 'reads:', '"Caution!'] + \
    ['Bear', 'room!"', 'center', 'completely', 'empty', 'dust.', 'toward', 'only', 'way', 'came'] + \
    ['in.', 'warm', 'From', 'steady', 'roar,', 'so', 'loud', 'entire', 'cave', 'trembling.'] + \
    ['boulders.', 'breath-taking', 'view.', 'Far', 'active', 'volcano,', 'great', 'gouts', 'molten'] + \
    ['lava', 'come', 'surging', 'out,', 'cascading', 'depths.', 'glowing', 'farthest', 'reaches', 'cavern'] + \
    ['blood-red', 'glare,', 'giving', 'every-thing', 'eerie,', 'macabre', 'appearance.', 'flickering', 'sparks', 'ash'] + \
    ['smell', 'brimstone.', 'hot', 'touch,', 'thundering', 'volcano', 'drowns', 'sounds.', 'Embedded', 'jagged'] + \
    ['roof', 'myriad', 'twisted', 'formations', 'composed', 'pure', 'alabaster,', 'scatter', 'murky', 'light'] + \
    ['sinister', 'apparitions', 'upon', 'gorge,', 'bizarre', 'chaos', 'tortured', 'crafted', 'devil', 'himself.'] + \
    ['immense', 'river', 'fire', 'crashes', 'depths', 'burns', 'its', 'plummets', 'bottomless'] + \
    ['Across', 'dimly', 'visible.', 'right,', 'geyser', 'blistering', 'steam', 'erupts', 'continuously', 'island'] + \
    ['sulfurous', 'lake,', 'bubbles', 'ominously.', 'flame', 'incandescence', 'own,', 'lends', 'additional', 'infernal'] + \
    ['splendor', 'already', 'hellish', 'scene.', 'dark,', 'foreboding', 'south.', 'This', 'Oriental', 'Ancient'] + \
    ['oriental', 'drawings', 'whose', 'resemble', 'Swiss', 'cheese.', 'Obvious', 'NE,', 'NW.', 'Part'] + \
    ['occupied', 'bedrock', 'block.', 'soft', 'curtains,', 'pile', 'carpet.', 'Moss', 'covers', 'ceiling.'] + \
    ['tall', 'canyon.', '3', 'Dead', 'place', 'further', 'following', 'outer', 'misty', 'cavern.'] + \
    ['below,', 'mist,', 'strange', 'splashing', 'noises', 'heard.', 'alcove.', 'NW', 'widen', 'after'] + \
    ['short', 'tunnel', 'looks', 'squeeze.', 'eerie', 'Plover', 'Dark', 'exit.', 'sizable', 'stalactite'] + \
    ['could', 'climb', 'it,', 'jump', 'floor,', 'having', 'done', 'unable', 'reach', 'junction'] + \
    ['three', 'canyons,', 'bearing', 'SE.', 'combined.', 'stalactite.', 'circular', 'slab', 'fallen', 'ceiling'] + \
    ['(Slab', 'room).', 'East', 'once', 'were', 'they', 'now', 'Low,', 'quickly', 'bends'] + \
    ['Twopit', 'littered', 'thin', 'slabs,', 'easy', 'descend', 'pits.', 'bypassing', 'pits', 'connect'] + \
    ['over,', 'directly', 'where', 'eastern', 'pool', 'oil', 'corner', 'western', 'Giant', 'lamp'] + \
    ['show', 'Cavernous', 'On', 'scrawled', 'inscription,', '"Fee', 'Fie', 'Foe', 'Foo"', '{sic}.'] + \
    ['magnificent', 'rushing', 'cascades', 'sparkling', 'waterfall', 'roaring', 'whirlpool', 'disappears', 'steep'] + \
    ['incline', 'alike.', 'level.', 'outside', 'again.', 'valley.', 'streambed.', 'grate.', 'cobble', 'dim'] + \
    ['"Magic', 'word', 'XYZZY".', 'nugget', 'gold', 'explosion,', 'machine.', '"Y2".', 'Mt', 'stream.'] + \
    ['Shell', 'cul-de-sac.', 'anteroom.', 'Bedquilt.', 'path.', 'cheese', 'mass', 'boulders', '--', 'Alcove.'] + \
    ['canyons.', 'Slab', 'Two', 'Pit', 'incline.', 'rickety', 'wooden', 'bridge', 'chasm,'] + \
    ['vanishing', 'reads,', '"STOP!', 'Pay', 'troll!"', 'not used','(and', 'not used', 'not used', 'not used', 'burly', 'troll', 'stands', 'insists'] + \
    ['him', 'cross.', 'not used', 'scurries', 'bridge,', '800', 'pound', 'bear,', 'collapses', 'currently', 'holding'] + \
    ['following:', 'carrying', 'anything.', 'carry', 'anything', 'more.', 'Yo', 'something', 'first.', 'locked'] + \
    ['grate!', 'I', 'not used', 'what', 'want', 'no', 'not used', 'you are', 'not used', 'will', 'stuck', 'tunnel.', 'Drop'] + \
    ['through.', 'do not', 'enough', 'clam.', 'glistening', 'pearl', 'falls', 'not used', 'rolls', 'away.', 'rustling'] + \
    ['darkness', 'Out', 'shadows', 'pounces', 'bearded', 'pirate!', '"Har,', 'har,"', 'he', 'chortles,'] + \
    ['I will', 'just', 'booty', 'hide', 'me', 'maze!"', 'He', 'snatches', 'vanishes', 'gloom.'] + \
    ['set', 'keys', 'shiny', 'brass', 'nearby.', 'tasty', 'food', 'bottle', 'Wicker', 'cage'] + \
    ['sitting', 'cute', 'black', 'rod', 'rusty', 'star', 'lies', 'axe', 'laying', 'pillow'] + \
    ['here!', 'golden', 'chain', 'copies', 'Spelunker', 'Today', 'magazine', 'beautiful', 'green', 'emerald'] + \
    ['ancient', 'Ming', 'Dynasty', 'vase', 'rare', 'Persian', 'rug', 'platinum', 'pyramid', 'not used', 'diamonds'] + \
    ['brown', 'bear', 'eggs', 'trident', 'bars', 'silver', 'fine', 'jewelry', 'being', 'followed'] + \
    ['tame', 'bear.', 'Your', 'off.', 'cannot', 'Nothing', 'happens.', 'Do', 'really', 'now?'] + \
    ['nothing', 'attack.', 'fierce', 'snake', 'way!', 'Attacking', 'does not', 'work', 'dangerous.', 'With'] + \
    ['hands?', 'might', 'catch', 'bird,', 'was', 'unafraid', 'when', 'entered,', 'approach', 'disturbed'] + \
    ['attacks', 'snake,', 'astounding', 'flurry', 'drives', 'Oh', 'dear.', 'nasty', 'hit', 'you!'] + \
    ['dwarf', 'corner,', 'saw', 'threw', 'missed', 'cursed', 'ran', 'killed', 'dwarf.', 'dwarf,'] + \
    ['he', 'dodges', 'way.', 'stabs', 'his', 'knife!', 'massive', 'metal', 'door', 'closed.'] + \
    ['open.', 'not used', 'not used', 'chain!', 'not used', 'climb.', 'Brass', 'lantern', 'Tasty', 'Glass', 'Black', 'Cute', 'Axe'] + \
    ['Soft', 'Oil', 'Coins', 'Golden', 'Magazines', 'Glistening', 'Green', 'Pyramid', 'Diamonds', 'Brown'] + \
    ['Trident', 'Gold', 'Silver', 'Somewhere', 'nearby', 'MyAdvent', '& Don Woods (1976).', 'others', 'found', 'fortunes'] + \
    ['gold,', 'though', 'rumored', 'never', 'Magic', 'said', 'cave.', 'eyes', 'hands.', 'Direct'] + \
    ['commands', '1', '2', 'words.', 'should', 'warn', 'first', 'letters', 'each', 'word.'] + \
    ['Should', 'stuck,', 'type', '"HELP"', 'general', 'hints.', 'know', 'places,', 'actions,', 'things.'] + \
    ['Most', 'my', 'vocabulary', 'describes', 'places', 'used', 'move', 'there.', 'move,', 'try'] + \
    ['FOREST,', 'BUILDING,', 'DOWNSTREAM,', 'ENTER,', 'EAST,', 'WEST,', 'few', 'special', 'objects,', 'hidden'] + \
    ['These', 'objects', 'manipulated', 'using', 'action', 'know.', 'Usually', 'need', 'give', 'object'] + \
    ['(in', 'order),', 'sometimes', 'infer', 'verb', 'alone.', 'Some', 'imply', 'verbs;', 'particular,'] + \
    ['"INVENTORY"', 'implies', '"TAKE', 'INVENTORY",', 'causes', 'list', 'carrying.', 'effects;', 'instance,', 'scares'] + \
    ['bird.', 'people', 'trouble', 'moving', 'more', 'trying', 'unsuccessfully', 'manipulate', 'attempting', 'their'] + \
    ['(or', 'my!', ')', 'capabilities', 'different', 'tack.', 'speed', 'game,', 'distances', 'single'] + \
    ['For', 'example,', '"BUILDING"', 'usually', 'gets', 'anywhere', 'ground', 'lost', 'Also,', 'turn'] + \
    ['lot,', 'leaving', 'does', 'guarantee', 'entering', 'Good', 'luck!', 'direction', 'proceed', 'direction!'] + \
    ['Sorry.', 'Please', 'Huh?', 'keys!', 'locked.', 'unlocked.', 'crystalline', 'spans', 'past', 'snake.'] + \
    ['pitch', 'dark.', 'likely', 'fall', 'hollow', 'voice', '"Plugh"', 'dragon', 'sprawled', 'rug.'] + \
    ['dragon.', 'tablet', 'imbedded', 'reads: "Congratulations', 'bringing', 'plant', 'murmuring', '"Water,', 'water,', '.'] + \
    ['spurts', 'furious', 'growth', 'seconds.', '12-foot-tall', 'beanstalk', 'bellowing', '"WATER!', '!', 'WATER!'] + \
    ['grows', 'explosively,', 'filling', 'over-watered', 'plant!', 'shriveled', 'up!', 'gigantic', 'door,', 'hinges'] + \
    ['rusted,', 'opened', 'oil.', 'Thud.', 'Did', 'something?', 'Smash!', 'land', 'on,', 'hits'] + \
    ['All', 'pieces', 'magically', 'vanish.', 'source', 'light.', 'not used', 'not used', 'not used', 'food.', 'not used', 'hungry', 'eats', 'released'] + \
    ['unlocked', 'purpose.', 'One', 'feeds', 'waste', 'water!', 'do', 'see', 'water.', 'bottle.'] + \
    ['Go', 'find', '"fill', 'bottle".', 'not used', 'rank', 'amateur.', 'Better', 'luck', 'time.', 'qualifies'] + \
    ['novice-class', 'adventurer.', 'achieved', 'rating;', '"Experienced', 'Adventurer".', 'consider', 'yourself', '"Seasoned', 'reached'] + \
    ['"Junior', 'Master"', 'status.', 'puts', 'Master', 'Adventurer', 'class', 'C.', 'B.', 'A.'] + \
    ['Adventuredom', 'gives', 'tribute', 'Grandmaster!', 'needs', 'vanished!', 'Wave', 'what?', 'cage.', 'flies'] + \
    ['nest.', 'not used', 'not used', '"open"', 'named', 'now.', 'shell', 'opens', 'moment', 'reveal', 'be.', 'not used', 'not used', 'lamp.'] + \
    ['(nugget)', 'opportunity', '"free"', '"take"', 'Beyond', 'glow', 'see.', 'dark', 'dear,', 'everything'] + \
    ['including', 'scoreboard!', 'Poof!', 'while', 'dangerous', 'Congratulations!', 'vanquished', 'hands!', 'makes', 'bright.'] + \
    ['think', '"unlock', 'grate".', 'not used', 'Adventure', 'based', 'mostly', 'text', 'Will', 'Crowther', '(1975)'] + \
    ['game', 'new', 'Python', '2x', 'code', 'written', 'George', 'Kauffman', '(2020).', 'uses'] + \
    ['navigation', '350', 'maps.', 'Once', 'loaded,', '32', 'kilobytes', 'ram', 'disk', 'access.'] + \
    ['65', 'words,', '36', '125', 'rooms,', '487', 'mysentences', '1543', 'Scoring:', '1/room'] + \
    ['(125)', '8/treasure', '(15),', '10/puzzle', '(10)', 'maximum.', 'Action', 'Words:', 'Object', 'words:'] + \
    ['Jewelry', 'getting', 'dim.', 'Are', 'fresh', 'batteries?', 'battery', 'dead.', 'Is', 'nearby?'] + \
    ['total', 'darkness.', 'As', 'pirate', 'making', 'hasty', 'edition', 'January', 'February', 'March'] + \
    ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'have.'] + \
    ['held.', 'points.', '350', '340', '270', '200', '130', '75', '25', 'crawled'] + \
    ['instructions', 'read:', '"Drop', 'receive', 'batteries".', ' puzzle', 'body', 'greasy', 'smoke.', 'sepulchral'] + \
    ['reverberating', 'closing', 'soon.', 'adventurers', 'immediately', 'Main', 'Office."', 'blast', 'detonate', 'intones,'] + \
    ['"The', 'closed."', 'echoes', 'fade,', 'blinding', 'flash', 'puff', 'smoke). . . .', 'not used', 'not used', 'refocus,', 'find...'] + \
    ['twenty-foot', 'burying', 'dwarves', 'rubble.', 'Office,', 'cheering band', 'friendly elves', 'nu', 'nu', 'nu', 'nu', 'nu', 'nu', 'nu', 'nu', 'nu', 'nu', 'conquering adventurer', 'sunset.', 'even larger than'] + \
    ['repository', '"Adventure" program.', 'Massive torches', 'bathe', 'smoky yellow', 'Scattered', 'bottles', 'northeast', '(all', 'them empty),'] + \
    ['nursery', 'young beanstalks', 'quietly,', 'oysters,', 'bundle', 'rods', 'stars', 'ends,', 'collection', 'lanterns.'] + \
    ['Off', 'many', 'sleeping', 'snoring loudly.', 'southwest', 'Repository.', 'snakes.', 'cages,', 'contains', 'sulking'] + \
    ['marks', 'ends.', '"Do', 'disturb', 'dwarves!"', 'against', 'stretches', 'various', 'sundry', 'glimpsed'] + \
    ['number', 'velvet pillows', 'scattered', 'grate,', '"Treasure Vault.', 'Keys', 'dynamite', 'burned', 'cinder.', 'blow'] + \
    ['How?', 'Colossal Cave,', 'spices', 'walk', 'run', 'where?', 'well.', 'probably', 'chain,', 'ferocious'] + \
    ['eying', 'room!', 'contented-looking', 'wandering', 'wants', '(except perhaps you).', 'mistakes, the Delete key erases,', '/', 'to erase a first word.', ''] + \
    ['bed','row','eat','ashes','disappears','line.','Bird','appears','For', 'a', 'summary', 'of', 'the', 'most', 'recent'] + \
    ['changes', 'to', 'the', 'game,', 'say', "'news'.", 'If', 'you', 'want', 'to', 'end', 'your', 'adventure', 'early,', 'say'] + \
    ["'quit'.", 'To', 'see', 'how', 'well', 'you', 'are', 'doing,', 'say', "'score'.", 'To', 'get', 'full', 'credit', 'for', 'a'] + \
    ['treasure,', 'you', 'must', 'have', 'left', 'it', 'safely', 'in', 'the', 'building.', 'There', 'are', 'also', 'points', 'based'] + \
    ['on', 'how', 'much', '(if any)', 'of', 'the', 'cave', 'you', 'have', 'managed', 'to', 'explore.']
    return mylist
#
# this list is the game sentence list, using mylist words
#
def mysent_init():
    mysent =[]
    mysent.append(["not used"])
# 1
    mysent.append([mylist[60],mylist[61],mylist[62],mylist[64],mylist[65],mylist[66],mylist[67]])
    mysent.append([mylist[68],mylist[69],mylist[70],mylist[71],mylist[72],mylist[73],mylist[74],mylist[75],mylist[76],mylist[77],mylist[75],mylist[78],mylist[79],mylist[80],mylist[81],mylist[65],mylist[82],mylist[75],mylist[83],mylist[84],mylist[78],mylist[85],mylist[86],mylist[87],mylist[74],mylist[72],mylist[26],mylist[88],mylist[13],mylist[75],mylist[89]])
    mysent.append([mylist[68],mylist[69],mylist[90],mylist[75],mylist[91],mylist[75],mylist[92],mylist[93],mylist[94],mylist[75],mylist[95],mylist[96]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[97],mylist[98],mylist[99],mylist[76],mylist[100],mylist[12],mylist[75],mylist[101],mylist[102],mylist[103]])
    mysent.append([mylist[68],mylist[104],mylist[105],mylist[12],mylist[75],mylist[106],mylist[107],mylist[108],mylist[72],mylist[83],mylist[99],mylist[76],mylist[109],mylist[110],mylist[13],mylist[72],mylist[111],mylist[112],mylist[74],mylist[72],mylist[113],mylist[114],mylist[82],mylist[75],mylist[26],mylist[108],mylist[72],mylist[115]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[38],mylist[27],mylist[116],mylist[117],mylist[75],mylist[118],mylist[88],mylist[75],mylist[119]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[38],mylist[120],mylist[121],mylist[75],mylist[122],mylist[118],mylist[61],mylist[123],mylist[124]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[118],mylist[108],mylist[72],mylist[27],mylist[125],mylist[75],mylist[85],mylist[126],mylist[127],mylist[75],mylist[128],mylist[129]])
    mysent.append([mylist[130],mylist[131],mylist[132],mylist[133],mylist[72],mylist[48],mylist[74],mylist[72],mylist[85],mylist[134],mylist[135],mylist[75],mylist[136],mylist[137],mylist[108],mylist[72],mylist[138],mylist[139],mylist[72],mylist[140],mylist[82],mylist[141],mylist[138]])
#10
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[142],mylist[143],mylist[144],mylist[121],mylist[141],mylist[145],mylist[146],mylist[135],mylist[72],mylist[147],mylist[82],mylist[75],mylist[148],mylist[149],mylist[150],mylist[151],mylist[108],mylist[152],mylist[84],mylist[153],mylist[140],mylist[154],mylist[135],mylist[72],mylist[155]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[78],mylist[156],mylist[157],mylist[75],mylist[158],mylist[149],mylist[150],mylist[61],mylist[72],mylist[159],mylist[84],mylist[160],mylist[161],mylist[162],mylist[163],mylist[154],mylist[164],mylist[61],mylist[72],mylist[165]])
    mysent.append([mylist[84],mylist[160],mylist[166],mylist[167],mylist[121],mylist[163],mylist[168],mylist[169],mylist[121],mylist[170],mylist[88],mylist[171],mylist[172],mylist[173],mylist[174],mylist[175],mylist[176],mylist[154],mylist[177],mylist[88],mylist[165]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[171],mylist[46],mylist[178],mylist[121],mylist[179],mylist[180],mylist[108],mylist[181],mylist[72],mylist[159]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[156],mylist[121],mylist[75],mylist[167],mylist[61],mylist[72],mylist[4],mylist[88],mylist[182],mylist[183],mylist[184],mylist[185]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[186],mylist[156],mylist[187],mylist[132],mylist[188],mylist[99],mylist[189],mylist[69],mylist[190],mylist[191],mylist[74],mylist[192],mylist[193],mylist[194],mylist[175],mylist[176],mylist[88],mylist[75],mylist[195],mylist[167],mylist[29],mylist[181],mylist[5],mylist[88],mylist[4],mylist[196],mylist[74],mylist[72],mylist[197],mylist[84],mylist[198],mylist[199],mylist[200],mylist[201],mylist[202]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[204],mylist[74],mylist[78],mylist[205],mylist[130],mylist[131],mylist[132],mylist[82],mylist[75],mylist[78],mylist[206],mylist[207],mylist[208],mylist[74],mylist[209],mylist[210],mylist[194],mylist[5],mylist[167],mylist[211],mylist[212],mylist[213],mylist[94],mylist[75],mylist[78],mylist[214],mylist[215],mylist[216],mylist[217],mylist[218],mylist[219],mylist[220],mylist[13],mylist[72],mylist[205]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[123],mylist[73],mylist[74],mylist[75],mylist[221],mylist[222],mylist[74],mylist[223],mylist[224],mylist[225],mylist[87],mylist[74],mylist[226],mylist[61],mylist[72],mylist[227],mylist[178],mylist[121],mylist[228],mylist[74],mylist[209],mylist[229],mylist[230],mylist[231],mylist[61],mylist[88],mylist[232],mylist[233],mylist[234],mylist[235],mylist[236],mylist[217],mylist[218],mylist[219],mylist[220],mylist[12],mylist[61],mylist[75],mylist[167],mylist[71],mylist[72],mylist[204],mylist[74],mylist[75],mylist[237],mylist[238],mylist[103],mylist[84],mylist[166],mylist[239],mylist[240],mylist[241],mylist[135],mylist[72],mylist[242],mylist[75],mylist[243],mylist[244],mylist[245],mylist[12],mylist[181],mylist[246],mylist[114],mylist[69],mylist[78],mylist[247],mylist[61],mylist[72],mylist[6],mylist[88],mylist[248],mylist[88],mylist[75],mylist[78],mylist[214],mylist[154],mylist[185]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[5],mylist[249],mylist[74],mylist[75],mylist[250],mylist[99],mylist[229],mylist[82],mylist[251],mylist[252],mylist[172],mylist[88],mylist[72],mylist[253],mylist[82],mylist[254],mylist[166],mylist[61],mylist[255]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[4],mylist[249],mylist[74],mylist[72],mylist[253],mylist[108],mylist[72],mylist[256],mylist[74],mylist[257]])
#20
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[160],mylist[46],mylist[121],mylist[75],mylist[258],mylist[259],mylist[40],mylist[72],mylist[260],mylist[99],mylist[259],mylist[261],mylist[262],mylist[263],mylist[37],mylist[264],mylist[12],mylist[72],mylist[265]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[4],mylist[73],mylist[74],mylist[256],mylist[74],mylist[257],mylist[84],mylist[160],mylist[166],mylist[161],mylist[266],mylist[4],mylist[88],mylist[267],mylist[268],mylist[269],mylist[270],mylist[72],mylist[7],mylist[82],mylist[75],mylist[271],mylist[167],mylist[272],mylist[132],mylist[41],mylist[72],mylist[273]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[5],mylist[73],mylist[74],mylist[75],mylist[274],mylist[275],mylist[276],mylist[277],mylist[278],mylist[112],mylist[279],mylist[270],mylist[72],mylist[280],mylist[75],mylist[160],mylist[166],mylist[161],mylist[281],mylist[282],mylist[270],mylist[72],mylist[6],mylist[283],mylist[284],mylist[285],mylist[286],mylist[281],mylist[287]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[4],mylist[73],mylist[74],mylist[75],mylist[274],mylist[275],mylist[294],mylist[295],mylist[99],mylist[222],mylist[296],mylist[12],mylist[121],mylist[75],mylist[297],mylist[298],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[300],mylist[74],mylist[301],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[301],mylist[271],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[300],mylist[74],mylist[304],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[301],mylist[300],mylist[74],mylist[271],mylist[302],mylist[133],mylist[303]])
# 30
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[301],mylist[271],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[304],mylist[271],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[304],mylist[300],mylist[74],mylist[271],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[304],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[271],mylist[301],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[271],mylist[304],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1033],mylist[308],mylist[309],mylist[202],mylist[99],mylist[1440],mylist[40],mylist[264],mylist[1441],mylist[1442],mylist[318],mylist[212],mylist[61],mylist[1443],mylist[1404],mylist[1444]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[325],mylist[74],mylist[326],mylist[121],mylist[327],mylist[328]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[95],mylist[329],mylist[121],mylist[75],mylist[167],mylist[61],mylist[72],mylist[248],mylist[75],mylist[167],mylist[61],mylist[72],mylist[227],mylist[88],mylist[75],mylist[330],mylist[74],mylist[331],mylist[332],mylist[61],mylist[72],mylist[185],mylist[114],mylist[82],mylist[75],mylist[95],mylist[333],mylist[40],mylist[75],mylist[332],mylist[108],mylist[72],mylist[334],mylist[335]])
    mysent.append([mylist[203],mylist[71],mylist[75],mylist[160],mylist[336],mylist[337],mylist[75],mylist[338],mylist[339],mylist[340],mylist[341],mylist[12],mylist[87],mylist[74],mylist[342],mylist[84],mylist[343],mylist[82],mylist[344],mylist[345],mylist[162],mylist[346],mylist[132],mylist[246],mylist[347],mylist[74],mylist[209],mylist[229],mylist[348],mylist[72],mylist[343],mylist[74],mylist[72],mylist[339],mylist[349],mylist[350],mylist[61],mylist[72],mylist[351],mylist[352],mylist[108],mylist[72],mylist[353],mylist[283],mylist[72],mylist[336],mylist[354],mylist[355],mylist[61],mylist[356],mylist[230],mylist[357],mylist[199],mylist[200],mylist[212],mylist[358],mylist[359],mylist[360],mylist[72],mylist[206],mylist[181],mylist[65],mylist[88],mylist[361],mylist[132],mylist[362],mylist[363],mylist[82],mylist[75],mylist[364],mylist[336],mylist[365],mylist[135],mylist[75],mylist[366],mylist[367],mylist[84],mylist[368],mylist[369],mylist[370],mylist[371],mylist[372],mylist[363],mylist[373],mylist[110],mylist[71],mylist[103]])
# 40
    mysent.append([mylist[203],mylist[71],mylist[75],mylist[160],mylist[336],mylist[337],mylist[75],mylist[338],mylist[339],mylist[340],mylist[341],mylist[12],mylist[87],mylist[74],mylist[342],mylist[84],mylist[343],mylist[82],mylist[344],mylist[345],mylist[162],mylist[346],mylist[132],mylist[246],mylist[347],mylist[74],mylist[209],mylist[229],mylist[348],mylist[72],mylist[343],mylist[74],mylist[72],mylist[339],mylist[349],mylist[350],mylist[61],mylist[72],mylist[374],mylist[352],mylist[108],mylist[72],mylist[353],mylist[283],mylist[72],mylist[336],mylist[354],mylist[355],mylist[61],mylist[356],mylist[230],mylist[357],mylist[199],mylist[200],mylist[212],mylist[358],mylist[359],mylist[360],mylist[72],mylist[206],mylist[181],mylist[65],mylist[88],mylist[361],mylist[132],mylist[362],mylist[363],mylist[82],mylist[75],mylist[364],mylist[336],mylist[365],mylist[135],mylist[75],mylist[366],mylist[367],mylist[84],mylist[368],mylist[369],mylist[370],mylist[371],mylist[372],mylist[363],mylist[373],mylist[110],mylist[71],mylist[103]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[160],mylist[291],mylist[167],mylist[71],mylist[75],mylist[286],mylist[108],mylist[72],mylist[273],mylist[99],mylist[286],mylist[268],mylist[13],mylist[61],mylist[174],mylist[292],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[256],mylist[74],mylist[72],mylist[375],mylist[376],mylist[121],mylist[247],mylist[41],mylist[108],mylist[133],mylist[377]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[4],mylist[112],mylist[156],mylist[74],mylist[72],mylist[256],mylist[74],mylist[72],mylist[375],mylist[378],mylist[84],mylist[167],mylist[266],mylist[4],mylist[88],mylist[12],mylist[202]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[7],mylist[112],mylist[156],mylist[321],mylist[61],mylist[72],mylist[256],mylist[74],mylist[72],mylist[375],mylist[378]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[176],mylist[340],mylist[212],mylist[240],mylist[380],mylist[381],mylist[382],mylist[162],mylist[75],mylist[274],mylist[383],mylist[176],mylist[384],mylist[132],mylist[246],mylist[385],mylist[65],mylist[386],mylist[13],mylist[65],mylist[387],mylist[388],mylist[371],mylist[389],mylist[61],mylist[37],mylist[110],mylist[282]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[291],mylist[176],mylist[238],mylist[75],mylist[95],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[298],mylist[176],mylist[390],mylist[361],mylist[132],mylist[391],mylist[99],mylist[343],mylist[82],mylist[392],mylist[393],mylist[209],mylist[229],mylist[394],mylist[108],mylist[181],mylist[72],mylist[269],mylist[99],mylist[189],mylist[395],mylist[177],mylist[94],mylist[92],mylist[162],mylist[396],mylist[397],mylist[398],mylist[181],mylist[399],mylist[400],mylist[401],mylist[402],mylist[238],mylist[403],mylist[174],mylist[307],mylist[404],mylist[405],mylist[82],mylist[406],mylist[407],mylist[61],mylist[88],mylist[408],mylist[409],mylist[72],mylist[176],mylist[410],mylist[411],mylist[405],mylist[82],mylist[412],mylist[413],mylist[94],mylist[72],mylist[414],mylist[74],mylist[72],mylist[415],mylist[416],mylist[234],mylist[65],mylist[417],mylist[69],mylist[418],mylist[419],mylist[84],mylist[78],mylist[336],mylist[370],mylist[371],mylist[372],mylist[108],mylist[420],mylist[421],mylist[399],mylist[422],mylist[132],mylist[282]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[423],mylist[176],mylist[121],mylist[247],mylist[61],mylist[72],mylist[6],mylist[88],mylist[185]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[424],mylist[425],mylist[74],mylist[75],mylist[95],mylist[426],mylist[427],mylist[84],mylist[252],mylist[428],mylist[74],mylist[209],mylist[229],mylist[429],mylist[72],mylist[329],mylist[430],mylist[181],mylist[72],mylist[431],mylist[74],mylist[72],mylist[48],mylist[88],mylist[432],mylist[433],mylist[434],mylist[99],mylist[435],mylist[82],mylist[436],mylist[393],mylist[75],mylist[437],mylist[340],mylist[438],mylist[87],mylist[74],mylist[75],mylist[286],mylist[108],mylist[72],mylist[330],mylist[390],mylist[439],mylist[132],mylist[440],mylist[88],mylist[134],mylist[441],mylist[135],mylist[72],mylist[48],mylist[116],mylist[72],mylist[442],mylist[443],mylist[260],mylist[84],mylist[444],mylist[167],mylist[445],mylist[446],mylist[72],mylist[443],mylist[421],mylist[173],mylist[65],mylist[447],mylist[37],mylist[360],mylist[72],mylist[48],mylist[61],mylist[37],mylist[61],mylist[324],mylist[448],mylist[167],mylist[154],mylist[7],mylist[181],mylist[202]])
# 50
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[449],mylist[450],mylist[114],mylist[82],mylist[75],mylist[451],mylist[452],mylist[172],mylist[453],mylist[102],mylist[75],mylist[454]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[95],mylist[46],mylist[455],mylist[74],mylist[456],mylist[457],mylist[114],mylist[82],mylist[75],mylist[458],mylist[286],mylist[108],mylist[72],mylist[273],mylist[114],mylist[69],mylist[327],mylist[459],mylist[88],mylist[75],mylist[167],mylist[215],mylist[185]])
    mysent.append([mylist[203],mylist[108],mylist[75],mylist[460],mylist[167],mylist[121],mylist[331],mylist[457],mylist[270],mylist[72],mylist[5],mylist[82],mylist[75],mylist[461],mylist[270],mylist[72],mylist[4],mylist[82],mylist[75],mylist[95],mylist[299],mylist[462],mylist[65],mylist[82],mylist[75],mylist[286],mylist[61],mylist[267],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[463],mylist[74],mylist[75],mylist[78],mylist[464],mylist[465],mylist[205],mylist[84],mylist[161],mylist[154],mylist[165]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[466],mylist[74],mylist[75],mylist[78],mylist[206],mylist[121],mylist[75],mylist[271],mylist[437],mylist[340],mylist[467],mylist[88],mylist[445],mylist[446],mylist[468],mylist[469]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[75],mylist[470],mylist[471],mylist[84],mylist[160],mylist[472],mylist[88],mylist[473],mylist[167],mylist[181],mylist[72],mylist[6],mylist[296],mylist[75],mylist[474],mylist[161],mylist[181],mylist[72],mylist[5],mylist[61],mylist[475],mylist[75],mylist[476],mylist[167],mylist[477],mylist[165],mylist[114],mylist[82],mylist[478],mylist[75],mylist[95],mylist[46],mylist[479],mylist[99],mylist[480],mylist[82],mylist[481],mylist[202]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[46],mylist[121],mylist[174],mylist[307],mylist[482],mylist[483],mylist[484],mylist[114],mylist[82],mylist[75],mylist[167],mylist[61],mylist[72],mylist[248],mylist[75],mylist[465],mylist[286],mylist[238],mylist[88],mylist[75],mylist[78],mylist[286],mylist[108],mylist[72],mylist[343],mylist[477],mylist[287]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[174],mylist[485],mylist[295],mylist[114],mylist[82],mylist[75],mylist[286],mylist[108],mylist[72],mylist[343],mylist[477],mylist[287]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[275],mylist[183],mylist[486],mylist[121],mylist[487],mylist[488],mylist[410]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[489],mylist[390],mylist[490],mylist[132],mylist[391]])
# 60
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[174],mylist[491],mylist[215],mylist[61],mylist[75],mylist[95],mylist[167],mylist[61],mylist[72],mylist[185],mylist[492],mylist[247],mylist[386],mylist[4],mylist[88],mylist[282],mylist[99],mylist[493],mylist[74],mylist[494],mylist[495],mylist[69],mylist[496],mylist[84],mylist[497],mylist[108],mylist[498],mylist[212],mylist[499],mylist[500],mylist[501],mylist[502],mylist[503],mylist[306],mylist[504],mylist[505],mylist[71],mylist[506],mylist[507],mylist[508],mylist[509],mylist[510]])
    mysent.append([mylist[203],mylist[71],mylist[511],mylist[512],mylist[513],mylist[220],mylist[41],mylist[108],mylist[514],mylist[377]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[515],mylist[75],mylist[275],mylist[516],mylist[167],mylist[121],mylist[517],mylist[328],mylist[270],mylist[518],mylist[71],mylist[519],mylist[520],mylist[521],mylist[522],mylist[523],mylist[524],mylist[525]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[95],mylist[160],mylist[367],mylist[526],mylist[220],mylist[527],mylist[528],mylist[88],mylist[529]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[530],mylist[73],mylist[161],mylist[238],mylist[75],mylist[95],mylist[160],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[275],mylist[531],mylist[486],mylist[183],mylist[87],mylist[74],mylist[226],mylist[108],mylist[117],mylist[377]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[123],mylist[112],mylist[74],mylist[75],mylist[532],mylist[122],mylist[533],mylist[84],mylist[534],mylist[209],mylist[229],mylist[430],mylist[12],mylist[181],mylist[535],mylist[536],mylist[133],mylist[537],mylist[74],mylist[72],mylist[402],mylist[124],mylist[84],mylist[538],mylist[182],mylist[154],mylist[362],mylist[181],mylist[72],mylist[539],mylist[135],mylist[75],mylist[531],mylist[540]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[402],mylist[112],mylist[74],mylist[72],mylist[533],mylist[84],mylist[541],mylist[182],mylist[154],mylist[362],mylist[181],mylist[72],mylist[539],mylist[40],mylist[306],mylist[124]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[542],mylist[297],mylist[292],mylist[486],mylist[224],mylist[87],mylist[74],mylist[226],mylist[61],mylist[72],mylist[165],mylist[84],mylist[543],mylist[544],mylist[545],mylist[370],mylist[371],mylist[546],mylist[108],mylist[72],mylist[115]])
    mysent.append([mylist[203],mylist[108],mylist[75],mylist[540],mylist[99],mylist[182],mylist[547],mylist[202],mylist[99],mylist[548],mylist[549],mylist[154],mylist[550],mylist[84],mylist[551],mylist[544],mylist[552],mylist[61],mylist[37],mylist[553],mylist[108],mylist[230],mylist[554],mylist[99],mylist[555],mylist[549],mylist[154],mylist[556],mylist[13],mylist[75],mylist[557],mylist[558],mylist[99],mylist[559],mylist[486],mylist[467],mylist[181],mylist[72],mylist[165]])
# 70
    mysent.append([mylist[68],mylist[69],mylist[476],mylist[127],mylist[75],mylist[560],mylist[183],mylist[298],mylist[167],mylist[561],mylist[121],mylist[562],mylist[563],mylist[564],mylist[565]])
    mysent.append([mylist[68],mylist[69],mylist[70],mylist[71],mylist[72],mylist[566],mylist[61],mylist[75],mylist[532],mylist[567],mylist[367],mylist[84],mylist[497],mylist[568],mylist[238],mylist[72],mylist[566],mylist[569],mylist[570],mylist[571],mylist[108],mylist[572]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[567],mylist[367],mylist[99],mylist[573],mylist[74],mylist[72],mylist[46],mylist[82],mylist[574],mylist[575],mylist[213],mylist[94],mylist[399],mylist[576],mylist[352],mylist[108],mylist[72],mylist[353],mylist[220],mylist[362],mylist[577],mylist[72],mylist[402],mylist[73],mylist[74],mylist[72],mylist[367],mylist[99],mylist[578],mylist[29],mylist[82],mylist[72],mylist[579],mylist[65],mylist[580],mylist[581]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[471],mylist[99],mylist[189],mylist[69],mylist[251],mylist[582],mylist[202],mylist[583],mylist[72],mylist[6],mylist[370],mylist[371],mylist[546],mylist[75],mylist[584],mylist[585],mylist[586],mylist[587],mylist[230],mylist[72],mylist[588],mylist[589],mylist[552],mylist[61],mylist[371],mylist[590],mylist[448],mylist[167],mylist[154],mylist[248],mylist[88],mylist[75],mylist[160],mylist[161],mylist[268],mylist[185]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[78],mylist[156],mylist[178],mylist[121],mylist[95],mylist[591]])
# 75 is a multiline sentence
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[425],mylist[74],mylist[75],mylist[592],mylist[593],mylist[594],mylist[535],mylist[65],mylist[82],mylist[174],mylist[595],mylist[596],mylist[181],mylist[340],mylist[597],mylist[598],mylist[74],mylist[599],mylist[600],mylist[601],mylist[602],mylist[603],mylist[604],mylist[110],mylist[13],mylist[135],mylist[72],mylist[605],mylist[99],mylist[606],mylist[332],mylist[429],mylist[72],mylist[607],mylist[608],mylist[74],mylist[72],mylist[609],\
    mylist[121],mylist[75],mylist[610],mylist[611],mylist[612],mylist[613],mylist[174],mylist[614],mylist[615],mylist[616],mylist[99],mylist[480],mylist[82],mylist[178],mylist[121],mylist[617],mylist[618],mylist[74],mylist[619],mylist[88],mylist[75],mylist[534],mylist[620],mylist[74],mylist[621],mylist[99],mylist[189],mylist[69],mylist[622],mylist[61],mylist[72],mylist[623],mylist[88],mylist[72],mylist[624],mylist[74],mylist[72],mylist[625],mylist[626],mylist[87],mylist[133],\
    mylist[111],mylist[627],mylist[628],mylist[108],mylist[72],mylist[629],mylist[630],mylist[402],mylist[440],mylist[69],mylist[631],mylist[632],mylist[633],mylist[634],mylist[74],mylist[635],mylist[209],mylist[636],mylist[340],mylist[637],mylist[72],mylist[638],mylist[639],mylist[135],mylist[640],mylist[641],mylist[642],mylist[72],mylist[410],mylist[270],mylist[123],mylist[112],mylist[82],mylist[75],mylist[122],mylist[643],mylist[178],mylist[121],mylist[75],mylist[644],mylist[645],mylist[74],\
    mylist[646],mylist[332],mylist[340],mylist[552],mylist[61],mylist[104],mylist[200],mylist[647],mylist[393],mylist[72],mylist[648],mylist[649],mylist[194],mylist[650],mylist[651],mylist[74],mylist[652],mylist[653],mylist[87],mylist[181],mylist[72],mylist[654],mylist[74],mylist[72],mylist[596],mylist[655],mylist[656],mylist[579],mylist[446],mylist[72],mylist[643],mylist[88],mylist[657],mylist[135],mylist[75],mylist[658],mylist[206],mylist[402],mylist[41],mylist[61],mylist[131],mylist[374],\
    mylist[659],mylist[72],mylist[643],mylist[72],mylist[566],mylist[61],mylist[75],mylist[118],mylist[82],mylist[660],mylist[661],mylist[270],mylist[72],mylist[662],mylist[174],mylist[650],mylist[663],mylist[74],mylist[664],mylist[665],mylist[666],mylist[667],mylist[181],mylist[75],mylist[567],mylist[668],mylist[108],mylist[72],mylist[573],mylist[74],mylist[75],mylist[669],mylist[670],mylist[340],mylist[671],mylist[672],mylist[99],mylist[402],mylist[555],mylist[330],\
    mylist[82],mylist[75],mylist[673],mylist[121],mylist[174],mylist[674],mylist[74],mylist[656],mylist[675],mylist[340],mylist[676],mylist[174],mylist[677],mylist[678],mylist[679],mylist[61],mylist[72],mylist[680],mylist[681],mylist[682],mylist[84],mylist[683],mylist[684],mylist[167],mylist[445],mylist[61],mylist[72],mylist[685]])
    mysent.append([mylist[686],mylist[82],mylist[72],mylist[687],mylist[367],mylist[688],mylist[689],mylist[589],mylist[690],mylist[348],mylist[72],mylist[410],mylist[84],mylist[560],mylist[183],mylist[167],mylist[154],mylist[177],mylist[61],mylist[72],mylist[527],mylist[267],mylist[167],mylist[154],mylist[528],mylist[88],mylist[75],mylist[472],mylist[88],mylist[473],mylist[161],mylist[154],mylist[165]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[46],mylist[691],mylist[189],mylist[692],mylist[693],mylist[694],mylist[695],mylist[247],mylist[386],mylist[227],mylist[280],mylist[696],mylist[88],mylist[697],mylist[698],mylist[74],mylist[72],mylist[46],mylist[82],mylist[699],mylist[393],mylist[75],mylist[95],mylist[700],mylist[701]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[702],mylist[367],mylist[99],mylist[189],mylist[69],mylist[392],mylist[121],mylist[534],mylist[703],mylist[72],mylist[343],mylist[121],mylist[75],mylist[252],mylist[704],mylist[705],mylist[706],mylist[707],mylist[72],mylist[708]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[709],mylist[292],mylist[710],mylist[84],mylist[160],mylist[383],mylist[161],mylist[268],mylist[711],mylist[132],mylist[6],mylist[88],mylist[552],mylist[61],mylist[38],mylist[282]])
# 80
    mysent.append([mylist[99],mylist[176],mylist[240],mylist[135],mylist[75],mylist[834],mylist[74],mylist[835],mylist[836],mylist[530],mylist[98]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[75],mylist[166],mylist[713],mylist[108],mylist[75],mylist[274],mylist[383],mylist[291],mylist[710],mylist[99],mylist[176],mylist[212],mylist[168],mylist[254],mylist[383],mylist[61],mylist[386],mylist[714],mylist[685]])
    mysent.append([mylist[381],mylist[82],mylist[254],mylist[383],mylist[202],mylist[114],mylist[82],mylist[75],mylist[383],mylist[291],mylist[176],mylist[6],mylist[74],mylist[103]])
    mysent.append([mylist[68],mylist[69],mylist[715],mylist[75],mylist[166],mylist[182],mylist[283],mylist[72],mylist[716],mylist[425],mylist[74],mylist[75],mylist[95],mylist[717],mylist[718],mylist[594],mylist[719],mylist[446],mylist[75],mylist[534],mylist[209],mylist[720],mylist[721],mylist[722],mylist[723],mylist[370],mylist[371],mylist[724],mylist[99],mylist[229],mylist[100],mylist[12],mylist[446],mylist[75],mylist[253],mylist[108],mylist[72],mylist[708],mylist[99],mylist[182],mylist[445],mylist[61],mylist[72],mylist[7],mylist[88],mylist[165]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[174],mylist[725],mylist[84],mylist[78],mylist[726],mylist[182],mylist[552],mylist[61],mylist[727],mylist[728],mylist[75],mylist[729],mylist[115],mylist[194],mylist[418],mylist[383],mylist[730],mylist[154],mylist[185],mylist[381],mylist[731],mylist[66],mylist[75],mylist[274],mylist[383],mylist[732],mylist[194],mylist[733],mylist[639],mylist[370],mylist[371],mylist[372],mylist[71],mylist[72],mylist[111],mylist[98]])
    mysent.append([mylist[203],mylist[108],mylist[734],mylist[367]])
    mysent.append([mylist[203],mylist[108],mylist[72],mylist[735],mylist[367],mylist[84],mylist[486],mylist[215],mylist[7],mylist[82],mylist[72],mylist[578],mylist[736]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[291],mylist[176],mylist[238],mylist[75],mylist[737],mylist[299],mylist[84],mylist[95],mylist[738],mylist[341],mylist[181],mylist[72],mylist[630],mylist[88],mylist[233],mylist[608],mylist[72],mylist[343],mylist[246],mylist[68],mylist[739],mylist[740],mylist[13],mylist[741],mylist[88],mylist[742],mylist[181],mylist[264],mylist[61],mylist[72],mylist[743],mylist[173],mylist[744],mylist[745],mylist[586],mylist[65],mylist[354],mylist[371],mylist[746],mylist[61],mylist[747],mylist[264],mylist[61],mylist[740],mylist[110],mylist[282]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[176],mylist[71],mylist[75],mylist[748],mylist[74],mylist[749],mylist[750],mylist[751],mylist[527],mylist[248],mylist[88],mylist[752],mylist[99],mylist[6],mylist[123],mylist[82],mylist[234],mylist[709],mylist[234],mylist[72],mylist[111],mylist[284],mylist[753]])
    mysent.append([mylist[203],mylist[71],mylist[204],mylist[74],mylist[754]])
# 90
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[95],mylist[160],mylist[755],mylist[156],mylist[691],mylist[343],mylist[82],mylist[174],mylist[650],mylist[756],mylist[757],mylist[181],mylist[72],mylist[758],mylist[759],mylist[760],mylist[761],mylist[88],mylist[4],mylist[363],mylist[762],mylist[763],mylist[95],mylist[302],mylist[173],mylist[764],mylist[69],mylist[765],mylist[178],mylist[121],mylist[591],mylist[766],mylist[78],mylist[247],mylist[386],mylist[6],mylist[88],mylist[248],mylist[88],mylist[72],mylist[7],mylist[123],mylist[767],mylist[768],mylist[4],mylist[283],mylist[72],mylist[591]])
    mysent.append([mylist[203],mylist[71],mylist[72],mylist[5],mylist[73],mylist[74],mylist[769],mylist[367]])
    mysent.append([mylist[203],mylist[71],mylist[72],mylist[4],mylist[73],mylist[74],mylist[769],mylist[367],mylist[99],mylist[343],mylist[212],mylist[82],mylist[770],mylist[121],mylist[771],mylist[332],mylist[772],mylist[340],mylist[475],mylist[264],mylist[773],mylist[61],mylist[774],mylist[72],mylist[775],mylist[114],mylist[82],mylist[75],mylist[182],mylist[212],mylist[776],mylist[72],mylist[777],mylist[61],mylist[778],mylist[247],mylist[181],mylist[5],mylist[88],mylist[165],mylist[114],mylist[69],mylist[517],mylist[133],mylist[779],mylist[173],mylist[72],mylist[578],mylist[458],mylist[123],mylist[82],mylist[40],mylist[72],mylist[330],mylist[780],mylist[162],mylist[72],mylist[4],mylist[206],mylist[781],mylist[65],mylist[447],mylist[37],mylist[61],mylist[324]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[466],mylist[74],mylist[72],mylist[782],mylist[206],mylist[108],mylist[72],mylist[769],mylist[367],mylist[114],mylist[82],mylist[75],mylist[78],mylist[783],mylist[74],mylist[784],mylist[108],mylist[123],mylist[785],mylist[74],mylist[72],mylist[205]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[466],mylist[74],mylist[72],mylist[786],mylist[206],mylist[108],mylist[72],mylist[769],mylist[367],mylist[114],mylist[82],mylist[75],mylist[95],mylist[286],mylist[108],mylist[72],mylist[330],mylist[390],mylist[361],mylist[132],mylist[238],mylist[103]])
    mysent.append([mylist[203],mylist[108],mylist[292],mylist[297],mylist[540]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[787],mylist[367],mylist[99],mylist[758],mylist[212],mylist[82],mylist[254],mylist[290],mylist[12],mylist[94],mylist[131],mylist[788],mylist[61],mylist[789],mylist[324],mylist[790],mylist[247],mylist[220],mylist[280],mylist[527],mylist[88],mylist[685],mylist[791],mylist[72],mylist[4],mylist[330],mylist[82],mylist[792],mylist[72],mylist[793],mylist[794],mylist[795],mylist[796],mylist[797],mylist[798]])
    mysent.append([mylist[203],mylist[108],mylist[75],mylist[530],mylist[73],mylist[5],mylist[74],mylist[72],mylist[787],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[123],mylist[73],mylist[74],mylist[174],mylist[650],mylist[298],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[799],mylist[609],mylist[121],mylist[75],mylist[800],mylist[437],mylist[340],mylist[801],mylist[162],mylist[75],mylist[802],mylist[803],mylist[135],mylist[75],mylist[804],mylist[805],mylist[340],mylist[806],mylist[446],mylist[75],mylist[286],mylist[108],mylist[72],mylist[273],mylist[513],mylist[29],mylist[61],mylist[72],mylist[7],mylist[88],mylist[165]])
# 100
    mysent.append([mylist[203],mylist[71],mylist[807],mylist[808],mylist[238],mylist[95],mylist[367],mylist[68],mylist[739],mylist[740],mylist[13],mylist[172],mylist[173],mylist[65],mylist[354],mylist[388],mylist[371],mylist[389],mylist[61],mylist[740],mylist[282],mylist[114],mylist[82],mylist[75],mylist[167],mylist[215],mylist[110],mylist[61],mylist[72],mylist[269]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[304],mylist[271],mylist[302],mylist[133],mylist[809]])
# 102 - 112 are blank
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 113
    mysent.append([mylist[712],mylist[512]])
# 114 - 120 are blank
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 121
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[75],mylist[463],mylist[321],mylist[61],mylist[75],mylist[205],mylist[68],mylist[739],mylist[740],mylist[13],mylist[212],mylist[173],mylist[65],mylist[739],mylist[388],mylist[37],mylist[110],mylist[282],mylist[99],mylist[300],mylist[266],mylist[71],mylist[306],mylist[810]])
# 122 - 124 are blank
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 125
    mysent.append([mylist[203],mylist[811],mylist[80]])
    mysent.append([mylist[203],mylist[90],mylist[80]])
    mysent.append([mylist[203],mylist[71],mylist[73],mylist[74],mylist[76],mylist[812]])
    mysent.append([mylist[203],mylist[71],mylist[101],mylist[108],mylist[119]])
    mysent.append([mylist[203],mylist[108],mylist[83]])
# 130
    mysent.append([mylist[203],mylist[108],mylist[120],mylist[116],mylist[75],mylist[813]])
    mysent.append([mylist[203],mylist[108],mylist[813]])
    mysent.append([mylist[203],mylist[71],mylist[137],mylist[108],mylist[814]])
    mysent.append([mylist[203],mylist[811],mylist[815]])
    mysent.append([mylist[203],mylist[535],mylist[72],mylist[815]])
    mysent.append([mylist[203],mylist[108],mylist[816],mylist[461],mylist[114],mylist[82],mylist[75],mylist[817],mylist[639],mylist[71],mylist[72],mylist[5],mylist[73],mylist[74],mylist[72],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[171],mylist[367],mylist[84],mylist[259],mylist[40],mylist[72],mylist[330],mylist[499],mylist[818],mylist[819],mylist[820]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[174],mylist[175],mylist[183],mylist[516],mylist[299]])
    mysent.append([mylist[203],mylist[108],mylist[198],mylist[197]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[75],mylist[463],mylist[74],mylist[78],mylist[205]])
# 140 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[203],mylist[40],mylist[72],mylist[5],mylist[249],mylist[74],mylist[250]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[72],mylist[4],mylist[249],mylist[74],mylist[250]])
    mysent.append([mylist[203],mylist[108],mylist[821],mylist[74],mylist[822],mylist[367]])
    mysent.append([mylist[203],mylist[71],mylist[4],mylist[73],mylist[74],mylist[256],mylist[74],mylist[257]])
    mysent.append([mylist[203],mylist[71],mylist[5],mylist[73],mylist[74],mylist[256],mylist[74],mylist[257]])
    mysent.append([mylist[203],mylist[71],mylist[5],mylist[73],mylist[74],mylist[75],mylist[275],mylist[295]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[75],mylist[289],mylist[74],mylist[75],mylist[290],mylist[291],mylist[167],mylist[88],mylist[75],mylist[160],mylist[292],mylist[293]])
    mysent.append([mylist[203],mylist[71],mylist[4],mylist[73],mylist[74],mylist[75],mylist[275],mylist[295]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[300],mylist[74],mylist[301],mylist[302],mylist[133],mylist[303]])
# 150
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[301],mylist[271],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[300],mylist[74],mylist[304],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[301],mylist[300],mylist[74],mylist[271],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[301],mylist[271],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[304],mylist[271],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[304],mylist[300],mylist[74],mylist[271],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[271],mylist[304],mylist[300],mylist[74],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[271],mylist[301],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[271],mylist[304],mylist[302],mylist[133],mylist[303]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[46],mylist[121],mylist[75],mylist[308],mylist[824]])
# 160
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[325],mylist[74],mylist[457]])
    mysent.append([mylist[203],mylist[71],mylist[825]])
    mysent.append([mylist[203],mylist[71],mylist[336],mylist[40],mylist[206],mylist[121],mylist[252],mylist[229],mylist[40],mylist[72],mylist[351]])
    mysent.append([mylist[203],mylist[71],mylist[336],mylist[40],mylist[206],mylist[121],mylist[252],mylist[229],mylist[40],mylist[72],mylist[374]])
    mysent.append([mylist[203],mylist[108],mylist[75],mylist[160],mylist[291],mylist[299]])
    mysent.append([mylist[203],mylist[108],mylist[256],mylist[74],mylist[826],mylist[378]])
    mysent.append([mylist[203],mylist[108],mylist[72],mylist[4],mylist[112],mylist[197]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[7],mylist[112],mylist[197]])
    mysent.append([mylist[203],mylist[108],mylist[379],mylist[292],mylist[176],mylist[238],mylist[383],mylist[291],mylist[710]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[291],mylist[710]])
# 170
    mysent.append([mylist[203],mylist[108],mylist[405],mylist[710]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[423],mylist[710]])
    mysent.append([mylist[203],mylist[40],mylist[424],mylist[425],mylist[74],mylist[427]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[72],mylist[449],mylist[450]])
    mysent.append([mylist[203],mylist[108],mylist[456],mylist[332],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[460],mylist[331],mylist[299]])
    mysent.append([mylist[203],mylist[71],mylist[204],mylist[74],mylist[78],mylist[205]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[206],mylist[121],mylist[75],mylist[78],mylist[827]])
    mysent.append([mylist[203],mylist[71],mylist[470],mylist[471]])
    mysent.append([mylist[203],mylist[108],mylist[828],mylist[367]])
# 180
    mysent.append([mylist[203],mylist[108],mylist[485],mylist[295]])
    mysent.append([mylist[203],mylist[108],mylist[183],mylist[540]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[829]])
    mysent.append([mylist[203],mylist[108],mylist[830]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[511],mylist[512]])
    mysent.append([mylist[203],mylist[110],mylist[71],mylist[831]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[532],mylist[160],mylist[367]])
    mysent.append([mylist[712],mylist[73],mylist[461]])
    mysent.append([mylist[203],mylist[108],mylist[531],mylist[540]])
    mysent.append([mylist[203],mylist[40],mylist[538],mylist[112],mylist[74],mylist[533]])
# 190
    mysent.append([mylist[203],mylist[40],mylist[541],mylist[112],mylist[74],mylist[533]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[275],mylist[292],mylist[540]])
    mysent.append([mylist[203],mylist[71],mylist[549],mylist[108],mylist[832]])
    mysent.append([mylist[203],mylist[108],mylist[564],mylist[299]])
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[566],mylist[74],mylist[72],mylist[567],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[90],mylist[75],mylist[567],mylist[367]])
    mysent.append([mylist[203],mylist[71],mylist[748],mylist[121],mylist[582],mylist[410]])
    mysent.append([mylist[203],mylist[108],mylist[156],mylist[74],mylist[591]])
    mysent.append([mylist[203],mylist[71],mylist[592],mylist[593]])
    mysent.append([mylist[203],mylist[108],mylist[687],mylist[367]])
# 200
    mysent.append([mylist[203],mylist[108],mylist[693],mylist[833],mylist[367]])
    mysent.append([mylist[203],mylist[108],mylist[702],mylist[367]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[709],mylist[292],mylist[710]])
    mysent.append([mylist[712],mylist[98]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[274],mylist[383],mylist[291],mylist[710]])
    mysent.append([mylist[381],mylist[82],mylist[254],mylist[383],mylist[202]])
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[75],mylist[166],mylist[182],mylist[108],mylist[75],mylist[95],mylist[717],mylist[718]])
    mysent.append([mylist[203],mylist[108],mylist[837]])
    mysent.append([mylist[203],mylist[108],mylist[734],mylist[367]])
    mysent.append([mylist[203],mylist[108],mylist[735],mylist[367]])
# 210
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[379],mylist[291],mylist[710]])
    mysent.append([mylist[203],mylist[71],mylist[748],mylist[74],mylist[749],mylist[379],mylist[838]])
    mysent.append([mylist[203],mylist[71],mylist[204],mylist[74],mylist[754]])
    mysent.append([mylist[203],mylist[108],mylist[839],mylist[367]])
    mysent.append([mylist[203],mylist[71],mylist[5],mylist[73],mylist[74],mylist[840],mylist[841],mylist[367]])
    mysent.append([mylist[203],mylist[71],mylist[4],mylist[73],mylist[74],mylist[840],mylist[841],mylist[367]])
    mysent.append([mylist[203],mylist[108],mylist[5],mylist[205]])
    mysent.append([mylist[203],mylist[108],mylist[4],mylist[205]])
    mysent.append([mylist[203],mylist[108],mylist[292],mylist[297],mylist[540]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[787],mylist[367]])
# 220
    mysent.append([mylist[712],mylist[73],mylist[299]])
    mysent.append([mylist[203],mylist[108],mylist[650],mylist[298],mylist[299]])
    mysent.append([mylist[203],mylist[108],mylist[799],mylist[718]])
    mysent.append([mylist[203],mylist[71],mylist[807],mylist[842]])
    mysent.append([mylist[68],mylist[69],mylist[108],mylist[75],mylist[300],mylist[74],mylist[304],mylist[271],mylist[302],mylist[133],mylist[809]])
# 225 - 247 are blank for dups of sentence 101 & 224
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 230
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 240
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 244  You are on a brink next to a pit. (fixed)
    mysent.append([mylist[68],mylist[69],mylist[40],mylist[75],mylist[463],mylist[321],mylist[61],mylist[75],mylist[205]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 248
    mysent.append([mylist[84],mylist[843],mylist[844],mylist[845],mylist[341],mylist[360],mylist[72],mylist[846],mylist[847],mylist[135],mylist[72],mylist[210]])
    mysent.append([mylist[84],mylist[497],mylist[568],mylist[40],mylist[72],mylist[845],mylist[848],mylist[849],mylist[850],mylist[851]])
# 250 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[84],mylist[857],mylist[858],mylist[859],mylist[393],mylist[72],mylist[845],mylist[88],mylist[860],mylist[65],mylist[45],mylist[861],mylist[75],mylist[451],mylist[77],mylist[65],mylist[387],mylist[862]])
# 252 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[88],mylist[864],mylist[362],mylist[87],mylist[74],mylist[342]])
    mysent.append([mylist[99],mylist[843],mylist[865],mylist[121],mylist[65],mylist[88],mylist[174],mylist[866],mylist[867],mylist[868],mylist[869],mylist[135],mylist[72],mylist[533]])
    mysent.append([mylist[68],mylist[69],mylist[870],mylist[871],mylist[72],mylist[872]])
    mysent.append([mylist[203],mylist[388],mylist[873],mylist[874]])
# 257 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[68],mylist[447],mylist[386],mylist[446],mylist[75],mylist[881],mylist[149],mylist[882]])
# 259 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[114],mylist[82],mylist[887],mylist[579],mylist[360],mylist[72],mylist[250]])
# 261 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[68],mylist[891],mylist[37],mylist[892],mylist[108],mylist[72],mylist[893],mylist[894],mylist[879],mylist[61],mylist[37],mylist[895]])
    mysent.append([mylist[68],mylist[896],mylist[104],mylist[876],mylist[148],mylist[897],mylist[61],mylist[38],mylist[72],mylist[898]])
# 264 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[114],mylist[69],mylist[543],mylist[905],mylist[723],mylist[181],mylist[72],mylist[906],mylist[102],mylist[103]])
    mysent.append([mylist[907],mylist[181],mylist[72],mylist[908],mylist[102],mylist[65],mylist[909],mylist[75],mylist[910],mylist[911],mylist[912],mylist[913],mylist[914],mylist[915],mylist[916],mylist[917],mylist[14],mylist[133],mylist[306],mylist[918],mylist[88],mylist[919],mylist[264],mylist[362],mylist[121],mylist[920],mylist[452],mylist[122],mylist[108],mylist[72],mylist[921],mylist[922],mylist[923],mylist[131],mylist[451],mylist[88],mylist[924],mylist[135],mylist[72],mylist[925]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[926],mylist[74],mylist[927],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[928],mylist[929],mylist[788],mylist[930]])
    mysent.append([mylist[114],mylist[82],mylist[399],mylist[931],mylist[932],mylist[202]])
# 270 is blank
    mysent.append([mylist[0]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[934],mylist[198],mylist[935],mylist[936],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[937],mylist[271],mylist[198],mylist[930]])
    mysent.append([mylist[84],mylist[749],mylist[285],mylist[938],mylist[939],mylist[121],mylist[75],mylist[940],mylist[941],mylist[40],mylist[123],mylist[73],mylist[942],mylist[930]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[198],mylist[108],mylist[75],mylist[935],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[933],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[271],mylist[943],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[945],mylist[202]])
    mysent.append([mylist[114],mylist[82],mylist[399],mylist[784],mylist[202]])
    mysent.append([mylist[114],mylist[69],mylist[318],mylist[946]])
# 280
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[947],mylist[948],mylist[946]])
    mysent.append([mylist[114],mylist[69],mylist[949],mylist[74],mylist[950],mylist[951],mylist[952],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[953],mylist[209],mylist[900],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[458],mylist[954],mylist[955],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[174],mylist[956],mylist[957],mylist[958],mylist[959],mylist[936],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[960],mylist[961],mylist[962],mylist[944],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[963],mylist[964],mylist[946]])
    mysent.append([mylist[0]])
    mysent.append([mylist[114],mylist[69],mylist[928],mylist[966],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[274],mylist[95],mylist[967],mylist[968],mylist[202]])
# 290
    mysent.append([mylist[114],mylist[69],mylist[947],mylist[969],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[970],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[95],mylist[821],mylist[74],mylist[822],mylist[946]])
    mysent.append([mylist[114],mylist[69],mylist[971],mylist[74],mylist[972],mylist[946]])
    mysent.append([mylist[114],mylist[82],mylist[973],mylist[974],mylist[944],mylist[946]])
    mysent.append([mylist[68],mylist[69],mylist[975],mylist[976],mylist[393],mylist[75],mylist[274],mylist[532],mylist[977],mylist[978]])
    mysent.append([mylist[979],mylist[788],mylist[82],mylist[765],mylist[216]])
    mysent.append([mylist[979],mylist[788],mylist[82],mylist[765],mylist[980]])
    mysent.append([mylist[0]])
    mysent.append([mylist[883],mylist[981],mylist[15],mylist[879],mylist[230],mylist[82],mylist[388],mylist[1430]])
# 300
    mysent.append([mylist[982],mylist[983]])
    mysent.append([mylist[984],mylist[65],mylist[985],mylist[886],mylist[61],mylist[3],mylist[986]])
    mysent.append([mylist[114],mylist[82],mylist[987],mylist[212],mylist[61],mylist[988]])
    mysent.append([mylist[84],mylist[338],mylist[954],mylist[989],mylist[990],mylist[971],mylist[72],mylist[991]])
    mysent.append([mylist[992],mylist[72],mylist[990],mylist[117],mylist[993],mylist[994],mylist[88],mylist[82],mylist[274],mylist[995]])
    mysent.append([mylist[996],mylist[131],mylist[141],mylist[997]])
    mysent.append([mylist[68],mylist[998],mylist[371],mylist[389],mylist[61],mylist[999],mylist[72],mylist[1000],mylist[173],mylist[65],mylist[739],mylist[388],mylist[875],mylist[324]])
    mysent.append([mylist[99],mylist[198],mylist[1001],mylist[1002],mylist[1003],mylist[65],mylist[1004],mylist[173],mylist[234],mylist[65],mylist[1005],mylist[264],mylist[168],mylist[1006],mylist[88],mylist[65],mylist[981],mylist[999],mylist[324]])
    mysent.append([mylist[99],mylist[271],mylist[198],mylist[1007],mylist[72],mylist[954],mylist[1008],mylist[88],mylist[108],mylist[174],mylist[1009],mylist[1010],mylist[1011],mylist[72],mylist[990],mylist[904]])
    mysent.append([mylist[1012],mylist[1013],mylist[99],mylist[1014],mylist[271],mylist[943],mylist[1015],mylist[1016]])
# 310
    mysent.append([mylist[84],mylist[1017],mylist[917],mylist[105],mylist[283],mylist[75],mylist[1018],mylist[1019],mylist[403],mylist[88],mylist[1020],mylist[75],mylist[271],mylist[943],mylist[71],mylist[1016]])
    mysent.append([mylist[99],mylist[943],mylist[1021],mylist[1016]])
    mysent.append([mylist[68],mylist[1024],mylist[75],mylist[271],mylist[1025],mylist[99],mylist[1446],mylist[924],mylist[108],mylist[75],mylist[428],mylist[74],mylist[1447],mylist[938],mylist[1448]])
    mysent.append([mylist[68],mylist[43],mylist[75],mylist[271],mylist[1026],mylist[173],mylist[1027],mylist[1028],mylist[87],mylist[74],mylist[72],mylist[1029]])
    mysent.append([mylist[68],mylist[43],mylist[75],mylist[271],mylist[1026],mylist[173],mylist[1027],mylist[1028],mylist[87],mylist[74],mylist[72],mylist[579],mylist[88],mylist[1030],mylist[65],mylist[121],mylist[1031],mylist[1014],mylist[488],mylist[1032]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1033],mylist[940],mylist[1034],mylist[1035],mylist[202]])
    mysent.append([mylist[99],mylist[1035],mylist[82],mylist[1036]])
    mysent.append([mylist[99],mylist[940],mylist[1035],mylist[82],mylist[1037]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 320
    mysent.append([mylist[68],mylist[981],mylist[386],mylist[12],mylist[61],mylist[72],mylist[286],mylist[278],mylist[399],mylist[579],mylist[61],mylist[1042]])
    mysent.append([mylist[146],mylist[74],mylist[927]])
    mysent.append([mylist[1043],mylist[788]])
    mysent.append([mylist[0]])
    mysent.append([mylist[1045],mylist[932]])
    mysent.append([mylist[1046],mylist[933]])
    mysent.append([mylist[934],mylist[198],mylist[935]])
    mysent.append([mylist[1047],mylist[939]])
    mysent.append([mylist[1048],mylist[198]])
    mysent.append([mylist[1046],mylist[933],mylist[121],mylist[48]])
# 330
    mysent.append([mylist[1049]])
    mysent.append([mylist[1050],mylist[945]])
    mysent.append([mylist[1051]])
    mysent.append([mylist[1052]])
    mysent.append([mylist[1053],mylist[948]])
    mysent.append([mylist[1054]])
    mysent.append([mylist[1055],mylist[900]])
    mysent.append([mylist[1056],mylist[955]])
    mysent.append([mylist[957],mylist[959]])
    mysent.append([mylist[961],mylist[962]])
# 340
    mysent.append([mylist[1057]])
    mysent.append([mylist[1058]])
    mysent.append([mylist[1059],mylist[968]])
    mysent.append([mylist[1053],mylist[969]])
    mysent.append([mylist[1060]])
    mysent.append([mylist[1061],mylist[821]])
    mysent.append([mylist[1062],mylist[971]])
    mysent.append([mylist[1063],mylist[1064],mylist[82],mylist[1543],mylist[781],mylist[1067],mylist[104],mylist[1068],mylist[1069],mylist[108],mylist[451],mylist[88],mylist[1070],mylist[1071],mylist[264],mylist[82],mylist[1072],mylist[230],mylist[399],mylist[416],mylist[28],mylist[69],mylist[1073],mylist[372],mylist[812],mylist[1074],mylist[82],mylist[1075],mylist[61],mylist[994],mylist[108],mylist[72],mylist[1076],mylist[883],mylist[891],mylist[371],mylist[131],mylist[1077],mylist[88],mylist[1078],mylist[1079],mylist[920],mylist[121],mylist[1080],mylist[74],mylist[1081],mylist[524],mylist[1082],mylist[1083],mylist[883],mylist[1084],mylist[1085],mylist[65],mylist[230],mylist[883],mylist[17],mylist[71],mylist[578],mylist[72],mylist[1086],mylist[490],mylist[1087],mylist[74],mylist[1088],mylist[1089],mylist[1090],mylist[65],mylist[37],mylist[1091],mylist[1092],mylist[1093],mylist[94],mylist[399],mylist[1094],mylist[1095]])
    mysent.append([mylist[883],mylist[1096],mylist[74],mylist[1097],mylist[1098],mylist[88],mylist[1099],mylist[1100],mylist[74],mylist[1101],mylist[1102],mylist[1103],mylist[1104],mylist[88],mylist[82],mylist[1105],mylist[61],mylist[1106],mylist[65],mylist[1107],mylist[270],mylist[1108],mylist[1109],mylist[57],mylist[66],mylist[1110],mylist[1111],mylist[1112],mylist[1113],mylist[1114],mylist[1115],mylist[521],mylist[522],mylist[523],mylist[524],mylist[525],mylist[883],mylist[1096],mylist[390],mylist[75],mylist[1116],mylist[1117],mylist[1118],mylist[66],mylist[75],mylist[938],mylist[939],mylist[1119],mylist[108],mylist[72],mylist[1076],mylist[1120],mylist[1121],mylist[370],mylist[371],mylist[1122],mylist[1123],mylist[399],mylist[74],mylist[72],mylist[1124],mylist[57],mylist[230],mylist[883],mylist[1125],mylist[1126],mylist[65],mylist[891],mylist[1127],mylist[61],\
    mylist[1128],mylist[117],mylist[72],mylist[1129],mylist[88],mylist[1124],mylist[57],mylist[1130],mylist[420],mylist[1131],mylist[173],mylist[1132],mylist[883],mylist[370],mylist[1133],mylist[72],mylist[1129],mylist[181],mylist[72],mylist[1134],mylist[1135],mylist[1136],mylist[1121],mylist[478],mylist[1137],mylist[1138],mylist[108],mylist[1139],mylist[1140],mylist[1141],mylist[1142],mylist[1143],mylist[340],mylist[1144],mylist[920],mylist[61],mylist[1128],mylist[65],mylist[75],mylist[1145],mylist[74],mylist[885],mylist[889],mylist[1146],mylist[99],mylist[1121],mylist[104],mylist[112],mylist[1147],mylist[94],mylist[1148],mylist[72],mylist[939],mylist[1149],mylist[72],mylist[1150],mylist[1126],mylist[1151],mylist[744],mylist[1152],mylist[1153],mylist[917],mylist[1127],mylist[61],mylist[1109],mylist[75],mylist[1116],mylist[1154],mylist[1083],mylist[1126],mylist[1151],mylist[1155],mylist[1156],mylist[61],mylist[1157],mylist[174],\
    mylist[1129],mylist[69],mylist[1158],mylist[879],mylist[503],mylist[1159],mylist[1160],mylist[1161],mylist[1162],mylist[1163],mylist[88],mylist[1084],mylist[1109],mylist[75],mylist[574],mylist[1164],mylist[1165],mylist[270],mylist[1166],mylist[72],mylist[1167],mylist[65],mylist[370],mylist[1132],mylist[1106],mylist[275],mylist[1168],mylist[121],mylist[75],mylist[1169],mylist[1089],mylist[1170],mylist[1171],mylist[1172],mylist[1173],mylist[1174],mylist[65],mylist[61],mylist[72],mylist[26],mylist[181],mylist[1175],mylist[238],mylist[1176],mylist[213],mylist[1003],mylist[1177],mylist[108],mylist[72],mylist[83],mylist[1178],mylist[259],mylist[230],mylist[589],mylist[247],mylist[1179],mylist[75],mylist[1180],mylist[88],mylist[230],mylist[1181],mylist[75],mylist[46],mylist[61],mylist[72],mylist[6],mylist[1182],mylist[388],mylist[1183],mylist[1184],mylist[72],mylist[321],mylist[181],mylist[72],mylist[685],mylist[1185],mylist[1186]])
    mysent.append([mylist[68],mylist[447],mylist[386],mylist[230],mylist[1187],mylist[181],mylist[202]])
# 350
    mysent.append([mylist[114],mylist[82],mylist[887],mylist[579],mylist[61],mylist[1188],mylist[108],mylist[230],mylist[1189]])
    mysent.append([mylist[1190],mylist[1191],mylist[1109],mylist[399],mylist[111],mylist[554]])
    mysent.append([mylist[1192]])
    mysent.append([mylist[68],mylist[104],mylist[887],mylist[1193]])
    mysent.append([mylist[99],mylist[150],mylist[82],mylist[1194]])
    mysent.append([mylist[99],mylist[150],mylist[82],mylist[1195]])
    mysent.append([mylist[84],mylist[1196],mylist[845],mylist[765],mylist[1197],mylist[72],mylist[250]])
    mysent.append([mylist[883],mylist[1271],mylist[887],mylist[1017],mylist[202]])
    mysent.append([mylist[68],mylist[981],mylist[37],mylist[1198],mylist[72],mylist[1199]])
    mysent.append([mylist[381],mylist[82],mylist[765],mylist[1200],mylist[1201],mylist[385],mylist[65],mylist[1188],mylist[65],mylist[891],mylist[1202],mylist[1203],mylist[135],mylist[75],mylist[205]])
# 360
    mysent.append([mylist[84],mylist[1204],mylist[1205],mylist[499],mylist[1206]])
    mysent.append([mylist[0]])
    mysent.append([mylist[68],mylist[981],mylist[37],mylist[1198],mylist[72],mylist[1210]])
    mysent.append([mylist[84],mylist[1033],mylist[218],mylist[1211],mylist[1212],mylist[108],mylist[72],mylist[330],mylist[1213],mylist[40],mylist[1214],mylist[639],mylist[135],mylist[72],mylist[735],mylist[572]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[468],mylist[271],mylist[1215],mylist[108],mylist[72],mylist[339],mylist[1216],mylist[1217],mylist[1218],mylist[1219],mylist[1219],mylist[1219]])
    mysent.append([mylist[99],mylist[1215],mylist[1220],mylist[135],mylist[1221],mylist[1222],mylist[94],mylist[75],mylist[1116],mylist[1223]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1224],mylist[1225],mylist[224],mylist[12],mylist[87],mylist[74],mylist[72],mylist[205]])
    mysent.append([mylist[381],mylist[82],mylist[1226],mylist[1227],mylist[1228],mylist[1229],mylist[1228]])
    mysent.append([mylist[99],mylist[1215],mylist[1230],mylist[1231],mylist[233],mylist[1232],mylist[72],mylist[466],mylist[74],mylist[72],mylist[205]])
    mysent.append([mylist[68],mylist[104],mylist[1233],mylist[72],mylist[1234],mylist[381],mylist[199],mylist[1235],mylist[1236]])
# 370
    mysent.append([mylist[114],mylist[82],mylist[765],mylist[75],mylist[1237],mylist[1225],mylist[224],mylist[133],mylist[72],mylist[579],mylist[12],mylist[61],mylist[75],mylist[286],mylist[479]])
    mysent.append([mylist[99],mylist[1033],mylist[1238],mylist[121],mylist[1239],mylist[1240],mylist[981],mylist[371],mylist[1241],mylist[278],mylist[399],mylist[1242]])
    mysent.append([mylist[1243],mylist[1244],mylist[65],mylist[15],mylist[1245]])
    mysent.append([mylist[1246],mylist[996],mylist[987],mylist[702],mylist[61],mylist[1247],mylist[1248],mylist[72],mylist[956],mylist[959],mylist[1249],mylist[72],mylist[273]])
    mysent.append([mylist[1250],mylist[74],mylist[72],mylist[959],mylist[1251],mylist[1252],mylist[1253]])
    mysent.append([mylist[68],mylist[104],mylist[887],mylist[1254],mylist[74],mylist[1255]])
    mysent.append([mylist[114],mylist[82],mylist[987],mylist[212],mylist[264],mylist[1556],mylist[61],mylist[1563],mylist[1557]])
    mysent.append([mylist[99],mylist[1261],mylist[968],mylist[1262],mylist[131],mylist[1259]])
    mysent.append([mylist[99],mylist[822],mylist[948],mylist[82],mylist[1263],mylist[181],mylist[72],mylist[968],mylist[88],mylist[82],mylist[1264],mylist[181],mylist[72],mylist[589],mylist[260]])
    mysent.append([mylist[68],mylist[886],mylist[72],mylist[932],mylist[94],mylist[267],mylist[1265]])
# 380
    mysent.append([mylist[1266],mylist[578],mylist[1267],mylist[75],mylist[968],mylist[1003],mylist[363],mylist[82],mylist[75],mylist[567],mylist[367]])
    mysent.append([mylist[984],mylist[388],mylist[1268],mylist[1269]])
    mysent.append([mylist[883],mylist[1270],mylist[388],mylist[1271],mylist[75],mylist[1215],mylist[202]])
    mysent.append([mylist[68],mylist[1270],mylist[388],mylist[104],mylist[75],mylist[933],mylist[996],mylist[1272]])
    mysent.append([mylist[114],mylist[82],mylist[887],mylist[48],mylist[108],mylist[72],mylist[1273],mylist[1274],mylist[1275],mylist[48],mylist[88],mylist[1276],mylist[1277]])
    mysent.append([mylist[114],mylist[82],mylist[887],mylist[48],mylist[202]])
    mysent.append([mylist[883],mylist[370],mylist[578],mylist[53],mylist[72],mylist[933],mylist[121],mylist[1272]])
    mysent.append([mylist[68],mylist[1270],mylist[388],mylist[104],mylist[75],mylist[1273]])
    mysent.append([mylist[0]])
    mysent.append([mylist[68],mylist[69],mylist[412],mylist[75],mylist[1279],mylist[1280],mylist[1281],mylist[1282],mylist[321],mylist[1283]])
# 390
    mysent.append([mylist[979],mylist[35],mylist[1284],mylist[65],mylist[234],mylist[75],mylist[1285],mylist[1286]])
    mysent.append([mylist[68],mylist[104],mylist[1287],mylist[72],mylist[1288],mylist[1289],mylist[1290]])
    mysent.append([mylist[68],mylist[387],mylist[765],mylist[1291],mylist[1292],mylist[75],mylist[1293],mylist[1290]])
    mysent.append([mylist[68],mylist[104],mylist[1294],mylist[1295],mylist[1296],mylist[1297]])
    mysent.append([mylist[979],mylist[35],mylist[1298],mylist[65],mylist[108],mylist[1299],mylist[1300],mylist[1301],mylist[1302]])
    mysent.append([mylist[979],mylist[35],mylist[1298],mylist[65],mylist[108],mylist[1299],mylist[1300],mylist[1301],mylist[1303]])
    mysent.append([mylist[979],mylist[35],mylist[1298],mylist[65],mylist[108],mylist[1299],mylist[1300],mylist[1301],mylist[1304]])
    mysent.append([mylist[1250],mylist[74],mylist[1305],mylist[1306],mylist[1307],mylist[61],mylist[403],mylist[1300],mylist[1308]])
    mysent.append([mylist[1266],mylist[1309],mylist[75],mylist[939],mylist[61],mylist[36],mylist[293]])
    mysent.append([mylist[99],mylist[1196],mylist[845],mylist[199],mylist[1310]])
# 400
    mysent.append([mylist[1311],mylist[1312]])
    mysent.append([mylist[68],mylist[69],mylist[388],mylist[871],mylist[75],mylist[1313]])
    mysent.append([mylist[68],mylist[1270],mylist[388],mylist[104],mylist[75],mylist[1150]])
    mysent.append([mylist[99],mylist[198],mylist[1314],mylist[110],mylist[61],mylist[656],mylist[1315]])
    mysent.append([mylist[1542]])
    mysent.append([mylist[883],mylist[981],mylist[1318],mylist[885],mylist[65],mylist[1319],mylist[524],mylist[1318],mylist[264],mylist[212],mylist[524],mylist[1318],mylist[264],mylist[1320]])
    mysent.append([mylist[84],mylist[899],mylist[900],mylist[901],mylist[87],mylist[74],mylist[72],mylist[1321],mylist[88],mylist[903],mylist[61],mylist[75],mylist[286],mylist[108],mylist[72],mylist[273]])
    mysent.append([mylist[99],mylist[1321],mylist[1322],mylist[94],mylist[75],mylist[1323],mylist[61],mylist[1324],mylist[781],mylist[75],mylist[899],mylist[900],mylist[1105],mylist[61],mylist[1325]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 410
    mysent.append([mylist[68],mylist[1270],mylist[388],mylist[104],mylist[75],mylist[1328]])
    mysent.append([mylist[883],mylist[1270],mylist[388],mylist[1271],mylist[75],mylist[1199]])
    mysent.append([mylist[68],mylist[104],mylist[75],mylist[947],mylist[1329],mylist[1330],mylist[6],mylist[74],mylist[202]])
    mysent.append([mylist[883],mylist[981],mylist[1331],mylist[885],mylist[65],mylist[1319],mylist[524],mylist[1331],mylist[264],mylist[212],mylist[524],mylist[1331],mylist[264],mylist[1320]])
    mysent.append([mylist[883],mylist[981],mylist[1332],mylist[885],mylist[65],mylist[1319],mylist[524],mylist[1332],mylist[264],mylist[212],mylist[524],mylist[1332],mylist[264],mylist[1320]])
    mysent.append([mylist[1333],mylist[72],mylist[954],mylist[1334],mylist[74],mylist[174],mylist[955],mylist[172],mylist[123],mylist[1309],mylist[75],mylist[788],mylist[61],mylist[1335]])
    mysent.append([mylist[381],mylist[82],mylist[254],mylist[1336],mylist[61],mylist[386],mylist[121],mylist[72],mylist[788],mylist[980]])
    mysent.append([mylist[1012],mylist[1337],mylist[68],mylist[104],mylist[757],mylist[135],mylist[75],mylist[205]])
    mysent.append([mylist[68],mylist[104],mylist[331],mylist[1338],mylist[1339],mylist[72],mylist[1340]])
    mysent.append([mylist[1341]])
# 420
    mysent.append([mylist[883],mylist[1270],mylist[388],mylist[1271],mylist[75],mylist[1207],mylist[202]])
    mysent.append([mylist[883],mylist[981],mylist[14],mylist[75],mylist[962],mylist[1342],mylist[75],mylist[1343],mylist[1207],mylist[82],mylist[944],mylist[40],mylist[324]])
    mysent.append([mylist[1344],mylist[68],mylist[104],mylist[917],mylist[1345],mylist[75],mylist[1207],mylist[121],mylist[131],mylist[141],mylist[1346]])
    mysent.append([mylist[99],mylist[308],mylist[309],mylist[1347],mylist[75],mylist[545],mylist[88],mylist[131],mylist[788],mylist[82],mylist[765],mylist[1348]])
    mysent.append([mylist[0]])
    mysent.append([mylist[883],mylist[1349],mylist[65],mylist[886],mylist[61],mylist[1350],mylist[1351]])
    mysent.append([mylist[883],mylist[1270],mylist[388],mylist[1271],mylist[75],mylist[845],mylist[202]])
    mysent.append([mylist[1065],mylist[82],mylist[1355],mylist[1354],mylist[40],mylist[1356],mylist[393],mylist[1357],mylist[1358],mylist[1359],mylist[1066]])
    mysent.append([mylist[99],mylist[1360],mylist[240],mylist[40],mylist[1361],mylist[1362],mylist[1363],mylist[1364],mylist[1365],mylist[393],mylist[1366],mylist[1367],mylist[1368]])
    mysent.append([mylist[686],mylist[1361],mylist[1364],mylist[1369],mylist[1360],mylist[1370],mylist[1355],mylist[1354],mylist[40],mylist[1371],mylist[401],mylist[1353],mylist[1372]])
# 430
    mysent.append([mylist[1373],mylist[1374],mylist[264],mylist[240],mylist[108],mylist[1375],mylist[1376],mylist[74],mylist[1377],mylist[121],mylist[887],mylist[1378],mylist[1379]])
    mysent.append([mylist[381],mylist[199],mylist[1380],mylist[1124],mylist[1381],mylist[1382],mylist[1118],mylist[1383],mylist[1384],mylist[1385],mylist[1386],mylist[88],mylist[1387],mylist[1083]])
    mysent.append([mylist[1388],mylist[1389],mylist[1390],mylist[1391],mylist[1392],mylist[1393],mylist[1394],mylist[1371],mylist[1395]])
    mysent.append([mylist[1396],mylist[1397]])
    mysent.append([mylist[1398],mylist[1399]])
    mysent.append([mylist[1400]])
    mysent.append([mylist[979],mylist[788],mylist[552],mylist[61],mylist[371],mylist[1401],mylist[1402],mylist[1403],mylist[65],mylist[365],mylist[94],mylist[1404],mylist[1405]])
    mysent.append([mylist[979],mylist[788],mylist[1406],mylist[82],mylist[233],mylist[1407],mylist[1408],mylist[363],mylist[75],mylist[206],mylist[1409]])
    mysent.append([mylist[99],mylist[788],mylist[1406],mylist[82],mylist[765],mylist[1407],mylist[68],mylist[69],mylist[108],mylist[1410],mylist[1411]])
    mysent.append([mylist[1412],mylist[65],mylist[28],mylist[72],mylist[329],mylist[363],mylist[82],mylist[75],mylist[1413],mylist[1414],mylist[75],mylist[1415],mylist[736]])
# 440
    mysent.append([mylist[0]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1207],mylist[1208],mylist[87],mylist[40],mylist[72],mylist[1209]])
    mysent.append([mylist[0]])
    mysent.append([mylist[1416],mylist[74],mylist[950],mylist[951],mylist[202]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
# 450
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[0]])
    mysent.append([mylist[883],mylist[981],mylist[45],mylist[879],mylist[230],mylist[65],mylist[1270],mylist[388],mylist[1429]])
    mysent.append([mylist[1412],mylist[72],mylist[933],mylist[1249],mylist[72],mylist[743],mylist[72],mylist[48],mylist[806]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1432],mylist[1431]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1433],mylist[1431]])
# 460
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1434],mylist[1431]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1435],mylist[1431]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1436],mylist[1431]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1437],mylist[1431]])
    mysent.append([mylist[99],mylist[321],mylist[1279],mylist[82],mylist[1438],mylist[1431]])
    mysent.append([mylist[68],mylist[104],mylist[1439],mylist[283],mylist[108],mylist[75],mylist[271],mylist[167],mylist[6],mylist[74],mylist[88],mylist[407],mylist[61],mylist[72],mylist[256],mylist[74],mylist[257]])
    mysent.append([mylist[1445],mylist[182]])
    mysent.append([mylist[99],mylist[1017],mylist[1022],mylist[88],mylist[1023],mylist[904]])
    mysent.append([mylist[84],mylist[1014],mylist[271],mylist[1017],mylist[82],mylist[930]])
    mysent.append([mylist[84],mylist[1449],mylist[1205],mylist[1450],mylist[446],mylist[72],mylist[589],mylist[261],mylist[500],mylist[1451],mylist[1452],mylist[1250],mylist[1453],mylist[29],mylist[1454],mylist[446],mylist[72],mylist[1455],mylist[1456]])
# 470
    mysent.append([mylist[99],mylist[1449],mylist[1205],mylist[1459],mylist[1460],mylist[589],mylist[82],mylist[765],mylist[1461],mylist[1412],mylist[72],mylist[1462],mylist[1463],mylist[363],mylist[82],mylist[75],mylist[1464],mylist[1465],mylist[74],mylist[639],mylist[853],mylist[75],mylist[78],mylist[1466],mylist[74],mylist[192],mylist[1467],mylist[1412],mylist[131],mylist[1077],mylist[1470],mylist[65],mylist[17],mylist[283],mylist[88],mylist[1471]])	
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[1499],mylist[73],mylist[74],mylist[174],mylist[650],mylist[329],mylist[1491],mylist[72],mylist[787],mylist[367],mylist[381],mylist[1569],mylist[61],mylist[371],mylist[75],mylist[1492],mylist[94],mylist[72],mylist[1493],mylist[1494],mylist[402],mylist[440],mylist[1495],mylist[72],mylist[46],mylist[121],mylist[1496],mylist[1255],mylist[1497],mylist[390],mylist[65],mylist[123],mylist[370],mylist[1271],mylist[75],mylist[704],mylist[74],mylist[1498],mylist[1500],mylist[74],mylist[1501],mylist[75],mylist[1502],mylist[74],mylist[1503],mylist[1216],mylist[1504],mylist[75],mylist[1562],mylist[74],mylist[1505],mylist[75],mylist[1506],mylist[74],mylist[938],mylist[1507],mylist[121],mylist[940],mylist[1508],mylist[40],mylist[1159],mylist[1509],mylist[88],mylist[75],mylist[1510],mylist[74],mylist[929],mylist[1511],\
    mylist[1512],mylist[61],mylist[123],mylist[112],mylist[75],mylist[597],mylist[1513],mylist[1474],mylist[69],mylist[1514],mylist[40],mylist[72],mylist[743],mylist[1515],mylist[84],mylist[497],mylist[1064],mylist[569],mylist[1524],mylist[388],mylist[1525],mylist[72],mylist[1526],mylist[194],mylist[650],mylist[405],mylist[82],mylist[406],mylist[1527],mylist[123],mylist[421],mylist[88],mylist[1528],mylist[61],mylist[72],mylist[111],mylist[73],mylist[74],mylist[72],mylist[329],mylist[781],mylist[1529],mylist[111],mylist[1530],mylist[1121],mylist[370],mylist[371],mylist[1531],mylist[660],mylist[108],mylist[72],mylist[115]])	
    mysent.append([mylist[68],mylist[69],mylist[71],mylist[72],mylist[1516],mylist[73],mylist[74],mylist[72],mylist[1517],mylist[270],mylist[123],mylist[112],mylist[82],mylist[75],mylist[206],mylist[455],mylist[74],mylist[989],mylist[954],mylist[1518],mylist[791],mylist[72],mylist[111],mylist[112],mylist[82],mylist[75],mylist[1562],mylist[74],mylist[78],mylist[934],mylist[1519],mylist[1088],mylist[74],mylist[340],mylist[1520],mylist[75],mylist[271],mylist[1521],mylist[1150],mylist[305],mylist[123],mylist[785],mylist[82],mylist[75],mylist[1506],mylist[74],mylist[938],mylist[1507],mylist[121],mylist[940],mylist[1522],mylist[40],mylist[1159],mylist[1523],mylist[84],mylist[95],mylist[1532],mylist[74],mylist[1533],mylist[69],mylist[1534],mylist[390],mylist[40],mylist[72],mylist[273],mylist[84],mylist[221],mylist[405],mylist[1528],mylist[41],mylist[61],mylist[72],mylist[550],mylist[130],mylist[131],mylist[132],mylist[82],mylist[75],mylist[95],mylist[149],mylist[1535],mylist[321],mylist[61],mylist[340],mylist[82],mylist[75],mylist[497],mylist[340],mylist[848],mylist[1536],mylist[1537],mylist[108],mylist[1455],mylist[1456],mylist[99],mylist[150],mylist[82],mylist[1194]])	
    mysent.append([mylist[203],mylist[71],mylist[541],mylist[98]])	
    mysent.append([mylist[203],mylist[71],mylist[538],mylist[98],mylist[99],mylist[150],mylist[82],mylist[1194]])	
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[587],mylist[823],mylist[88],mylist[75],mylist[1472],mylist[286],mylist[1569],mylist[108],mylist[72],mylist[402],mylist[421],mylist[1473],mylist[72],mylist[1474],mylist[108],mylist[72],mylist[1475],mylist[68],mylist[386],mylist[446],mylist[72],mylist[286],mylist[88],mylist[1275],mylist[1292],mylist[108],mylist[72],mylist[1455],mylist[1476],mylist[781],mylist[75],mylist[1477],mylist[74],mylist[1478],mylist[875],mylist[403],mylist[72],mylist[1489],mylist[41],mylist[135],mylist[72],mylist[1490]])	
    mysent.append([mylist[883],mylist[1271],mylist[887],mylist[1538],mylist[202]])	
    mysent.append([mylist[883],mylist[1271],mylist[887],mylist[150],mylist[202]])	
    mysent.append([mylist[883],mylist[1271],mylist[987],mylist[61],mylist[33],mylist[202]])	
    mysent.append([mylist[99],mylist[271],mylist[198],mylist[1007],mylist[72],mylist[954],mylist[1207],mylist[88],mylist[108],mylist[174],mylist[1009],mylist[1010],mylist[1174],mylist[1539],mylist[61],mylist[75],mylist[1540],mylist[99],mylist[1565],mylist[1541],mylist[904]])
# 480
    mysent.append([mylist[114],mylist[69],mylist[960],mylist[1544],mylist[946]])
    mysent.append([mylist[960],mylist[1544]])
    mysent.append([mylist[270],mylist[1547]])
    mysent.append([mylist[99],mylist[968],mylist[82],mylist[881],mylist[61],mylist[72],mylist[330],mylist[121],mylist[75],mylist[947],mylist[1040]])
    mysent.append([mylist[114],mylist[82],mylist[887],mylist[579],mylist[61],mylist[37],mylist[1198],mylist[72],mylist[968],mylist[61],mylist[33],mylist[72],mylist[1550],mylist[340],mylist[82],mylist[1549],mylist[917],mylist[234],mylist[1548]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1551],mylist[589],mylist[968],mylist[1552],mylist[65],mylist[181],mylist[72],mylist[402],mylist[73],mylist[74],mylist[72],mylist[1553]])
    mysent.append([mylist[114],mylist[82],mylist[75],mylist[1554],mylist[968],mylist[1555],mylist[390],mylist[930]])
    mysent.append([mylist[1170],mylist[1558],mylist[414],mylist[72],mylist[1559],mylist[1560]])
    mysent.append([mylist[1568],mylist[108],mylist[935]])
# 489 new info
    mysent.append([mylist[1570],mylist[1571],mylist[1572],mylist[1573],mylist[1574],mylist[1575],mylist[1576],mylist[1577],mylist[1578],mylist[1579],mylist[1580], \
    mylist[1581],mylist[1582],mylist[1583],mylist[1584],mylist[1585],mylist[1586],mylist[1587],mylist[1588],mylist[1589],mylist[1590],mylist[1591],mylist[1592], \
    mylist[1593],mylist[1594],mylist[1595],mylist[1596],mylist[1597],mylist[1598],mylist[1599],mylist[1600],mylist[1601],mylist[1602],mylist[1603],mylist[1604], \
    mylist[1605],mylist[1606],mylist[1607],mylist[1608],mylist[1609],mylist[1610],mylist[1611],mylist[1612],mylist[1613],mylist[1614],mylist[1615],mylist[1616], \
    mylist[1617],mylist[1618],mylist[1619],mylist[1620],mylist[1621],mylist[1622],mylist[1623],mylist[1624],mylist[1625],mylist[1626],mylist[1627],mylist[1628], \
    mylist[1629],mylist[1630],mylist[1631],mylist[1632],mylist[1633],mylist[1634]])
    return mysent
#
# only used to review the converted word list
#
def word_review(mylist,base):
    x = int(base)
    while x < int(base) + 100:
        print(str(x),mylist[x])
        x += 1
        if x > 1567:
            break
    return
#
#####################
# program starts here
#####################
mylist = mylist_init()
mysent = mysent_init()
myvars = myvars_init()
if 'Windows' == platform.system():
    import msvcrt
main_loop(mylist,mysent,myvars)
