import domain
from .strategy import resolvd
class core:
    def systemDnsSet(self,profile:domain.profile):
        if profile == None:
            self.turnOffDns()
            return
        self.currentStrategy = resolvd(profile)
        self.currentStrategy.connect()
        
        
    def turnOffDns(self):
        if self.currentStrategy:
            self.currentStrategy.disconnect()
            self.currentStrategy = None