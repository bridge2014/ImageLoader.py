import hashlib
import time
import openslide

class MetadataExtractor:
    PROPERTIES = [
        "objective-power",
        "mpp-x",
        "mpp-y",
        "vendor",
        "width",
        "height",
        "level_count",
        "timestamp",
        "md5sum",
        "file-location", #From CSV
        "Id"
    ]
    fileMetadata = {}
    def __init__(self, fileMetadata):
        self.fileMetadata = fileMetadata
        self.imageMetadata = self.extractImageMetadata()
        if(self.imageMetadata == []):
            print("Couldn't fetch image metadaa")
    def extractImageMetadata(self):
        fileMetadata = self.fileMetadata
        fileLocation = fileMetadata['file-location']
        try:
            openslideF = openslide.OpenSlide(fileLocation)
            payLoad = openslideF

            return payLoad
        except:
            print("Couldn't read "+fileLocation)

        return []

    def generateMD5Checksum(self,fileName):
        m = hashlib.md5()
        blocksize = 2**20
        with open(fileName, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()



    def createPayLoad(self):
        payLoad = {}
        fileMetadata = self.fileMetadata
        imageMetadata = self.imageMetadata
        #print(imageMetadata.properties)
        
        if(imageMetadata):
            for prop in self.PROPERTIES:
                #print(prop)
                if prop == "file-location":
                    payLoad['file-location'] = fileMetadata['file-location']
                elif prop == "Id":
                    payLoad['id'] = fileMetadata['id']
                elif prop in ["mpp-x", "mpp-y", "objective-power"]:
                    property_ = 'openslide.'+str(prop)
                    if(property_ in imageMetadata.properties):

                        payLoad[prop] = float(imageMetadata.properties['openslide.'+str(prop)])
                    else:

                        if(prop == "objective-power"):
                            if("aperio.AppMag" in imageMetadata.properties):
                                payLoad[prop] = float(imageMetadata.properties["aperio.AppMag"])
                            else:
                                print(imageMetadata.properties)

                elif prop in ["height", "width"]:
                    hw = "openslide.level["+str(imageMetadata.level_count - 1)+"]."+str(prop)
                    payLoad[prop] = int(imageMetadata.properties[hw])
                elif prop == "vendor":
                    payLoad[prop] = imageMetadata.properties['openslide.'+str(prop)]
                elif prop == "md5sum":
                    payLoad[prop] = self.generateMD5Checksum(fileMetadata['file-location'])
                elif prop == "level_count":
                    payLoad[prop] = int(imageMetadata.level_count)
                elif prop == "timestamp":
                    payLoad[prop] = time.time() 
                else:
                    print("Couldn't handle: "+ prop)

        return payLoad




