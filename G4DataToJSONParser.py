import re
import json
from math import sqrt

CONST_G4WT0 = "G4WT0 > " 
CONST_END_OF_LOCAL_RUN = "End of Local Run"
G4TRACK_PATTERN = re.compile("\* G4Track Information:   Particle = (.+),   Track ID = (\d+),   Parent ID = (\d+)")
G4DATA_PATTERN = re.compile("(\d)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+([\d\.\+-e]+)\s+(\w+)\s+(\w+)") 

def readG4Output(outfile): 
    ignore = False
    
    g4wt0 = []
    with open(outfile, "r") as g4out:
        for line in g4out:
            #filter lines starting with G4WT0 >  
            if line.startswith(CONST_G4WT0) : 
                #remove the leading "G4WT0 > "
                line = line.replace(CONST_G4WT0, "").strip().rstrip('*')
                #ignore end of local run summary
                if line.find(CONST_END_OF_LOCAL_RUN) != -1:
                    ignore = True
                #not empty
                if line and not ignore:
                    g4wt0.append(line)
    return g4wt0

def matchG4Track(line): 
    m = G4TRACK_PATTERN.match(line)
    if m:
        return {'Particle' : m.group(1), 
                'Track_ID' : int(m.group(2)), 
                'Parent_ID' : int(m.group(3))}
    else:
        return None

def matchG4Data(line): 
    m = G4DATA_PATTERN.match(line)
    if m:
        return {'Step' : int(m.group(1)), 
                'X' : float(m.group(2)), 
                'Y' : float(m.group(3)),
                'Z' : float(m.group(4)),
                'KinE' : float(m.group(5)),
                'dE' : float(m.group(6)),
                'StepLeng' : float(m.group(7)),
                'TrackLeng' : float(m.group(8)),
                'NextVolume' : m.group(9),
                'ProcName' : m.group(10)}
    else:
        return None
    
def getG4Summary(t):
    tid = t['G4Track Info']['Track_ID']
    pid = t['G4Track Info']['Parent_ID']
    particle = t['G4Track Info']['Particle']
    step0 = t['G4Data'][0]
    stepF = t['G4Data'][-1]
    x0 = float(step0['X'])
    y0 = float(step0['Y'])
    z0 = float(step0['Z'])
    kinE  = float(step0['KinE'])
    xF = float(stepF['X'])
    yF = float(stepF['Y'])
    zF = float(stepF['Z'])
    trackLeng = stepF['TrackLeng']
    travelDist = sqrt((xF - x0)**2 + (yF - y0)**2 + (zF - z0)**2)
    return {'Track_ID': tid, 'Parent_ID': pid,  'Particle': particle, 'KinE': kinE, 'TravelDist': travelDist, 'TrackLeng': trackLeng }
    
    
def getG4Tracks():
    
    tracks = []
    track = {}
    for line in raw:
        
        t = matchG4Track(line)
        
        if t:
          #Flush previous track if any
          if track:
#              track['G4Summary'] = getG4Summary(track)
#              tracks.append(track.copy())
              tracks.append(getG4Summary(track))
        
          track.clear()
          track['G4Track Info'] = t
          track['G4Data'] = [] 
        
        else:
           
           d = matchG4Data(line)    
           if d:
               track['G4Data'].append(d)
               
    return tracks


def getG4RunSummary(r: dict):
    summary = {}
    for t in r['Tracks']:

        if t['Particle'] in summary.keys():
           summary[t['Particle']] += 1
        else:
           summary[t['Particle']] = 1
           
    return summary    
    
    

def getG4Runs():
    
    runs = []
    run = {}
    run_ID = 0
    
#    sortedTracks = sorted(tracks, key=lambda t: t['G4Track Info']['Track_ID']) 
    for t in tracks:
         
#        if t['G4Track Info']['Parent_ID'] == "0":
         if t['Parent_ID'] == 0:
            
            if run:
               run['Summary'] = getG4RunSummary(run)
               runs.append(run.copy())
            
            run_ID += 1
            run.clear()
            run['Run_ID'] = run_ID  
            run['Tracks'] = [t]
            
         else :
            
            run['Tracks'].append(t)
            
    if run:
       run['Summary'] = getG4RunSummary(run)
       runs.append(run.copy())
    
        
    return runs

#step0 XYZ K
#stepN XYZ TrackLenght

def trackTree(p: dict , trks: list ):

#    pid = p['G4Track Info']['Track_ID']
    pid = p['Track_ID']
    tracktree = {'Parent' : p.copy(), 'Children' : []} 
    for t in trks:
#        if t['G4Track Info']['Parent_ID'] == pid:
        if t['Parent_ID'] == pid:
            trks.remove(t)
            tracktree['Children'].append(trackTree(t, trks))
          
    return tracktree 
     
    
    

def getNestedRun():
    
    nruns = []
    
    for fr in flatRuns:
#        sortedTrucks  = sorted(fr['Tracks'], key=lambda t: t['G4Track Info']['Track_ID'])  
        sortedTrucks  = sorted(fr['Tracks'], key=lambda t: t['Track_ID'])  
        root = sortedTrucks.pop(0)
        nruns.append({'Run_ID': fr['Run_ID'], "Root": trackTree(root, sortedTrucks)})       

    return nruns

    

#read geant4 output  
raw  = readG4Output("C:/Users/Jonathan/3rdYearProject/verbose1simulation.txt")
with open('C:/Users/Jonathan/3rdYearProject/rawdata.txt', 'w') as datafile:
    datafile.writelines(raw)

#arrange data by track

#A track is dictionary {'G4Track Information': {}, 'G4Data' : [ {} ] } 
tracks = getG4Tracks()

#A flatten run is an unordered list of related tracks
flatRuns = getG4Runs()


#nestedRun = getNestedRun()
        
        
#runs = [t for t in tracks if t['G4Track Info']['Parent_ID'] == "0"]
        
with open('C:/Users/Jonathan/3rdYearProject/data.json', 'w') as outfile:
    json.dump(flatRuns, outfile)


