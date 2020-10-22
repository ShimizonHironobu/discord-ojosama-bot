import json

def get(param):
    param_array = param.split('.')

    f = open("./config/"+param_array.pop(0)+".json", "r")
    json_data = json.load(f)
    f.close()

    if len(param_array) != 0 :
        for item in param_array :
            json_data = json_data.get(item)

    return json_data
    