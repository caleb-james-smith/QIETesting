# calculateOrbits.py

import bridge_test as bridge

def calcOrbs(rm,slot,seconds,verbose=0):
    a = bridge.control_reg_orbit_histo(rm,slot,0)
    b = bridge.control_reg_orbit_histo(rm,slot,seconds)

    orbitTime1 = 88.924 # microseconds
    # Frequency = 11kHz... this corresponds to b

    bunches = 3564 # total number of bunches
    # spacing = 25.0 * 10**-3 # spacing in microseconds... 25ns
    bunchFrequency = 40.07897 # MHz
    orbitFrequency = 11.2455 # kHz
    spacing = 1/bunchFrequency # 24.95 ns
    orbitTime2 = bunches * spacing # 88.924 microseconds
    orbitTime3 = (1/11.2455) * 10**3 # 88.924 microseconds

    orbits = float(b - a)
    orbitsPerSec = orbits/seconds
    if int(orbitsPerSec) == 0:
        print '\n ***** Orbit Error: orbitsPerSec = 0'
        secondsPerOribt = 0
    else:
        secondsPerOribt = 1/orbitsPerSec # seconds per orbit
    orbitTimeMeasured = secondsPerOribt * 10**6 # microseconds per orbit

    percErr = 100 * abs(orbitTimeMeasured-orbitTime1)/orbitTime1

    print '\nRead Oribt Histos, RM ', rm, ' Slot ', slot
    if verbose:
        print 'num orbits a = ', a
        print 'num orbits b = ', b
        # print 'orbits diff = b - a = ', orbits
        # print 'time delay (s) = ', seconds
        print 'orbits per second = ', orbitsPerSec
        # print 'seconds per orbit = ', secondsPerOribt

    # print 'theoretical orbit time (microseconds) = ', orbitTime1
    # print orbitTime2
    print 'measured orbit time (microseconds) = ', round(orbitTimeMeasured,3)
    print 'percent error = ', round(percErr,3), ' % error'
    if percErr < 0.5:
        print '\n---PASS orbit time'
    else:
        print '\n---FAIL orbit time'
    if bridge.zeroOrbits(rm,slot):
        print '--- PASS zero orbits'
    else:
        print '--- FAIL zero orbits'    

# calcOrbs(rm,slot,seconds,verbose=0)
delay = 1

calcOrbs(4,1,delay,1)
calcOrbs(4,4,delay,1)
