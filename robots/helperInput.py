def keyInSelect(prefixes):
    print("")
    
    for i in range(len(prefixes)):
        print("[{}] {}".format(i+1, prefixes[i]))

    indexOptions = "["
    for i in range(len(prefixes)):
        indexOptions += str(i+1)+", "
    indexOptions = str(indexOptions[:-2]+"]")

    print("")
    indexArrayPrefix = int(input(("Choose one option {}: ".format(indexOptions))))-1

    return indexArrayPrefix