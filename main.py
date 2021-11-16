import requests
import json
def url_input_control(url_sayisi):
    while (True):
        print(url_sayisi,end='')
        url_parameter = input(". url'i giriniz: ")
        print(url_sayisi, end='')
        token_parameter = input(". token'ı giriniz (Başında 'Token' ile birlikte): ")
        try:
            request_url = requests.get(url=url_parameter,
                                           headers={'Authorization': token_parameter})
            if (request_url.status_code >= 300):
                print("Token veya url id hatası var! Tekrar deneyin.")
                continue
        except:
                print("Url hatası! Yeniden deneyiniz.")
                continue
        return request_url
def url_control():
    while(True):
        request_staging=url_input_control(1)
        request_panel=url_input_control(2)
        staging_json_string = json.dumps(request_staging.json())
        staging_json_dictionary = json.loads(staging_json_string)
        panel_json_string = json.dumps(request_panel.json())
        panel_json_dictionary = json.loads(panel_json_string)
        return staging_json_dictionary,panel_json_dictionary
def panel_value_none_control(panel_parameter,panel_key):
    try:
        panel_parameter[panel_key]
    except:
        return False
    return True
def return_panel_keys_diff(staging_parameter,panel_parameter):
    panel_keys=[]
    for panel_key in panel_parameter.keys():
        try:
            staging_parameter[panel_key]
        except:
            panel_keys.append(panel_key)
    return panel_keys
def control_list(staging_list,panel_list):
    max_counter = len(staging_list)
    min_counter = len(panel_list)
    if (len(staging_list) < len(panel_list)):
        max_counter, min_counter = min_counter, max_counter
    if (type(staging_list) != type(panel_list) and panel_list!=None):
        print(staging_list,"---Değişti.--->",panel_list)
    elif(type(staging_list) != type(panel_list) and panel_list==None):
        print(staging_list,"---Kaldırıldı.---> None")
    else:
        for i in range(min_counter):
            if (type(staging_list[i]) == list):
                print("[")
                control_list(staging_list[i], panel_list[i])
                print("]")
            elif (type(staging_list[i]) == dict):
                print("{")
                diff_checker(staging_list[i], panel_list[i])
                print("}")
            else:
                if (type(staging_list[i]) != type(panel_list[i])):
                    print(staging_list[i],"---Değişti.--->",panel_list[i])
                else:
                    staging_list_value=staging_list[i]
                    panel_list_value=panel_list[i]
                    if(staging_list_value == panel_list_value):
                        print(staging_list_value,"---Değişmedi.--->",panel_list_value)
                    else:
                        print("Değişti")

        if(min_counter!=max_counter):
            if(len(staging_list) < len(panel_list)):
                for i in range(len(panel_list)-len(staging_list)):
                    print("None ---Eklendi.--->",panel_list[len(staging_list)+i])
            else:
                for i in range(len(staging_list)-len(panel_list)):
                    print(staging_list[len(panel_list)+i],"---Kaldırıldı.---> None")

def return_array(json_parameter):
    dictionary_array=[]
    for one_json in json_parameter:
        one_json_string = json.dumps(one_json)
        one_json_dictionary = json.loads(one_json_string)
        dictionary_array.append(one_json_dictionary)
    return dictionary_array
def diff_checker(staging_parameter,panel_parameter):
    staging_keys=list(staging_parameter.keys())
    for i in range(len(staging_keys)):
        if(type(staging_parameter.get(staging_keys[i]))!=type(panel_parameter.get(staging_keys[i])) and panel_parameter.get(staging_keys[i])!=None):
            print(staging_keys[i],":",staging_parameter.get(staging_keys[i]),"---Değişti.--->",staging_keys[i],":",panel_parameter.get(staging_keys[i]))
        elif(type(staging_parameter.get(staging_keys[i]))!=type(panel_parameter.get(staging_keys[i])) and panel_value_none_control(panel_parameter,staging_keys[i])==False):
            print(staging_keys[i],":",staging_parameter.get(staging_keys[i]),"----Kaldırıldı.---> None")
        else:
            if(type(staging_parameter.get(staging_keys[i]))==list):
                print(staging_keys[i],": [")
                control_list(staging_parameter.get(staging_keys[i]),panel_parameter.get(staging_keys[i]))
                print("]")
            elif(type(staging_parameter.get(staging_keys[i]))==dict):
                print(staging_keys[i], ": [")
                diff_checker(staging_parameter.get(staging_keys[i]),panel_parameter.get(staging_keys[i]))
                print("]")
            else:
                staging_value=staging_parameter.get(staging_keys[i])
                panel_value=panel_parameter.get(staging_keys[i])
                if(staging_value == panel_value):
                    print(staging_keys[i],":",staging_value,"---Değişmedi.--->",staging_keys[i],":",panel_value)
                else:
                    print(staging_keys[i],":",staging_value,"---Değişti.--->",staging_keys[i],":",panel_value)
    diff_panel_keys=return_panel_keys_diff(staging_parameter,panel_parameter)
    for i in range(len(diff_panel_keys)):
        print("None ---Eklendi.--->",diff_panel_keys,":",panel_parameter[diff_panel_keys[i]])
def main():
    staging_json_dictionary_main, panel_json_dictionary_main=url_control()
    diff_checker(staging_json_dictionary_main,panel_json_dictionary_main)

main()


