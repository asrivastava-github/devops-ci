#! /usr/bin/env python3

import os
import subprocess
import sys
import logging
from time import gmtime, strftime, sleep
from threading import Thread


class LAUNCHER:
    def __init__(self):
        self.logger, self.logfileName = self.getlogger()
        self.kubeappyml = os.path.join('deployment', 'blogapp.yml')

    def getlogger(self):
        logfile = "Logs%s.log" % (strftime("%Y-%m-%d%H%M%S", gmtime()))
        logger = logging.getLogger('%s' % logfile)
        logfile = logging.FileHandler('logs/%s' % logfile)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logfile.setFormatter(formatter)
        logger.addHandler(logfile)
        logger.setLevel(logging.INFO)
        return logger, logfile

    def changeflcon(self):
        if os.path.exists(self.kubeappyml):
            with open(self.kubeappyml, 'r') as readfl:
                with open(self.kubeappyml, 'w') as readfl:
                    for lines in readfl:
                        if 'image: blogapp' in lines:
                            lines = 'image: ' + sys.argv[1]

    def proccheck(self, procname, dockname):
        while procname.is_alive():
            self.logger.info('Building fresh image: ' + dockname)
            sleep(2)
        else:
            self.logger.info('Built image: ' + dockname)

    def dockerbuild(self, dockbuild, cmdarg):
        dockbuilder = Thread(target=self.runoscmd, args=[cmdarg])
        dockbuilder.start()
        self.proccheck(dockbuilder, dockbuild)

    def runoscmd(self, cmdarg):
        os.system(cmdarg)

    def runosreturn(self, cmdarg):
        out = subprocess.check_output(cmdarg, shell=True).strip()
        return out

    def rundocker(self, dockbuild=None, dockrun=None):
        if dockbuild:
            checkrepo, checktag, checkimageid = self.getimage(dockbuild)
            if checkrepo:
                self.logger.info('Already Exists image: ' + dockbuild)
                dockerrmimage = Thread(target=self.runoscmd, args=['docker image rm -f {0}:latest'.format(dockbuild)])
                dockerrmimage.start()
                self.proccheck(dockerrmimage, dockbuild)
                self.dockerbuild(dockbuild, 'docker build -t {0} .'.format(dockbuild))
            else:
                self.dockerbuild(dockbuild, 'docker build -t {0} .'.format(dockbuild))

        if dockrun:
            self.logger.info('Running docker image: ' + dockbuild)
            self.dockerbuild(dockbuild, 'docker run -it -p 8080:5000 {0} .'.format(dockrun))

    def getimage(self, reponame):
        repo = "'{print $1}'"
        tag = "'{print $2}'"
        image = "'{print $3}'"
        repository = self.runosreturn('docker images | grep {0} | awk {1}'.format(reponame, repo)).decode('utf-8')
        tagname = self.runosreturn('docker images | grep {0} | awk {1}'.format(reponame,  tag)).decode('utf-8')
        imageid = self.runosreturn('docker images | grep {0} | awk {1}'.format(reponame, image)).decode('utf-8')
        return repository, tagname, imageid


if __name__ == "__main__":
    launch = LAUNCHER()
    launch.rundocker(dockbuild=sys.argv[1], dockrun=sys.argv[1])
    REPO, TAG, IMAGEID = launch.getimage(sys.argv[1])
