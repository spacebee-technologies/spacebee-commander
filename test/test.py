from commander import Commander
import time

contador=0
while True:
    commander = Commander()

    tc_test=commander.getTelecommand(1)  #Get timestamp TC

    delay=0.01

    for i in range(0,50):
        tc_test.loadInputArguments(None)
        commander.send_message(tc_test,1) #1:Send protocol 
        time.sleep(delay)
    contador=contador+50
    print(contador)
    time.sleep(10)