import os
import random

Ivalue    = [-7.0,-10.0,7.0,10.0]
couplings =['SMEFTcpv','ctGIm','ctGRe','cQj38','cQj18','cQu8','cQd8','ctj8','ctu8','ctd8','cQj31','cQj11','cQu1','cQd1','ctj1','ctu1','ctd1']
n=-1

rwgtCards = ''
rwgtCards = rwgtCards + 'launch /scratch365/rgoldouz/MG33/new/MG5_aMC_v2_6_5/TT0j2l_ref'+ '\n'

for WC1 in couplings:
    for i in Ivalue:
        if WC1=='ctGRe':
            i = i/10.0
        rwgtCards = rwgtCards + 'launch -n '+ WC1 + '=' + str(i) +'\n'
        n  = n+1
        for WC2 in couplings:
            if WC1 == WC2:
                rwgtCards = rwgtCards +'set param_card ' + WC2 + ' ' + str(i)  + '\n'
            else:
                rwgtCards = rwgtCards +'set param_card ' + WC2 + ' ' + str(0.0)  + '\n'
rwgtCards = rwgtCards + 'launch -n SM' +'\n'
for WC2 in couplings:
    rwgtCards = rwgtCards +'set param_card ' + WC2 + ' ' + str(0.0)  + '\n'
open('AutoRun.dat', 'wt').write(rwgtCards)
