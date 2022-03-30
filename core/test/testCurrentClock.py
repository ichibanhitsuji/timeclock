from graphene_django.utils import GraphQLTestCase
from django.contrib.auth.models import User


class CurrentClockTestCase(GraphQLTestCase):
    """
    Test case for currentClock query
    """
    GRAPHQL_SCHEMA = "schema"
    GRAPHQL_URL = "/graphql"

    clock_in_query = '''
            mutation {
                clockIn {
                    clock {
                        id,
                        clockedIn,
                        clockedOut
                    } 
                }
            }
        '''

    clock_out_query = '''
                mutation {
                    clockOut {
                        clock {
                            id,
                            clockedIn,
                            clockedOut
                        } 
                    }
                }
            '''

    current_clock_query = '''
                        query {
                            currentClock {
                                id,
                                clockedIn,
                                clockedOut
                            }
                        }
                    '''

    def setUp(self):
        """
        Create a user and login before each test
        """
        self.user = User.objects.create_user(
            username="test1",
            email="test1@test.co.jp",
            password="test1")
        self.client.login(username="test1", password="test1")

    def test_current_clock_without_clockIn_should_return_null(self):
        """
        Test currentClock query without previous clockIn
        """
        response = self.client.post(self.GRAPHQL_URL, {"query": self.current_clock_query})
        self.assertResponseNoErrors(response)

        # currentClock should be null
        self.assertIsNone(response.json()["data"]["currentClock"])

    def test_current_clock_with_clockIn(self):
        """
        Test currentClock query with previous clockIn
        """
        self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})
        response = self.client.post(self.GRAPHQL_URL, {"query": self.current_clock_query})
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(response.json()["data"]["currentClock"]["clockedIn"])

    def test_current_clock_with_clockin_and_clockout_should_return_null(self):
        """
        Test currentClock query with previous clockIn and clockOut
        """
        self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})
        self.client.post(self.GRAPHQL_URL, {"query": self.clock_out_query})
        response = self.client.post(self.GRAPHQL_URL, {"query": self.current_clock_query})
        self.assertResponseNoErrors(response)
        self.assertIsNone(response.json()["data"]["currentClock"])

    def tearDown(self):
        """
        Logout and Delete the user after each test
        """
        self.client.logout()
        self.user.delete()
