from graphene_django.utils import GraphQLTestCase
from django.contrib.auth.models import User


class ClockInOutTestCase(GraphQLTestCase):
    """
    Test case for clock in and out
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

    def setUp(self):
        """
        Create a user and login before each test
        """
        self.user = User.objects.create_user(
            username="test1",
            email="test1@test.co.jp",
            password="test1")
        self.client.login(username="test1", password="test1")

    def test_clock_in(self):
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(response.json()["data"]["clockIn"]["clock"]["id"])
        self.assertIsNotNone(response.json()["data"]["clockIn"]["clock"]["clockedIn"])
        self.assertIsNone(response.json()["data"]["clockIn"]["clock"]["clockedOut"])

    def test_clock_in_twice_should_raise_error(self):
        self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})

        # assert exception has been raised
        self.assertResponseHasErrors(response)
        self.assertEqual(response.json()["errors"][0]["message"], "You have already clocked in")

    def test_clock_out_should_raise_error_if_not_clocked_in(self):
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clock_out_query})
        self.assertResponseHasErrors(response)
        self.assertEqual(response.json()["errors"][0]["message"], "You have not clocked in yet")

    def test_clock_out(self):
        self.client.post(self.GRAPHQL_URL, {"query": self.clock_in_query})
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clock_out_query})
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(response.json()["data"]["clockOut"]["clock"]["id"])
        self.assertIsNotNone(response.json()["data"]["clockOut"]["clock"]["clockedIn"])
        self.assertIsNotNone(response.json()["data"]["clockOut"]["clock"]["clockedOut"])

    def tearDown(self):
        """
        Logout and Delete the user after each test
        """
        self.client.logout()
        self.user.delete()
