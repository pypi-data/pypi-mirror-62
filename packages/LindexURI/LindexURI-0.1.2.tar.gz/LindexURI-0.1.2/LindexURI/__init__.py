from urlparse import urlparse, parse_qs, parse_qsl
from collections import OrderedDict

__version__ = "0.1.2"
__author__ = 'Alessio Palma'


def supposedToBeUsed(**kwargs):
    def decorator(function):
        schema = kwargs['With']

        def wrapper(*args, **kwargs):
            if schema != args[0].schema:
                raise RuntimeError(
                    "Warning the schema of the URI [{}] does not match the requested one [{}]".format(args[0].schema,
                                                                                                      schema))
            return function(*args, **kwargs)

        return wrapper

    return decorator


class LindexURI(object):
    HIVE = "hive"
    HDFS = "hdfs"
    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"
    SFTP = "sftp"
    URI = ""
    # this class accept only URI which start with
    ALLOWED_SCHEMAS = [HTTP, HTTPS, FTP, SFTP, HIVE, HDFS]
    scheme = database = table = partitions = None

    def __init__(self, sURI):
        schema, database, hdfs_path, partitions = LindexURI._parseURI(sURI)
        self.schema = schema
        self.hostname = self.database = database
        self.hdfs_path = hdfs_path
        self.table = hdfs_path.replace("/", "")
        self.partitions = partitions

    @staticmethod
    def _parseURI(sURI):
        parts = urlparse(sURI)
        if parts.scheme.lower() not in LindexURI.ALLOWED_SCHEMAS:
            raise RuntimeError("This schema:[{}] is not supported by this class".format(parts.scheme))
        database = parts.netloc
        if len(database) == 0:
            raise RuntimeError("No database defined into the URI: [{}]!".format(sURI))
        hdfs_path = parts.path  # works also for table after "/" filtering
        if len(hdfs_path) == 0:
            raise RuntimeError("No table defined into the URI: [{}]!".format(sURI))
        partitions = None
        if len(parts.query):
            partitions = OrderedDict(parse_qsl(parts.query))
        return (parts.scheme, database, hdfs_path, partitions)

    @staticmethod
    def isValid(sURI):
        try:
            LindexURI._parseURI(sURI)
        except Exception as e:
            return False
        return True

    @supposedToBeUsed(With=HIVE)
    def isPartitioned(self, ):
        return self.partitions is not None

    @supposedToBeUsed(With=HIVE)
    def getPartitions(self, ):
        """this will return a dictionary which holds the data about the partitions"""
        return self.partitions

    @supposedToBeUsed(With=HIVE)
    def getDatabase(self, ):
        return self.database

    @supposedToBeUsed(With=HDFS)
    def getHDFSHostname(self, ):
        return self.hostname

    @supposedToBeUsed(With=HDFS)
    def getHDFSPath(self, ):
        return self.hdfs_path

    @supposedToBeUsed(With=HIVE)
    def getTable(self, ):
        return self.table

    def getSchema(self, ):
        return self.schema

    #
    # Conversion functions
    #

    @supposedToBeUsed(With=HIVE)
    def getPartitionsAsHDFSPath(self):
        """This function gets the partitions defined into the hive schema and coverts them into a path
         { "country" : "au", "op" : "Tim" } is converted in country=au/op=Tim """
        return "/".join(["{}={}".format(k, v) for k, v in self.getPartitions().items()])

    @supposedToBeUsed(With=HDFS)
    def getHDFSPathAsPartition(self):
        """Hive partitioned tables have a special HDFS path, this function tries to return the root path and the 
        partitions coordinates as dictionary:

        'hdfs://hdfs-production/Vault/Docomodigital/Production/Newton/events/prod/year=2018/month=08/day=07/hour=09'

        root path : "/Vault/Docomodigital/Production/Newton/events/prod/"

        partitions : {
            "year" : "2018",
            "month" : "08",
            "day" : "07",
            "hour" : "09"
        }

        """
        hdfs_path_parts = self.getHDFSPath().split("/")
        p = OrderedDict([x.split("=") for x in hdfs_path_parts if "=" in x])
        root_path = "/".join([x for x in hdfs_path_parts if "=" not in x])
        return p, root_path

    @supposedToBeUsed(With=HDFS)
    def looksPartitioned(self, ):
        """Return true if the current HDFS path contains parts that are suitable to define a partiioned table, for
        example:

            'hdfs://hdfs-production/Vault/Docomodigital/Production/DBA/warehouse/repl_jmailer_au.db/mo20160217'
            DOES NOT LOOK LIKE PARTITIONED

            'hdfs://hdfs-production/Vault/Docomodigital/Production/UnifiedData/warehouse/unifieddata_cashlog.db/raw_au_enabler_vodafone_pe_tracking/dt=20190513'
            THIS DOES LOOK LIKE PARTITIONED ( dt=xxxxx )
        """
        partitions, root_path = self.getHDFSPathAsPartition()
        return True if partitions else False
