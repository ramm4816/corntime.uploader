import ffmpeg, json

class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MetaData:

    @staticmethod
    def get(filename):
        metadata = ffmpeg.probe(filename)["streams"]
        for _metadata in metadata:
            if _metadata['codec_type']=="video":
                return _metadata
            
