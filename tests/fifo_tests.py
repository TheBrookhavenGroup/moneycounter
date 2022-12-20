import unittest
from datetime import datetime
import pandas as pd
from src.pnl import fifo, realized_gains
from src.dt import our_localize


class FifoTests(unittest.TestCase):
    def setUp(self, a=None, t=None):
        df = pd.read_csv('trades.csv', parse_dates=['dt'])

        self.df = df

    def get_df(self, year, a=None, t=None):
        year = 2022
        dt = our_localize(datetime(year, 1, 1))
        eoy = our_localize(datetime(year, 12, 31, 23, 59, 59))
        # dt = pd.Timestamp(dt, tz='UTC')
        df = self.df
        if a is not None:
            df = df[df.a == a]
        if t is not None:
            df = df[df.t == t]

        df = df[df.dt <= eoy]
        return df, dt

    def test_fifo(self):
        year = 2022
        df, dt = self.get_df(year, a='ACCNT1', t='TICKER1')
        pnl = fifo(df, dt)
        self.assertAlmostEqual(pnl, 90)

    def test_realized(self):
        year = 2022
        df, _ = self.get_df(year)
        pnl = realized_gains(df, year)
        expected = pd.DataFrame({'a': ['ACCNT1', 'ACCNT2', 'ACCNT2'],
                                 't': ['TICKER1', 'TICKER1', 'TICKER2'],
                                 'realized': [90.0, 500.0, 105.0]})
        pd.testing.assert_frame_equal(pnl, expected)


if __name__ == '__main__':
    unittest.main()
