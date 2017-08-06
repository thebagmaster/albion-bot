import mem
import msvcrt

filename = "test-r.txt"
done = False
todo = ['move','gather','bank','repair']
resource = 'move'
base = mem.BASE
while not done:
    if msvcrt.kbhit():
        char = msvcrt.getch().decode('UTF-8')
        if(char == ']'):
            x=mem.readMemFloat(base + 0x1042B18,[0])
            y=mem.readMemFloat(base + 0x1042B20,[0])
            with open(filename, "a") as f :
                f.write(str(x) + ',' + str(y) + ',' + str(resource) + '\n')
            print (x,y,resource)
        if(char == '['):
            done = True
        if(char == 'f'):
            filename = input('Input File Name: ')
        if(char == '\''):
            resource = todo[(todo.index(resource)+1)%len(todo)]
            print ('todo: ', resource)
