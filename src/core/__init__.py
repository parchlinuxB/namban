import domain
class core:
    def systemDnsSet(self,profile:domain.profile):
        if profile == None:
            self.turnOffDns()
            return
        
    def turnOffDns(self): ...