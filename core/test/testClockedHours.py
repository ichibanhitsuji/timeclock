from graphene_django.utils import GraphQLTestCase
from django.contrib.auth.models import User
from core.models import Clock
from datetime import datetime, timedelta
from freezegun import freeze_time


class ClockedHoursTestCase(GraphQLTestCase):
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
    clocked_hours_query = '''
                            query { 
                                clockedHours {
                                    today
                                    currentWeek,
                                    currentMonth,
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

    @freeze_time("2022-03-30 22:00:00")
    def test_clockedHours_return_0_when_no_clock_in(self):
        """
        Test that the clockedHours query returns 0 when no clock in
        """
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clocked_hours_query})
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["clockedHours"]["today"], 0)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentWeek"], 0)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentMonth"], 0)

    @freeze_time("2022-03-30 22:00:00")
    def test_when_multiple_clockin_clockout(self):
        """
        Test that the clockedHours query returns the correct time when multiple clock in and clock out occurred
        """
        # Arrange
        # Create two new Clock for the current user
        morning_clock_in = Clock.objects.create(user=self.user,
                                                clocked_out=datetime(2022, 3, 30, 12, 0, 0))
        morning_clock_in.clocked_in = datetime(2022, 3, 30, 9, 0, 0)
        morning_clock_in.save()

        afternoon_clock_in = Clock.objects.create(user=self.user, clocked_out=datetime(2022, 3, 30, 18, 00))
        afternoon_clock_in.clocked_in = datetime(2022, 3, 30, 13, 00)
        afternoon_clock_in.save()

        hours_worked_in_week = Clock.objects.create(user=self.user, clocked_out=datetime(2022, 3, 28, 13, 00))
        hours_worked_in_week.clocked_in = datetime(2022, 3, 28, 12, 00)
        hours_worked_in_week.save()

        hours_worked_in_week = Clock.objects.create(user=self.user, clocked_out=datetime(2022, 3, 2, 18, 00))
        hours_worked_in_week.clocked_in = datetime(2022, 3, 2, 17, 00)
        hours_worked_in_week.save()

        # Act
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clocked_hours_query})
        # Assert
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["clockedHours"]["today"], 8)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentWeek"], 9)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentMonth"], 10)

    @freeze_time("2022-03-30 22:00:00")
    def test_when_the_clockin_clockout_is_longer_than_one_day(self):
        """
        Test that the clockedHours query returns the correct time when deltat between the clock and clock out
        is longer than one day
        """
        # Arrange
        # Create a new Clock for the current user
        new_clock = Clock.objects.create(user=self.user, clocked_out=datetime(2022, 3, 30, 12, 0, 0))

        # set up the clockin 3 days earlier
        new_clock.clocked_in = new_clock.clocked_out - timedelta(days=3)
        new_clock.save()

        # Act
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clocked_hours_query})

        # Assert
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["clockedHours"]["today"], 12)
        # 27th is a sunday. So hour worked in the week should be from 28 to 30 at 12:00 (60)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentWeek"], 60)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentMonth"], 72)

    @freeze_time("2022-03-30 22:00:00")
    def test_user_clockin_but_not_clockout_after_one_month(self):
        """
        Test that the clockedHours query returns the correct time when the user clock in but not clock out
        after one month elapsed
        """
        # Arrange
        # Create a new Clock for the current user
        new_clock = Clock.objects.create(user=self.user)

        clock_in_date = datetime(2022, 3, 30, 12, 0, 0).replace(month=2, day=27)

        # set up the clockin 3 days earlier
        new_clock.clocked_in = clock_in_date
        new_clock.save()

        # Act
        response = self.client.post(self.GRAPHQL_URL, {"query": self.clocked_hours_query})

        # Assert
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()["data"]["clockedHours"]["today"], 22)

        # 27th is a sunday. Hours worked in the week should be from 28 to 30 at 22:00 (70)
        self.assertEqual(response.json()["data"]["clockedHours"]["currentWeek"], 70)

        # hours worked before today ( 29 * 24 = 696 ) + today (22) = 718
        self.assertEqual(response.json()["data"]["clockedHours"]["currentMonth"], 718)

    def tearDown(self):
        """
        Logout and Delete the user after each test
        """
        self.client.logout()
        self.user.delete()
