#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from subprocess import *
import sys
import getopt
import os
import random
from pathlib import Path
import shutil
from glob import glob
import SceyeDb


#Creating a relative path to easily refer to files & folder
base_path = Path(__file__).parent

def main(argv):
    projectname = 'Sceye.py'
    scrapers = []
    scraperfolders = []
    spiders = []
    selectedscrapers = []
    scrapersToReset = []
    resetscrapers = False
    listscrapers = False
    storedata = False
    charchosen = False
    scrapechar = 'A';

    #Getting command line input
    try:
        (opts, args) = getopt.getopt(argv, 'hls:r:c:', ['list','storedata', 'select=','reset=','char='])
    except getopt.GetoptError:
        print ('Usage:', projectname, '[options]')
        print('\n(Use', projectname, '-h to view options)')
        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print ('Usage:', projectname, '[options]')
            print('\nAvailable options: \n')
            print ('-h \t\t Documentation')
            print ('-l, --list \t Show list of scraper(s)')
            print ('-s, --select \t Select scraper(s) (ID\'s seperated with commas)')
            print ('-c, --char \t Character or letter to start the scraping from. By default \n \t\t it scrapes on alphabetical order')
            print ('-r, --reset \t Reset state of scraper(s). By default a scraper resumes \n \t\t scraping where it stopped. (ID\'s seperated with commas)')
            print ('--storedata \t Store all scraped data inside the JSON folder into the Database')
            print ('\nCurrently only one scraper can be chosen at the same time')

            sys.exit()
        elif opt in ('-l', '--list'):
            listscrapers = True
        elif opt in ('-r', '--reset'):
            resetscrapers = True
            scrapersToReset = (arg.split(","))
            scrapersToReset = [int(i) for i in scrapersToReset]
        elif opt in ('-s', '--select'):
            selectedscrapers = (arg.split(","))
            selectedscrapers = [int(i) for i in selectedscrapers]
        elif opt in ('-c', '--char'):
            charchosen = True
            scrapechar = str(arg)
            print(scrapechar)
        elif opt in ('--storedata'):
            storedata = True

    #Finding all scrapers & spiders in the /scrapers folder and storing it in the array (alphabetical order)
    allfiles = []
    for file in os.listdir(base_path / 'Scraper'):
        allfiles.append(file)
    scrapers = sorted(allfiles, key=str.lower)
    scraperfolders = sorted(allfiles, key=str.lower)
    for x in scraperfolders:
        for file in os.listdir(base_path / 'Scraper' / x / x / 'spiders'):
            if file.endswith(".py") and not file.endswith("__.py"):
                spiders.append(file.replace('.py', ''))

    #When you run -l or --list
    if listscrapers == True:
        #Printing list of scrapers
        print("List of current scrapers:")
        print('ID','\t','Name','\t\t','Spider')
        i = -1
        for x in scrapers:
            i += 1
            print(i,':\t',x,'\t',spiders[i])
        print('\nUse -s or --select in order to use them')

    #When you run -r or --reset
    if resetscrapers == True:
        for x in scrapersToReset:
            print('Resetting scraper #'+ str(x))
            try:
                #Deleting the cache folder of the scraper
                folder ='Scraper/'+ scrapers[x] + '/crawls/' + spiders[x] + '-1'
                shutil.rmtree(folder)
                print('Done!')
            except:
                print('Error, this scraper has no data to reset!')

    #When you run --storedata
    if storedata == True:
        filesToStore = []
        filesToMove = []
        #Collecting all files in the JSON folder
        for file in os.listdir(base_path / 'JSON'):
            if file.endswith(".json"):
                filesToStore.append('JSON/'+ file)
                filesToMove.append(file)
        #Calling script to import files into the database
#        importdb = SceyeDb.main(filesToStore)
        os.chdir(base_path / 'JSON')
        for file in filesToMove:
            cmd = 'mv ' + file + ' stored'
            subprocess.call(cmd, shell=True)


    #The code when the program starts
    if selectedscrapers:
        #Printing project information
        print("---------------------")
        print("NHTCU project OSINT")
        print("Team 10")
        print("Framework v1.3")
        print("---------------------")

        #Printing list of chosen scrapers
        print("You've chosen the following scraper(s):")
        print('ID','\t','Name','\t\t','Spider')
        for x in selectedscrapers:
            try:
                print(x,':\t',scrapers[x],'\t',spiders[x])
            except:
                print('Could not choose scraper #',x,'because it doesn\'t exist. Please try again')
                exit()
        print('\nScraping will start from the following character: '+ scrapechar)
        print('Make sure to clear cache before scraping a new charactar (-r or --reset)')
        starting = input("\nPress Enter to start scraping (Pause with CTRL + C)")
        if starting == "":
            print("Scraping...")
        #Random file name
        randomfile = "scrape" + str(random.randint(0,99999)) + ".json"
        jsonFolder = '../../JSON/'+randomfile
        #The command that is ran to start the scraper
        cmd = 'scrapy crawl '+ spiders[selectedscrapers[0]] + ' -a ip='+ scrapechar + ' -o ' + jsonFolder + ' -s LOG_ENABLED=False -s JOBDIR=crawls/'+spiders[selectedscrapers[0]]+'-1'
        try:
            #Running the command in cmd inside the scraper folder
            os.chdir(base_path / 'Scraper' / scrapers[0])
            subprocess.call(cmd, shell=True)
        except KeyboardInterrupt:
            print("\n\nScraped data saved into JSON/"+ randomfile)



if __name__ == '__main__':
    main(sys.argv[1:])
