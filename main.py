import hashlib # alright imported the libary that we need in order
# to use our hash function, next we need to create hash object an instance of it

import json 


def getHash(ourFile):
    chunk_size = 4096
    SHA_256 = hashlib.sha256() # we have created an instance of the sha_256 object that we imported from hashlib cool
    with open(ourFile, "rb") as f: 
        # we are reading the file in bytes okay, cool 
        
        while True: 
            toBeProccessed = f.read(chunk_size) # this will get the next 4096 bytes everytime i call it 
            
            if (toBeProccessed == b""):
                break
            
            SHA_256.update(toBeProccessed)
            
    return SHA_256.hexdigest()






listOfFiles = ["/bin/bash", "/bin/ls", "/usr/bin/ssh", "/etc/passwd", "/etc/shadow"]

 
try: 
    with open('baseline.json', 'r') as f:
        mainDic = json.load(f) # top level data will be our top container dictionary
        baselines = mainDic["1"]
        hashReCalc = {}

        for key in baselines:
            newHash = getHash(key)
            if (newHash != baselines[key]):
                hashReCalc[key] = newHash

        if (len(hashReCalc) > 0):
            print("Modifications Occurred!\n")
            for key in hashReCalc:
                print(f"Expected: {key} -> {baselines[key]}, Actual: {key} -> {hashReCalc[key]}\n")
        else:
            print("No Modifications Made!")

except (json.JSONDecodeError, FileNotFoundError):
    # okay we know the file is empty right now conceptually, hence secure baseliens must be created
    baselines = {}

    for curr in listOfFiles:
        hashVal = getHash(curr)
        baselines[curr] = hashVal # we added the key value which is the file path, along with 
        # its actual value which is the hash value we created
    
    topDic = {}
    topDic[1] = baselines
    
    with open('baseline.json', 'w') as f:
        json.dump(topDic, f)

        
    






        






