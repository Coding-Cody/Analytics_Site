import unittest

from utils.data import load_inflation_energy_data, load_macro_kpi_data


class MacroSourceDataTests(unittest.TestCase):
    def test_monthly_signal_series_keep_their_reference_months(self):
        _, trends = load_macro_kpi_data()
        groups = {name: rows for name, rows in trends.groupby("indicator")}

        self.assertEqual(
            set(groups),
            {"Canada CPI inflation", "Canada unemployment", "Bank of Canada policy rate"},
        )
        self.assertEqual(groups["Canada CPI inflation"]["period"].max(), "2026-08")
        self.assertEqual(groups["Canada unemployment"]["period"].max(), "2026-09")
        self.assertEqual(groups["Bank of Canada policy rate"]["period"].max(), "2026-09")
        self.assertEqual(set(groups["Bank of Canada policy rate"]["value"]), {2.25})

    def test_cpi_detail_matches_headline_card(self):
        cards, _ = load_macro_kpi_data()
        cpi, _ = load_inflation_energy_data()
        headline = cards.loc[cards["indicator"].eq("CPI inflation")].iloc[0]
        all_items = cpi.loc[cpi["measure"].eq("All-items CPI")].iloc[0]

        self.assertEqual(all_items["value"], headline["value"])
        self.assertEqual(all_items["period"], headline["period"])
        self.assertEqual(all_items["source_url"], headline["source_url"])
        self.assertEqual(set(cpi["unit"]), {"12-month % change"})

    def test_wti_is_dated_weekly_price_series(self):
        _, wti = load_inflation_energy_data()

        self.assertEqual(len(wti), 15)
        self.assertTrue(wti["week_end"].is_monotonic_increasing)
        self.assertTrue(wti["week_end"].is_unique)
        self.assertEqual(wti.iloc[-1]["week_end"], "2026-10-09")
        self.assertEqual(wti.iloc[-1]["value"], 96.88)
        self.assertEqual(set(wti["unit"]), {"USD per barrel"})
        self.assertTrue(wti["source_url"].str.startswith("https://www.eia.gov/").all())


if __name__ == "__main__":
    unittest.main()
