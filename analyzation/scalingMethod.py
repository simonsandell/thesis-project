import intersection

def binderIntersection(Ldictavg):
    Llist = sorted(list(Ldictavg.keys()));
    Tlist = sorted(list(Ldictavg[Llist[0]].keys()));
    intersections = [];
    for L,L2 in zip(Llist[:-1],Llist[1:]):
        for T,T2 in zip(Tlist[:-1],Tlist[1:]):
            [doesInt,ix,iy] = intersection.checkcheckIntersection(Ldictavg[L][T].Bin,Ldictavg[L][T2].Bin,Ldictavg[L2][T].Bin,Ldictavg[L2][T2].Bin);
            if doesInt:
                ax = ix + T;
                ay = Ldictavg[L][T]
                intersections.append([T+ix,iy]);
                break;

    return intersections;

def densityIntersection(Ldictavg):
    Llist = sorted(list(Ldictavg.keys()));
    Tlist = sorted(list(Ldictavg[Llist[0]].keys()));
    intersections = [];
    for L,L2 in zip(Llist[:-1],Llist[1:]):
        for T,T2 in zip(Tlist[:-1],Tlist[1:]):
            [doesInt,ix,iy] = intersection.checkcheckIntersection(Ldictavg[L][T].Rs,Ldictavg[L][T2].Rs,Ldictavg[L2][T].Rs,Ldictavg[L2][T2].Rs);
            if doesInt:
                ax = ix + T;
                ay = Ldictavg[L][T]
                intersections.append([1/L2,T+ix,iy]);
                break;

    return intersections;

