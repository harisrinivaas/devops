import sys

from ConfigrationReader import ConfigrationReader

class ChangedResources(object):
    def __init__(self, gitChangesFile, config, couldfomrationOutputs):
        self.configReaderObj = ConfigrationReader(gitChangesFile, config, couldfomrationOutputs)
        self.changedResources = self.identifyChangedResources()

    def identifyChangedResources(self):
        with open(self.configReaderObj.gitFile, "r") as ins:
            service_list = []
            for line in ins:
                for each in self.configReaderObj.configuration['lambda']:
                    if each['folder'] in line:
                        array = {}
                        array['serviceName'] = each['serviceName']
                        array['serviceType'] = 'lambda'
                        service_list.append(array)
                for each in self.configReaderObj.configuration['emr']:
                    if each['folder'] in line:
                        array = {}
                        array['serviceName'] = each['serviceName']
                        array['serviceType'] = 'emr'
                        service_list.append(array)
        return service_list

    def getChangedLambdas(self):
        changedLambdas = []
        for each in self.changedResources:
            if each['serviceType'] == 'lambda':
                changedLambdas.append(each['serviceName'])
        return list(set(changedLambdas))

    def getChangedEMRs(self):
        changedEMRS= []
        for each in self.changedResources:
            if each['serviceType'] == 'emr':
                changedEMRS.append(each['serviceName'])
        return list(set(changedEMRS))

    def getARN(self, resourceName):
        for each in self.configReaderObj.output:
            if each['OutputKey'] == resourceName:
                return each['OutputValue']
        return None

    def identifyEMRjobs(self, emrServiceName):
        emrConfiguration = self.configReaderObj.getConfiguration(emrServiceName)
        with open(self.configReaderObj.gitFile, "r") as ins:
            array = []
            for line in ins:
                for eachOozieJob in emrConfiguration['oozieJobs']:
                    if eachOozieJob['folder'] in line:
                        arr = {}
                        arr['jobName'] = eachOozieJob['jobName']
                        arr['jobType'] = 'oozie'
                        array.append(arr)
                for eachDatapipelineJob in emrConfiguration['dataPipelineJobs']:
                    if eachDatapipelineJob['folder'] in line:
                        arr = {}
                        arr['jobName'] = eachDatapipelineJob['jobName']
                        arr['jobType'] = 'datapipeline'
                        array.append(arr)
        return array

# Unit Test Purpose
if __name__ == '__main__':
    if len(sys.argv) < 2: raise Exception(
        "ERROR: Insufficient number of arguments, changes.txt, config.json and output.json file paths must be given")
    crobj = ChangedResources(sys.argv[1], sys.argv[2], sys.argv[3])

    # print "Lambdas: " , crobj.getChangedLambdas()
    # print "EMRs: " , crobj.getChangedEMRs()
    print "EMR Jobs: ", crobj.identifyEMRjobs('SimpleEMR')
    # for eachJobChanged in crobj.identifyEMRjobs('SimpleEMR'):
    #     print "Config for %s : %s " %(eachJobChanged, crobj.configReaderObj.getEMRJobConfiguration(eachJobChanged))