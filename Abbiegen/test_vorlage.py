
def schonbesucht(knoten,name):
        for s in knoten.predecessors:
                if s.name==name:
                        return True
        return False

def insertNodeSorted(liste,knoten):
        i=0
        for oldNode in liste:
                if oldNode.cost>knoten.cost:
                        liste.insert(i,knoten)
                        return liste
                else:
                        i=i+1
        liste.insert(i,knoten)
        return liste

class node(object):
        def __init__(self,name,uID,pre=None,costInc=1):
                self.uniqueID=uID
                self.name=name
                self.predecessors=[]
                self.cost=0
                if pre != None:
                        self.predecessors.extend(pre.predecessors)
                        self.predecessors.append(pre)
                        self.cost=pre.cost+costInc

def breitensuche(adj, start, suche,verbose=False):
        nodeCount=0
        s=node(start,nodeCount)
        queue = [ s ]
        while len(queue) > 0:
                aktiverKnoten = queue.pop(0)
                if aktiverKnoten.name==suche:
                        return aktiverKnoten
                if verbose:
                        print (aktiverKnoten.name)
                if adj[aktiverKnoten.name]:
                        for andererKnoten in adj[aktiverKnoten.name].keys():
                                if schonbesucht(aktiverKnoten,andererKnoten):
                                        continue
                                if verbose:
                                        print ("         ",andererKnoten)
                                nodeCount+=1
                                cost=adj[aktiverKnoten.name][andererKnoten]
                                s=node(andererKnoten,nodeCount,pre=aktiverKnoten,costInc=cost)
                                queue.append(s)
                if verbose:
                        print ([a.name for a in queue])
        return False

def tiefensuche(adj, startnode, suche,nodeCount=0,verbose=False):
        if startnode.name == suche:
                return startnode
        #startnode=node(start,nodeCount)
        if adj[startnode.name]:
                for andererKnoten in adj[startnode.name].keys():
                        if schonbesucht(startnode,andererKnoten):
                                        continue
                        if verbose:
                                        print("         ",andererKnoten)
                        nodeCount+=1
                        cost=adj[startnode.name][andererKnoten]
                        newnode=node(andererKnoten,nodeCount,pre=startnode,costInc=cost)
                        a = tiefensuche(adj,newnode,suche,nodeCount,verbose)
                        if a:
                                return a
        return False

def uniformCostSearch(adj, start, suche,verbose=False):
        nodeCount=0
        s=node(start,nodeCount)
        queue = [ s ]
        while len(queue) > 0:
                aktiverKnoten = queue.pop(0)
                if aktiverKnoten.name==suche:
                        return aktiverKnoten
                if verbose:
                        print (aktiverKnoten.name)
                if adj[aktiverKnoten.name]:
                        for andererKnoten in adj[aktiverKnoten.name].keys():
                                if schonbesucht(aktiverKnoten,andererKnoten):
                                        continue
                                if verbose:
                                        print ("         ",andererKnoten)
                                nodeCount+=1
                                cost=adj[aktiverKnoten.name][andererKnoten]
                                s=node(andererKnoten,nodeCount,pre=aktiverKnoten,costInc=cost)
                                insertNodeSorted(queue,s)
                if verbose:
                        print ([a.name for a in queue])
        return False

if __name__=="__main__":
    
        streetMap=dict({'frankfurt':{'wuerzburg':111,'mannheim':85},
                                        'wuerzburg':{'frankfurt':111,'stuttgart':140,'ulm':183,'nuernberg':104},
                                        'nuernberg':{'wuerzburg':104,'muenchen':170,'ulm':171,'mannheim':230,'bayreuth':75,'passau':220},
                                        'mannheim':{'frankfurt':85,'karlsruhe':67,'nuernberg':230},
                                        'karlsruhe':{'mannheim':67,'stuttgart':64,'basel':191},
                                        'stuttgart':{'karlsruhe':64,'wuerzburg':140,'ulm':107},
                                        'ulm':{'stuttgart':107,'wuerzburg':183,'nuernberg':171,'muenchen':123,'memmingen':55},
                                        'muenchen':{'ulm':123,'nuernberg':170,'rosenheim':59,'memmingen':115,'passau':189},
                                        'memmingen':{'muenchen':115,'ulm':55,'zuerich':184},
                                        'basel':{'zuerich':85,'karlsruhe':191,'bern':91},
                                        'bern':{'basel':91,'zuerich':120},
                                        'zuerich':{'basel':85,'bern':120,'memmingen':184},
                                        'rosenheim':{'muenchen':59,'salzburg':81,'innsbruck':93},
                                        'innsbruck':{'rosenheim':93,'landeck':73},
                                        'landeck':{'innsbruck':73},
                                        'salzburg':{'rosenheim':81,'linz':126},
                                        'linz':{'passau':102,'salzburg':126},
                                        'passau':{'linz':102,'nuernberg':220,'muenchen':189},
                                        'bayreuth':{'nuernberg':75},
                                        })

        FROM="frankfurt"
        TO="muenchen"

        print( "-"*40+" Breitensuche "+"-"*40)
        found = breitensuche(streetMap,FROM,TO)
        print ("Found ",found.name)
        print ("Total cost: ",found.cost)
        print ("Node ID: ",found.uniqueID)
        print ("on path ")
        for a in found.predecessors:
                print (a.name,a.cost)
        print()

        print ("-"*40+" Tiefensuche "+"-"*40)
        FROMNODE=node(FROM,0)
        found = tiefensuche(streetMap,FROMNODE,TO,verbose=True)
        print("Found ",found.name)
        print ("Total cost: ",found.cost)
        print ("Node ID: ",found.uniqueID)
        print ("on path ")
        for a in found.predecessors:
                print (a.name,a.cost)
        print()

        print ("-"*40+" Uniform Cost Search "+"-"*40)
        found = uniformCostSearch(streetMap,FROM,TO)
        print ("Found ",found.name)
        print ("Total cost: ",found.cost)
        print ("Node ID: ",found.uniqueID)
        print ("on path ")
        for a in found.predecessors:
                print (a.name,a.cost)