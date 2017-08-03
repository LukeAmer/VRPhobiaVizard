import viz
import vizact 
import viztask
import vizshape
import vizmultiprocess

import SetupHMD
import NPCSpawner

import EnvironmentSetup
import HeartRate

#viz.setMultiSample(4)
#viz.fov(60)

viz.go(viz.EMBEDDED)


def RecordHR():
    while not viz.done():
        yield viztask.waitTime(3) # Record Heart Rate into Array every 3 seconds
        global recordedHR
        
        if(HeartRate.heartRate > 20): 
            recordedHR.append(HeartRate.heartRate) # Add value to Array
        

# Setup Audio
trainAtStation = viz.addAudio('Assets/Audio/AtStation.wav')
trainAtStation.loop(viz.OFF) 
trainAtStation.volume(1.0)

trainMove = viz.addAudio('Assets/Audio/TrainLoop.wav')
trainMove.loop(viz.OFF) 
trainMove.volume(1.0) 

trainCrowdLow = viz.addAudio('Assets/Audio/Crowds.wav')
trainCrowdLow.loop(viz.ON) 
trainCrowdLow.volume(0.1) 

trainCrowdMed = viz.addAudio('Assets/Audio/Crowds.wav')
trainCrowdMed.loop(viz.ON) 
trainCrowdMed.volume(0.5) 

trainCrowdHigh = viz.addAudio('Assets/Audio/Crowds.wav')
trainCrowdHigh.loop(viz.ON) 
trainCrowdHigh.volume(1.0) 

# Train Move forward for 60 seconds function
moveForward = vizact.move(0,0,4,60)

# Global Variables
playerOnTrain = False;
stage = -1
averageHR = 0
age = 0
recordedHR = []
spacePressed = False
restingHR = 0
overwriteHR = 0

viz.mouse.setOverride() # Disable mouse movement and rotation control

# Black screen overlay allowed Fade in and Fade out
blackScreen = viz.addTexQuad(size=100, pos=[0,0,1], color=viz.BLACK)
blackScreen.setReferenceFrame(viz.RF_EYE)
blackScreen.disable([viz.LIGHTING, viz.INTERSECTION, viz.DEPTH_TEST, viz.SHADOW_CASTING])
blackScreen.drawOrder(100)
blackScreen.alpha(1.0)

def FadeOut():
    yield viztask.waitCall(blackScreen.runAction,vizact.fadeTo(1.0,time=2.0)) # fade out black screen effect
    
def FadeIn():
    yield viztask.waitCall(blackScreen.runAction,vizact.fadeTo(0.0,time=2.0)) # fade in black screen effect

def MoveToNextStation(): # Leave Station
    print('Leaving Station')
    trainMove.play() # Train Audio
    train.addAction(moveForward) # Move train forward
    SetupHMD.MovePlayer()
    yield viztask.waitTime(30) # Wait 30 seconds
    print('Reset Train Pos')
    train.setPosition(-120, -1, 6) # Reset train at other end of tunnel

    if(SetupHMD.hmdconnected):
        SetupHMD.SetRotation(180)
        trainPos = train.getPosition()
        trainPos[1] += 1.5
        trainPos[2] += 1.6
        SetupHMD.SetPos(trainPos)
    else:
        pos = train.getPosition(viz.ABS_GLOBAL)
        pos[0] += 0.3 # Along Seat
        pos[1] = 1.7 # Eye Height
        pos[2] += 1.3 # Depth
        viz.MainView.setPosition(pos)
        viz.MainView.setEuler(180,0,0)
    
    yield viztask.waitTime(30) # Wait 30 seconds
    print('Arrived at Station')
    trainMove.stop() # Stop Audio
    viztask.schedule(StationReached()) # Trigger next function

def StationReached():
    print('Station Reached')
    trainAtStation.play() # Station audio
    yield viztask.waitTime(5)
    viztask.schedule(FadeOut()) # Old fade out effect
    
    yield viztask.waitTime(2)
    print('Spawn People')
    
    stage = SetStage() # Get stage
    NPCSpawner.SpawnSeatedNPC(train, stage)
    NPCSpawner.SpawnStandingNPC(train, stage)
    
    yield viztask.waitTime(2)
    viztask.schedule(FadeIn())
    
    yield viztask.waitTime(20)
    print('Leave Station')
    trainAtStation.stop()
    viztask.schedule(MoveToNextStation())

def PressSpace():
    global spacePressed
    spacePressed = True

def OverwriteHeartRate(value): # Overwrite Heart Rate value to increase or decrease Stage number
    global overwriteHR
    overwriteHR += value

    if(overwriteHR < 0): # Arrow Key Overwrites -- Up Increases stage - Down Decreases stage
        overwriteHR = 0
    elif(overwriteHR > 5):
        overwriteHR = 5
    
    print('Overwrite Next Stage: ' + str(overwriteHR))

# Keypress events
vizact.onkeydown(' ', PressSpace)
vizact.onkeydown(viz.KEY_UP, OverwriteHeartRate, 1)
vizact.onkeydown(viz.KEY_DOWN, OverwriteHeartRate, -1)
 
def InitalSetup(train):   
#        t1 = viz.add('Assets/Textures/black.png')
#        wall1 = vizshape.addCube() # Setup black room for start and fade transition
#        wall1.setScale([10,5,0.2])
#        wall1.setPosition(0,1,10)
#        wall1.texture(t1)
#        
#        wall2 = vizshape.addCube()
#        wall2.setScale([10,5,0.2])
#        wall2.setPosition(0,1,20)
#        wall2.texture(t1)
#        
#        wall3 = vizshape.addCube()
#        wall3.setScale([0.2,5,10])
#        wall3.setPosition(5,1,15)
#        wall3.texture(t1)
#        
#        wall4 = vizshape.addCube()
#        wall4.setScale([0.2,5,10])
#        wall4.setPosition(-5,1,15)
#        wall4.texture(t1)
#        
#        wall5 = vizshape.addCube()
#        wall5.setScale([10,0.2,10])
#        wall5.setPosition(0,2.5,15)
#        wall5.texture(t1)
#        
#        wall6 = vizshape.addCube()
#        wall6.setScale([10,1.0,10])
#        wall6.setPosition(0,1.0,15)
#        wall6.texture(t1)  
    
        text3D = viz.addText3D('Press Space to begin',pos=[0,0.5,20]) # Create text & position infront of player at a readable distance
        text3D.alignment(viz.ALIGN_CENTER_BOTTOM)
        text3D.setScale(1,1,1)
        text3D.setEuler(0,0,0)
        text3D.setReferenceFrame(viz.RF_EYE)
        text3D.disable([viz.LIGHTING, viz.INTERSECTION, viz.DEPTH_TEST, viz.SHADOW_CASTING])
        text3D.drawOrder(101)
        
        global spacePressed
        global playerOnTrain
        
        if(SetupHMD.hmdconnected):
            SetupHMD.SetRotation(0)
            SetupHMD.SetPos([0, 0, 15])
        else:
            viz.MainView.setPosition([0, 1, 11]) 
            
        while(spacePressed is not True):
            yield viztask.waitFrame(1)

        if(SetupHMD.hmdconnected):
            SetupHMD.SetRotation(180)
            trainPos = train.getPosition()
            trainPos[1] += 1.5
            trainPos[2] += 1.6
            SetupHMD.SetPos(trainPos)
        else:
            pos = train.getPosition(viz.ABS_GLOBAL)
            pos[0] += 0.3 # Along Seat
            pos[1] = 1.7 # Eye Height
            pos[2] += 1.3 # Depth
            viz.MainView.setPosition(pos)
            viz.MainView.setEuler(180,0,0)
        
        
        yield viztask.waitTime(0.1)
        text3D.remove()
        spacePressed = False
        playerOnTrain = True
        
        viztask.schedule(StationReached())
 
        
def SetStage():
    global stage
    global recordedHR
    global restingHR
    global overwriteHR

    if(overwriteHR == stage or stage < 0):
        # Get Heart Rate
        if len(recordedHR) > 0:
            # Average Heart Rate
            averageHeartRate = reduce(lambda x, y: x + y, recordedHR) / len(recordedHR)
            print('Average Heart Rate')
            print averageHeartRate
            recordedHR[:] = []
            if(stage >= 0):
                if(restingHR == 0):
                    restingHR = averageHeartRate
                    print('Resting HeartRate Recorded!')
                    print restingHR
                    
                    if(stage < 5):
                        stage += 1
                else:
                    # Calculate HR difference
                    print('Resting Heart Rate')
                    print restingHR
                    value = restingHR / 10 # 10% of resting heart rate
                    value = averageHeartRate + value # Calculate max heart rate = Resting + 10%
                    print('Max Heart Rate: ' + str(value))
                    print(value)
                    
                    if(averageHeartRate >= value): # If current average heart rate exceeds resting heart rate + 10%, decrease the stage
                        if(stage > 0):
                            stage -= 1
                            print('Decrease Stage')
                    else: # Otherwise, increase stage
                        if(stage < 5):
                            stage += 1
                            print('Increase Stage')                    
            else:
                stage += 1 # First Stage Increase
                
        else:
            stage += 1 # Heart Rate Not Recorded
    else:
        stage = overwriteHR
    

    overwriteHR = stage
    
    trainCrowdLow.stop()
    trainCrowdMed.stop()
    trainCrowdHigh.stop()
    
    if stage == 1: # Set crowd audio
        trainCrowdLow.play()
    elif stage == 2:
        trainCrowdMed.play()
    elif stage == 3:
        trainCrowdMed.play()
    elif stage == 4:
        trainCrowdHigh.play()
    elif stage == 5:
        trainCrowdHigh.play()
    
    return stage
    

def main(): 
    global train
    train = viz.addChild('Assets/Railcar_Main_OS.osgb', scene = viz.Scene1)
    platform = viz.addChild('Assets/environment.osgb', scene = viz.Scene1)
    viz.addChild('sky_day.osgb', scene = viz.Scene1)
    EnvironmentSetup.Start(train)
    NPCSpawner.InitPlat(platform)
    NPCSpawner.InitSeatedPos(train)
    NPCSpawner.InitStandingPos(train)
    NPCSpawner.SpawnPlatformNPC()
    viztask.schedule(RecordHR())
    viztask.schedule(InitalSetup(train))
    

if __name__ == '__main__':
    # This is the main entry point of the program.
    main()

while not viz.done():
    #if(HeartRate.heartRate > 20):        
        #print HeartRate.heartRate
    
    
        # OLD -- Updating position every frame, resulted in judders/shaking of camera
    
#    if(playerOnTrain): # 
#        # Set Player Position
#        if(SetupHMD.hmdconnected):
#            trainPos = train.getPosition()
#            trainPos[1] += 1.7
#            trainPos[2] += 1.6
#            SetupHMD.SetPos(trainPos)
#        else:
#            pos = train.getPosition(viz.ABS_GLOBAL)
#            pos[0] += 0.3 # Along Seat
#            pos[1] = 1.7 # Eye Height
#            pos[2] += 1.3 # Depth
#
#            viz.MainView.setPosition(pos)
#    else:
#        if(SetupHMD.hmdconnected):
#            SetupHMD.SetPos([0, 1, 11])
#        else:
#            viz.MainView.setPosition([0, 1, 11])     
        
    viz.frame()
