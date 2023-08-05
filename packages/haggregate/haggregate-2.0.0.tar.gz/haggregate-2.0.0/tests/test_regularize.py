import textwrap
from io import StringIO
from unittest import TestCase

import numpy as np
from htimeseries import HTimeseries

from haggregate import RegularizeError, regularize


class BadTimeStepTestCase(TestCase):
    def test_unspecified_time_step(self):
        ts = HTimeseries()
        msg = "The source time series does not specify a time step"
        with self.assertRaisesRegex(RegularizeError, msg):
            regularize(ts)

    def test_malformed_time_step(self):
        ts = HTimeseries()
        ts.time_step = "hello"
        msg = (
            "The time step is malformed or is specified in months. Only time steps "
            "specified in minutes, hours or days are supported."
        )
        with self.assertRaisesRegex(RegularizeError, msg):
            regularize(ts)

    def test_malformed_time_step2(self):
        ts = HTimeseries()
        ts.time_step = "5M"
        msg = (
            "The time step is malformed or is specified in months. Only time steps "
            "specified in minutes, hours or days are supported."
        )
        with self.assertRaisesRegex(RegularizeError, msg):
            regularize(ts)


class RegularizeTestCase(TestCase):
    def setUp(self):
        input = textwrap.dedent(
            """\
            2008-02-07 10:30,10.71,FLAG1
            2008-02-07 10:41,10.93,FLAG2
            2008-02-07 10:50,11.10,
            """
        )
        ts = HTimeseries(StringIO(input))
        ts.time_step = "10min"
        self.result = regularize(ts)

    def test_length(self):
        self.assertEqual(len(self.result.data), 3)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:30"].value, 10.71)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:40"].value, 10.93)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:50"].value, 11.10)

    def test_flags_1(self):
        self.assertEqual(self.result.data.loc["2008-02-07 10:30"]["flags"], "FLAG1")

    def test_flags_2(self):
        self.assertEqual(
            self.result.data.loc["2008-02-07 10:40"]["flags"], "FLAG2 DATEINSERT"
        )

    def test_flags_3(self):
        self.assertEqual(self.result.data.loc["2008-02-07 10:50"]["flags"], "")


class RegularizeFirstRecordTestCase(TestCase):
    def setUp(self):
        input = textwrap.dedent(
            """\
            2008-02-07 10:31,10.71,
            2008-02-07 10:40,10.93,
            2008-02-07 10:50,11.10,
            """
        )
        ts = HTimeseries(StringIO(input))
        ts.time_step = "10min"
        self.result = regularize(ts)

    def test_length(self):
        self.assertEqual(len(self.result.data), 3)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:30"].value, 10.71)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:40"].value, 10.93)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:50"].value, 11.10)


class RegularizeLastRecordTestCase(TestCase):
    def setUp(self):
        input = textwrap.dedent(
            """\
            2008-02-07 10:30,10.71,
            2008-02-07 10:40,10.93,
            2008-02-07 10:49,11.10,
            """
        )
        ts = HTimeseries(StringIO(input))
        ts.time_step = "10min"
        self.result = regularize(ts)

    def test_length(self):
        self.assertEqual(len(self.result.data), 3)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:30"].value, 10.71)

    def test_value_2(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:40"].value, 10.93)

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:50"].value, 11.10)


class RegularizeNullRecordTestCase(TestCase):
    def setUp(self):
        input = textwrap.dedent(
            """\
            2008-02-07 10:30,10.71,
            2008-02-07 10:51,11.10,
            2008-02-07 11:00,10.93,
            """
        )
        ts = HTimeseries(StringIO(input))
        ts.time_step = "10min"
        self.result = regularize(ts)

    def test_length(self):
        self.assertEqual(len(self.result.data), 4)

    def test_value_1(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:30"].value, 10.71)

    def test_value_2(self):
        self.assertTrue(np.isnan(self.result.data.loc["2008-02-07 10:40"].value))

    def test_value_3(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 10:50"].value, 11.10)

    def test_value_4(self):
        self.assertAlmostEqual(self.result.data.loc["2008-02-07 11:00"].value, 10.93)


class RegularizeEmptyTestCase(TestCase):
    def setUp(self):
        ts = HTimeseries()
        ts.time_step = "10min"
        self.result = regularize(ts)

    def test_length(self):
        self.assertEqual(len(self.result.data), 0)


class SetsMetadataTestCase(TestCase):
    def setUp(self):
        input = textwrap.dedent(
            """\
            2008-02-07 10:30,10.71,FLAG1
            2008-02-07 10:41,10.93,FLAG2
            2008-02-07 10:50,11.10,
            """
        )
        self.ts = HTimeseries(StringIO(input))
        self.ts.time_step = "10min"
        self.ts.title = "hello"
        self.ts.precision = 1
        self.ts.comment = "world"
        self.ts.timezone = "EET (+0200)"
        self.result = regularize(self.ts)

    def test_sets_title(self):
        self.assertEqual(self.result.title, "Regularized hello")

    def test_sets_precision(self):
        self.assertEqual(self.result.precision, 1)

    def test_sets_comment(self):
        self.assertEqual(
            self.result.comment,
            "Created by regularizing step of timeseries "
            "that had this comment:\n\nworld",
        )

    def test_sets_time_step(self):
        self.assertEqual(self.result.time_step, "10min")

    def test_sets_timezone(self):
        self.assertEqual(self.result.timezone, "EET (+0200)")
