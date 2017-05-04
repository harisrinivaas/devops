import sys
import os
import json

class ConfigrationReader(object):
    def __init__(self, gitChangesFile, config, couldfomrationOutputs):
        try:
            self.configuration = json.loads(open(config, "r").read())
            self.__outputFile = json.loads(open(couldfomrationOutputs, "r").read())
            self.output = self.__outputFile['Stacks'][0]['Outputs']
            self.gitFile = gitChangesFile
        except Exception as error:
            print "FATAL ERROR: %s" % str(error)

    def getConfiguration(self, resourceName):
        for each in self.configuration['lambda']:
            if each['serviceName'] == resourceName:
                each['arn'] = self.getARN(each['serviceName'])
                return each
        for each in self.configuration['emr']:
            if each['serviceName'] == resourceName:
                each['arn'] = self.getARN(each['serviceName'])
                return each
        return None

    def getARN(self, resourceName):
        for each in self.output:
            if each['OutputKey'] == resourceName:
                return each['OutputValue']
        return None

    def getEMRJobConfiguration(self, emrJobName):
        for eachEMR in self.configuration['emr']:
            for eachOozieJob in eachEMR['oozieJobs']:
                if eachOozieJob['jobName'] == emrJobName:
                    return eachOozieJob
            for eachDatapipelineJob in eachEMR['oozieJobs']:
                if eachDatapipelineJob['jobName'] == emrJobName:
                    return eachDatapipelineJob
        return None