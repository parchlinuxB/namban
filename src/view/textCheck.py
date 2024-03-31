class baseCheck:
    def check(self,text):
        return False
    def __call__(self, text):
        return self.check(text)

class regexCheck(baseCheck):
    pattern = ""
    def check(self,check):
        import re
        if re.match(self.pattern, check):
            return True
        return False

class isIp(regexCheck):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
