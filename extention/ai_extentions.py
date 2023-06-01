import os
import json
import datetime

#load / save network

def get_network(): # get input for importing/generating neural network
    read = input("Read from Network in Networks Folder(y/n):")

    if read == "y":
        rel_path = "Networks/" + input("Name of file in Networks Folder:")
        script_dir = os.path.dirname(__file__)
        
        file = open(os.path.join(script_dir, rel_path))

        return None, file
    elif read == "n":
        sizes_string = input("Please type the number of neurons for each layer(seperated by spaces):\n")
        sizes_array = sizes_string.split()
        sizes = [int(numeric_string) for numeric_string in sizes_array]
        return sizes, None
    else:
        return get_network()

def ask_to_save(network, file_name=False): # get the file, where the network should be safed
    if file_name:
        rel_path = "Networks/" + file_name
        script_dir = os.path.dirname(__file__)
        
        file = os.path.join(script_dir, rel_path)
        
        write_to_json(file, network)

        return file
    elif (input("Save Network to Networks Folder(y/n):") == "y"):
        rel_path = "Networks/" + input("Name of file in Networks Folder:")
        script_dir = os.path.dirname(__file__)
        
        file = os.path.join(script_dir, rel_path)
        
        write_to_json(file, network)

        return file
    
def write_to_json(file, network):
        Network = {
            "sizes": network.sizes,
            "biases": [array.tolist() for array in network.biases],
            "weights": [array.tolist() for array in network.weights]
        }

        with open(file, "w") as outfile:
            json.dump(Network, outfile)

# logging

def save_log(new_data):
    rel_path = "Networks/log.txt"
    script_dir = os.path.dirname(__file__)
    
    file = os.path.join(script_dir, rel_path)

    time = datetime.datetime.now()

    with open(file, "a") as text_file:
        text_file.write("[{0}] Time: {1}\n".format(new_data, time))

# Adjust values

def ai_infos_converter(ai_infos):
    output = []
    
    for i in ai_infos:
        output.append(i)
    
    return output