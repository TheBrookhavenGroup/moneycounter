
from test_base import TradesBaseTest
from src.moneycounter.pnl import pnl, separate_trades, wap_calc


class PnLTests(TradesBaseTest):

    def _assert_lists_almost_equal(self, a, b):
        self.assertEqual(len(a), len(b))
        for x, y in zip(a, b):
            self.assertAlmostEqual(x, y)

    def test_pnl(self):
        year = 2023
        price = 305
        for a, t, expected_total, expected_realized in [['ACCNT1', 'TICKER4', 460, 10],
                                                        ['ACCNT1', 'TICKER1', 650, 700],
                                                        ['ACCNT2', 'TICKER1', 800, 800],
                                                        ['ACCNT2', 'TICKER2', 185, 207],
                                                        ['ACCNT1', 'TICKER3', -187, -199],
                                                        ['ACCNT1', 'TICKER5', -330.0, -330.0]]:

            expected_unrealized = expected_total - expected_realized
            df, dt = self.get_df(year, a=a, t=t)
            realized, unrealized, total = pnl(df, price=price)

    def test_divide_trades(self):

        expected = [['CASE1', [4, 2, 1], [2, -2, 6, -5, -1]],
                    ['CASE2', [2], []],
                    ['CASE3', [-10, -1, -2], [10, -5, -10, 5]],
                    ['CASE4', [-3, -1], [10, -5, -11, -4, -2, 12]],
                    ['CASE5', [3, 1], [-10, 5, 11, 4, 2, -12]]]

        for case, expected_unrealized_q, expected_realized_q in expected:
            df, _ = self.get_df(a='ACCNT5', t=case)
            realized_df, unrealized_df = separate_trades(df)
            realized_df_q = list(realized_df.q)
            unrealized_df_q = list(unrealized_df.q)
            try:
                self._assert_lists_almost_equal(realized_df_q, expected_realized_q)
            except AssertionError:
                raise AssertionError(f"AssertionError {case} {realized_df_q} not equal to {expected_realized_q}")

            try:
                self._assert_lists_almost_equal(unrealized_df_q, expected_unrealized_q)
            except AssertionError:
                raise AssertionError(f"AssertionError {unrealized_df_q} not equal to {expected_unrealized_q}")

    def test_wap(self):

        for a, t in (('ACCNT1', 'TICKER1'),
                     ('ACCNT1', 'TICKER3'),
                     ('ACCNT1', 'TICKER4'),
                     ('ACCNT1', 'TICKER5'),
                     ('ACCNT2', 'TICKER1'),
                     ('ACCNT2', 'TICKER2'),
                     ('ACCNT3', 'TICKER6'),
                     ('ACCNT4', 'TICKER6')):

            df, _ = self.get_df(a=a, t=t)

            position = df.q.sum()

            _, pl_expected, _ = pnl(df, 1.0)

            wap = wap_calc(df)

            pl_calculated = position * (1.0 - wap)

            self.assertAlmostEqual(pl_expected, pl_calculated)
