#-To do List:
#  Transform enemy declarations all to one spot, rather than zone specific
#  create functional enemy AI other than attack
#  more zones
#  random encounters
#  item management
#  clean up pawnbroker code, abysmal

import rpgClass
import time
import os
import random

#assign globals, arbitrary values, overwrote in main
hero=rpgClass.Character(20,20,0,0,10,10,1,0,0,20)
inventory=[]
zone="Nowhere"

#--------Core Functions---------##--------Core Functions---------##--------Core Functions---------##--------Core Functions---------#


def validate(argList,default):
    if default != 'none':
        argList.append('')
        print "        Your command? [" + default.upper() + "] : ",
    else:
        print "        Your command?     : ",
    command=raw_input()
    while command.lower() not in (argList):
        command=raw_input("Invalid command, try again : ")
    if command != '':
        return command.lower()
    else:
        return default

def clrscr():
    os.system('CLS')
    
def sureToQuit():
    clrscr()
    print "Keep Playing Hobo Quest?"
    print
    print "(Q)uit"
    print "(B)ack to being a hobo, don't quit!"
    print
    command = validate(['q','b'],'b')
    if command == 'q':
        saveGame()
        print "\n\nThanks for playing!  Your game's been saved! \n\nPress enter to close."
        raw_input()
        import sys
        sys.exit()
    if command == 'b':
        global zone
        print "Returning back to the " + zone,
        dotdotdot()
        fastdotdotdot()
                
        
def dotdotdot():
    #time.sleep(.4)
    for x in range(3):
        print ".",
        #time.sleep(.4)
        
def fastdotdotdot():
    #time.sleep(.23)
    for x in range(3):
        print ".",
        #time.sleep(.23)
        
def slowdotdotdot():
    #time.sleep(1.6)
    for x in range(4):
        print ".",
        #time.sleep(1)
        
def displayStats():
    global hero, zone
    string = "| HP: " + str(hero.getHp()) + "/" + str(hero.getMaxHp()) + "    " + \
          "SP: " + str(hero.getSp()) + "/" + str(hero.getMaxSp()) + \
          "    Fights Left until Rest: " +  str(hero.getFights())
    string2 = "| Money: $" + str(hero.getMoney()) + "              Press (V) to view Stats + Inventory."
    
    hyphens=(65-len(zone))/2
    if len(zone)%2 == 1:
        string3 = "  \\" + '-'*hyphens + zone + '-'*hyphens + "/"
    else:
        string3 = "  \\-" + '-'*hyphens + zone + '-'*hyphens + "/"
    print
    print "  /----------------------------Hobo Quest---------------------------\\"
    print "  %-66s|" % string
    print "  %-66s|" % string2
    print string3
    print        


def death():
    clrscr()
    print "Oh good lord, oh the humanity!  You were so young!"
    import sys
    sys.exit("Try again, noob!  Preferably without the dying part!")
    
    
def win():
    clrscr()
    print "CONGRATULATIONS!  You're not a hobo anymore!  You got a job"
    print "and an apartment, and only had to kill and mug a few dozen people"
    print "to make it this far.  Maybe some day you'll rebuild your capital"
    print "enough to be a wall street investor again!"
    print 
    print "The End."
    zone = 'Quit'
    print
    raw_input("<Press Enter to Continue>\n")
    
def loadGame():
    global hero, inventory, zone
    try:
        inventory = []
        zone = ''
        gameFile = open("savegame.txt",'r')
        hero.setHp(int((gameFile.readline()).rstrip()))
        hero.setMaxHp(int((gameFile.readline()).rstrip()))
        hero.setSp(int((gameFile.readline()).rstrip()))
        hero.setMaxSp(int((gameFile.readline()).rstrip()))
        hero.setStr(int((gameFile.readline()).rstrip()))
        hero.setDef(int((gameFile.readline()).rstrip()))
        hero.setLvl(int((gameFile.readline()).rstrip()))
        hero.setExp(int((gameFile.readline()).rstrip()))
        hero.setMoney(int((gameFile.readline()).rstrip()))
        hero.setFights(int((gameFile.readline()).rstrip()))
        zone=((gameFile.readline()).rstrip())
        itemInfo = (gameFile.readline()).rstrip()
        while itemInfo != 'END':
            if itemInfo == 'Item':
                name = (gameFile.readline()).rstrip()
                value = int((gameFile.readline()).rstrip())
                inventory.append(rpgClass.Item(name,value))
            if itemInfo == 'Weapon':
                name = (gameFile.readline()).rstrip()
                value = int((gameFile.readline()).rstrip())
                mod = int((gameFile.readline()).rstrip())
                inventory.append(rpgClass.Weapon(name,value,mod))
            if itemInfo == 'Armor':
                name = (gameFile.readline()).rstrip()
                value = int((gameFile.readline()).rstrip())
                mod = int((gameFile.readline()).rstrip())
                inventory.append(rpgClass.Armor(name,value,mod))
            if itemInfo == 'Consumable':
                name = (gameFile.readline()).rstrip()
                value = int((gameFile.readline()).rstrip())
                effIndex = int((gameFile.readline()).rstrip())
                inventory.append(rpgClass.Consumable(name,value,effIndex))  
            itemInfo = (gameFile.readline()).rstrip()
        gameFile.close()
    except IOError:
        print "Oh crap, disaster while trying to load game!"
        print "savegame.txt doesn't exist, or is corrupt!"
        time.sleep(3)
        print "Something is wrong in this savegame!  Closing!  Armageddoooooooon!!!!"
        time.sleep(1)
        import sys
        sys.exit()
    
def saveGame():
    global hero, inventory, zone
    gameFile = open("savegame.txt",'w')
    gameFile.write(str(hero.getHp())+'\n')
    gameFile.write(str(hero.getMaxHp())+'\n')
    gameFile.write(str(hero.getSp())+'\n')
    gameFile.write(str(hero.getMaxSp())+'\n')
    gameFile.write(str(hero.getStr())+'\n')
    gameFile.write(str(hero.getDef())+'\n')
    gameFile.write(str(hero.getLvl())+'\n')
    gameFile.write(str(hero.getExp())+'\n')
    gameFile.write(str(hero.getMoney())+'\n')
    gameFile.write(str(hero.getFights())+'\n')
    gameFile.write(zone+'\n')
    for line in inventory:
        gameFile.write(line.dumpInfo())
    gameFile.write("END")
    gameFile.close()
    
#--------END Core Functions---------##--------END Core Functions---------##--------END Core Functions---------#
#--------Combat Functions---------##--------Combat Functions---------##--------Combat Functions---------##--------Combat Functions---------#
        
        
def initiateCombat(enemy):
    global hero
    if hero.getFights() <= 0:
        print "Can't fight anymore!  You need to rest!"
        time.sleep(2)
        fastdotdotdot()
    else:
        if enemy == "string":
            enemy = rpgClass.Enemy('Name',HP,MaxHp,Str,Def,Exp,Money,AIType)
        if not isinstance(enemy,rpgClass.Enemy):
            enemy = getRandomEnemy()
        print "\n\nYou've encountered a", enemy.getName(), "!!!\n\n"
        hero.fight()
        time.sleep(1.3)
        clrscr()
        combat(enemy)
    

def getRandomEnemy():
    global hero
    nameList = ['Drunk Guy','Thief','Cutpurse','Marion Barry','Thief','Repo Man', \
                'Bearded Lady', 'Osama Bin Laden', 'Thief']
    randName=nameList[random.randint(0,8)]
    enemy = rpgClass.Enemy(randName,hero.getLvl()*6+10,hero.getLvl()*6+10, \
                           hero.getLvl()*2+10, hero.getLvl()*2+4, \
                           hero.getLvl()*4+5, hero.getLvl()*4+2,1)
    return enemy

    
def combat(enemy):
    global hero
    victoryFlag = False
    skipEnemyTurn = False
    while victoryFlag != True:
        print enemy.getName()
        print "HP: ", enemy.getHp(), "/", enemy.getMaxHp()
        print
        print "You"
        print "HP: ", hero.getHp(), "/", hero.getMaxHp()
        print "SP: ", hero.getSp(), "/", hero.getMaxSp()
        print
        print "(A)ttack the " + enemy.getName()
        if hero.getSp() > 0:
            print "(C)ast a spell"
        print "(R)un away"
        print
        command=validate(['a','c','r'],'a')
        #------------------------------User action                                        
        if command == 'a':
            damage = hero.getStr() - 6 + equippedWeaponMod() + random.randint(1,10) - enemy.getDef()
            clrscr()
            print "You attack with your " + equippedWeaponName() + ".",
            dotdotdot()
            critical=random.randint(1,15)
            if critical >= 14:
                damage = damage * 3
                print "And critically hit!\n"
                critText(enemy.getName(), damage)
                enemy.setHp(enemy.getHp()-damage)
                time.sleep(1.25)
            elif damage > 0:
                print "And Hit!"
                print enemy.getName() + " takes", damage, "damage!!"
                enemy.setHp(enemy.getHp()-damage)
            if damage <= 0:
                print "And Miss!"
                print enemy.getName() + " laughs at your attempt!"
        elif command == 'r':
            exitChance = random.randint(1,20) - (2 * enemy.getMaxHp() / hero.getMaxHp())
            clrscr()           
            print "You attempt to run away.",          
            dotdotdot()
            if exitChance >= 6:
                print "And flee like a little girl!"
                time.sleep(2)
                return
            else:
                print "And fail horribly!"
        elif command == 'c' and hero.getSp() > 0:
            damage = castSpell(enemy.getName())
            print "\n" + enemy.getName() + " takes ", damage, " damage!!"
            time.sleep(1.25)
            enemy.setHp(enemy.getHp()-damage)
        else:
            print "You don't have any spell points to cast a spell!"
            skipEnemyTurn = True
        #------------------------------End User Action                                      
        time.sleep(1.25)
        if enemy.getHp() <= 0:
            victoryFlag=True
            victory(enemy.getName(), enemy.getExp(), enemy.getMoney())
        else:
            if skipEnemyTurn == True:
                skipEnemyTurn == False
                clrscr()
            else:
                enemyAction = random.randint(1,10)
                if enemy.getAIType() == 1 or enemyAction >= 5:
                    damage = enemy.getStr() + random.randint(1,10) - hero.getDef() - equippedArmorMod()
                    print "\n"
                    print enemy.getName() + " attacks you.",
                    fastdotdotdot()
                    if damage > 0:    
                        print " and hits!  You take ", damage, "damage!"
                        hero.setHp(hero.getHp()-damage)
                    if damage <= 0:
                        print "you dodge!"
                if enemy.getAIType() == 2 and enemyAction < 5:
                    print "\n"
                    print "The policeman rushes at you, tazers you and attempts to arrest you!"
                    fastdotdotdot()
                    if random.randomint(1,5) == 5:
                        print "And he succeeds!  Oh crap, you're in big trouble now!"
                        print
                        print "<Press Enter to Continue>"
                        global zone
                        zone = "Jail"
                        return
                    else:
                        damage = enemy.getStr() + random.randint(5,10)
                        hero.setHp(hero.getHp()-damage)
                        print "And he electrocutes you for", damage, " but you resist arrest!"
                if enemy.getAIType() == 3 and enemyAction < 5:
                    print "\n"
                    print "The exec throws his PDA at your face!"
                    fastdotdotdot()
                    damage = enemy.getStr() + random.randint(5,10)
                    print "It was an old-generation blackberry!  Your nose is broke!"
                    print "He hit you for", damage, "damage!"
                    hero.setHp(hero.getHp()-damage)
                time.sleep(1.3)
                clrscr()
                if hero.getHp() <= 0:
                    death()
    
   
def castSpell(enemyName):
    global hero
    clrscr()
    print "You focus your hobo energies into your outstretched palm.",
    dotdotdot()
    print "\n"
    if hero.getLvl() in (2,3):
        print "You cast a barrage of magic hot baked beans at " + enemyName +" .",
        dotdotdot()
        damage = 20 + random.randint(1,20) + (hero.getLvl()*6)
        hero.setSp(hero.getSp() - 1)
    if hero.getLvl() in (4,5):
        print "You immolate " + enemyName + " in a burst of magic trashcan fire.",
        dotdotdot()
        damage = 30 + random.randint(1,30) + (hero.getLvl()*12)
        hero.setSp(hero.getSp() - 1)
    if hero.getLvl() in (6,7):
        dollars=random.randint(1,3)+4
        print "You telekinetically pick up " + enemyName + ", shake them upside down to" + \
              "\nempty their pockets of " + str(dollars) + ", and then slam them into \n" + \
              "a wall a half dozen times!",
        dotdotdot()
        damage = 40 + random.randint(1,40) + (hero.getLvl()*16)
        hero.setSp(hero.getSp() - 1)
        hero.setMoney(hero.getMoney()+dollars)
    if hero.getLvl() in (8,9):
        print "You hypnotize " + enemyName + " completely, and order it to go jump\n" + \
              "into the middle of the road.",
        dotdotdot()
        print "\nAnd is promptly struck by a Big Daddy Taxi!"
        damage = 50 + random.randint(1,50) + (hero.getLvl()*20)
        hero.setSp(hero.getSp() - 1)
    print
    return damage


def critText(enemyName, damage):
    if equippedWeaponName() in ['Knife','Serrated Knife']:
        print "The sharp", equippedWeaponName(), "slips deep into the" + \
              " chest of the", enemyName, ".",
        dotdotdot()
        print
        print "It's heart is punctured, and bursts into a bloody mess!"
        print
        print enemyName + " takes", damage, "damage!!"
    if equippedWeaponName() in ['Ninja Sword']:
        print "You draw back your sword, and do a frontal somersault, slashing " + \
              "as you come down upon the head of the ", enemyName, ".",
        dotdotdot()
        print
        print enemyName+"'s head is cleaved in two!  Ninja Gaiden would be proud!"
        print
        print enemyName + " takes", damage, "damage!!"
    if equippedWeaponName() in ['Tazer']:
        print "You step back as you overload your tazer, and jam it into the chest \n" + \
              " of the ", enemyName, ".",
        dotdotdot()
        print
        print enemyName+"'s eyes roll backwards into it's skull as it's heart EXPLODES internally!"
        print
        print enemyName + " takes", damage, "damage!!"
    if equippedWeaponName() in ['9mm Pistol','Shotgun']:
        print "You aim your", equippedWeaponName(), "at the", enemyName, "and \ncarefully channel the spirit" + \
              " of FPS Doug.",
        dotdotdot()
        print
        print "BOOM!  HEADSHOT!"
        print
        print enemyName + " takes", damage, "damage!!"


        
def victory(name,exp,money):
    global hero
    clrscr()
    print "You've defeated the " + name + "!!"
    print "You've gained", exp,"experience, and", money, "dollars!"
    hero.setExp(hero.getExp()+exp)
    hero.setMoney(hero.getMoney()+money)
    time.sleep(2)
    threshhold=[0,50,125,300,600,1000,1600,2500,4000,10000000000000]
    if threshhold[hero.getLvl()] <= hero.getExp():
        lvlUp()
    else:
        fastdotdotdot()
        fastdotdotdot()


def lvlUp():
    global hero
    hero.setLvl(hero.getLvl()+1)
    HpGain= (hero.getLvl()*2+1)
    SpGain= (hero.getLvl()%2)
    if hero.getLvl()==2:
        SpGain=1
    StrGain= (hero.getLvl()*hero.getLvl()/4) + 1
    DefGain= (hero.getLvl()*hero.getLvl()/12) + 2
    print
    print "Congrats, you've leveled up to lvl", hero.getLvl(), "!!!"
    print "You gained the following:"
    print HpGain, "Max HP"
    if SpGain >= 1:
        print SpGain, "Max SP"
    print StrGain, "Strength"
    print DefGain, "Defense"
    if hero.getLvl() % 2 == 0:
        print "And you've learned more powerful ancient hobo magic!"
    hero.setMaxHp(hero.getMaxHp()+HpGain)
    hero.setMaxSp(hero.getMaxSp()+SpGain)
    hero.setStr(hero.getStr()+StrGain)
    hero.setDef(hero.getDef()+DefGain)
    hero.setSp(hero.getSp() +SpGain)
    hero.setHp(hero.getHp() +HpGain)
    time.sleep(4.5)
    dotdotdot()
    fastdotdotdot()
        
        
#-------- END Combat Functions---------##-------- END Combat Functions---------##-------- END Combat Functions---------#

#--------Zone Functions---------##--------Zone Functions---------##--------Zone Functions---------##--------Zone Functions---------#
        
    
def loadZone():
    global zone
    while zone != "Quit":
        if zone == "Home Turf":
            homeTurf()
        if zone == "Streets":
            streetsArea()
        if zone == "Streets Motel Six":
            streetsMotelSix()
        if zone == "Bayview Homeless Shelter":
            streetsShelter()
        if zone == "Streets Pawn Shop":
            streetsPawnShop()
        if zone == "Red Cross":
            redCross()
        if zone == "Downtown":
            downtownArea()
        if zone == "Joseph A. Banks: Menswear":
            josephABanks()
        if zone == "McDonalds":
            mcDonalds()
        if zone == "Hull Apartments":
            hullApartments()
        if zone == "Jail":
            jail()
        
        
def ZONETEMPLATE():
    global zone, hero
    while zone == "ZONE NAME":
        clrscr()
        displayStats()
        print "zone descript here"
        print
        print "(z)one menus here"
        print
        command=validate(['','v'],'')
        clrscr()
        if command=='':
            zone = ""
        if command=='v':
            viewStats()


#--------END Zone Functions---------#--------END Zone Functions---------#--------END Zone Functions---------#--------------------

#--------HOME TURF Functions---------##--------HOME TURF Functions---------##--------HOME TURF Functions---------#---------------
            
    
def homeTurf():
    global zone, hero
    while zone == "Home Turf":
        clrscr()
        displayStats()
        print "This is your Home Turf, the streets where you ended up.  It smells of"
        print "urine, and is a series of alleys filled with strung out junkies, criminals,"
        print "and hobos."
        print "A cardboard box on the corner is painted with a sign that says PSYKIK."
        print 
        print "(T)alk to Joe, the psychic Hobo"
        print "(F)ight some worn out junkies"
        print "(W)ander around and look for a fight"
        print "(S)treets"
        print 
        command=validate(['t','f','v','s','w'],'none')
        clrscr()
        if command=='t':
            print "\n"
            print "You knock politely on Joe's cardboard box."
            dotdotdot()
            psychicJoe()
        if command=='f':
            print "\n"
            print "You run off to the ghetto to find a junkie to kill.",
            dotdotdot()
            print
            initiateCombat(rpgClass.Enemy('Junkie',20,20,9,4,10,7,1))
        if command=='w':
            print "\n"
            print "You wander around aimlessly.",
            dotdotdot()
            print
            initiateCombat("lol")
        if command=='v':
            viewStats()
        if command=='s':
            zone = "Streets"
        
def psychicJoe():
    command = ''
    while command != 'l':
        clrscr()
        print "The inside of Joe's cardboard box is covered with rhinestones and"
        print "strings of crappy doorway beads from the 1950's."
        print 
        print "Joe stares at you, with his crazy eyes."
        print
        print "(A)sk Joe what you should do"
        print "(T)ell Joe he should get a shower"
        print "(L)eave this dirty box"
        print
        command=validate(['a','t','l'],'l')
        clrscr()
        if command == 'a':
            print "Joe coughs for a few seconds, then wipes his mouth with his sleeve and says,"
            print
            print '"Boy, yous gonna be a king of all hobos!  That there job at mcdonalds is'
            print 'up for grabs to the best hobo ever, and you gotta be a magical kind of hobo'
            print 'to get that.  You need to buy an apartment, a pair of shoes, and a suit!'
            print 'You get that job and you aint ever gonna have to fight a hobo to the death'
            print 'for a ham sandwich again!  Go on, get outta here!"'
            print
            print "<Press Enter to Continue>"
            raw_input()
        if command == 't':
            print "Joe sniffs his armpits and recoils in horror."
            print
            print '"I KNOW THAT!  CUZ IM A PSYCHIC!"'
            print
            print "<Press Enter to Continue>"
            raw_input()
            
#--------END HOME TURF Functions---------##--------END HOME TURF Functions---------##--------END HOME TURF Functions---------#----#

#--------STREETS Functions---------##--------STREETS Functions---------##--------STREETS Functions---------##-----------------##---

def streetsArea():
    global zone, hero
    while zone == "Streets":
        clrscr()
        displayStats()
        print "The streets of New York's ghettos are dark and filled with danger."
        print "You see a variety of storefronts among the boarded up buildings."
        print "Well, where to?"
        print
        print "(H)ome Turf"
        print "(B)ayview Homeless Shelter"
        print "(M)otel Six"
        print "(R)ed Cross"
        print "(P)awn Shop"
        print "(D)owntown"
        print
        command=validate(['b','h','m','r','v','d','p'],'none')
        clrscr()
        if command=='d':
            zone = "Downtown"
        if command=='h':
            zone = "Home Turf"
        if command=='b':
            zone = "Bayview Homeless Shelter"
        if command=='r':
            zone = "Red Cross"
        if command=='m':
            zone = "Streets Motel Six"
        if command=='p':
            zone = "Streets Pawn Shop"
        if command=='v':
            viewStats()

            

def redCross():
    global zone, hero
    while zone == "Red Cross":
        clrscr()
        displayStats()
        print "This small urban red cross is busy with activity.  A nurse walks up"
        print "and looks at you expectantly..."
        print
        print "(D)onate Blood for $25 [Lose 10 HP]"
        print "(T)alk to the nurse"
        print "(L)eave"
        print
        command=validate(['d','t','l','v'],'l')
        clrscr()
        if command=='d':
            print "The nurse sits you down and feeds you a snickers bar as she draws"
            print "your blood.",
            dotdotdot()
            print
            print "<Press Enter to Continue>"
            raw_input()
            hero.setMoney(hero.getMoney() + 25)
            hero.setHp(hero.getHp - 10)
            if hero.getHp() <= 0:
                clrscr()
                print "You stumble out of the chair in a fatigued stupor",
                dotdotdot()
                print " and pass out as the last of your life force is drained from you!"
                print
                print "You've died of blood loss!"
                raw_input()
                import sys
                sys.exit("Know your limits!")
            
        if command=='t':
            print '''"We can't afford to help too much around here, but the hospitals'''
            print '''pay us good money to get some blood to them.  We are also taking'''
            print '''donations of nasty string beans or soggy corn in a can."'''
            print
            print "<Press Enter to Continue>"
            raw_input()
        if command=='l':
            zone = "Streets"
        if command=='v':
            viewStats()
            
            
            
            

def streetsPawnShop():
    global zone, hero
    while zone == "Streets Pawn Shop":
        clrscr()
        displayStats()
        print "The pawnbroker is busy grinding the serial numbers off some guns when you"
        print "walk in the door.  He turns around quickly and hides what he is doing."
        print
        print '''"What are you lookin' to trade, today, eh?"'''
        print
        print "(W)eapons"
        print "(A)rmor"
        print "(I)tems"
        print "(R)eturn to Streets"
        print
        command=validate(['w','a','i','r','v'],'r')
        clrscr()
        if command=='w':
            pawnBrokerWeapon()
        if command=='a':
            pawnBrokerArmor()
        if command=='i':
            pawnBrokerItem()
        if command=='r':
            zone = "Streets"
        if command=='v':
            viewStats()
       

def streetsShelter():
    global zone, hero
    while zone == "Bayview Homeless Shelter":
        clrscr()
        displayStats()
        print "A haggard volunteer greets you with a shot of whiskey and a smile."
        print '''"Well, what'll it be, you stinky hobo?"'''
        print 
        print "(S)leep in the cots [Save Game]"
        print "(A)sk the volunteer to be healed"
        print "(R)eturn to the streets"
        print
        command=validate(['r','a','s','v'],'r')
        clrscr()
        if command=='a':
            print "You ask the volunteer very nicely for a bandaid.",
            fastdotdotdot()
            print
            print '''\n"HAHA!  You're kidding, right?  Obama rationed all the health'''
            print '''care last year.  We can't afford to give out bandaids.'''
            print '''Try the Motel Six, I heard they have some fresh coffee and a pack'''
            print '''of bandaids with every room."'''
            print
            print "<Press Enter to Continue>"
            raw_input()
        if command=='s':
            print "You lay down in a stinky cot next to a smelly fat guy.",
            dotdotdot()
            print
            print "\nYou are awoken after 20 minutes by the horrible sound of snoring"
            print "and junkies writhing in agony from withdrawal..."
            print
            print "Your game has been saved!"
            print
            slowdotdotdot()
            if hero.getFights() < 3:
                hero.setFights(3)
            if hero.getHp() < hero.getMaxHp()/2:
                hero.setHp(hero.getMaxHp()/2)
            if hero.getSp() == 0 and hero.getMaxSp() >= 1:
                hero.setSp(1)
            saveGame()
            sureToQuit()
            clrscr()
            print "You cover your head with your jacket to muffle the noise, and try to go back"
            print "to sleep, but this night doesn't look too good.",
            slowdotdotdot()
        if command=='r':
            zone = "Streets"
        if command=='v':
            viewStats()
    
def streetsMotelSix():
    global zone, hero
    while zone == "Streets Motel Six":
        clrscr()
        displayStats()
        print "The lobby of this Motel Six is decorated in a very spartan manner."
        print "Everything is bolted down, and the clerk is behind a sheet of 2 inch"
        print "bulletproof glass.  There is a drug dealer sitting on one of the metal"
        print "benches off to the side."
        print
        print "(G)et a Room [$25]"
        print "(T)alk to the dealer"
        print "(R)eturn to the Streets"
        print
        command=validate(['g','r','t','v'],'r')
        clrscr()
        if command=='v':
            viewStats()
        if command=='g':
            if hero.getMoney()>=25:
                print "You slip the money under the bulletproof glass.  The teller gives"
                print "you a key to room 1B."
                print
                dotdotdot()
                dotdotdot()
                print "\n\nAfter using up all the free bandaids, drinking all the coffee, "
                print "and stealing all the shampoo, you feel refreshed!"
                print
                print "Your game has been saved!"
                print
                print "<Press Enter to Continue>"
                hero.restore()
                saveGame()
                hero.setMoney(hero.getMoney() - 25)
                raw_input()
                sureToQuit()
            else:
                print "The teller frowns at you and pushes the emergency 911 button..."
                print '''"If you can't pay, you better get the hell out of here!"'''
                print
                print "You decide it would be best to run before the cops show up to"
                print "beat the hell out of you."
                print
                print "<Press Enter to Continue>"
                raw_input()
        if command=='t':
            drugDealer()     
        if command=='r':
            zone = "Streets"    
            
#--------END STREETS Functions---------##--------STREETS Functions---------##--------STREETS Functions---------#----------##
#-------DOWNTOWN Functions-------##-------DOWNTOWN Functions-------##-------DOWNTOWN Functions-------##-------DOWNTOWN Functions-------#
            
def downtownArea():
    global zone, hero
    while zone == "Downtown":
        clrscr()
        displayStats()
        print "This area of downtown New York is much busier than the ghettos you are"
        print "used to.  People with suits walk by, glaring at your haggard appearance."
        print "Well, where to?"
        print
        print "(M)cDonalds"
        print "(J)oseph A. Banks: Menswear"
        print "(H)ull Apartments"
        print "(F)ind some rich guy to mug   NYI COMBATTYPE2/3"
        print "(S)treets"
        print
        command=validate(['m','j','f','s','h','v'],'none')
        clrscr()
        if command=='m':
            zone = "McDonalds"
        if command=='h':
            zone = "Hull Apartments"
        if command=='j':
            zone = "Joseph A. Banks: Menswear"
        if command=='s':
            zone = "Streets"
        if command=='v':
            viewStats()            
        if command=='f':
            print "\n"
            print "You hide in a garbage can on a street corner, looking for"
            print "potential marks...",
            dotdotdot()
            print
            enemyId = random.randint(1,10)
            if enemyId in [1,2,3]:
                initiateCombat(rpgClass.Enemy('Policeman',190,190,28,22,250,75,3))
            elif enemyId in [4,5]:
                initiateCombat(rpgClass.Enemy('Company Executive',50,50,19,28,40,100,2))
            else:
                initiateCombat(rpgClass.Enemy('Drunk Socialite',100,100,28,15,70,50,1))


def jail():
    global hero, inventory, zone
    clrscr()
    print "The officer beats you up until you can't move anymore, and hauls you to"
    print "jail.  They search you, and confiscate half your cash, and eat any"
    print "sandwiches and food you have.   Bummer dude!"
    print
    dotdotdot()
    print
    print "After a night in jail, you feel weak and frail, but they release you."
    print
    print "<Press Enter to Continue>"
    raw_input()
    for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
        if isinstance(inventory[line],rpgClass.Consumable):
            inventory.delete(line)
    hero.setMoney(hero.getMoney()/2)
    hero.setHp(1)
    hero.setSp(0)
    zone = "Downtown"

def josephABanks():
    global zone, hero
    while zone == "Joseph A. Banks: Menswear":
        clrscr()
        displayStats()
        print "As you enter the upscale store, you hear the sound of salesman charging"
        print "towards you in a full sprint."
        print
        print '''"Hey there Buddy, you look like a man who could use a good suit.'''
        print '''...Or three.  I got kids to feed."'''
        print
        print "(G)et a suit"
        print "(A)sk about shoes"
        print "(L)eave"
        print
        command=validate(['g','a','l','v'],'l')
        clrscr()
        if command=='g':
            print '''"YES, I knew I smelled commission when you came in the door."'''
            print
            print "The salesman nearly body tackles you as he takes your measurements,"
            print "and disappears into the back to get a suit."
            print
            print '''"OK Buddy, how does this one look?  It's our deluxe, stuffed with'''
            print '''genuine bald eagle feathers.  Only $200!  But just for you, I'll take'''
            print '''$80 off if you buy it right now!  $120, out the door!"'''
            print
            print "(Y)es or (N)o?"
            print
            suitbuy=validate(['y','n'],'n')
            clrscr()
            if suitbuy=='y' and hero.getMoney() >= 120:
                print '''The salesman jumps up and down in excitement!  "Excellent!"'''
                print 
                print "As you walk over to the register, you notice his sales manager"
                print "pushing him towards the shoes rack.  You pay him the $120 for"
                print "your suit...",
                if len(inventory) >= 10:
                    deleteFlag = 99
                    for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
                        if isinstance(inventory[line],rpgClass.Consumable) and deleteFlag==99:
                            deleteFlag = line 
                    print "You drop your "+inventory[deleteFlag].getName()+" to make room for the suit."
                    inventory.remove(deleteFlag)
                dotdotdot()
                dotdotdot()
                inventory.append(rpgClass.Item('Suit',120))
                hero.setMoney(hero.getMoney()-120)
                clrscr()
                command='a'
            else: 
                print '''"Oh god.  That wasn't commission I smelled....  IT WAS DIRTY'''
                print '''PENNILESS HOBO!  GET OUT OF HERE!  NO FREE SUITS!"'''
                print
                print "<Press Enter to Continue>"
                raw_input()   
                
        if command=='a':
            print '''"Oh, yes, you're going to need some great looking shoes to go'''
            print '''along with that suit.  The normal ones are $40, but the super'''
            print '''deluxe fancy ones, which were worn by Mick Jagger and are made'''
            print '''out of cheetah leather, are $400.'''
            print
            print "(R)egular Shoes [$40]"
            print "(C)heetah skin shoes [$400]"
            print "(N)o thanks"
            print
            shoesbuy=validate(['r','c','n'],'n')
            clrscr()
            if shoesbuy=='r':
                if hero.getMoney() >= 40:
                    print '''"Well, a small commission check is still a commission'''
                    print '''check.  My kids will just be hungry..."'''
                    print
                    print "You pay him, trying to ignore his guilt trip...",
                    if len(inventory) >= 10:
                        deleteFlag = 99
                        for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
                            if isinstance(inventory[line],rpgClass.Consumable) and deleteFlag==99:
                                deleteFlag = line 
                        print "You drop your "+inventory[deleteFlag].getName()+" to make room for the shoes."
                        inventory.remove(deleteFlag)
                    dotdotdot()
                    dotdotdot()
                    inventory.append(rpgClass.Item('Shoes',40))
                    hero.setMoney(hero.getMoney()-40)
                    clrscr()
                else:
                    print '''"Oh god.  That wasn't commission I smelled....  IT WAS DIRTY'''
                    print '''PENNILESS HOBO!  GET OUT OF HERE!  NO FREE SHOES!"'''
                    print
                    print "<Press Enter to Continue>"
                    raw_input()
                    
            if shoesbuy=='c':
                if hero.getMoney() >= 400:
                    print '''"YES!  No ramen noodle for me tonight!"'''
                    print '''The excitement on this salesman is palpable.'''
                    print
                    print "You pay him for the cheetah skin shoes...",
                    if len(inventory) >= 10:
                        deleteFlag = 99
                        for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
                            if inventory[line].getName() == 'Shoes':
                                deleteFlag = line
                            if isinstance(inventory[line],rpgClass.Consumable) and deleteFlag==99:
                                deleteFlag = line 
                        print "You drop your "+inventory[deleteFlag].getName()+" to make room for the cheetah shoes."
                        inventory.remove(deleteFlag)
                    deleteFlag = 99
                    for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
                        if inventory[line].getName() == 'Shoes':
                            deleteFlag = line
                    if deleteFlag != 99:
                        print "You drop your "+inventory[deleteFlag].getName()+" to make room for the cheetah shoes."
                        inventory.remove(deleteFlag)
                    dotdotdot()
                    dotdotdot()
                    inventory.append(rpgClass.Item('Cheetah Shoes',400))
                    hero.setMoney(hero.getMoney()-400)
                    clrscr()
                else:
                    print '''"Oh god.  That wasn't commission I smelled....  IT WAS DIRTY'''
                    print '''PENNILESS HOBO!  GET OUT OF HERE!  NO FREE SHOES!"'''
                    print
                    print "<Press Enter to Continue>"
                    raw_input()
                    
        if command=='l':
            zone = "Downtown"
        if command=='v':
            viewStats()
            
            
            
def hullApartments():
    global zone, hero
    while zone == "Hull Apartments":
        clrscr()
        displayStats()
        print "You enter the nice looking building, only to be greeted with the kind of"
        print "mistreatment and disrepair you would normally find back at your ghetto"
        print "home.  What kind of a place is this?"
        print
        print "(G)o the office to rent an apartment [$500]"
        print "(K)nock on Eric Fusciardi's door"
        print "(U)rinate on the fake plants"
        print "(L)eave"
        print
        command=validate(['g','k','u','l','v'],'l')
        clrscr()
        if command=='l':
            zone = "Downtown"
        if command=='u':
            print "You relieve yourself on the ancient looking faded fake plants, like"
            print "no doubt, hundreds of other hobos have, judging by the smell."
            print
            print "<Press Enter to Continue>"
            raw_input()
        if command=='k':
            print "You knock on Eric's Apartment.",
            dotdotdot()
            print "\n"
            print "You can hear him getting up and moving to the door, and he is "
            print "probably staring at you through the peephole."
            print
            print "He knows you just want to tell him some lie about your kids and"
            print "try to sell him a $10 candy bar, so he goes back to programming a game"
            print "about a guy with a strangely similar fate as yours.... hmm..."
            print
            print "<Press Enter to Continue>"
            raw_input()
        if command=='g':
            print "The office manager quickly alt-f4's the game of solitaire he was"
            print "playing as you enter the room."
            print
            print '"Hi there, looking for an apartment?  God knows we have a ton of '
            print 'vacancies in this place!  All we need is $500 deposit, and the'
            print 'rent will go up every month for no reason.  We also like to repair'
            print 'stuff that isnt broke and leave broke stuff broke.  Sign here!"'
            print
            dotdotdot()
            print
            print "<Press Enter to Continue>"
            raw_input()
            if hero.getMoney() >= 500:
                clrscr()
                print '''"Thanks!  You'll regret it!  I mean, won't!  Won't regret it!"'''
                print 
                print 'You got an Apartment Key!  And an address!'
                print
                print "<Press Enter to Continue>"
                raw_input()
                global inventory
                if len(inventory) >= 10:
                    deleteFlag = 99
                    for line in range(len(inventory)):   #THIS SCANS INV FOR CONSUMABLE
                        if isinstance(inventory[line],rpgClass.Consumable) and deleteFlag==99:
                            deleteFlag = line 
                    print "You drop your "+inventory[deleteFlag].getName()+" to make room for the key."
                    inventory.remove(deleteFlag)
                inventory.append(rpgClass.Item('Apartment Key',500))
                hero.setMoney(hero.getMoney()-500)
            else:
                clrscr()
                print '"Well, we dont have many standards in this place, except for one:'
                print
                dotdotdot()
                print
                print 'CASH UP FRONT!!!!"'
                print
                print "<Press Enter to Continue>"
                raw_input()
            
        if command=='v':
            viewStats()
            
def mcDonalds():
    global zone, hero
    while zone == "McDonalds":
        clrscr()
        displayStats()
        print "This downtown McDonalds is full of trendy people who spend all their"
        print "money at Starbucks and can't afford to eat well anymore.  There is a "
        print "sense of shame in the air, and you are unsure whether it is from the"
        print "customers or the employees.  You approach the counter, and are greeted"
        print "by a zombie-like young kid."
        print
        print "(O)rder a double cheeseburger"
        print "(T)alk to the manager for a job"
        print "(L)eave"
        print
        command=validate(['o','t','l','v'],'l')
        clrscr()
        if command=='o':
            if hero.getMoney() < 1:
                print "The lifeless clerk looks up at you, expecting payment.",
                fastdotdotdot()
                print "but sees that you cannot pay!"
                print
                print '"Get out of here you freakin hobo, go donate blood if you need a dollar!"'
                print
                print "<Press Enter to Continue>"
                raw_input()
            else:
                print "The lifeless clerk takes your order and your dollar, and gives you"
                print "the poorly made and mass produced reconstituted pile of empty calories."
                print "The inner fatty in all of us rejoice."
                print
                print "<Press Enter to Continue>"
                hero.setMoney(hero.getMoney()- 1)
                hero.setHp(hero.getHp() - 6 + random.randint(1,8))
                raw_input()
                if hero.getHp() <= 0:
                    clrscr()
                    print "As you eat the cheeseburger, you feel a sharp pain in your left arm."
                    print "It suddenly goes numb, and your chest feels like it is caving in on"
                    print "itself.  OH GOD!  Heart attack!"
                    print
                    print "You've died!  From trans fat, of all things!"
                    print "<Press Enter to Continue>"
                    raw_input()
                    import sys
                    sys.exit("")
                
            
        if command=='t':
            suitFlag = 0
            addressFlag = 0
            shoesFlag = 0
            watchFlag = 0
            FAIL = 0
            clrscr()
            print "The manager lumbers out of the back, his unwashed polo shirt covered in"
            print "fryer grease, which matches his unwashed greasy hair.",
            dotdotdot()
            print
            for line in range(len(inventory)):  
                if inventory[line].getName() in ['Suit']:
                    suitFlag = 1
                if inventory[line].getName() in ['Shoes']: 
                    shoesFlag = 1
                if inventory[line].getName() in ['Cheetah Shoes']: 
                    shoesFlag = 2
                if inventory[line].getName() in ['Apartment Key']:                    
                    addressFlag = 1
                if inventory[line].getName() in ['Gold Watch']:                    
                    watchFlag = 1
            if suitFlag == 0:
                print 'He takes one look at you and says: "Dude, I know this is McDonalds'
                print 'and everything, but I just cannot take you seriously when you come in'
                print 'here with your street clothes.  Go get something nicer."'
                print
                FAIL = 1
            elif shoesFlag == 0:
                print 'He takes a look at you, and looks pleased, then immediately frowns.'
                print '"Come on man, you dont even have any shoes on.  I cant hire you!"'
                print
                print "You think that maybe that sales rep was right..."
                print
                FAIL = 1
            elif addressFlag == 0:
                print 'He takes a look at you, and looks pleased.  "You look like an OK'
                print 'guy, just trying to make something of himself.  Here, fill this'
                print 'Application out and we can talk."'
                print
                print 'You fill in your name, and look at the next question.',
                dotdotdot()
                print
                print 'Oh crap!  You need an address!  You back away slowly, but none'
                print 'of the employees notice, since they are soul-dead zombies.'
                FAIL = 1
                
            if FAIL == 0:
                print 'He takes a look at you, and looks pleased.  "You look like an OK'
                print 'guy, just trying to make something of himself.  Here, fill this'
                print 'Application out and we can talk."'
                print
                print "You fill in your name, and almost forget your new address.  You make"
                print "up a bunch of references and prior history since this guy obviously"
                print "doesn't care at all."
                print
                raw_input("<Press Enter to Continue>\n")
                clrscr()
                
                
                if watchFlag == 1:
                    print "The manager picks up your application, and you notice his eyes"
                    print "always moving down off the paper towards your amazing gold watch."
                    print
                    print '"You know what, dude, you are hired.  Welcome to McDonalds, I'
                    print 'can tell by that watch of yours that you care."'
                    print
                    raw_input("<Press Enter to Continue>\n")
                    win()
                
                if shoesFlag == 1:
                    print "The manager picks up your application, and you can tell he is"
                    print "just pretending to read it, as he only understands words when also"
                    print "accompanied by a hamburger or french fry icon next to it."
                    print
                    print '"Well, OK, everything looks in order here, but I have a few'
                    print 'Questions for you before you get this McJob"'
                    raw_input("<Press Enter to Continue>\n")
                    clrscr()
                    print '"Question 1:  Will you steal from the register to buy crack?"'
                    print
                    decision = validate(['y','n'],'y')
                    clrscr()
                    if decision == 'y':
                        print '"I applaud your honesty, but you understand when I say that'
                        print 'I cannot hire you, right?  Sorry dude."'
                        print
                        print "You hang your head in shame, but figure that this guy is going"
                        print "to go smoke pot, and will forget all about this in a few minutes."
                        print
                        raw_input("<Press Enter to Continue>\n")
                    if decision == 'n':
                        print '"Well then, that is that!  Welcome to McDonalds!  I cannot believe'
                        print 'a hobo like you passed our vigorous entrance exam! No one answers'
                        print 'that question right!  Now get in uniform and work the deep frier."'
                        print
                        raw_input("<Press Enter to Continue>\n")
                        win()
                if shoesFlag == 2:
                    print "The manager picks up your application, and you notice his eyes"
                    print "always moving down off the paper towards your fancy dress shoes."
                    print
                    print '"You know what, dude, you are hired.  Welcome to McDonalds, I'
                    print 'can tell by your awesome cheetah leather shoes that you care."'
                    print
                    raw_input("<Press Enter to Continue>\n")
                    win()
        if command=='l':
            zone = "Downtown"
        if command=='v':
            viewStats()             
            
            
            
            
            
            
#------- END DOWNTOWN Functions-------##------- END DOWNTOWN Functions-------##------- END DOWNTOWN Functions-------#
#--------SEMI-AMBIGUOUS SHOPS Functions---------##--------SEMI-AMBIGUOUS SHOPS Functions---------##------------####-------##

def pawnBrokerWeapon():
    global hero, inventory
    command=''
    while command != 'n':
        clrscr()
        displayStats()
        for line in range(len(inventory)):   #THIS SCANS INV FOR WPN
            if isinstance(inventory[line],rpgClass.Weapon):
                wpnIndex = line              #THIS SCANS INV FOR WPN
        tradeIn = int(inventory[wpnIndex].getValue()/2.0)
        print '''"Hmm... Not a bad looking ''' + equippedWeaponName() + " you have there..."
        print "I'll give you", tradeIn, 'dollars in credit if you trade for a new weapon."'
        print
        shopInv=[rpgClass.Weapon('Serrated Knife',40,9),rpgClass.Weapon('Ninja Sword',100,15), \
                 rpgClass.Weapon('Tazer',300,25),rpgClass.Weapon('9mm Pistol',750,40), \
                 rpgClass.Weapon('Shotgun',1500,65)]
        tempList=[]
        for line in range(len(shopInv)):       #THIS PRINTS THE ITEM LIST
            print "("+str(line+1)+") "+shopInv[line].getName()+" [$"+str(shopInv[line].getValue())+"]"
            tempList.append(str(line+1))       #THIS PRINTS THE ITEM LIST
        print "(N)o Thanks"
        print
        tempList.append('n')
        command=validate(tempList,'n')
        if command=='n':
            return
        if (hero.getMoney() + tradeIn) < shopInv[int(command)-1].getValue():
            print "Get the hell out of here, you penniless bum!"
            print "Come back when you've got the cash for it."
        else:
            inventory.remove(inventory[wpnIndex])
            hero.setMoney(hero.getMoney() + tradeIn - shopInv[int(command)-1].getValue())
            inventory.append(shopInv[int(command)-1])
            print "Thanks!  Enjoy your new", equippedWeaponName(), "!!"
        print
        print "<Press Enter to Continue>"
        raw_input()
        
def pawnBrokerArmor():
    global hero, inventory
    command=''
    while command != 'n':
        clrscr()
        displayStats()
        for line in range(len(inventory)):   #THIS SCANS INV FOR ARMOR
            if isinstance(inventory[line],rpgClass.Armor):
                armorIndex = line              #THIS SCANS INV FOR ARMOR
        tradeIn = int(inventory[armorIndex].getValue()/2.0)
        print '''"Hmm... Not a bad looking ''' + equippedArmorName() + " you have there..."
        print "I'll give you", tradeIn, 'dollars in credit if you trade for a new set of armor."'
        print
        shopInv=[rpgClass.Armor('Leather Jacket',70,7),rpgClass.Armor('Tin Foil Armor',180,10), \
                 rpgClass.Armor('Red Man Suit',500,13),rpgClass.Armor('Bulletproof Jacket',1250,18)]
        tempList=[]
        for line in range(len(shopInv)):       #THIS PRINTS THE ITEM LIST
            print "("+str(line+1)+") "+shopInv[line].getName()+" [$"+str(shopInv[line].getValue())+"]"
            tempList.append(str(line+1))       #THIS PRINTS THE ITEM LIST
        print "(N)o Thanks."
        print
        tempList.append('n')
        command=validate(tempList,'n')
        if command=='n':
            return
        if (hero.getMoney() + tradeIn) < shopInv[int(command)-1].getValue():
            print "Get the hell out of here, you penniless bum!"
            print "Come back when you've got the cash for it."
        else:
            inventory.remove(inventory[armorIndex])
            hero.setMoney(hero.getMoney() + tradeIn - shopInv[int(command)-1].getValue())
            inventory.append(shopInv[int(command)-1])
            print "Thanks!  Enjoy your new", equippedArmorName(), "!!"
        print
        print "<Press Enter to Continue>"
        raw_input()
        
def pawnBrokerItem():
    global hero, inventory
    command=''
    while command != 'n':
        clrscr()
        displayStats()
        emptySlots = 10-len(inventory)
        if emptySlots == 0:
            print '''"Listen my hobo friend.  You don't have any more room in your backpack'''
            print '''to put anything I can sell you.  Sorry."'''
            return
        print '''"Hmm... looks like you've got room for''',emptySlots,'''more items"'''
        print
        shopInv=[rpgClass.Consumable('Sandwich',5,2),rpgClass.Consumable('Ham Sandwich',10,1), \
                 rpgClass.Consumable('Booze',20,3),rpgClass.Consumable('Mountain Dew',2,4), \
                 rpgClass.Item('Gold Watch',500)]
        tempList=[]
        for line in range(len(shopInv)):       #THIS PRINTS THE ITEM LIST
            print "("+str(line+1)+") "+shopInv[line].getName()+" [$"+str(shopInv[line].getValue())+"]"
            tempList.append(str(line+1))       #THIS PRINTS THE ITEM LIST
        print "(N)o Thanks"
        print
        tempList.append('n')
        command=validate(tempList,'n')
        if command=='n':
            return
        if hero.getMoney() < shopInv[int(command)-1].getValue():
            print "Get the hell out of here, you penniless bum!"
            print "Come back when you've got the cash for it."
        else:
            hero.setMoney(hero.getMoney() - shopInv[int(command)-1].getValue())
            inventory.append(shopInv[int(command)-1])
            print "Thanks!  Enjoy your new", shopInv[int(command)-1].getName(), "!!"
        print
        print "<Press Enter to Continue>"
        raw_input()
    
            
         
def drugDealer():
    global hero
    clrscr()
    displayStats()
    print "The dealer looks up at you, his dark eyes obscured by his bright"
    print "purple fuzzy pimp hat."
    print
    print '''"Well, what it be, you dirty whino?  What you want???"'''
    print
    print "(B)uy some Drugs"
    print "(N)evermind"
    print
    command=validate(['b','v','n'],'n')
    clrscr()
    if command=='v':
        viewStats()
    if command=='b':
        displayStats()
        print '''"Well well, alright then, what it be?"'''
        print
        shopInv=[rpgClass.Drug('Crack',20,'Grants Temp HP + Fights, Risk permanent HP dmg'), \
                 rpgClass.Drug('Speed',50,'Increase Defense, Risk permanent magic dmg'), \
                 rpgClass.Drug("'Roids",50,'Increase Strength, Risk permanent magic dmg'), \
                 rpgClass.Drug('LSD',200,'Increase Magic, Risk permanent HP dmg')]
        tempList=[]
        for line in range(len(shopInv)):       #THIS PRINTS THE DRUG LIST
            print "("+str(line+1)+") "+shopInv[line].getName()+" ["+shopInv[line].getDesc()+"- $"+str(shopInv[line].getPrice())+"]"
            tempList.append(str(line+1))       #THIS PRINTS THE DRUG LIST
        print "\n(N)evermind, I'm staying clean"
        tempList.append('n')
        tempList.append('v')
        drug=validate(tempList,'n')
        clrscr()
        if drug=='v':
            viewStats()
        if drug=='n':
            return
        if hero.getMoney() < shopInv[int(drug)-1].getPrice():
            print "The dealer pimpslaps the hell out of you and tells you to come"
            print "back when you have money."
            print "\n<Press Enter to Continue>"
            raw_input()
            return
        print "The dealer draws out a syringe full of a brown liquid..."
        print 
        print '''"Don't move, this aint gonna hurt a bit."''',
        dotdotdot()
        print "\n"
        print "You feel a BURNING in your veins.",
        slowdotdotdot()
        print "\n"
        hero.setMoney(hero.getMoney()-shopInv[int(drug)-1].getPrice())
        if shopInv[int(drug)-1].getName()=="Crack":
            if random.randint(1,2) == 1:
                print "You feel INVINCEABLE!  But you've become addicted and have"
                print "become frail...  You lose 6 max HP"
                hero.setMaxHp(hero.getMaxHp() - 6)
                if hero.getMaxHp()<0:
                    print
                    print "You've become too addicted and frail to continue living!"
                    raw_input("You die in the corner, shuddering from cold... Drugs are bad, mmkay")
                    import sys
                    sys.exit()
            else:
                print "You feel INVINCABLE!"
            hero.setHp(hero.getMaxHp()*2)
            hero.setFights(hero.getFights()+5)
        if shopInv[int(drug)-1].getName()=="Speed":
            if random.randint(1,2) == 1:
                print "You feel NIMBLE!  But you've become addicted and have"
                print "become frail...  You lose 1 max SP"
                hero.setMaxSp(hero.getMaxSp() - 1)
                if hero.getMaxSp()<0:
                    hero.setMaxSp(0)
            else:
                print "You feel NIMBLE!"
            hero.setDef(hero.getDef()+2)
        if shopInv[int(drug)-1].getName()=="Steroids":
            if random.randint(1,2) == 1:
                print "You feel STRONG!  But you've become addicted and have"
                print "become frail...  You lose 1 max SP"
                hero.setMaxSp(hero.getMaxSp() - 1)
                if hero.getMaxSp()<0:
                    hero.setMaxSp(0)
            else:
                print "You feel STRONG!"
            hero.setStr(hero.getStr()+2)
        if shopInv[int(drug)-1].getName()=="LSD":
            if random.randint(1,2) == 1:
                if random.randint(1,5)==10:
                    print "You feel completely disoriented... and have lost all of your"
                    print "memories and knowledge of arcane hobo arts!  If only you had"
                    print "listened to your high school drug counselor!!!!!"
                    hero.setMaxSp(0)
                    hero.setSp(0)
                else:
                    print "Your mind EXPANDS!  But you've become addicted and have"
                    print "become frail...  You lose 10 max HP"
                    hero.setMaxHp(hero.getMaxHp() - 10)  
                    if hero.getMaxHp()<0:
                        print
                        print "You've become too addicted and frail to continue living!"
                        raw_input("You die in the corner, shuddering from cold... Drugs are bad, mmkay")
                        import sys
                        sys.exit()
            else:
                print "Your mind EXPANDS!"
            hero.setMaxSp(hero.getMaxSp()+1)
        print "\n<Press Enter to Continue>"
        raw_input()
                        
            
#--------END SEMI-AMBIGUOUS SHOPS Functions---------##--------END SEMI-AMBIGUOUS SHOPS Functions---------###------------###
        
#--------Menu Functions---------##--------Menu Functions---------##--------Menu Functions---------##--------Menu Functions-----#    

def viewStats():
    global hero, zone, inventory
    tempList=[]
    string = "HP: " + str(hero.getHp()) + "/" + str(hero.getMaxHp()) + "    " + \
          "SP: " + str(hero.getSp()) + "/" + str(hero.getMaxSp()) + \
          "    Fights Left until Rest: " +  str(hero.getFights())   
    print "Your Stats:"
    print
    print string 
    print
    print "Level:  %3d               Experience: %5d" % (hero.getLvl(), hero.getExp())
    print
    print "                       Equipped Weapon:", equippedWeaponName()
    print "Base Strength: %3d        Weapon Power: %d" % (hero.getStr(), equippedWeaponMod())
    print "                        Equipped Armor:", equippedArmorName()
    print "Base Defense:  %3d         Armor Power: %d" % (hero.getDef(), equippedArmorMod())
    print
    print "Money:  $" + str(hero.getMoney())
    print "----------------Inventory-----------------"
    for line in range(len(inventory)):
        print str(line+1) + ") %-15s\t " % inventory[line].getName(),
        tempList.append(str(line+1))
        if ((line)%2):
            print
    print "\n------------------------------------------\n"
    print "[#] Use Item"
    print "[R]eturn"
    tempList.append('r')
    print
    command=validate(tempList,'r')
    if command != 'r':
        useItem(int(command)-1)


def equippedWeaponMod():
    global inventory
    mod=0
    for line in range(len(inventory)):
        if isinstance(inventory[line],rpgClass.Weapon):
            mod = inventory[line].getMod()
    return mod

def equippedArmorMod():
    global inventory
    mod=0
    for line in range(len(inventory)):
        if isinstance(inventory[line],rpgClass.Armor):
            mod = inventory[line].getMod()
    return mod

def equippedWeaponName():
    global inventory
    wpnName = "Fists"
    for line in range(len(inventory)):
        if isinstance(inventory[line],rpgClass.Weapon):
            wpnName = inventory[line].getName()
    return wpnName

def equippedArmorName():
    global inventory
    armorName = "Rags"
    for line in range(len(inventory)):
        if isinstance(inventory[line],rpgClass.Armor):
            armorName = inventory[line].getName()
    return armorName

def useItem(invIndex):
    global inventory, hero
    if inventory[invIndex].getEffIndex() == 1:
        clrscr()
        print "You chow down on the delicious Ham Sandwich",
        hero.setHp(hero.getHp()+20)
        if hero.getHp() > hero.getMaxHp():
            hero.setHp(hero.getMaxHp())
        dotdotdot()
        print "\nYou feel better!\n"
        print "<Press Enter to Continue>"
        inventory.remove(invIndex)
        raw_input()
    elif inventory[invIndex].getEffIndex() == 2:
        clrscr()
        print "You chow down on the semi-delicious Sandwich",
        hero.setHp(hero.getHp()+10)
        if hero.getHp() > hero.getMaxHp():
            hero.setHp(hero.getMaxHp())
        dotdotdot()
        print "\nYou feel better!\n"
        print "<Press Enter to Continue>"
        inventory.remove(invIndex)
        raw_input()
    elif inventory[invIndex].getEffIndex() == 3:
        clrscr()
        print "You drink the cheap booze, and feel great!"
        print "You stumble around for a half hour.",
        hero.setHp(hero.getHp()+30)
        hero.fight()
        dotdotdot()
        print "\nYou feel INVINCEABLE!  But you lost some rest.\n"
        print "<Press Enter to Continue>"
        inventory.remove(invIndex)
        raw_input()
    elif inventory[invIndex].getEffIndex() == 4:
        clrscr()
        print "You drink the citrusy awesomeness and feel the dew rush hit!"
        hero.setHp(hero.getHp()+5)
        hero.setFights(hero.getFights() + 2)
        dotdotdot()
        print "\nYou feel QUICK!  You don't need any rest! CAFFFFEEEEEINE!\n"
        print "<Press Enter to Continue>"
        inventory.remove(invIndex)
        raw_input()
    else:
        clrscr()
        print "You stare at the " + inventory[invIndex].getName() + " resolutely, but nothing happens."
        print
        print "<Press Enter to Continue>"
        raw_input()
        

#--------END Menu Functions---------##--------END Menu Functions---------##--------END Menu Functions---------##------####


def intro():
    clrscr()
    print "You step outside your mansion, and stroll over to the garage.  You can't wait"
    print "to drive your Ferrari to work at wall street.",
    slowdotdotdot()
    slowdotdotdot()
    print "\n"
    print "Until you realize that the ferrari isn't in the garage!  You run back to"
    print "the house to see repo men bashing down walls and grabbing all your furniture!"
    print 'You wildly ask one of the men, "What are you doing here??"',
    slowdotdotdot()
    slowdotdotdot()
    print "\n"
    print '"Sorry boss, your financial manager defaulted on his loans from your money.'
    print 'We gotta take everything.", he says as he grabs the suit from your chest and'
    print 'yanks off your fancy dress slacks and shoes.',
    slowdotdotdot()
    slowdotdotdot()
    slowdotdotdot()
    print "\n"
    print "This is unreal!  You had a real good guy managing your money!  You think his"
    print "name was Ben... or Bennie.  No no no, it was Bernie!",
    slowdotdotdot()
    print "Bernie Madoff!"
    print
    slowdotdotdot()
    print "\n"
    print "The repo man hands you a bus ticket to the ghetto and a knife, and wishes"
    print "you luck."
    print
    print "<Press Enter to Continue>"
    raw_input()
    clrscr()
    print "One year passes, and you've become a hardened shell of the man you once were..."
    print
    print "<Press Enter to Continue>"
    raw_input()
    

def main():
    global zone
    while zone=="Nowhere":
        print "\t\t/------------------------\\"
        print "\t\t| Welcome to HOBO QUEST! |"
        print "\t\t\\------------------------/"
        print "\t\t             Developed by: Eric Fusciardi"
        print "\t\t     Poorly maintained by: Eric Fusciardi\n\n"
        print "(S)aved game"
        print "(N)ew game"
        print "(H)elp?"
        command=validate(['s','n','h'], 's')
        if command=='s':
            clrscr()
            print "Attempting to load savegame.txt"
            dotdotdot()
            loadGame()
            print "Load successful!"
            time.sleep(3)
        elif command=='n':
            global hero, inventory
            hero=rpgClass.Character(20,20,0,0,10,10,1,0,5,20) 
            inventory=[]
            inventory.append(rpgClass.Weapon('Knife',10,5))
            inventory.append(rpgClass.Armor('Clothes',10,5))
            inventory.append(rpgClass.Consumable('Ham Sandwich',10,1))
            zone='Home Turf'
            intro()
        elif command=='h':
            clrscr()
            print "This is a horrible little game from Eric's horrible little mind."
            print "It's not politically correct, and is a very generic RPG"
            print 
            print "In any menu, the default value for just pressing the enter key is"
            print 'shown in square brackets.  So, instead of pressing "A" then "Enter"'
            print "to attack, you can just press enter, since attack is defaulted."
            print
            print "Save and quit the game at any various inn or street hostel."
            print
            raw_input("<Press Enter to Return>\n")
            clrscr()
    loadZone()
        
    
    
    
main()