import re
import pandas as pd
import random
import string


def normalize_column(column):
    return re.sub(r"[^a-zA-Z0-9_]", "", column).lower()


def get_random_string(length):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def transform_df(df, categorical_columns, numeric_columns, scaler, one_hot_encoder):
    df = df.rename(columns={column: normalize_column(column) for column in df.columns})

    one_hot_as_df = None
    scaled_features_as_df = None

    if one_hot_encoder:
        transformed = one_hot_encoder.transform(df[categorical_columns]).toarray()
        one_hot_as_df = pd.DataFrame(transformed, columns=one_hot_encoder.get_feature_names_out())

    if scaler:
        scaled_features = scaler.transform(df[numeric_columns])
        scaled_features_as_df = pd.DataFrame(scaled_features, columns=scaler.get_feature_names_out())

    df = df.drop(columns=categorical_columns + numeric_columns).reset_index(drop=True)

    df = df[sorted(df.columns)]
    return pd.concat([df, one_hot_as_df, scaled_features_as_df], axis=1)
