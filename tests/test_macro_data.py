import unittest

import pandas as pd

from utils.data import load_macro_kpi_data


class MacroDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards, cls.trends = load_macro_kpi_data()

    def test_monthly_card_uses_latest_trend_observation(self):
        self.assertEqual(
            set(self.trends["indicator"]),
            {"CPI inflation", "Unemployment rate", "WTI crude oil"},
        )
        for indicator, series in self.trends.groupby("indicator"):
            latest = series.loc[series["period"].idxmax()]
            card = self.cards.loc[self.cards["indicator"] == indicator].iloc[0]
            self.assertEqual(card["value"], latest["value"])
            self.assertEqual(card["period"], pd.Timestamp(latest["period"]).strftime("%b %Y"))

    def test_oil_price_and_sources(self):
        oil = self.cards.loc[self.cards["indicator"] == "WTI crude oil"].iloc[0]
        self.assertEqual(oil["value"], 97.31)
        self.assertEqual(oil["unit"], "USD/bbl")
        self.assertTrue(self.cards["source_url"].str.startswith("https://").all())

    def test_flat_policy_rate_and_qoq_abbreviation_are_absent(self):
        self.assertFalse(self.cards["indicator"].str.contains("policy rate", case=False).any())
        self.assertFalse(self.trends["indicator"].str.contains("policy rate", case=False).any())
        self.assertFalse(self.cards["unit"].str.contains("q/q", case=False).any())


if __name__ == "__main__":
    unittest.main()
