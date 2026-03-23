import pandas as pd
import numpy as np

class GroupEstimate:
    
    def __init__(self, estimate="mean"):
        if estimate not in ["mean", "median"]:
            raise ValueError("estimate must be 'mean' or 'median'")
        
        self.estimate = estimate
        self.group_values = None
        self.columns = None

    def fit(self, X, y):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        self.columns = X.columns

        df = X.copy()
        df["target"] = y

        if self.estimate == "mean":
            grouped = df.groupby(list(self.columns))["target"].mean()
        else:
            grouped = df.groupby(list(self.columns))["target"].median()

        self.group_values = grouped

    def predict(self, X_):
        if not isinstance(X_, pd.DataFrame):
            X_ = pd.DataFrame(X_, columns=self.columns)

        results = []
        missing_count = 0
    for _, row in X_.iterrows():
        key = tuple(row[col] for col in self.columns)

    if key in self.group_values.index:
        results.append(self.group_values.loc[key])
    else:
        results.append(np.nan)
        missing_count += 1

        if missing_count > 0:
            print(f"{missing_count} missing group(s) encountered.")

        return np.array(results)
