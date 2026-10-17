import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "placement_predict_50k Dataset.csv"
)


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    return pd.read_csv(DATA_PATH)


def get_data_summary():

    df = load_data()

    missing_counts = df.isna().sum()

    missing_details = []

    for column in df.columns:

        missing = int(missing_counts[column])

        if missing > 0:

            percentage = round(
                (missing / len(df)) * 100,
                2
            )

            missing_details.append({
                "column": column,
                "missing": missing,
                "percentage": percentage
            })

    return {
        "n_rows": int(df.shape[0]),

        "n_cols": int(df.shape[1]),

        "columns": list(df.columns),

        "dtypes": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },

        "missing_counts": {
            column: int(missing_counts[column])
            for column in df.columns
        },

        "total_missing": int(
            df.isna().sum().sum()
        ),

        "missing_columns": len(
            missing_details
        ),

        "missing_details": missing_details,

        "duplicate_count": int(
            df.duplicated().sum()
        ),

        "preview": df.head(10).fillna(
            "-"
        ).to_dict(
            orient="records"
        )
    }


def get_processing_summary():

    df = load_data()

    rows_before = int(df.shape[0])

    columns_before = int(df.shape[1])

    missing_before = int(
        df.isna().sum().sum()
    )

    duplicates_before = int(
        df.duplicated().sum()
    )


    # ---------------------------------------
    # Missing value details
    # ---------------------------------------

    missing_details = []

    for column in df.columns:

        missing = int(
            df[column].isna().sum()
        )

        if missing > 0:

            percentage = round(
                (missing / len(df)) * 100,
                2
            )

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):
                method = "Median"

            else:
                method = "Mode"

            missing_details.append({

                "column": column,

                "missing": missing,

                "percentage": percentage,

                "method": method,

                "status": "Will be handled"

            })


    # ---------------------------------------
    # Create processed copy
    # ---------------------------------------

    processed = df.copy()


    # Numeric columns
    numeric_columns = processed.select_dtypes(
        include="number"
    ).columns


    for column in numeric_columns:

        if processed[column].isna().any():

            median_value = processed[
                column
            ].median()

            processed[column] = processed[
                column
            ].fillna(
                median_value
            )


    # Categorical columns
    categorical_columns = processed.select_dtypes(
        exclude="number"
    ).columns


    for column in categorical_columns:

        if processed[column].isna().any():

            mode_value = processed[
                column
            ].mode()

            if not mode_value.empty:

                processed[column] = processed[
                    column
                ].fillna(
                    mode_value.iloc[0]
                )


    # ---------------------------------------
    # Remove duplicates
    # ---------------------------------------

    processed = processed.drop_duplicates()


    # ---------------------------------------
    # After processing
    # ---------------------------------------

    missing_after = int(
        processed.isna().sum().sum()
    )

    duplicates_after = int(
        processed.duplicated().sum()
    )

    rows_after = int(
        processed.shape[0]
    )

    columns_after = int(
        processed.shape[1]
    )


    return {

        "missing_before":
            missing_before,

        "missing_after":
            missing_after,

        "missing_columns":
            len(missing_details),

        "missing_details":
            missing_details,

        "duplicates_before":
            duplicates_before,

        "duplicates_after":
            duplicates_after,

        "rows_before":
            rows_before,

        "rows_after":
            rows_after,

        "columns_before":
            columns_before,

        "columns_after":
            columns_after

    }


def get_analysis_summary():

    df = load_data()


    total_students = len(df)


    placed = int(
        (df["PlacementStatus"] == 1).sum()
    )


    not_placed = int(
        (df["PlacementStatus"] == 0).sum()
    )


    placement_rate = round(
        (placed / total_students) * 100,
        2
    )


    average_cgpa = round(
        df["CGPA"].mean(),
        2
    )


    average_attendance = round(
        df["AttendancePercent"].mean(),
        2
    )


    average_coding = round(
        df["CodingTestScore"].mean(),
        2
    )


    average_aptitude = round(
        df["AptitudeTestScore"].mean(),
        2
    )


    average_soft_skills = round(
        df["SoftSkillsRating"].mean(),
        2
    )


    placed_students = df[
        df["PlacementStatus"] == 1
    ]


    average_salary = round(
        placed_students["Salary Package"].mean(),
        2
    )


    return {

        "total_students":
            total_students,

        "placed":
            placed,

        "not_placed":
            not_placed,

        "placement_rate":
            placement_rate,

        "average_cgpa":
            average_cgpa,

        "average_attendance":
            average_attendance,

        "average_coding":
            average_coding,

        "average_aptitude":
            average_aptitude,

        "average_soft_skills":
            average_soft_skills,

        "average_salary":
            average_salary
    }


def get_dashboard_summary():

    data = get_data_summary()

    analysis = get_analysis_summary()

    return {

        "students":
            data["n_rows"],

        "features":
            data["n_cols"],

        "missing":
            data["total_missing"],

        "duplicates":
            data["duplicate_count"],

        "placement_rate":
            analysis["placement_rate"]

    }


def get_preview():

    df = load_data()

    return df.head(10).fillna(
        "-"
    ).to_dict(
        orient="records"
    )