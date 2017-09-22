import os

def AppendToFile(file, stringtoappend):
    hs = open(file,"a")
    
    if(os.path.getsize(file) > 0):
        hs.write("\n" + stringtoappend)
    else:
        hs.write(stringtoappend)

    hs.close()