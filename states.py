
import sys
import requests

"""
Returns economic demographic data given a list of states

Assumptions
-----------

- That invoking utilility with 'python states.py ...'
  is good enough for the purpose at hand

- That simply printing an error message when bad arguments
  are passed is good enough. A more rubust implementation
  might raise an error or print to standarderr given the
  context

- That more sophisticated input handling (eg, parsing 'OR'
  as 'ore' isn't necessary for the purposes of this exercise
"""

VALID_FORMATS = ('csv', 'averages')
URLS = {
    'GET_FIPS_ID_BY_STATE': 'https://www.broadbandmap.gov/broadbandmap/census/state/{}?format=json',
    'GET_CENSUS_DATA_BY_IDS': 'https://www.broadbandmap.gov/broadbandmap/demographic/jun2014/state/ids/{}?format=json'
}

class StateLevelDemographicReporter(object):

    """ Wraps up functionality for retrieving state-level
        demographic data

        @param <list>states - a list of three-letter state abbreviations

        Usage:

        my_states = StateLevelDemographicReporter(['cal', 'ore'])
        my_states.output()
    """

    def __init__(self, states):
        self.fips_ids = states
        self.state_data = self.get_state_data()

    @property
    def fips_ids(self):
        return self._fips_ids

    @fips_ids.setter
    def fips_ids(self, states):
        """ Queries the API for the FIPS ID of each state in the input
        """
        self._fips_ids = []
        for state in states:
            url = URLS['GET_FIPS_ID_BY_STATE'].format(state)
            res = requests.get(url)
            results = res.json()['Results']
            if results != {}:
                self._fips_ids.append(results['state'][0]['fips'])
            else:
                print("Input not recognized: '{}'\n".format(state))
        if self._fips_ids == []:
            print("Error: States may not have been in a valid format ('ore', 'cal')")
            exit()

    def get_state_data(self):
        """ Queries the API for complete demographic data for each FIPS ID
            in self.fips_ids
        """
        url = URLS['GET_CENSUS_DATA_BY_IDS'].format(','.join(self.fips_ids))
        res = requests.get(url)
        json = res.json()
        return json['Results'] if 'Results' in json else []

    @property
    def average(self):
        """ Averages the income belowe poverty value for all states in the set
        """
        total_households = sum([v['households'] for v in self.state_data])
        weighted_average = sum([v['incomeBelowPoverty'] * (v['households'] / total_households) for v in self.state_data]) * 100
        return round(weighted_average)

    def output(self, output_format='csv'):
        """ Convenience method to print to the console
        """
        if output_format.lower() == 'csv':
            # <state name>, <population>, <households>, <income below poverty>, <median income>
            print("state, population, households, income_below_poverty_level, median_income")
            for state in self.state_data:
                row = "{state}, {population}, {households}, {income_below_poverty}, {median_income}".format(
                    state=state['geographyName'],
                    population=state['population'],
                    households=state['households'],
                    income_below_poverty=state['incomeBelowPoverty'],
                    median_income=state['medianIncome']
                )
                print(row)

        elif output_format.lower() == 'averages':
            print("{}%".format(self.average))

        else:
            print("Output format not recoginzed. Usage: python states.py <state1>,<state2> [csv/averages]")

if __name__ == '__main__':
    args = sys.argv

    if len(args) >= 2:
        states = args[1].split(',')
        data = StateLevelDemographicReporter(states)
        if len(sys.argv) == 3:
            data.output(args[2])
        else:
            data.output()
    else:
        print("Missing required argument 'states'. Usage: python states.py <state1>,<state2> [csv/averages]")









