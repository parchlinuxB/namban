import domain
import settings
import report
import os
import json

def read():
    def loadServer(rawServ)->domain.server:
        return domain.server(
            **rawServ
        )
    emptyConf = domain.appData([])
    if not os.path.exists(settings.APP_DATA_FILE):
        report.DataFile.InvalidFile()
        return emptyConf
    with open(settings.APP_DATA_FILE,"r") as f:
        try:
            rawData = json.loads(
                f.read()
            )
        except:
            report.DataFile.InvalidFile()
            return emptyConf
        profiles = []
        for rawProf in  rawData.get('profiles',[]):
            try:
                profWargs = {
                    "server1" : loadServer(rawProf['server1']),
                    "name": rawProf['name']
                }
                if "server2" in rawProf:
                    profWargs['server2'] = loadServer(rawProf['server2'])
                profiles.append(
                    domain.profile(**profWargs)
                )
            except:
                report.DataFile.InvalidProfile()
        return domain.appData(
            profiles
        )

def write(appData:domain.appData):
    def dumpServ(serv:domain.server) -> dict:
        return {
            'type' : serv.type,
            'url' : serv.url
        }
    def dumpProf(prof:domain.profile) -> dict:
        rawProf = {
            "server1":dumpServ(prof.server1),
            "name":prof.name
        }
        if prof.server2:
            rawProf['server2'] = dumpServ(prof.server2)
        return rawProf
    rawData = {
        "profiles":[
            dumpProf(p) for p in appData.profiles
        ]
    }
    try:
        with open(settings.APP_DATA_FILE,"w+") as f:
            f.write(
                json.dumps(rawData)
            )
    except:
        report.DataFile.InvalidFile()
    
