'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import algorithms
import audioOutput
# import json
import keypadInput
import math
from Navigator import Navigator
from DummyPiMegaCommunicator import PiMegaCommunicator # <-----------------------------
import stringHelper
# from threading import Thread
from time import sleep

def main():
    algorithms.printWelcomeMsg()
    
    keypadInput.initKeypad()
    audioOutput.initAudio()
    piMegaCommunicator = PiMegaCommunicator() # <-----------------------------
    piMegaCommunicator.startUp() # <-----------------------------
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    audioOutput.playAudio('welcomeToIris')
    
    srcNodeId = int(keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInOriginNodeIdFollowedByTheHashKey'))
    destNodeId = int(keypadInput.waitAndGetKeyPressesUntilHashKeyWithConfirmationDialog(
            'plsKeyInDestinationNodeIdFollowedByTheHashKey'))
    print(stringHelper.INFO + ' srcNodeId = ' + str(srcNodeId))
    print(stringHelper.INFO + ' destNodeId = ' + str(destNodeId))
    
    mapOfCom1Level1 = algorithms.downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = algorithms.downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = algorithms.downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = algorithms.downloadAndParseMap('COM2', 3)
    linkedMap = algorithms.linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    
    route = algorithms.computeRoute(linkedMap, srcNodeId, destNodeId)
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])
    
    # =========================== NAVIGATION START ===========================================
    
    isNavigationInProgress = True
    currBuildingId = int(str(srcNodeId)[0])
    currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
    routeIdxOfPrevNode = 0
    routeIdxOfNextNode = 1
    
    navigator = Navigator(linkedMap, route, currLocation[0], currLocation[1])
    
    while isNavigationInProgress:
        piMegaCommunicator.pollData() # <-----------------------------
        
        distanceWalked_north = piMegaCommunicator.distanceWalked_north
        distanceWalked_northeast = piMegaCommunicator.distanceWalked_northeast
        distanceWalked_east = piMegaCommunicator.distanceWalked_east
        distanceWalked_southeast = piMegaCommunicator.distanceWalked_southeast
        distanceWalked_south = piMegaCommunicator.distanceWalked_south
        distanceWalked_southwest = piMegaCommunicator.distanceWalked_southwest
        distanceWalked_west = piMegaCommunicator.distanceWalked_west
        distanceWalked_northwest = piMegaCommunicator.distanceWalked_northwest
        heading = piMegaCommunicator.heading
        
        print('distanceWalked_north = ' + str(distanceWalked_north))
        print('distanceWalked_northeast = ' + str(distanceWalked_northeast))
        print('distanceWalked_east = ' + str(distanceWalked_east))
        print('distanceWalked_southeast = ' + str(distanceWalked_southeast))
        print('distanceWalked_south = ' + str(distanceWalked_south))
        print('distanceWalked_southwest = ' + str(distanceWalked_southwest))
        print('distanceWalked_west = ' + str(distanceWalked_west))
        print('distanceWalked_northwest = ' + str(distanceWalked_northwest))
        print('heading = ' + str(heading))
        
        currLocation = [linkedMap.nodesDict[srcNodeId].x, linkedMap.nodesDict[srcNodeId].y]
        currLocation[0] -= distanceWalked_north/math.sqrt(2)
        currLocation[1] += distanceWalked_north/math.sqrt(2)
        currLocation[1] += distanceWalked_northeast
        currLocation[0] += distanceWalked_east/math.sqrt(2)
        currLocation[1] += distanceWalked_east/math.sqrt(2)
        currLocation[0] += distanceWalked_southeast
        currLocation[0] += distanceWalked_south/math.sqrt(2)
        currLocation[1] -= distanceWalked_south/math.sqrt(2)
        currLocation[1] -= distanceWalked_southwest
        currLocation[0] -= distanceWalked_west/math.sqrt(2)
        currLocation[1] -= distanceWalked_west/math.sqrt(2)
        currLocation[0] -= distanceWalked_northwest
        print(stringHelper.INFO + ' currLocation = ' + str(currLocation))
        
        navigator.updateLocation(currLocation[0], currLocation[1], heading)
        
        if navigator.clearedRouteIdx + 1 == len(navigator.route):
            print(stringHelper.AUDIO + ' Navigation completed.')
            audioOutput.playAudio('navigationCompleted')
            break
        
        naviInfo = navigator.getNaviInfo()
        
        print('nextNodeId = ' + str(navigator.route[navigator.clearedRouteIdx + 1]))
        
        if naviInfo[1] > 67.5 and naviInfo[1] < 180:
            print(stringHelper.AUDIO + ' Turn right.')
            audioOutput.playAudio('turnRight')
        elif naviInfo[1] > 180 and naviInfo[1] < 292.5:
            print(stringHelper.AUDIO + ' Turn left.')
            audioOutput.playAudio('turnLeft')
        
        print(stringHelper.INFO + ' heading = ' + str(heading))
        expectedHeading = algorithms.computeBearing(linkedMap.nodesDict[route[routeIdxOfPrevNode]].x,
                                                    linkedMap.nodesDict[route[routeIdxOfPrevNode]].y,
                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].x,
                                                    linkedMap.nodesDict[route[routeIdxOfNextNode]].y,
                                                    ) + 45
        print(stringHelper.INFO + ' expectedHeading = ' + str(expectedHeading))
        print(linkedMap.nodesDict[route[routeIdxOfNextNode]].x)
        print(linkedMap.nodesDict[route[routeIdxOfNextNode]].y)
        print(linkedMap.nodesDict[route[routeIdxOfPrevNode]].x)
        print(linkedMap.nodesDict[route[routeIdxOfPrevNode]].y)
        
        if heading - expectedHeading > 25:
            print(stringHelper.AUDIO + ' Adjust your bearing slightly to the left.')
            audioOutput.playAudio('adjustYourBearingSlightlyToTheLeft')
        elif heading - expectedHeading < -25:
            print(stringHelper.AUDIO + ' Adjust your bearing slightly to the right.')
            audioOutput.playAudio('adjustYourBearingSlightlyToTheRight')
        
        
        
        sleep(10)
    
    # =========================== NAVIGATION END ===========================================
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

if __name__ == '__main__':
    main()
