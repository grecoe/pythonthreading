import json
import os
from pageparser.persist import createPath, writeContent, loadContent, normalizeBase

class SiteDataPath:
    def __init__(self, path):
        self.full_path = path

        res = os.path.split(path)
        self.day = res[1]
        res = os.path.split(res[0])
        self.month = res[1]
        res = os.path.split(res[0])
        self.year = res[1]
        res = os.path.split(res[0])
        self.name = res[1]
        self.base = res[0]

class WebSiteDataPersist:
    _SitRunHistoryFile = 'run_history'
    _SiteDataFile = 'data'
    _SiteImageFile = 'images'
    _SiteLinkFile = 'links'

    @staticmethod
    def updateSiteRunHistory(path, job_time):
        '''
            Update runs for the day, format is a simple JSON list with 
            string date times.
        '''
        history_file = WebSiteDataPersist._SitRunHistoryFile
        run_data = loadContent(path, history_file)
        if run_data:
            run_data = json.loads(run_data)
            run_data.append(str(job_time))
        else:
            run_data = [str(job_time)]
        writeContent(path,history_file, run_data)

    @staticmethod
    def updateSiteData(path, job_time, new_data):
        '''
            Update data for the day. 

            Format is JSON dictionary:

            "content: [string list of times seem]
        '''
        data_file = WebSiteDataPersist._SiteDataFile
        existing_data = WebSiteDataPersist._loadFileDataAsJson( os.path.join(path, data_file))
        if existing_data:
            for data in new_data:
                if data in existing_data.keys():
                    existing_data[data].append(str(job_time))
                else:
                    existing_data[data] = [str(job_time)]
        else:
            existing_data = {}
            for data in new_data:
                existing_data[data] = [str(job_time)]
        writeContent(path, data_file, existing_data)

    @staticmethod
    def updateSiteImages(path, job_time, image_list):
        WebSiteDataPersist._updateSiteTrackedData(path,WebSiteDataPersist._SiteImageFile, job_time, image_list)

    @staticmethod
    def updateSiteLinks(path, job_time, link_list):
        WebSiteDataPersist._updateSiteTrackedData(path,WebSiteDataPersist._SiteLinkFile, job_time, link_list)

    @staticmethod 
    def loadSiteData(base, name, year, month, day):
        data_path = WebSiteDataPersist._createPath(base,name,year,month,day,WebSiteDataPersist._SiteDataFile)
        return WebSiteDataPersist._loadFileDataAsJson(data_path)

    @staticmethod
    def getAllDataPaths(base, name):
        return_paths = []

        base = normalizeBase(base)
        directory = os.path.join(base,name)

        additional_parts = len(directory.split('\\'))
        total_parts = additional_parts + 3

        paths = [x[0] for x in os.walk(directory) if len(x[0].split('\\')) == total_parts]
        for path in paths:
            return_paths.append(SiteDataPath(path))
        return return_paths

    @staticmethod 
    def _createPath(base, name, year, month, day, file_name):
        if not base:
            base = '.\\'

        parts = [name,year,month,day, file_name]

        return  os.path.join(base, *parts)

    @staticmethod
    def _loadFileDataAsJson(file_path):
        return_data = None
        if os.path.isfile(file_path):
            file_content = loadContent(file_path)
            if file_content:
                return_data = json.loads(file_content)
        return return_data


    @staticmethod
    def _updateSiteTrackedData(path, data_type, job_time, new_data):
        '''
            path: disk path of directory
            data_type : File name
            job_time : Time to stamp
            new_data : Dictionary in "uuid" : "content"
            Update data in the form of a dictionary:

            {
                "content" :
                {
                    "id" : "uuid",
                    "occurance" :[string list of times]
                }
            }
        ''' 
        existing_data = WebSiteDataPersist._loadFileDataAsJson( os.path.join(path, data_type))
        if existing_data:
            # Format above
            for data in new_data.keys():
                if new_data[data] in existing_data.keys():
                    existing_data[new_data[data]]['occurance'].append(str(job_time))
                else:
                    existing_data[new_data[data]] = {'id' : data, 'occurance' : [str(job_time)]}
        else:
            existing_data = {}
            for data in new_data.keys():
                existing_data[new_data[data]] = {'id' : data, 'occurance' : [str(job_time)]}

        writeContent(path, data_type, existing_data)
