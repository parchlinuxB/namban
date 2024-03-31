import domain
import settings
import report
import os
import json
class storage:

    def loadProf(self, rawProf):
        try:
            profWargs = {
                "server1" : self.loadServ(rawProf['server1']),
                "name": rawProf['name']
            }
            if "server2" in rawProf:
                profWargs['server2'] = self.loadServ(rawProf['server2'])
            return(
                domain.profile(**profWargs)
            )
        except:
            report.DataFile.InvalidProfile()
    def loadServ(self,rawServ)->domain.server:
        return domain.server(
            **rawServ
        )

    def read(self):
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
                r = self.loadProf(rawProf)
                if r:
                    profiles.append(r)
            return domain.appData(
                profiles
            )

    def write(self,appData:domain.appData):
        rawData = {
            "profiles":[
                self.dumpProf(p) for p in appData.profiles
            ]
        }
        try:
            with open(settings.APP_DATA_FILE,"w+") as f:
                f.write(
                    json.dumps(rawData)
                )
        except:
            report.DataFile.InvalidFile()

    def dumpServ(self, serv:domain.server) -> dict:
        return {
            'type' : serv.type,
            'url' : serv.url
        }
    def dumpProf(self, prof:domain.profile) -> dict:
        rawProf = {
            "server1":self.dumpServ(prof.server1),
            "name":prof.name
        }
        if prof.server2:
            rawProf['server2'] = self.dumpServ(prof.server2)
        return rawProf
