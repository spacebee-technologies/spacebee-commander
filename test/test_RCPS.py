#The test evaluates packet loss during the transmission of telecommands by continuously sending requests,
# monitoring responses.
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_src_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'src/'))
sys.path.append(parent_src_dir)

from commander import Commander


contador=0
batch=50
recibidos=0

while True:
    commander = Commander()

    tc_test=commander.getTelecommand(1)  #use getTimestamp() TC

    delay=0.01

    for i in range(0,batch):
        tc_test.loadInputArguments(None)
        response=commander.send_message(tc_test,3) #3:Request protocol 
        if response:
            recibidos+=1
        time.sleep(delay)
    contador=contador+batch

    print("\n\n------------------------------------------------")
    print(f"Send {contador} packages")
    print(f"{recibidos/contador*100}% packages receive  \n\n")

    time.sleep(10)