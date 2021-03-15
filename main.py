import requests
import json

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config
from pprint import pprint

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def verify_intersight():
    url = f"{BASE_URL}/cond/Alarms"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        print("Intersight access verified")
    else:
        print(f"Intersight access denied. status code: {response.status_code}")

# Get the ntp policy 
def ntp_poliy():
    url = f"{BASE_URL}/ntp/Policies"

    response = requests.get(url, auth=auth)     

    pprint(response.json(), indent=4)

# Get alarms (description)
def alarms():
    url = f"{BASE_URL}/cond/Alarms"

    response = requests.get(url, auth=auth)     

    parsed = response.json()

    # write_json(parsed,"alarms")

    for entry in parsed["Results"]:
        pprint(entry["Description"], indent=4)  

# Get a summary of the physical infrastructure (Management Mode, Management IP, Name, CPUs, Cores, PowerState, Firmware, Model, Serial and License Tier)
def physical_infrastructure():
    url = f"{BASE_URL}/compute/PhysicalSummaries"

    response = requests.get(url, auth=auth)     

    parsed = response.json()

    #write_json(parsed,"physical_infrastructure")

    filteredInfrastructure = []

    for entry in parsed["Results"]:
        infraEntries = {
            "ManagementMode" : entry["ManagementMode"],
            "MgmtIpAddress" : entry["MgmtIpAddress"],
            "Name" : entry["Name"],
            "CPUs" : entry["NumCpus"],
            "Cores" : entry["NumCpuCores"],
            "PowerState" : entry["OperPowerState"],
            "Firmware" : entry["Firmware"],
            "Model" : entry["Model"],
            "Serial" : entry["Serial"],
            "License Tier" : licenseTier(entry["Tags"])
        }
        filteredInfrastructure += [infraEntries]
        
    print(json.dumps(filteredInfrastructure, indent=4))  

# Getting license tier from the Tags list
def licenseTier(tagsList):
    for entry in tagsList:
        if entry["Key"] == "Intersight.LicenseTier":
            return entry["Value"]

# Get the Compliance with Hardware Compatibility List (HCL). (OS Vendor and OS version)
def hardware_compatability_list():
    url = f"{BASE_URL}/cond/HclStatuses"

    response = requests.get(url, auth=auth)     

    parsed = response.json()

    #write_json(parsed,"HCL")

    HCL = []

    for entry in parsed["Results"]:
        hclEntries = {
            "OS Vendor" : entry["HclOsVendor"],
            "OS Version" : entry["HclOsVersion"]
        }
        HCL += [hclEntries]
        
    print(json.dumps(HCL, indent=4)) 

# Get the Kubernetes Cluster names
def kubernetes_clusters ():
    url = f"{BASE_URL}/kubernetes/Deployments"

    response = requests.get(url, auth=auth)     

    parsed = response.json()

    #write_json(parsed,"KubernetesDeployment")

    kubernetesDeployments = []

    for entry in parsed["Results"]:
        deploymentEntries = {
            "Name" : entry["Name"]
        }
        kubernetesDeployments += [deploymentEntries]
        
    print(json.dumps(kubernetesDeployments, indent=4)) 

# Write dictionary into CSV file
def write_json(data, filename):
    with open(filename + ".json", "w") as f:
        try:
            f.write(json.dumps(data, indent=4, sort_keys=True))
        except:
            print("Something went wrong")
    f.close()
    print("Result written to " + filename + ".json")


# Check for ACI simulator access
def verify_APIC():
    aci_session = get_authenticated_aci_session(config['ACI_USER'], config['ACI_PASSWORD'], config['ACI_BASE_URL'])

    if aci_session is not None:
        print("ACI access verified")
    else:
        print("Failed to verify access to ACI.")




verify_intersight()
ntp_poliy()
alarms()
physical_infrastructure()
hardware_compatability_list()
kubernetes_clusters()

