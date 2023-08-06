""" Sample that demonstrates how to enable CSV logging for a view
and download the resulting CSV log file once it is disabled.

The sample operates under the following assumptions:
    - it is for an established IxNetwork GUI session
    - traffic is running
    - there is a Port Statistics view

"""
from ixnetwork_restpy.testplatform.testplatform import TestPlatform

# connect to a test tool platform
test_platform = TestPlatform('127.0.0.1')
test_platform.Authenticate('admin', 'admin')
sessions = test_platform.Sessions.add()
ixnetwork = sessions.Ixnetwork


# assumes that the view exists and it sets up csv logging for the view
view = ixnetwork.Statistics.View.find(Caption='Port Statistics')
view.update(EnableCsvLogging=True)

# this builds the full path of the csv file on the server
remote_csv_filename = '%s/%s' % (ixnetwork.Statistics.CsvFilePath, view.CsvFileName)

# setup a local path
local_csv_filename = 'c:/temp/%s' % view.CsvFileName

# in order to download the csv log file the csv logging must be disabled 
# otherwise a sharing violation from the server will be returned
ixnetwork.Statistics.EnableCsvLogging = False
sessions.DownloadFile(remote_csv_filename, local_csv_filename)
