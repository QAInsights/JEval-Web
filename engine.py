import xml.etree.ElementTree as ET
import xml.dom.minidom as XD
import pdb
import yaml
import logging
import json
import os

def createJSON():
    try:
        with open("./output/output.json","w") as f:
            data={"details": [
                {
                    "result": "Check",
                    "result_message": "Result",
                    "result_recommendation": "Recommendation"
                }
            ]}
            json.dump(data,f,ensure_ascii=False, indent=4)
        f.close()

    except FileNotFoundError:
        print("Err")
    return
def parseJMX(jmxFile):
    cleanup()
    createJSON()
    validateJMX(jmxFile)
    findJMeterVersion(jmxFile)
    findThreadGroups(jmxFile)
    return

def cleanup():
    if os.path.exists("./output/output.json"):
        os.remove("./output/output.json")
    else:
        pass
    return
def findJMeterVersion(jmxFile):
    tree = ET.parse(jmxFile)
    # Get JMeter version
    root = tree.getroot()    
    jmeterversion = root.items()
    #Call JMeter Version
    #expectedJMeterVersion = getJMeterVersion()
    expectedJMeterVersion = "5.3"
    #Check JMeter Version
    if expectedJMeterVersion == jmeterversion[2][1]:
        outcome_message=f"JMeter version is {jmeterversion[2][1]}."
        outcome = "Pass"
        outcome_recommedation="None"
        writeJSON(outcome,outcome_message,outcome_recommedation)
    else:
        outcome_message=f"Found outdated JMeter version: {jmeterversion[2][1]}."
        outcome="Fail"
        outcome_recommedation = "Consider updating to the latest version of JMeter."       
        writeJSON(outcome,outcome_message,outcome_recommedation)
    return

def findThreadGroups(jmxFile):
    '''
    This function find the number of thread groups.
    '''
    with open('./config.yaml','r') as file:
        try:
            #Reading Config file
            elements=yaml.safe_load(file)
            #Looping JMeter > Thread Group
            for element in elements['JMeter']['ThreadGroups']:
                #print((element))
                findThreadGroupStatus(jmxFile,element)                
        except yaml.YAMLError as e:
            print(e)    
    return

def findThreadGroupStatus(jmxFile,element):
    '''
    This function detects Thread Group and types. It will read from the config.yaml for the
    list of Thread Groups.
    writeJSON(outcome,outcome_message,outcome_recommedation="None")
    '''
    tree = ET.parse(jmxFile)
    root = tree.getroot()
    enabledCount = 0
    flag = 0
    outcome_message=f"No element found for {element}."
    for node in root.iter(element):                    
        if node.attrib:
            #Find Enabled Thread Groups
            if str.__contains__(str(node.attrib),'\'enabled\': \'true\''):            
                #Find enabled count
                enabledCount += 1
                #Set flag for success
                flag=1
                outcome_message=f"{enabledCount} {element} enabled "
            elif str.__contains__(str(node.attrib),'\'enabled\': \'false\''):
                outcome_message=f"No {element} enabled."
                #Set flag for fail
                flag=0
        else:
            outcome_message=f"No {element} found."
    if flag == 1:
        outcome = "Pass"
        writeJSON(outcome,outcome_message,outcome_recommedation="None")
        enabledCount = 0                
    if flag == 0:
        #printRed(message)
        outcome_recommedation = f"Consider enabling one or more {element}."
        outcome = "Fail"
        writeJSON(outcome,outcome_message,outcome_recommedation)
        #addRecommendation(recommendation)   
        enabledCount = 0     

    return
def validateJMX(jmxFile):
    #with open(jmxFile,'r') as f:
    #    print(f.read())
    #f.close()
    '''
    This function validates the JMeter test plan.
    '''
    try:
        element=XD.parse(jmxFile)
        outcome_message = "Valid JMeter Test Plan."
        outcome = "Pass"
        writeJSON(outcome,outcome_message,outcome_recommedation="None")
        return 
    except:
        exit(1)    
    return

def writeJSON(outcome,outcome_message,outcome_recommedation):
    with open("./output/output.json", "r") as f:
        data = json.load(f)
    f.close()
    tmp=data['details']
    y={"result" : outcome,"result_message" : outcome_message,"result_recommendation" : outcome_recommedation}
    tmp.append(y)
    with open("./output/output.json", "w+") as f:
        f.write(json.dumps(data))
    f.close()
    tmp=""
    return