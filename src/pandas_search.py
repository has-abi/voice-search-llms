from pandas import DataFrame

from src.search_query import SearchQuery


class PandasSearch:
    def __init__(self, df: DataFrame):
        self.df = df

    def search(self, search_query: SearchQuery) -> DataFrame:
        filtered_df = self.df.copy()
        if search_query.localisation:
            filtered_df = self._filter_by_value(filtered_df, "location", search_query.localisation)
        if search_query.niveau_etudes:
            filtered_df = self._filter_by_value(filtered_df, "level_of_study", search_query.niveau_etudes)
        if search_query.experience:
            range_values = [search_query.experience.min, search_query.experience.max]
            filtered_df = self._filter_by_range(filtered_df, "experience_in_years", range_values)
        if search_query.competences:
            filtered_df = self._filter_by_list(filtered_df, "skills", search_query.competences)
        if search_query.langues_parlees:
            filtered_df = self._filter_by_list(filtered_df, "spoken_languages", search_query.langues_parlees)
        return filtered_df

    @staticmethod
    def _filter_by_value(df: DataFrame, column: str, value: str | int | float) -> DataFrame:
        return df[df[column].apply(lambda val: str(val).lower() == str(value).lower())]

    @staticmethod
    def _filter_by_list(df: DataFrame, column: str, items: list[any]) -> DataFrame:
        if items:
            return df[df[column].apply(lambda x: bool(set(items) <= set(x)))]
        return df

    @staticmethod
    def _filter_by_range(df: DataFrame, column: str, range_values: list[int]) -> DataFrame:
        if not range_values:
            raise ValueError("range_values should not be None or empty")
        if len(range_values) != 2:
            raise ValueError("range_values should contain 2 values a min and a max")

        min_value, max_value = range_values
        if min_value is None and max_value is None:
            return df

        if min_value is None:
            return df[df[column].apply(lambda val: val <= max_value)]
        elif max_value is None:
            return df[df[column].apply(lambda val: val >= min_value)]
        else:
            return df[df[column].apply(lambda val: (min_value <= val <= max_value))]
