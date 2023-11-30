import unittest
from src.loader import SlackDataLoader

class TestSlackDataLoader(unittest.TestCase):
    def setUp(self):
        # Set up the SlackDataLoader instance with a sample path
        self.loader = SlackDataLoader('data')

    def test_parse_slack_reaction_columns(self):
        # Choose a specific channel for testing
        channel_name = 'all-week8'
        
        # Call the method to get reactions
        df = self.loader.parse_slack_reaction(channel_name)

        # Define the expected columns
        expected_columns = ['reaction_name', 'reaction_count', 'reaction_users_count', 'message', 'user_id', 'channel']

        # Check if the actual columns match the expected columns
        self.assertEqual(list(df.columns), expected_columns)

    def test_slack_parser_columns(self):
        # Choose a specific channel for testing
        channel_name = 'all-week8'
        
        # Call the method to parse slack data
        df = self.loader.slack_parser(channel_name)

        # Define the expected columns
        expected_columns = ['msg_type', 'msg_content', 'sender_name', 'msg_sent_time',
       'msg_dist_type', 'time_thread_start', 'reply_count',
       'reply_users_count', 'reply_users', 'tm_thread_end', 'channel',
       'directory']

        # Check if the actual columns match the expected columns
        self.assertEqual(list(df.columns), expected_columns)

        # Additionally, check if the DataFrame is not empty
        self.assertFalse(df.empty, "DataFrame should not be empty")

if __name__ == '__main__':
    unittest.main()
