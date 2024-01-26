
import os
import csv
import copy
import numpy as np
os.chdir(".")
graddict = {}
global sentimentdict
sentimentdict = {}

if os.path.exists("Analysis/accuracy.csv"):
    os.remove("Analysis/accuracy.csv")
with open("Analysis/accuracy.csv","a") as f:
    newdict = {"Subject":None,"Experience_Sampling_Questions_Response_Time":None,
        "GoNoGo_Task_Response_Time":None, "Go_Task_Accuracy":None,"NoGo_Task_Accuracy":None,
        "Finger_Tapping_Task_Response_Time":None, "Finger_Tapping_Task_Accuracy":None,
        "Two-Back_Task-faces_Response_Time":None, "Two-Back_Task-faces_Accuracy":None,
        "Two-Back_Task-scenes_Response_Time":None, "Two-Back_Task-scenes_Accuracy":None,
        "One-Back_Task_Response_Time":None, "One-Back_Task_Accuracy":None,
        "Zero-Back_Task_Response_Time":None, "Zero-Back_Task_Accuracy":None,
        "Hard_Math_Task_Response_Time":None, "Hard_Math_Task_Accuracy":None,
        "Easy_Math_Task_Response_Time":None, "Easy_Math_Task_Accuracy":None,
        "Friend_Task_Response_Time":None, "Friend_Task_Sentiment":None,
        "You_Task_Response_Time":None, "You_Task_Sentiment":None
        }
    writer = csv.writer(f)
    writer.writerow(newdict)


with open("Tasks/taskScripts/resources/Self_Task/Self_Stimuli.csv",'r') as f:
    reader = csv.reader(f)
    for e,row in enumerate(reader):
        if e == 0:
            continue
        sentimentdict.update({row[6]:row[8]})
        #print(row)

with open("Tasks/taskScripts/resources/Other_Task/Other_Stimuli.csv",'r') as f:
    reader = csv.reader(f)
    for e,row in enumerate(reader):
        if e == 0:
            continue
        sentimentdict.update({row[6]:row[8]})
        #print(row)

with open('Analysis/coords.csv','r') as ft:
    rd = csv.reader(ft)
    for e,row in enumerate(rd):
        if e == 0:
            continue
        graddict.update({row[0]:[float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])]})
        #print(row)


line_dict= {"Task_name":None,
        "Id_number":None,
        "Runtime_mod":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Gradient_1":None,
        "Gradient_2":None,
        "Gradient_3":None,
        "Gradient_4":None,
        "Gradient_5":None
        }

if os.path.exists(os.path.join(os.getcwd(),"Analysis/output.csv")):
        os.remove(os.path.join(os.getcwd(),"Analysis/output.csv"))


with open(os.path.join(os.getcwd(),"Analysis/output.csv"), 'a', newline="") as outf:
    wr = csv.writer(outf)
    wr.writerow(list(line_dict.keys()))



def sortingfunction(exp,row,resps):
    global prevtime
    global en
    if exp == "Reading_Task":
        # Collect no data
        pass
    if exp == "Experience_Sampling_Questions":
        # Collect response time
        
        #print(row)
        if row[3].split("_")[1] == "start":
            prevtime = float(row[1])
        elif row[3].split("_")[1] == "response":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        pass
    if exp == "Memory_Task":
        # Collect no data
        pass
    if exp == "GoNoGo_Task":
        # Collect response time, % correct
        try:
            # Resp time
            if row[0].split(" ")[1] == "start":
                prevtime = float(row[1])
            elif row[0].split(" ")[1] == "end":
                resptime = float(row[1]) - prevtime  
                resps[exp]["Response_Time"].append(resptime)
            # Accuracy
            if row[2] != '':
                if row[2] == 'noResponse':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy_Go"].append(False)
                        resps[exp]["Accuracy_All"].append(False)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy_Go"].append(True)
                        resps[exp]["Accuracy_All"].append(True)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy_NoGo"].append(False)
                        resps[exp]["Accuracy_All"].append(False)
                if row[2].upper() == 'TRUE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy_NoGo"].append(True)
                        resps[exp]["Accuracy_All"].append(True)
        except Exception as e:
            #print(e)
            pass
        pass
    if exp == "Finger_Tapping_Task": #### NO RESPONSE TIME
        #print(row)
        if row[1] != "":    
            try:
                if row[0].split(" ",2)[2] == "Trial Start":
                    prevtime = float(row[1])
                elif row[0].split(" ",2)[2] == "Trial End":
                    resptime = float(row[1]) - prevtime  
                    resps[exp]["Response_Time"].append(resptime)
            except:
                pass
        if row[0] == 'Finger Tapping Trial End':
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        # Collect response time, % correct
        pass
    if exp == "Two-Back_Task-faces": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        #print(row)
        if row[0] == "Choice presented":
            prevtime = float(row[1])
        elif row[0] == "2-back Trial End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "2-back Trial End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "Two-Back_Task-scenes": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        #print(row)
        if row[0] == "Choice presented":
            prevtime = float(row[1])
        elif row[0] == "2-back Trial End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "2-back Trial End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "One-Back_Task": #DONT HAVE THE CORRECT TRUE/FALSE ON TRIALS
        #print(row)
        if row[0] == "OneBackStimulus Start":
            prevtime = float(row[1])
        elif row[0] == "OneBackStimulus End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "OneBackStimulus End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
    if exp == "Zero-Back_Task":
        if row[0] == "ZeroBackStimulus Start":
            prevtime = float(row[1])
        elif row[0] == "ZeroBackStimulus End":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == "ZeroBackStimulus End":
            if row[2].upper() == "TRUE":
                resps[exp]["Accuracy"].append(True)
            elif row[2].upper() == "FALSE":
                resps[exp]["Accuracy"].append(False)
            else:
                return 1/0
        pass
        # Collect response time, % correct
        pass
    if exp == "Hard_Math_Task":
        #print(row)
        if row[0] == 'Choice presented':
            prevtime = float(row[1])
        elif row[0] == 'Choice made':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == 'Math Trial End':
            if not "en" in globals():
                
                en = 0
            if en == 0:
                en = 1
                if row[2].upper() == "TRUE":
                    resps[exp]["Accuracy"].append(True)
                elif row[2].upper() == "FALSE":
                    resps[exp]["Accuracy"].append(False)
                else:
                    return 1/0
            elif en == 1:
                en = 0
            
        pass
    if exp == "Easy_Math_Task":
        if row[0] == 'Choice presented':
            prevtime = float(row[1])
        elif row[0] == 'Choice made':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == 'Math Trial End':
            if not "en" in globals():
                # global en
                en = 0
            if en == 0:
                en = 1
                if row[2].upper() == "TRUE":
                    resps[exp]["Accuracy"].append(True)
                elif row[2].upper() == "FALSE":
                    resps[exp]["Accuracy"].append(False)
                else:
                    return 1/0
            elif en == 1:
                en = 0
        # Collect response time, % correct
        pass
    if exp == "Friend_Task": #NO RESPONSE TIMES
        #print(row)
        if row[0].split('_')[0] == 'Start':
            prevtime = float(row[1])
        elif row[0].split('_')[0] == 'End':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, sentiment
        if row[0].split('_')[0] == 'End':
            sentdirection = sentimentdict[row[0].split('_')[2]]
            
            if row[8] == 'right':
                applies = True
            if row[8] == 'left':
                applies = False
            if row[8] == "None":
                #resps[exp]["Sentiment"].append("noresponse")
                return  
            if sentdirection == 'Negative':
                if applies == True:
                    resps[exp]["Sentiment"].append(False)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(True)  
                
            if sentdirection == 'Positive':
                if applies == True:
                    resps[exp]["Sentiment"].append(True)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(False)  
                        
            
            
        pass
    if exp == "You_Task":
        if row[0].split('_')[0] == 'Start':
            prevtime = float(row[1])
        elif row[0].split('_')[0] == 'End':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, sentiment
        if row[0].split('_')[0] == 'End':
            sentdirection = sentimentdict[row[0].split('_')[2]]
            
            if row[8] == 'right':
                applies = True
            if row[8] == 'left':
                applies = False
            if row[8] == "None":
                #resps[exp]["Sentiment"].append("noresponse")
                return  
            if sentdirection == 'Negative':
                if applies == True:
                    resps[exp]["Sentiment"].append(False)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(True)  
                
            if sentdirection == 'Positive':
                if applies == True:
                    resps[exp]["Sentiment"].append(True)      
                elif applies == False:
                    resps[exp]["Sentiment"].append(False)  
        # Collect response time, sentiment
        pass
    
        ##print("e")    
    pass


from tqdm import tqdm
import re
for file in tqdm(os.listdir("Tasks/log_file")):
    
    ftemp = file.split('.')[0]
    resps = {"Experience_Sampling_Questions":{"Response_Time":[]},
             "GoNoGo_Task":{"Response_Time":[], "Accuracy_Go":[],"Accuracy_NoGo":[],"Accuracy_All":[]},
             "Finger_Tapping_Task":{"Response_Time":[], "Accuracy":[]},
             "Two-Back_Task-faces":{"Response_Time":[], "Accuracy":[]},
             "Two-Back_Task-scenes":{"Response_Time":[], "Accuracy":[]},
             "One-Back_Task":{"Response_Time":[], "Accuracy":[]},
             "Zero-Back_Task":{"Response_Time":[], "Accuracy":[]},
             "Hard_Math_Task":{"Response_Time":[], "Accuracy":[]},
             "Easy_Math_Task":{"Response_Time":[], "Accuracy":[]},
             "Friend_Task":{"Response_Time":[], "Sentiment":[]},
             "You_Task":{"Response_Time":[], "Sentiment":[]}
             }

    if not 'full' in ftemp.split('_'):
        line_dict= {"Task_name":None,
        "Id_number":None,
        "Runtime_mod":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Gradient 1":None,
        "Gradient 2":None,
        "Gradient 3":None,
        "Gradient 4":None,
        "Gradient 5":None
        }

        _,_,subject,seed = ftemp.split("_")
        subject = "subject_"+str(int(re.findall(r'\d+', subject)[0]))
        line_dict["Id_number"] = subject
        
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            for row in reader:
                
                if row[0] == 'Runtime Mod':
                    line_dict["Runtime_mod"] = row[1]
                if row[0] == 'ESQ':
                    enum +=1
                    if ect == 0:
                        task_name = row[10]
                        
                        line_dict["Task_name"] = task_name.replace(" ","_")
                        ect = 1
                    if task_name == row[10]:
                        line_dict[row[3]]=row[4]
                    if enum == 16:
                        if task_name == "Movie Task-Movie Task-bridge":
                            task_name = "Movie Task-bridge"
                            line_dict["Task_name"] = task_name.replace(" ","_")
                        if task_name == "Movie Task-Movie Task-incept":
                            task_name = "Movie Task-incept"
                            line_dict["Task_name"] = task_name.replace(" ","_")
                        grads = graddict[line_dict["Task_name"]]
                        line_dict["Gradient 1"],line_dict["Gradient 2"],line_dict["Gradient 3"],line_dict["Gradient 4"],line_dict["Gradient 5"] = grads
                        with open("Analysis/output.csv", 'a', newline="") as outf:
                            wr = csv.writer(outf)
                            #wr.writerow(list(line_dict.keys()))
                            wr.writerow(list(line_dict.values()))
                        task_name = row[10]
                        for _ in ["Absorption_response",
                                    "Other_response",
                                    "Problem_response",
                                    "Words_response",
                                    "Sounds_response",
                                    "Images_response",
                                    "Past_response",
                                    "Distracting_response",
                                    "Focus_response",
                                    "Intrusive_response",
                                    "Deliberate_response",
                                    "Detailed_response",
                                    "Future_response",
                                    "Emotion_response",
                                    "Self_response",
                                    "Knowledge_response"]:
                            line_dict[_] = None
                        
                        line_dict[row[3]]=row[4]
                        line_dict["Task_name"] = task_name.replace(" ","_")
                    ##print(row)
                else:
                    ect = 0
                    enum =0
                
        #print(file)
    else:
        stats = {}
        expdict = {}
        captsubj = False
        ready = False
        resps.update({"Subject":subject})
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            for row in reader:
                
                # Subject name
                if captsubj == True:
                    stats.update({"Subject":row[2]})
                    captsubj = False
                if row[0] == "Block Runtime":
                    if row[2] == "Subject":
                        captsubj = True
                        
                # Experiment name
                elif row[0] == "EXPERIMENT DATA:":
                    expdict = {}
                    expdict.update({"Experiment":row[1].replace(" ","_")})
                    ready = False
                
                # Trigger start on next line
                elif row[0] == "Start Time":
                    ready = True
                elif ready == True:
                    if expdict["Experiment"] == 'Two-Back_Task':
                        sortingfunction(expdict["Experiment"] + "-" + row[9],row,resps)  
                    else:
                        sortingfunction(expdict["Experiment"],row,resps)  
                    
                #print(row)
        newresps = copy.copy(resps)
        for rsp in ["GoNoGo_Task","Finger_Tapping_Task","Two-Back_Task-faces",
                    "Two-Back_Task-scenes","One-Back_Task","Zero-Back_Task",
                    "Hard_Math_Task","Easy_Math_Task"]:
            o = newresps[rsp]
            if rsp == "GoNoGo_Task":
                
                realtrials = [o["Response_Time"][e] for e,x in enumerate(o["Accuracy_All"]) if x ]
                #o["Response_Time"][o["Accuracy_All"]]
            else:
                realtrials = [o["Response_Time"][e] for e,x in enumerate(o["Accuracy"]) if x ]
            newresps[rsp] = np.mean(realtrials)
            print('')
        with open("Analysis/accuracy.csv","a",newline="") as f:
            newdict = {"Subject":resps['Subject'],
             "Experience_Sampling_Questions_Response_Time":np.mean(resps['Experience_Sampling_Questions']['Response_Time']),
             "GoNoGo_Task_Response_Time":newresps['GoNoGo_Task'], "NoGo_Task_Accuracy":(resps['GoNoGo_Task']['Accuracy_NoGo'].count(True)/len(resps['GoNoGo_Task']['Accuracy_NoGo'])), "Go_Task_Accuracy":(resps['GoNoGo_Task']['Accuracy_Go'].count(True)/len(resps['GoNoGo_Task']['Accuracy_Go'])),
             "Finger_Tapping_Task_Response_Time":newresps['Finger_Tapping_Task'], "Finger_Tapping_Task_Accuracy":(resps['Finger_Tapping_Task']['Accuracy'].count(True)/len(resps['Finger_Tapping_Task']['Accuracy'])),
             "Two-Back_Task-faces_Response_Time":newresps['Two-Back_Task-faces'], "Two-Back_Task-faces_Accuracy":(resps['Two-Back_Task-faces']['Accuracy'].count(True)/len(resps['Two-Back_Task-faces']['Accuracy'])),
             "Two-Back_Task-scenes_Response_Time":newresps['Two-Back_Task-scenes'], "Two-Back_Task-scenes_Accuracy":(resps['Two-Back_Task-scenes']['Accuracy'].count(True)/len(resps['Two-Back_Task-scenes']['Accuracy'])),
             "One-Back_Task_Response_Time":newresps['One-Back_Task'], "One-Back_Task_Accuracy":(resps['One-Back_Task']['Accuracy'].count(True)/len(resps['One-Back_Task']['Accuracy'])),
             "Zero-Back_Task_Response_Time":newresps['Zero-Back_Task'], "Zero-Back_Task_Accuracy":(resps['Zero-Back_Task']['Accuracy'].count(True)/len(resps['Zero-Back_Task']['Accuracy'])),
             "Hard_Math_Task_Response_Time":newresps['Hard_Math_Task'], "Hard_Math_Task_Accuracy":(resps['Hard_Math_Task']['Accuracy'].count(True)/len(resps['Hard_Math_Task']['Accuracy'])),
             "Easy_Math_Task_Response_Time":newresps['Easy_Math_Task'], "Easy_Math_Task_Accuracy":(resps['Easy_Math_Task']['Accuracy'].count(True)/len(resps['Easy_Math_Task']['Accuracy'])),
             "Friend_Task_Response_Time":np.mean(resps['Friend_Task']['Response_Time']), "Friend_Task_Sentiment":(resps['Friend_Task']['Sentiment'].count(True)/(len(resps['Friend_Task']['Sentiment']) + 1e-6)),
             "You_Task_Response_Time":np.mean(resps['You_Task']['Response_Time']), "You_Task_Sentiment":(resps['You_Task']['Sentiment'].count(True)/(len(resps['You_Task']['Sentiment']) + 1e-6))
             }
            writer = csv.writer(f)
            writer.writerow(newdict.values())
