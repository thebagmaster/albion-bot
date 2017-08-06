import mem
import win32api, win32con
import ctypes, ctypes.wintypes
import win32ui
import math
from time import sleep
import sys
import threading
from key import Key
import random

base = mem.BASE
base2 = 0x10000000 #mono.dll base
pos = 0
tol = .7
searchrad = 70
txt = 'test-r.txt'
txtrep = 'swampcross-rep.txt'
go = (235,1,'move')
now = (0,0)

path = []
reppath = []
gather = False
key = Key()

rect = win32ui.FindWindow(None,u'Albion Online Client').GetWindowRect()
x = rect[0]
y = rect[1] - 40
w = rect[2] - x
h = rect[3] - y

while 0:
    print(win32api.GetCursorPos()[0]-x,win32api.GetCursorPos()[1]-y)

up = (x+w/2,y)
dn = (x+w/2,y+h)
lf = (x,y+h/2)
rt = (x+w,y+h/2)

c = (int(x+w/2),int(+h/2))
r = 150

with open(txt) as f:
    path = f.readlines()
path = [x.strip() for x in path]

with open(txtrep) as f:
    reppath = f.readlines()
reppath = [x.strip() for x in reppath]

def main():
    followPath(path,bankCallback)

def click(pt):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pt[0],pt[1],0,0)
    sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pt[0],pt[1],0,0)
def closeto(pt1,pt2):
    return (math.fabs(pt1[0]-pt2[0])<tol and math.fabs(pt1[1]-pt2[1])<tol)
def move_click(pos):
    random_movement(pos)
    click(pos)
def random_movement(pos):
    #win32api.SetCursorPos(pos)
    #return
    start = (0,0)
    start = win32api.GetCursorPos()
    x1 = pos[0]
    y1 = pos[1]
    x2 = start[0]
    y2 = start[1]

    if((x2-x1) == 0):
        return
    slo=(y2-y1)/(x2-x1)
    th=math.atan(slo)
    c=math.cos(th)
    s=math.sin(th)
    A=-slo/(2*math.pi)
    A*=0.01
    K=(x2-x1)/c

    t=1
    for i in range(50):
        t = 1 - i * 0.02
        win32api.SetCursorPos((int(K * (c * t - s * math.sin(2*math.pi*t)) + x1),
                               int(K *( s * t + A * math.sin(2*math.pi*t)) + y1)))
        sleep(0.005)

def todo(go):
    action = go[2]
    if(action != 'move'):
        win32api.SetCursorPos(c)
        ctypes.windll.user32.mouse_event(0x0008,int(go[0]),int(go[1]),0,0)
        ctypes.windll.user32.mouse_event(0x0010,int(go[0]),int(go[1]),0,0) #right mouse up
    else:
        return

    def searchUntilCursor(maxserches,callback):
        searches = 0
        deg = 2*math.pi*random.random()
        while searches < maxserches:
            sleep(0.05)
            searches += 1
            r = searchrad + (10-20*random.random())
            #random_movement((int(c[0]),int(c[1])))
            cur = (int(c[0]+math.cos(deg)*r),int(c[1]+math.sin(deg)*r))
            random_movement(cur)
            sleep(0.05)
            #check if cursor diff 9 normal 24 is clickable
            if(mem.readMemFloat(base + 0x1093224,[0,0x18]) == 24):
                callback(cur)
                searches = 99999
            deg+=.4#~70deg
    def gather(cur):
        click(cur)
        harvesting = True
        gathers = 0
        while harvesting:
            sleep(0.2)
            gathers += 1
            if(mem.readMemFloat(base + 0x109060C,[0,0x6f4,0xd8,0x1f4,0x5c8,0x318]) == 0 or gathers > 100):
                harvesting = False
                break
    def repair(cur):
        click(cur)
        sleep(2)
        repairall = (x+110,y+410)
        move_click(repairall)
        sleep(2)
        pay = (x+740,y+471)
        move_click(pay)
        sleep(1)

    def bank(cur):
        click(cur)
        sleep(1)
        #inventory 80px tiles
        #topleft 1590,540
        key.PressKey(0x2A)#lshift
        sleep(0.05)
        cols = 4
        rows = 5
        xi = x + 1060
        yi = y + 425
        for i in range(rows):
            for j in range(cols):
                cur = (xi+j*55,yi+i*55)
                if (not(i == 0 and j < 2)):
                    move_click(cur)
                    sleep(0.2)
        key.ReleaseKey(0x2A)
        key.KeyStroke('escape')
    if(action=='gather'):
        searchUntilCursor(12,gather)
    elif(action=='repair'):
        searchUntilCursor(22,repair)
    elif(action=='bank'):
        searchUntilCursor(80,bank)

    ctypes.windll.user32.mouse_event(0x0002,int(go[0]),int(go[1]+200),0,0) #right mouse up
    ctypes.windll.user32.mouse_event(0x0004,int(go[0]),int(go[1]+200),0,0) #right mouse dn

    ctypes.windll.user32.mouse_event(0x0008,int(go[0]),int(go[1]+200),0,0) #right mouse dn


def repairAndBank():
    followPath(reppath,bankCallback)
    ctypes.windll.user32.mouse_event(0x0008,int(go[0]),int(go[1]+200),0,0) #right mouse dn
def adjustVector():
    global now
    now = (mem.readMemFloat(base + 0x1042B18,[0]),mem.readMemFloat(base + 0x1042B20,[0]))
    sys.stdout.write(str(now) + ',' + str(go) + '\r')
    sys.stdout.flush()
    dy = (now[1] - go[1])
    dx = -(go[0] - now[0])
    deg = math.atan2(dy,dx)
    random_movement((int(c[0]+math.cos(deg)*r),int(c[1]+math.sin(deg)*r)))
def getNextPos(path):
    global go
    go = path[pos].split(',')
    go[0] = float(go[0])
    go[1] = float(go[1])
    print(pos,':heading to ', go[0], ',', go[1], ' to ' + go[2], ' currently', now[0], ',', now[1],)
def followPath(path,callback):
    global pos
    getNextPos(path)
    while not win32api.GetAsyncKeyState(0x1B):
        adjustVector()
        sleep(.1)
        if(closeto(now,go)):
            pos += 1
            if(pos >= len(path)):
                pos = 0 #and check if full
                callback()
            todo(go)
            getNextPos(path)
def bankCallback():
    key.KeyStroke('i')
    key.KeyStroke('i')
    sleep(.1)
    load = mem.readMemFloat(base + 0x01044B24,[0,0x68,0x778,0xc,0x54,0x5c])
    if(load >= 98):
        repairAndBank()

if __name__ == "__main__":
    main()
