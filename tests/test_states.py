
import unittest
import mock
import states

class TestStateLevelDemographicReporter(unittest.TestCase):

    def setUp(self):
        self.states_list = ['col','ore']

    @mock.patch('states.StateLevelDemographicReporter.get_state_data')
    @mock.patch('requests.get')
    def test_fips_ids(self, mock_get, mock_gsd):
        d = states.StateLevelDemographicReporter(self.states_list)
        d.fips_ids = ['wyo']
        url = states.URLS['GET_FIPS_ID_BY_STATE'].format('wyo')
        mock_get.assert_called_with(url)
        mock_get.return_value.json.assert_called()
        self.assertEqual(
            d.fips_ids,
            [mock_get.return_value.json.return_value['Results']['state'][0]['fips']]
        )

    @mock.patch('states.StateLevelDemographicReporter.fips_ids')
    @mock.patch('requests.get')
    def test_get_state_data(self, mock_get, mock_fips_ids):
        mock_fips_ids.return_value = ['col','ore']
        mock_get.return_value.json.return_value = {'Results': "meow"}
        d = states.StateLevelDemographicReporter(self.states_list)
        result = d.get_state_data()
        url = states.URLS['GET_CENSUS_DATA_BY_IDS'].format(','.join(mock_fips_ids.return_value))
        mock_get.assert_called_with(url)
        mock_get.return_value.json.assert_called_with()
        self.assertEqual(result, "meow")

    @mock.patch('states.StateLevelDemographicReporter.get_state_data')
    @mock.patch('states.StateLevelDemographicReporter.fips_ids', new_callable=mock.PropertyMock)
    def test_average(self, mock_fips_ids, mock_gsd):
        mock_gsd.return_value = [
            {'incomeBelowPoverty': 5.0, 'households':1000},
            {'incomeBelowPoverty': 10.0, 'households':2000}
        ]
        d = states.StateLevelDemographicReporter(self.states_list)
        avg = d.average
        self.assertEqual(avg, 833)

    @mock.patch('states.StateLevelDemographicReporter.average', new_callable=mock.PropertyMock)
    @mock.patch('states.StateLevelDemographicReporter.fips_ids', new_callable=mock.PropertyMock)
    @mock.patch('states.StateLevelDemographicReporter.get_state_data')
    def test_output(self, mock_gsd, mock_fips_ids, mock_avg):
        mock_state_obj = mock.MagicMock()
        mock_gsd.return_value = [mock_state_obj]
        d = states.StateLevelDemographicReporter(self.states_list)
        d.output(output_format='csv')
        d.output(output_format='averages')
        mock_avg.assert_called()

if __name__ == '__main__':
    unittest.main()
