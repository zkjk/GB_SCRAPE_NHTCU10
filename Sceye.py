#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from subprocess import *
import sys
import getopt
import os
import random
from pathlib import Path

#Creating a relative path to easily refer to files & folder
base_path = Path(__file__).parent

def main(argv):
    projectname = 'Sceye.py'
    scrapers = []
    scraperfolders = []
    spiders = []
    selectedscrapers = []
    listscrapers = False

    #Getting command line input
    try:
        (opts, args) = getopt.getopt(argv, 'hls:', ['list', 'select='
                ])
    except getopt.GetoptError:
        print ('Usage:', projectname, '<start/pause/stop> [options]')
        print('\n(Use', projectname, '-h to view options)')

        sys.exit(2)
    for (opt, arg) in opts:
        if opt == '-h':
            print ('Usage:', projectname, '[options]')
            print('\n Available options: \n')
            print ('-h \t\t Documentation')
            print ('-l, --list \t Show list of scraper(s)')
            print ('-s, --select \t Select scraper(s) (ID\'s seperated with commas)')
            print ('Currently only 1 scraper can be chosen at the same time')

            sys.exit()
        elif opt in ('-l', '--list'):
            listscrapers = True
        elif opt in ('-s', '--select'):
            selectedscrapers = (arg.split(","))
            selectedscrapers = [int(i) for i in selectedscrapers]


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

    #The code when the program starts
    if selectedscrapers:
        #Printing project information
        print("---------------------")
        print("NHTCU project OSINT")
        print("Team 10")
        print("Framework v0.2")
        print("---------------------")

        #Printing list of chosen scrapers
        print("You've chosen the following scraper(s):")
        print('ID','\t','Name','\t\t','Spider')
        for x in selectedscrapers:
            try:
                print(x,':\t',scrapers[x],'\t',spiders[x])
            except:
                print('Could not choose scraper #',x,'because it doesn\'t exist')
                exit()

        starting = input("\nPress Enter to start scraping (Stop with CTRL + C)")
        if starting == "":
            print("Scraping...")
        #Random file name
        randomfile = "scrape" + str(random.randint(0,99999)) + ".json"
        #The command that is ran to start the scraper
        cmd = 'scrapy crawl '+ spiders[selectedscrapers[0]] + ' -o ' +randomfile + ' -s LOG_ENABLED=False'

        try:
            #Running the command in cmd inside the scraper folder
            os.chdir(base_path / 'Scraper' / scrapers[0])
            subprocess.call(cmd, shell=True)
        except KeyboardInterrupt:
            print("\n\nScraped data saved into "+ randomfile)


if __name__ == '__main__':
    main(sys.argv[1:])
