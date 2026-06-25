import unittest

import pandas as pd

from utils.visualization import outlier_box_plot


class VisualizationTests(unittest.TestCase):
    def test_outlier_box_plot_renders(self):
        df = pd.DataFrame({"Sales Count": [1, 2, 3, 100]})

        fig = outlier_box_plot(df, "Sales Count", "Sales Outliers")

        self.assertIsNotNone(fig)
        self.assertGreaterEqual(len(fig.data), 1)


if __name__ == "__main__":
    unittest.main()
