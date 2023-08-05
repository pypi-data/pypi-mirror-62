import textwrap
from io import StringIO
from unittest import TestCase

from htimeseries import HTimeseries

from haggregate import AggregateError, aggregate

tenmin_test_timeseries = textwrap.dedent(
    """\
            2008-02-07 09:40,10.32,
            2008-02-07 09:50,10.42,
            2008-02-07 10:00,10.51,
            2008-02-07 10:10,10.54,
            2008-02-07 10:20,10.71,
            2008-02-07 10:30,10.96,
            2008-02-07 10:40,10.93,
            2008-02-07 10:50,11.10,
            2008-02-07 11:00,11.23,
            2008-02-07 11:10,11.44,
            2008-02-07 11:20,11.41,
            2008-02-07 11:30,11.42,MISS
            2008-02-07 11:40,11.54,
            2008-02-07 11:50,11.68,
            2008-02-07 12:00,11.80,
            2008-02-07 12:10,11.91,
            2008-02-07 12:20,12.16,
            2008-02-07 12:30,12.16,
            2008-02-07 12:40,12.24,
            2008-02-07 12:50,12.13,
            2008-02-07 13:00,12.17,
            2008-02-07 13:10,12.31,
            """
)


tenmin_allmiss_test_timeseries = textwrap.dedent(
    """\
            2005-05-01 00:10,,
            2005-05-01 00:20,,
            2005-05-01 00:30,,
            2005-05-01 00:40,,
            2005-05-01 00:50,,
            2005-05-01 01:00,,
            2005-05-01 01:10,,
            2005-05-01 01:20,1,
            2005-05-01 01:30,,
            2005-05-01 01:40,1,
            2005-05-01 01:50,,
            2005-05-01 02:00,1,
            """
)


aggregated_hourly_allmiss = textwrap.dedent(
    """\
            2005-05-01 02:00,3,MISS\r
            """
)


class HourlySumTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "1H", "sum", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 31.25)
        self.assertEqual(self.result.data["flags"].loc["2008-02-07 10:00"], "MISS")

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 65.47)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 69.29)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 72.77)


class TimestampIrregularityTestCase(TestCase):
    def test_raises_exception(self):
        # In the time series below, it's 10:41 instead of 10:40
        ts = HTimeseries(
            StringIO(
                textwrap.dedent(
                    """\
                   2008-02-07 10:10,10.54,
                   2008-02-07 10:20,10.71,
                   2008-02-07 10:30,10.96,
                   2008-02-07 10:41,10.93,
                   2008-02-07 10:50,11.10,
                   2008-02-07 11:00,11.23,
                   """
                )
            )
        )
        with self.assertRaises(AggregateError):
            aggregate(ts, "1H", "sum")


class WrongTimeStepTestCase(TestCase):
    def test_raises_exception(self):
        msg = "The target step can currently only be 1H or 1D"
        with self.assertRaisesRegex(AggregateError, msg):
            aggregate(HTimeseries(), "5D", "sum")


class HourlySumWithLargerMinCountTestCase(TestCase):
    """Same as HourlySumTestCase but with slightly larger min_count.
    """

    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "1H", "sum", min_count=4, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 3)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 65.47)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 69.29)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 72.77)


class HourlyMeanTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "1H", "mean", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 10:00"].value, 10.4166667
        )

    def test_value_2(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 11:00"].value, 10.9116667
        )

    def test_value_3(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 12:00"].value, 11.5483333
        )

    def test_value_4(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 13:00"].value, 12.1283333
        )


class HourlyMeanWithOffsetTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(
            self.ts,
            "1H",
            "mean",
            min_count=3,
            missing_flag="MISS",
            target_timestamp_offset="1min",
        )

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 09:59"].value, 10.4166667
        )

    def test_value_2(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 10:59"].value, 10.9116667
        )

    def test_value_3(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 11:59"].value, 11.5483333
        )

    def test_value_4(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 12:59"].value, 12.1283333
        )


class HourlyMeanWithNegativeOffsetTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(
            self.ts,
            "1H",
            "mean",
            min_count=3,
            missing_flag="MISS",
            target_timestamp_offset="-1min",
        )

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 10:01"].value, 10.4166667
        )

    def test_value_2(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 11:01"].value, 10.9116667
        )

    def test_value_3(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 12:01"].value, 11.5483333
        )

    def test_value_4(self):
        self.assertAlmostEqual(
            self.result.data.loc["2008-02-07 13:01"].value, 12.1283333
        )


class HourlyMaxTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "1H", "max", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 10.51)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 11.23)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 11.8)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 12.24)


class HourlyMinTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.result = aggregate(self.ts, "1H", "min", min_count=3, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:00"].value, 10.32)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 10.54)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 12:00"].value, 11.41)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 13:00"].value, 11.91)


class AggregateEmptyTestCase(TestCase):
    def test_completely_empty(self):
        ts = HTimeseries()
        result = aggregate(ts, "1H", "sum", min_count=3, missing_flag="MISS")
        self.assertEqual(len(result.data), 0)

    def test_empty_result_from_nonempty_source(self):
        ts = HTimeseries(
            StringIO(
                textwrap.dedent(
                    """
                    2020-01-22 19:10,27,
                    2020-01-22 19:20,28,
                    2020-01-22 19:30,29,
                    """
                )
            )
        )
        result = aggregate(ts, "1H", "sum", min_count=4, missing_flag="MISS")
        self.assertEqual(len(result.data), 0)


class AllMissAggregateTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_allmiss_test_timeseries))
        self.result = aggregate(self.ts, "1H", "sum", min_count=1, missing_flag="MISS")

    def test_length(self):
        self.assertEqual(len(self.result.data), 1)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2005-05-01 02:00"].value, 3)


class SetsMetadataTestCase(TestCase):
    def setUp(self):
        self.ts = HTimeseries(StringIO(tenmin_test_timeseries))
        self.ts.title = "hello"
        self.ts.precision = 1
        self.ts.comment = "world"
        self.ts.timezone = "EET (+0200)"
        self.result = aggregate(self.ts, "1H", "sum", min_count=3, missing_flag="MISS")

    def test_sets_title(self):
        self.assertEqual(self.result.title, "Aggregated hello")

    def test_sets_precision(self):
        self.assertEqual(self.result.precision, 1)

    def test_sets_comment(self):
        self.assertEqual(
            self.result.comment,
            "Created by aggregating the time series that had this comment:\n\nworld",
        )

    def test_sets_time_step(self):
        self.assertEqual(self.result.time_step, "1H")

    def test_sets_timezone(self):
        self.assertEqual(self.result.timezone, "EET (+0200)")
