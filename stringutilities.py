def SplitStringFromXTillY(input, Startdelimeter, EndDelim ):
    Snippets = []
    while (input.find(Startdelimeter) != -1): 
        startloc = input.find(Startdelimeter) + len(Startdelimeter)
       
        input = input[startloc:]
        
        split = input.split(EndDelim,1)
        Snippets.append(split[0])
        input = split[1]
        print(split[0])
    return Snippets









