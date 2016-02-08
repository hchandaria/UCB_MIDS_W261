# function to calculate purity of cluster and print it. Its a generic function that can be called

def calc_purity(cluster_dist):
    #calculate purity and print class distribution
    print 'Cluster distribution'
    print '-'*100

    user_class =  { 0:'Human', 1:'Cyborg', 2:'Robot', 3:'Spammer' }
    human = sum([cluster_dist[k].get('0',0) for k in cluster_dist.keys()])
    cyborg = sum([cluster_dist[k].get('1',0) for k in cluster_dist.keys()])
    robot = sum([cluster_dist[k].get('2',0) for k in cluster_dist.keys()])
    spammer = sum([cluster_dist[k].get('3',0) for k in cluster_dist.keys()])
    print "{0:>5} |{1:>15} |{2:>15} |{3:>15} |{4:>15}".format(
        "k", "Human"+':'+str(human), "Cyborg"+':'+str(cyborg), "Robot"+':'+str(robot), "Spammer"+':'+str(spammer))
    print '-'*100
    max_cl={}
    total = 0
    for cid, cvalue in cluster_dist.iteritems():
        total += sum(cvalue.values())
        print "{0:>5} |{1:>15} |{2:>15} |{3:>15} |{4:>15}".format(
        cid, cvalue.get('0',0) ,cvalue.get('1',0) ,cvalue.get('2',0) , cvalue.get('3',0))
        max_cl[cid]=max(cvalue.values())
    print '-'*100
    print 'purity : %3.3f' %(100*sum(max_cl.values())*1.0/total)
    print '-'*100