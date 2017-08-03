import oculus
import steamvr
import viz

global yOffset
global viewLink
yOffset = 1

def SetPos(pos):
	global navigationNode
	global viewLink
	global yOffset
	import vizact
	
	pos[1] *= yOffset
	
	navigationNode.setPosition(pos) # Move navigation node to new position
	viewLink = viz.link(navigationNode, viz.MainView) # Link the navigation node and main view
	viewLink.preMultLinkable(hmd.getSensor()) # Also link hmd sensor

def SetRotation(rot):
	global navigationNode
	global viewLink

	navigationNode.setEuler(rot,0,0) # Alter rotation on the X axis
	viewLink = viz.link(navigationNode, viz.MainView) # Update navigation node linking
	viewLink.preMultLinkable(hmd.getSensor())
	
def MovePlayer():
	import vizact
	if(hmdconnected):
		global navigationNode
		global viewLink
		navigationNode.addAction(vizact.move(-4,0,0,60)) # Move player on the X axis for 60 seconds, at the same speed as the train -- Rather than updating the position relitive to the train every frame, which resulted in jittery movement.
		viewLink = viz.link(navigationNode, viz.MainView)
		viewLink.preMultLinkable(hmd.getSensor())
	else:
		viz.MainView.addAction(vizact.move(-4,0,0,60))

global hmdConnected
hmdconnected = False

hmd = oculus.Rift() # First Look for Oculus Rift -- Return error if not detected

if not hmd.getSensor():
	print 'Oculus Rift not detected'
else:
	hmdconnected = True
	
	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())

	# Apply user profile eye height to view
	profile = hmd.getProfile()
	if profile:
		viewLink.setOffset([0,profile.eyeHeight,0]) # Offset depending on positional tracking eye height
	else:
		viewLink.setOffset([0,1.7,0])
	yOffset = 3.0
		
if(hmdconnected == False): # If Oculus not detected, try find a HTC VIVE
	hmd = steamvr.HMD()
	
	if not hmd.getSensor():
		print 'HTC VIVE not detected'
	else:
		hmdconnected = True
		
		navigationNode = viz.addGroup()
		viewLink = viz.link(navigationNode, viz.MainView)
		viewLink.preMultLinkable(hmd.getSensor())