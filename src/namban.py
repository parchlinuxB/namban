import application
import os
import sys
import checks
if __name__ == "__main__":
    if os.getgid() != 0:
        print('Run it as root!')
        sys.exit(1)
    checks.checkStartupService()
    sys.exit(
        application.main()
    )
