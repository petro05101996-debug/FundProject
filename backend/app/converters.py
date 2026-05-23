from __future__ import annotations
import dataclasses
from typing import Any
import math
import numpy as np
import pandas as pd

def dataframe_to_records(value: Any):
    if isinstance(value, pd.DataFrame):
        return value.to_dict(orient='records')
    return value

def records_to_dataframe(records: list[dict[str, Any]] | None) -> pd.DataFrame:
    df = pd.DataFrame(records or [])
    if "asset_class" in df.columns and "raw_asset_class" not in df.columns:
        df["raw_asset_class"] = df["asset_class"]
    return df

def result_to_jsonable(result: Any):
    if isinstance(result, pd.DataFrame):
        return result_to_jsonable(result.to_dict(orient='records'))
    if dataclasses.is_dataclass(result):
        return result_to_jsonable(dataclasses.asdict(result))
    if isinstance(result, dict):
        return {k: result_to_jsonable(v) for k, v in result.items()}
    if isinstance(result, list):
        return [result_to_jsonable(v) for v in result]
    if isinstance(result, tuple):
        return [result_to_jsonable(v) for v in result]
    if isinstance(result, (np.integer, np.floating)):
        result = result.item()
    if result is pd.NA:
        return None
    if isinstance(result, float):
        return result if math.isfinite(result) else None
    return result
