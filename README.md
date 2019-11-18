# MMA-parser-for-Sherdog-and-UFC-data
Python web scraper for Sherdog &amp; UFC data. Creates output of your choice in .csv or .json format.

## Table of Contents

* [Requirements](#Requirements)
* [Brief description](#Brief-description)
* [Contact](#Contact)
* [Quick Tutorial](#quick-tutorial)
* [Wrap-Up](#setup)

## Requirements:

*requests==2.21.0*

*beautifulsoup4==4.8.1*

## Brief description

Parser was built from scratch in Python 3.7 in order to support MMA data analysis project i have been working on.
Parser can perform few different tasks, the main utility is parsing all pro fights information for each fighter in *www.sherdog.com* database.  
Below you can find example of collected data saved as csv file:

```
Fighter,Opponent,Result,Event,Event_date,Method,Referee,Round,Time
Tony Galindo,Tony Lopez,loss,KOTC 49 - Soboba,Mar / 20 / 2005,KO (Punches),N/A,1,3:24   	
Tony Galindo,Joey Villasenor,loss,KOTC 21 - Invasion,Feb / 21 / 2003,TKO (Corner Stoppage),Larry Landless,1,5:00  	 
Tony Galindo,Brian Sleeman,loss,GC 6 - Caged Beasts,Sep / 09 / 2001,TKO (Corner Stoppage),Larry Landless,2,3:10  	  
Tony Galindo,Reggie Cardiel,win,KOTC 9 - Showtime,Jun / 23 / 2001,Decision,N/A,2,5:00  	  
Tony Galindo,Reggie Cardiel,draw,KOTC 7 - Wet and Wild,Feb / 24 / 2001,Draw,N/A,2,5:00
Tony Galindo,Brian Hawkins,win,KOTC 6 - Road Warriors,Nov / 29 / 2000,TKO (Punches),N/A,1,1:30 	 
Tony Galindo,Kurt Rojo,win,KOTC 4 - Gladiators,Jun / 24 / 2000,KO (Punch),N/A,1,0:07 	
Kurt Rojo,Phillip Miller,loss,GC 1 - Gladiator Challenge 1,Dec / 09 / 2000,Decision,N/A,3,5:00 	 
Kurt Rojo,Tony Galindo,loss,KOTC 4 - Gladiators,Jun / 24 / 2000,KO (Punch),N/A,1,0:07
```

Second utility you may find useful is scraping information about current ufc roster from official UFC site.  
Here is an example of csv outcome for mentioned function:

```
Name,Division,Nickname
Shamil Abdurakhimov,Heavyweight,Abrek
Klidson Abreu,Light Heavyweight,White Bear
Juan Adams,Heavyweight,The Kraken
Israel Adesanya,Middleweight,The Last Stylebender
Kevin Aguilar,Featherweight,Angel of Death
Omari Akhmedov,Middleweight,Wolverine
Rostem Akman,Welterweight,NA
Heili Alateng,Bantamweight,The Mongolian Knight
Junior Albini,Heavyweight,Baby
```

You can also scrape only selected fighters from sherdog using your own list as an argument, or pass what was returned by ufc roster function, if you wish to scrape only data about current ufc fighters.

## Contact

Feel free to send me feedback at montana102@gmail.com

## Quick tutorial

### 1. scrape_all_fighters function

Main function that you may find yourself using. It allows you to scrape all fighters from sherdog database and save results to either .csv file or .json. Function takes following arguments:

* filename - string
* filetype - string (csv or json) *csv is default*

**Examples:**
```
scrape_all_fighters('sherdog')
```

This will scrape all the fighters to sherdog.csv file.

```
scrape_all_fighters('sherdog', filetype='json')
```

This will do the same but result will be stored in json file.

### 2. scrape_ufc_roster function

Scrapes information about all fighters in UFC current roster. You can store the outcome in .csv file, .json file or just in variable.
It takes following arguments:

* save - string (either 'yes' or 'no) *'no' is default
* filetype - string (csv or json) *None is default*

Function will return dictionary containing two keys - men and women, each key contains list of tuples where each tuple represents the fighter in the following form (name, weight-division, nickname).

**Examples:**
```
ufc = scrape_ufc_roster(save='no', filetype=None):
```

This one will scrape ufc roster information and assign returned dictionary to ufc variable.

```
scrape_ufc_roster(save='yes', filetype='csv'):
```

This will scrape ufc roster and save output to csv file. Csv will be named *ufc-roster.csv* be default.

### 3. scrape_list_of_fighters function

Scrapes information about specified list of fighters from sherdog site. You can store the outcome in .csv file or .json file. 
It takes following arguments:

* fighters_list - list of tuples where each tuple represents fighter in the following manner (name, weight-division, nickname)
* filename - string
* filetype - string (csv or json) *csv is default*                 





## Wrap-Up

You may find docstrings to be helpful, make sure you read them before using.  
Please also make sure you are not violiting site's terms of use before you will scrape data!
