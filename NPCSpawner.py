import viz
import random


trainSeatedNPC = []
trainStandingNPC = []

trainSeatedPos = []
trainStandingPos = []
platStandingPos = []

platformNPC = []

def InitSeatedPos(train):
	for x in range(0, 6):
		for i in range(0, 5):
			if(x == 4 and i == 2):
				# Skip Player Position
				print('Player Position')
			else:
				trainSeatedPos.append(1)
				trainSeatedPos[len(trainSeatedPos) - 1] = train.getTransform('Seat ' + str(x + 1) + ' Pos ' + str(i + 1)).getPosition() # Get seated transform positions from Model
				
def InitStandingPos(train):
	for x in range(0, 83):
		trainStandingPos.append(1)
		trainStandingPos[len(trainStandingPos) - 1] = train.getTransform('Standing Pos ' + str(x + 1)).getPosition() # Get seated transform positions from Model

def InitPlat(plat):
	for x in range(0, 30):
		platStandingPos.append(1)
		platStandingPos[len(platStandingPos) - 1] = plat.getTransform('Platform Pos ' + str(x + 1)).getPosition() # Get seated transform positions from Model

def SpawnSeatedNPC(train, stage):
	# Remove
	if(len(trainSeatedNPC) > 0):
		for x in range(0, len(trainSeatedNPC)):
			trainSeatedNPC[x].remove()
	
	trainSeatedNPC[:] = []
	
	seatTaken = []
	for x in range(0, 29):
		seatTaken.append(1)
		seatTaken[x] = False
	
	#xPos = -1.0 # Depth
	#yPos = 1.2 # Height
	#zPos = -7.0 # Along Seat
	
	xRot = 90.0
	
	if(stage == 0):
		numToSpawn = 0
	elif(stage == 1):
		numToSpawn = 5
	elif(stage == 2):
		numToSpawn = 15
	elif(stage == 3):
		numToSpawn = 25
	elif(stage == 4):
		numToSpawn = 27
	elif(stage == 5):
		numToSpawn = 28
	else:
		numToSpawn = 0
	
	if(numToSpawn > 0):
		for x in range(0, numToSpawn):
				pos = None
						
				# Random Spawn Test
				numFound = False
				rand = 0
				
				while(numFound == False):
					rand = random.randint(0, 28)
					if(seatTaken[rand] == False):
						numFound = True
						seatTaken[rand] = True
				
				pos = trainSeatedPos[rand]
				
				if(rand < 15):
					xRot = -90
				else:
					xRot = 90
				
				trainSeatedNPC.append(1)
				trainSeatedNPC[x] = viz.addChild('vcc_male2.cfg')
				trainSeatedNPC[x].state(6) # Looping idle animation
				trainSeatedNPC[x].setEuler(xRot,0,0) # Turns him to face you
				trainSeatedNPC[x].setPosition(pos) # Moves him back so that he is in full view xPos,yPos,zPos
				trainSeatedNPC[x].setParent(train)
			
def SpawnStandingNPC(train, stage):	
	# Remove
	if(len(trainStandingNPC) > 0):
		for x in range(0, len(trainStandingNPC)):
			trainStandingNPC[x].remove()
	
	trainStandingNPC[:] = []
	
	spotsTaken = []
	for x in range(0, 82):
		spotsTaken.append(1)
		spotsTaken[x] = False	
	
	numToSpawn = 0
	
	if(stage == 0):
		numToSpawn = 0
	elif(stage == 1):
		numToSpawn = 2
	elif(stage == 2):
		numToSpawn = 20
	elif(stage == 3):
		numToSpawn = 55
	elif(stage == 4):
		numToSpawn = 75
	elif(stage == 5):
		numToSpawn = 80
	else:
		numToSpawn = 0
	
	if(numToSpawn > 0):
		for x in range(0, numToSpawn):
				# Random Pos
				numFound = False
				rand = 0
				
				while(numFound == False):
					rand = random.randint(0, 81)
					if(spotsTaken[rand] == False):
						numFound = True
						spotsTaken[rand] = True
				
				pos = trainStandingPos[rand]
				
				trainStandingNPC.append(1)
				
				randGener = random.randint(0, 10)
				if(randGener < 5):
					trainStandingNPC[x] = viz.addChild('vcc_male.cfg')
				else:
					trainStandingNPC[x] = viz.addChild('vcc_female.cfg')
					
				trainStandingNPC[x].state(1) # Looping idle animation
				trainStandingNPC[x].setEuler(random.randint(-180, 180),0,0) # Turns him to face you
				trainStandingNPC[x].setPosition(pos) # Moves him back so that he is in full view xPos,yPos,zPos
				trainStandingNPC[x].setParent(train)


def SpawnPlatformNPC():
	seatTaken = []
	for x in range(0, 29):
		seatTaken.append(1)
		seatTaken[x] = False	
	
	for x in range(0, 10):
		# Random Pos
		numFound = False
		rand = 0
		
		while(numFound == False):
			rand = random.randint(0, 28)
			if(seatTaken[rand] == False):
				numFound = True
				seatTaken[rand] = True
		
		pos = platStandingPos[rand]
		
		platformNPC.append(1)
		
		randGener = random.randint(0, 10)
		if(randGener < 5):
			platformNPC[x] = viz.addChild('vcc_male.cfg')
		else:
			platformNPC[x] = viz.addChild('vcc_female.cfg')
				
		platformNPC[x].state(1) # Looping idle animation
		platformNPC[x].setEuler(0,0,0) 
		platformNPC[x].setPosition(pos)

#seatedNPC.append(1)
#seatedNPC[0] = viz.addChild('vcc_male2.cfg')
#seatedNPC[0].state(6) # Looping idle animation
#seatedNPC[0].setEuler(180,0,) # Turns him to face you
#seatedNPC[0].setPosition(-0.8,0.2,7) # Moves him back so that he is in full view
##man.collideMesh()
#
#seatedNPC.append(1)
#seatedNPC[1] = viz.addChild('vcc_male2.cfg')
#seatedNPC[1].state(6) # Looping idle animation
#seatedNPC[1].setEuler(180,0,) # Turns him to face you
#seatedNPC[1].setPosition(0.0,0.2,7) # Moves him back so that he is in full view
##man.collideMesh()
#
#seatedNPC.append(1)
#seatedNPC[2] = viz.addChild('vcc_male2.cfg')
#seatedNPC[2].state(6) # Looping idle animation
#seatedNPC[2].setEuler(180,0,) # Turns him to face you
#seatedNPC[2].setPosition(0.7,0.2,7) # Moves him back so that he is in full view
##man.collideMesh()
#
#seatedNPC.append(1)
#seatedNPC[3] = viz.addChild('vcc_male2.cfg')
#seatedNPC[3].state(6) # Looping idle animation
#seatedNPC[3].setEuler(180,0,) # Turns him to face you
#seatedNPC[3].setPosition(1.4,0.2,7) # Moves him back so that he is in full view
##man.collideMesh()