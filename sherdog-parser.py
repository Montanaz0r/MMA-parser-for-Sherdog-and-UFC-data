# Python 3.7
# MMA/Sherdog scraper - enables scraping fighters data from sherdog & getting UFC's fighters roster.
# please get familiar with readme file before using!
# Created by - Montanaz0r (https://github.com/Montanaz0r)

from bs4 import BeautifulSoup
import requests
import csv
import logging
import json

# Initializes logging file.
logging.basicConfig(filename='sherdog.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class Fighter(object):
    """Fighter class - creating fighter instance based on fighter's Sherdog profile.
    """

    def __init__(self):
        """
        Initializes a Fighter instance.
        """
        self.url = None
        self.name = None  # str: fighter's name, None by default
        self.resource = None  # setting up resource based on url, None by default
        self.soup = None  # creating BeautifulSoup object, None by default
        self.pro_range = None  # selector: selecting range to pro fights exclusively, None by default
        self.validation = False  # boolean: confirms if scraped data for fighter instance is validated, False by default

        # Information about all pro fights, which certain Fighter instance had.

        self.result_data = None  # list of str: fight results
        self.opponents = None  # list of str: opponents
        self.events = None  # list of str: events
        self.events_date = None  # list of str: events date
        self.method = None  # list of str: methods in which fights have ended
        self.judges = None  # list od str: judges names
        self.rounds = None  # list of str: rounds in which fights have ended
        self.time = None  # list of str: exact point of time in the round where fights have ended

    def _set_url_from_index(self, fighter_index):
        """
        Sets up url for fighter's instance.
        :param fighter_index: integer with fighter's index
        :return: None
        """
        self.url = f'https://www.sherdog.com/fighter/index?id={fighter_index}.'

    def _set_url_from_selector(self, fighter_page):
        """
        Sets up url from css selector match.
        :param fighter_page: css selector result
        :return: None
        """
        self.url = f'http://www.sherdog.com{fighter_page}'

    def _set_resource(self):
        """
        Sets up response object based on self.url value.
        :return: response object
        """
        resource = requests.get(self.url)
        self.resource = resource
        return resource

    def _set_soup(self):
        """
        Sets up soup for Fighter's instance using data provided in self.resource.
        :return: BeautifulSoup instance
        """
        soup = BeautifulSoup(self.resource.text, features='html.parser')
        self.soup = soup
        return soup

    def set_pro_fights(self):
        """
        Sets up range of pro fights for Fighter instance with html code scraped from the site.
        :return: None
        """
        all_sections = self.soup.find_all('section')
        for section in all_sections:
            if section.find('div', text='FIGHT HISTORY - PRO'):
                pro_fights = section
                self.pro_range = pro_fights

    def set_name(self):
        """
        Collects and sets name for Fighter instance.
        :return: sets self.name to scraped string with fighter's name, returns AttributeError in case none was found
        """
        name = self.soup.find('span', class_='fn')
        try:
            self.name = name.get_text()
        except AttributeError:
            return AttributeError

    def grab_result_data(self):
        """
        Collects and sets results for all pro fights in range of Fighter instance.
        :return: list of strings with results
        """
        results = []
        try:
            finder = self.pro_range.find_all('span', class_='final_result')
            for result in finder:
                results.append(result.get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing result data for {self.name}, the data might be missing!')
        else:
            self.result_data = results
            return results

    def grab_opponents(self):
        """
        Collects and sets names of opponents in range of pro fights for Fighter instance.
        :return: list of strings with opponents names
        """
        fighters = []
        try:
            finder = self.pro_range.find_all('a')
            for index in range(0, len(finder), 2):
                fighters.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing opponent data for {self.name}, the data might be missing!')
        else:
            self.opponents = fighters
            return fighters

    def grab_events(self):
        """
        Collects and sets events in range of pro fights for Fighter instance.
        :return: list of strings with events
        """
        events = []
        try:
            finder = self.pro_range.find_all('a')
            for index in range(1, len(finder), 2):
                events.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing event data for {self.name}, the data might be missing!')
        else:
            self.events = events
            return events

    def grab_events_date(self):
        """
        Collects and sets events dates in range of pro fights for Fighter instance.
        :return: list of strings with events dates
        """
        events_date = []
        try:
            finder = self.pro_range.find_all('span', class_='sub_line')
            for index in range(0, len(finder), 2):
                events_date.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing event dates for {self.name}, the data might be missing!')
        else:
            self.events_date = events_date
            return events_date

    def grab_judges(self):
        """
        Collects and sets judges names in range of pro fights for Fighter instance.
        :return: list of strings with judges names
        """
        judges = []
        try:
            finder = self.pro_range.find_all('span', class_='sub_line')
            for index in range(1, len(finder), 2):
                judges.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing judges data for {self.name}, the data might be missing!')
        else:
            self.judges = judges
            return judges

    def grab_method(self):
        """
        Collects and sets fight end methods in range of pro fights for Fighter instance.
        :return: list of strings with fight end methods
        """
        methods = []
        try:
            finder = self.pro_range.find_all('td')
            for index in range(9, len(finder), 6):
                checker = 0  # small trick that will allow scraper to only get end methods and leave judge name.
                for text in finder[index].stripped_strings:
                    if checker % 2 == 0:
                        methods.append(text)
                        checker += 1
                    else:
                        checker += 1
        except AttributeError:
            logging.info(f'Attribute Error while grabbing methods data for {self.name}, the data might be missing!')
        else:
            self.method = methods
            return methods

    def grab_rounds(self):
        """
        Collects and sets information about round in which fight was finished in range of pro fights for
        Fighter instance.
        :return: list of strings with rounds
        """
        rounds = []
        try:
            finder = self.pro_range.find_all('td')
            for index in range(10, len(finder), 6):
                rounds.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing rounds data for {self.name}, the data might be missing!')
        else:
            self.rounds = rounds
            return rounds

    def grab_time(self):
        """
        Collects and sets fight time end in range of pro fights for Fighter instance.
        :return: list of strings with time
        """
        time = []
        try:
            finder = self.pro_range.find_all('td')
            for index in range(11, len(finder), 6):
                time.append(finder[index].get_text())
        except AttributeError:
            logging.info(f'Attribute Error while grabbing time data for {self.name}, the data might be missing!')
        else:
            self.time = time
            return time

    def get_validation(self):
        """
        Making validation by comparing collected data, checking if length of all information matches number of fights
        that was scraped for fighter instance.
        :return: boolean value or TypeError in case any of lists was empty (self.validation is False by default)
        """
        for_validation = [self.time, self.rounds, self.method, self.judges, self.events_date, self.events,
                          self.result_data]
        try:
            if all(len(x) == len(self.opponents) for x in for_validation):
                self.validation = True
                return True
            else:
                print(f'Warning: validation unsuccessful for {self.name}!')
                return False
        except TypeError:
            return TypeError

    def is_valid(self):
        """
        Supporting method for checking status of validation for fighter instance.
        :return: boolean value
        """
        if self.validation is True:
            return True
        else:
            return False

    def save_to_csv(self, filename):
        """
        Writing all collected information regarding fighter instance to csv file.
        :param filename: string with name of the file we want to save data to; file will be created with given name
        :return: None
        """
        with open(f'{filename}.csv', 'a', newline='', encoding="ISO-8859-1") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for index in range(len(self.result_data)):
                try:
                    opp = self.opponents[index]
                except IndexError:
                    opp = 'N/A'
                try:
                    result = self.result_data[index]
                except IndexError:
                    result = 'N/A'
                try:
                    event = self.events[index]
                except IndexError:
                    event = 'NA'
                try:
                    event_date = self.events_date[index]
                except IndexError:
                    event_date = 'NA'
                try:
                    method = self.method[index]
                except IndexError:
                    method = 'NA'
                try:
                    judges = self.judges[index]
                except IndexError:
                    judges = 'NA'
                try:
                    rounds = self.rounds[index]
                except IndexError:
                    rounds = 'NA'
                try:
                    time = self.time[index]
                except IndexError:
                    time = 'NA'
                try:
                    writer.writerow([self.name, opp, result, event, event_date, method, judges, rounds, time])
                except UnicodeEncodeError:
                    print(f'Coding error while attempting to save date for {self.name}, line was dropped!')
            print(f'CSV file was successfully overwritten for {self.name}!')

    def save_to_json(self, filename):
        """
        Writing all collected information regarding fighter instance to json file.
        :param filename: string with name of the file we want to save data to; file will be created with given name
        :return: None
        """
        fighter_dictionary = {self.name: []}  # initializing dictionary that will be passed into json file.

        for index in range(len(self.result_data)):
            try:
                opp = self.opponents[index]
            except IndexError:
                opp = 'N/A'
            try:
                result = self.result_data[index]
            except IndexError:
                result = 'N/A'
            try:
                event = self.events[index]
            except IndexError:
                event = 'NA'
            try:
                event_date = self.events_date[index]
            except IndexError:
                event_date = 'NA'
            try:
                method = self.method[index]
            except IndexError:
                method = 'NA'
            try:
                judges = self.judges[index]
            except IndexError:
                judges = 'NA'
            try:
                rounds = self.rounds[index]
            except IndexError:
                rounds = 'NA'
            try:
                time = self.time[index]
            except IndexError:
                time = 'NA'
            line = {'opponent': opp, 'result': result, 'event': event, 'date': event_date, 'method': method,
                    'judge': judges, 'round': rounds, 'time': time}
            fighter_dictionary[self.name].append(line)

        with open(f'{filename}.json') as fighter_json:
            data = json.load(fighter_json)
        data.update(fighter_dictionary)
        with open(f'{filename}.json', 'w') as fighter_json:
            json.dump(data, fighter_json, indent=4)
        print(f'JSON file was successfully overwritten for {self.name}!')

    def scrape_fighter(self, filetype, filename, fighter_index=None, fighter_page=None):
        """
        :param filetype: string with either 'csv' or 'json' as a type of file where results will be stored.
        :param filename: string with name of the file we want to save data to; file will be created with given name
        :param fighter_index: optional - integer with fighter's index, or None
        :param fighter_page: optional - css selector match with fighter's page, or None
        :return: True for valid fighter's page and False if page was empty
        """
        if fighter_index is not None:
            self._set_url_from_index(fighter_index)
        elif fighter_page is not None:
            self._set_url_from_selector(fighter_page)
        else:
            print("Error, please pass fighter's index, or fighter's page in order to proceed.")
        self._set_resource()
        self._set_soup()
        if self.set_name() != AttributeError:  # checking if there is existing name for a fighter instance.
            self.set_pro_fights()
            self.grab_result_data()
            self.grab_opponents()
            self.grab_events_date()
            self.grab_events()
            self.grab_judges()
            self.grab_method()
            self.grab_rounds()
            self.grab_time()
            if self.get_validation() != TypeError:  # if there was an empty list while validating data,
                if filetype == 'csv':               # fighter instance will be dropped.
                    self.save_to_csv(filename)
                elif filetype == 'json':
                    self.save_to_json(filename)
            return True
        else:
            return False

# END OF FIGHTER CLASS


def scrape_all_fighters(filename, filetype='csv'):
    """
    Scrapes information about all fighters in Sherdog's database and saves them into csv or json file.
    :param filename: string with name of the file we want to save data to; file will be created with given name
    :param filetype: string with either 'csv' or 'json' as a type of file where results will be stored
    :return: None
    """
    if filetype == 'csv':
        headers = ['Fighter', 'Opponent', 'Result', 'Event', 'Event_date', 'Method', 'Referee', 'Round', 'Time']
        with open(f'{filename}.csv', 'w', newline='') as csvfile:
            init_writer = csv.writer(csvfile, delimiter=',')
            init_writer.writerow(headers)

    elif filetype == 'json':
        json_init = {}
        with open(f'{filename}.json', 'w') as fighter_json:
            json.dump(json_init, fighter_json)

    fighter_index = 0   # sets up and stores index of a fighter that scraper is collecting information about.
    fail_counter = 0    # amount of 'empty' indexes in a row.

    while fail_counter <= 10:  # scraper will be done after there were 10 non-existing sites (indexes) in a row.
        F = Fighter()          # creating fighter's instance object.
        scrapped_data = F.scrape_fighter(filetype, filename, fighter_index=fighter_index)
        if scrapped_data is True:
            fail_counter = 0  # resetting fail counter after finding valid page(index) for a fighter.
        else:
            fail_counter += 1  # incrementing fail counter if there was no data for certain index.
        fighter_index += 1  # incrementing index.


def scrape_ufc_roster(save='no', filetype=None):
    """
    Scrapes information about all fighters in UFC database and saves them into csv or json file.
    :param save: string with 'yes' or 'no' depends on output data allocation. Default is 'no' and data will be stored
                 only in variable
    :param filetype: string with either 'csv' or 'json' as a type of file where results will be stored. Default is None
    :return: dictionary with information about UFC roster, for each fighter there will be a tuple containing
             (name, weight-division, nickname)
    """
    ufc_roster = {
        'men': [],
        'women': []
    }

    men_roster = []
    women_roster = []

    for gender_index in range(1, 3):
        page = 0
        while True:
            resource = requests.get(f'https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23&'
                                    f'gender={gender_index}&page={page}')
            soup = BeautifulSoup(resource.text, features='html.parser')
            fighter = soup.find_all('div', class_='c-listing-athlete__text')
            if len(fighter) == 0:  # if page is empty = there are no fighters left, current gender index is done.
                break
            else:
                for index in range(len(fighter)):
                    name = fighter[index].find('span', class_='c-listing-athlete__name').get_text().strip()
                    division = fighter[index].find_all('div', class_='field__item')
                    try:
                        div = division[1].get_text()
                    except IndexError:
                        try:
                            div = division[0].get_text()
                        except IndexError:
                            div = 'NA'
                    try:
                        nickname = fighter[index].find('span', class_='c-listing-athlete__nickname').div.get_text()
                        nickname = nickname.replace('\n', '')
                    except AttributeError:
                        nickname = 'NA'
                    if gender_index == 2:
                        women_roster.append((name, div, nickname))
                    elif gender_index == 1:
                        men_roster.append((name, div, nickname))
                page += 1

    ufc_roster['men'] = men_roster
    ufc_roster['women'] = women_roster

    if save == 'yes':
        if filetype == 'csv':
            headers = ['Name', 'Division', 'Nickname']
            with open('ufc-roster.csv', 'w', newline='') as csvfile:
                init_writer = csv.writer(csvfile, delimiter=';')
                init_writer.writerow(headers)
            with open('ufc-roster.csv', 'a', newline='', encoding="ISO-8859-1") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for index in range(len(ufc_roster['men'])):
                    try:
                        writer.writerow([ufc_roster['men'][index][0], ufc_roster['men'][index][1],
                                         ufc_roster['men'][index][2]])
                    except UnicodeEncodeError:
                        print(f'Unfortunately record containing {ufc_roster["men"][index]} '
                              f'dropped due to UnicodeEncodeError!')
                for index in range(len(ufc_roster['women'])):
                    try:
                        writer.writerow([ufc_roster['women'][index][0], ufc_roster['women'][index][1],
                                         ufc_roster['women'][index][2]])
                    except UnicodeEncodeError:
                        print(f'Unfortunately record containing {ufc_roster["women"][index]} '
                              f'dropped due to UnicodeEncodeError!')
        elif filetype == 'json':
            with open('ufc-roster.json', 'w') as fighter_json:
                json.dump(ufc_roster, fighter_json, indent=4)
    return ufc_roster


def scrape_list_of_fighters(fighters_list, filename, filetype='csv'):
    """
    Scrapes information about list of fighters in sherdog's database and saves them into csv or json file.
    :param fighters_list: list with fighters to be scrapped from sherdog, fighter list should contain tuple with
           (name, weight-division, nickname) for each fighter
    :param filename: string with name of the file we want to save data to; file will be created with given name
    :param filetype: string with either 'csv' or 'json' as a type of file where results will be stored. Default is 'csv'
    :return: None
    """
    
    def search_fighter(fighter_tuple):
        """
        Nested function that creates response objects for fighter based on the information included in fighter's tuple.
        :param fighter_tuple: tuple that contains (name, weight-division, nickname) for certain fighter.
        :return: list of four response objects [1, 2, 3, 4].
                 1 - based only on fighter's name
                 2 - based on fighter's name and weight class
                 3 - based on fighter's name and nickname
                 4 - based on fighter's name, nickname and weight class
        """
        res_1 = requests.get(f'https://www.sherdog.com/stats/fightfinder?SearchTxt={fighter_tuple[0]}')
        res_2 = requests.get(f'https://www.sherdog.com/stats/fightfinder?SearchTxt={fighter_tuple[0]}'
                             f'&weight={weight_classes[fighter_tuple[1]]}')
        res_3 = requests.get(f'https://www.sherdog.com/stats/fightfinder?SearchTxt={fighter_tuple[0]}'
                             f'+{fighter_tuple[2]}')
        res_4 = requests.get(f'https://www.sherdog.com/stats/fightfinder?SearchTxt={fighter_tuple[0]}'
                             f'+{fighter_tuple[2]}&weight={weight_classes[fighter_tuple[1]]}')

        return [res_1, res_2, res_3, res_4]

    def soup_selector(request):
        """
        Nested function that makes setting up soup object and css selector for fighter instance more convenient.
        :param request: response object
        :return: css selector
        """
        soup = BeautifulSoup(request.text, features='html.parser')
        css_selector = soup.select('body > div.container > div:nth-child(3) > div.col_left > section:nth-child(2) > '
                                   'div > div.content.table > table')
        return css_selector

    def check_result(css_selector):
        """
        Nested function that makes checking for searching results based on css selector more convenient.
        :param css_selector: css selector
        :return: css selector's match, or IndexError if there is none
        """
        try:
            result = css_selector[0].find_all('a')
            return result
        except IndexError:
            return IndexError

    def create_fighter_instance(matching):
        """
        Nested function that makes creating and scraping fighter's instance object more convenient.
        :param matching: css selector results
        :return: None
        """
        fighter_page = matching[0]['href']
        F = Fighter()
        F.scrape_fighter(filetype, filename, fighter_page=fighter_page)

    weight_classes = {
        "Heavyweight": 2,
        "Light Heavyweight": 3,
        "Middleweight": 4,
        "Welterweight": 5,
        "Lightweight": 6,
        "Featherweight": 7,
        "Bantamweight": 9,
        "Flyweight": 10,
        "Women's Strawweight": 13,
        "Women's Flyweight": 10,
        "Women's Bantamweight": 9,
        "Women's Featherweight": 7,
    }

    if filetype == 'csv':
        headers = ['Fighter', 'Opponent', 'Result', 'Event', 'Event_date', 'Method', 'Referee', 'Round', 'Time']
        with open(f'{filename}.csv', 'w', newline='') as csvfile:
            init_writer = csv.writer(csvfile, delimiter=';')
            init_writer.writerow(headers)

    elif filetype == 'json':
        json_init = {}
        with open(f'{filename}.json', 'w') as fighter_json:
            json.dump(json_init, fighter_json)

    for fighter in fighters_list:
        search_results = search_fighter(fighter)   # variable that stores different searching results.
        find_fighter = search_results[0]           # assigning first result to variable.
        selector = soup_selector(find_fighter)     # creating selector based on search result.
        results = check_result(selector)           # checking if there is a valid outcome.
        if results == IndexError:
            logging.info(f'Error occurred with {fighter}, please check carefully '
                         f'if there is no mistake in fighter name!')
        else:
            if len(results) == 1:
                create_fighter_instance(results)         # creating Fighter's instance and saving it.
            else:
                find_fighter = search_results[1]         # assigning second result to variable.
                selector = soup_selector(find_fighter)   # creating selector based on search result.
                results = check_result(selector)         # checking if there is a valid outcome.
                if results == IndexError:
                    try:
                        find_fighter = search_results[2]         # assigning third result to variable.
                    except KeyError:
                        print('Search engine tried to narrow down findings by using weight-class filter, apparently '
                              'you have not specified weight-class data!')
                    else:
                        selector = soup_selector(find_fighter)   # creating selector based on search result.
                        results = check_result(selector)         # checking if there is a valid outcome.
                        if results == IndexError:
                            logging.info(f'Error occured with {fighter}, please check carefully if there is no mistake '
                                         f'in nickname!')
                        else:
                            if len(results) == 1:
                                create_fighter_instance(results)  # creating Fighter's instance and saving it.
                else:
                    selector = soup_selector(find_fighter)        # creating selector based on search result.
                    results = check_result(selector)              # checking if there is a valid outcome.
                    if results == IndexError:
                        logging.info(f'Error occured with {fighter}, please check carefully if there is no mistake '
                                         f'in nickname!')
                    else:
                        if len(results) == 1:
                            create_fighter_instance(results)      # creating Fighter's instance and saving it.
                        else:
                            try:
                                find_fighter = search_results[2]  # assigning third result to variable.
                            except KeyError:
                                print(f'Search engine tried to narrow down findings by name & nickname, apparently this'
                                      f'was not enough to find {fighter[0]}!')
                            else:
                                selector = soup_selector(find_fighter)  # creating selector based on search result.
                                results = check_result(selector)        # checking if there is a valid outcome.
                                if results == IndexError:
                                    logging.info(f'Error occurred with {fighter}, please check carefully '
                                                 f'- searching with name & nickname data was unsuccessful!')
                                else:
                                    if len(results) == 1:
                                        create_fighter_instance(results)  # creating Fighter's instance and saving it.
                                    else:
                                        try:
                                            find_fighter = search_results[3]  # assigning fourth result to variable.
                                        except KeyError:
                                            print(f'Search engine tried to narrow down findings by using all filters, '
                                                  f'apparently this was not enough to find {fighter[0]}!')
                                        else:
                                            # creating selector based on search result.
                                            selector = soup_selector(find_fighter)
                                            # checking if there is a valid outcome.
                                            results = check_result(selector)
                                            if results == IndexError:
                                                logging.info(f'Error occurred with {fighter}, please check carefully '
                                                             f'- searching with all provided data was unsuccessful!')
                                            else:
                                                # creating Fighter's instance and saving it.
                                                create_fighter_instance(results)


def helper_read_fighters_from_csv(filename, delimiter=','):
    """
    Helper function that will help creating fighters list from existing csv file.
    :param filename: csv filename
    :param delimiter: string with delimiter used in csv file, default = ','
    :return: list of fighters, where each fighter is a tuple(name, weight-division, nickname)
    """
    fighters_list = []
    with open(f'{filename}.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader, None)
        for row in reader:
            str_row = f'{delimiter}'.join(row)
            split_str = str_row.split(f'{delimiter}')
            fighters_list.append(split_str)
    return fighters_list


if __name__ == '__main__':
    scrape_all_fighters('sherdog')







