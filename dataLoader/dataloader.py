import sys, getopt
import csv
import os
import pprint
import requests
from metadataextractor import MetadataExtractor
import datetime
import logging



def postPayLoad(payLoad,url,apiKey):
    headers = {'api_key': apiKey}
    r = requests.post(url, json=payLoad, headers=headers)
    return r


""" Returns a dictionary with the key as the ID and value as the file locations """
def parseInputFile(inputfile):
    inputFileDict = {}
    if os.path.exists(inputfile):
        with open(inputfile, newline='') as f:
            try:
                #header = [h.strip() for h in f.next().split(',')]
                csv.register_dialect('MyDialect', quotechar='"', skipinitialspace=True, quoting=csv.QUOTE_NONE, lineterminator='\n', strict=True)

                #process
                inputReader = csv.DictReader(f, dialect='MyDialect')
                #print(inputReader[0])
                x = []
                for r in inputReader:
                  #print(r)
                  x.append(r)
                #for row in inputReader:
                inputFileDict = {rows for rows in inputReader}

                return x

            except IOError:
                print("troubles parsing inputfile:"+ inputfile)
                sys.exit(2)
    else:
        print("ERROR! Couldnt read: "+ inputfile)
        sys.exit(2)

def parseInputs(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:a:", ["ifile=", "ofile=", "apiKey="])
    except getopt.GetoptError:
        print("dataLoader -i <inputfile> -o <rest> -a <apiKey>")
        sys.exit(2)
    output = ""
    inputfile = ""
    apiKey = ""
    for opt, arg in opts:
        if opt == '-h':
            print("Usage: dataLoader -i <inputfile> -o <REST> -a <apiKey>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-a", "--apikey"):
            apiKey = arg
    if(inputfile == "" or output == "" or apiKey == ""):
        print("Usage: dataLoader -i <inputfile> -o <REST> -a <apiKey>")
        sys.exit()


    return {'inputfile': inputfile, 'output': output, 'apiKey': apiKey}


def main(argv):
    inputfile=""
    output=""
    inputs = parseInputs(argv)
    #print(inputs)
    inputfile = inputs['inputfile']
    outputfile = inputs['output']
    apiKey = inputs['apiKey']
    url = outputfile

  
    logging.basicConfig(filename='dataloader.log',  filemode='w', level=logging.DEBUG)

    logging.info("Log started on: "+str(datetime.datetime.now()))
    parsedInput = parseInputFile(inputfile)
    print(parsedInput)
    for inp in parsedInput:
      extractor = MetadataExtractor(inp)
      payLoad  = extractor.createPayLoad()
      if(payLoad == {}):
        logging.warning("Failed: Id: "/ " couldn't find file or failed to fetch metadata")

      print(inp)
      print(payLoad)
      print("---")
      payLoad.update(inp)
      response = postPayLoad(payLoad, url, apiKey)
      if(response.status_code != 200):
        print("Failed: "+ " with HTTP status code " + str(response.status_code))
        logging.warning("Failed: "+ " with HTTP status code " + str(response.status_code))
      else:
        logging.info("Success: ")    
      logging.info("Compeleted on: "+str(datetime.datetime.now()))
      print(payLoad)

    '''
    for uId in parsedInput:

        if not uId == "case_id":
            fileMetadata = {}
            fileMetadata['id']= uId
            fileMetadata['study_id'] = parsedInput[uId][0]
            fileMetadata['file-location'] = parsedInput[uId][1]
            print(fileMetadata)
            extractor = MetadataExtractor(fileMetadata)
        
            payLoad = extractor.createPayLoad()
            if(payLoad == {}):
                logging.warning("Failed: Id: "+str(uId)+" file-location: "+ parsedInput[uId][1] + " couldn't find file or failed to fetch metadata")
                continue

            vresponse = postPayLoad(payLoad, url, apiKey)
            print(response.status_code)
            if(response.status_code != 200):
                print("Failed: "+str(uId)+" file-location: "+ parsedInput[uId][1] + " with HTTP status code " + str(response.status_code))
                logging.warning("Failed: "+str(uId)+ " with HTTP status code " + str(response.status_code))
            else:
                logging.info("Success: "+str(uId))
      '''
    logging.info("Compeleted on: "+str(datetime.datetime.now()))
if __name__ == "__main__":
    main(sys.argv[1:])


