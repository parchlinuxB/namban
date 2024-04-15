import domain as domain
import storage

class control:
    def addProfile(self, p:domain.profile):
        data = self.read()
        data.profiles.append(p)
        self.write(data)
        self.window.update()
    def deleteProfile(self, p:domain.profile):
        data = self.read()
        data.profiles.remove(p)
        self.write(data)
        self.window.update()
    def editProfile(self, p:domain.profile, newp:domain.profile):
        def indexOfProf(all,p):
            i = 0
            for c in all:
                if c==p:
                    return i
                i += 1
        data = self.read()
        data.profiles[indexOfProf(data.profiles,p)] = newp
        self.write(data)
    def connectProfile(self, profile:domain.profile):
        self.connectedProfile = profile
        self.systemDnsSet(profile)
        self.window.update()
    def disconnectProfiles(self):
        self.connectedProfile = None
        self.systemDnsSet(None)