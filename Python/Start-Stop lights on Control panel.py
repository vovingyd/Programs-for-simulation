from pyModbusTCP.client import *
from random import *
from time import sleep

# create ModbusClient instance
client = ModbusClient(host="127.0.0.1", port=502)

# define input and output registers
input_registers = {
    "start": 0,
    "stop": 2,
    "emergency_stop": 3
}
output_registers = {
    "start_light": 9,
    "stop_light": 11
}

# On launch start button is deactivated and stop light is acivated 
client.write_single_coil(output_registers["start_light"], 0)
client.write_single_coil(output_registers["stop_light"], 1)

# define function to check if stop or emergency stop buttons are pressed
def is_stop_mode():
    # read input registers
    if inputs[input_registers["stop"]] == False or inputs[input_registers["emergency_stop"]] == 0:
        return True
    return False

def is_run_mode():
    if inputs[input_registers["start"]] == True and not is_stop_mode():
        return True
    return False

while True:
    inputs = client.read_discrete_inputs(1, 4)
    if is_stop_mode():
        client.write_single_coil(output_registers["start_light"], 0)
        client.write_single_coil(output_registers["stop_light"], 1)
        
    elif is_run_mode():
        client.write_single_coil(output_registers["start_light"], 1)
        client.write_single_coil(output_registers["stop_light"], 0)
    
