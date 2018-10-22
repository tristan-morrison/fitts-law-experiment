from graphics import *
from datetime import datetime
import time
import random
import csv

def seconds_to_milliseconds (numSeconds):
    return numSeconds * 1000

class App():
    def __init__(self, myIterations, myOutfilename):
        self.iterations = myIterations
        self.outfilename = myOutfilename
        self.winHeight = self.winWidth = 500
        self.window = GraphWin("Fitt's Law Experimenter", self.winWidth, self.winHeight)
        self.data = list()
        self.currentButton = RandomButton(self.winWidth, self.winHeight)
        self.clickCounter = 0;
        self.lastMouseStartPos = Point(0, 0)
        self.lastClickTime = time.time()
        self.startTime = time.time()

        # self.currentButton = self.generateRandomButton()
        # self.currentButton.draw(self.window)

    def clickIsInCurrentButton(self, clickPoint):
        if (pow(clickPoint.getX() - self.currentButton.center.getX(), 2) + pow(clickPoint.getY() - self.currentButton.center.getY(), 2)) <= pow(self.currentButton.circleObj.radius, 2):
            return True
        else:
            return False

    def handleSuccessfulButtonClick(self, clickPoint, timeOfClick):
        nextEntry = list()
        nextEntry.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        nextEntry.append(self.lastClickTime - self.startTime)
        nextEntry.append(timeOfClick - self.startTime)
        nextEntry.append(self.lastMouseStartPos.getX())
        nextEntry.append(self.lastMouseStartPos.getY())
        nextEntry.append(clickPoint.getX())
        nextEntry.append(clickPoint.getY())
        nextEntry.append(self.currentButton.center.getX())
        nextEntry.append(self.currentButton.center.getY())
        nextEntry.append(self.currentButton.radius)
        nextEntry.append(self.clickCounter)
        self.data.append(nextEntry)


    def recycleCurrentButton(self, window):
        self.currentButton.undraw()
        self.currentButton = RandomButton(self.winWidth, self.winHeight)
        self.currentButton.draw(window)

    def writeCSVFromData(self):
        headers = ["Timestamp", "Start Time", "Stop Time", "Start Mouse X", "Start Mouse Y", "Click Mouse X", "Click Mouse Y", "Button Center X", "Button Center Y", "Button Radius", "Failed Clicks"]
        with open(self.outfilename, 'w+') as outputFile:
            writer = csv.writer(outputFile, dialect='excel')
            writer.writerow(headers)
            writer.writerows(self.data)

class RandomButton():
    def __init__(self, winWidth, winHeight):
        self.radius = random.randint(10, 60)
        self.center = Point(random.randint(self.radius, winWidth - self.radius), random.randint(self.radius, winHeight - self.radius))
        self.circleObj = Circle(self.center, self.radius)
        self.circleObj.setFill("blue")
        self.timeOfCreation = seconds_to_milliseconds(time.time())

    def draw(self, window):
        self.circleObj.draw(window)

    def undraw(self):
        self.circleObj.undraw()


    # def blockForStart(self):

def main ():
    iterations = input("Number of clicks to record:")
    outfilename = input("Filename for output file:")

    app = App(iterations, outfilename)

    startText = Text(Point(app.winHeight / 2, app.winWidth / 2), "Click anywhere to start")
    startText.draw(app.window)

    app.lastMouseStartPos = app.window.getMouse()
    startText.undraw()
    app.recycleCurrentButton(app.window)
    successfulClicks = 0
    while successfulClicks < int(app.iterations):
        clickPoint = app.window.getMouse()
        clickTime = time.time()
        if app.clickIsInCurrentButton(clickPoint):
            app.handleSuccessfulButtonClick(clickPoint, clickTime)
            app.lastClickTime = clickTime
            app.lastMouseStartPos = clickPoint
            app.clickCounter = 0
            app.recycleCurrentButton(app.window)
            successfulClicks += 1
        else:
            app.clickCounter += 1
    app.writeCSVFromData()

main()
