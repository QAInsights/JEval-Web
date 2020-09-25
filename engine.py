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