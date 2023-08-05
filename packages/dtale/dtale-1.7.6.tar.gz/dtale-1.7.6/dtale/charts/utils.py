import pandas as pd

from dtale.utils import (classify_type, find_dtype_formatter, get_dtypes,
                         grid_columns, grid_formatter, json_int, make_list)

YAXIS_CHARTS = ['line', 'bar', 'scatter']
ZAXIS_CHARTS = ['heatmap', '3d_scatter', 'surface']


def valid_chart(chart_type=None, x=None, y=None, z=None, **inputs):
    """
    Helper function to determine based on inputs (chart_type, x, y, z...) whether a chart can be build or not.
    For example, charts must have an x & y value and for 3-dimensional charts they must have a Z-Axis as well.

    :param chart_type: type of chart to build (line, bar, scatter, pie, heatmap, wordcloud, 3dscatter, surface)
    :type chart_type: str, optional
    :param x: column to use for the X-Axis
    :type x: str, optional
    :param y: columns to use for the Y-Axes
    :type y: list of str, optional
    :param z: column to use for the Z-Axis
    :type z: str, optional
    :param inputs: keyword arguments containing
    :return: `True` if executed from test, `False` otherwise
    :rtype: bool
    """
    if x is None or not len(y or []):
        return False

    if chart_type in ZAXIS_CHARTS and z is None:
        return False

    if inputs.get('agg') == 'rolling' and (inputs.get('window') is None or inputs.get('rolling_comp') is None):
        return False
    return True


def build_formatters(df):
    """
    Helper around :meth:`dtale.utils.grid_formatters` that will build a formatter for the data being fed into a chart as
    well as a formatter for the min/max values for each column used in the chart data.

    :param df: dataframe which contains column names and data types for formatters
    :type df: :class:`pandas:pandas.DataFrame`
    :return: json formatters for chart data and min/max values for each column used in the chart
    :rtype: (:class:`dtale.utils.JSONFormatter`, :class:`dtale.utils.JSONFormatter`)
    """
    cols = grid_columns(df)
    data_f = grid_formatter(cols, nan_display=None)
    overrides = {'F': lambda f, i, c: f.add_float(i, c, precision=2)}
    range_f = grid_formatter(cols, overrides=overrides, nan_display=None)
    return data_f, range_f


def date_freq_handler(df):
    """
    This returns a column definition handler which returns a series based on the specs from the front-end.
    Column definitions can be a column name 'Col1' or a column name with a frequency 'Col1|M' for
    columns which are of type datetime.

    :Example:
        Col1 -> returns series for Col1
        Col1|M -> returns series for Col1 in monthly format with name 'Col1|M'

    :param df: dataframe whose data needs to be checked
    :type df: :class:`pandas:pandas.DataFrame`
    :return: handler function
    :rtype: func
    """
    dtypes = get_dtypes(df)
    orig_idx = df.index

    def _handler(col_def):
        col_def_segs = col_def.split('|')
        if len(col_def_segs) > 1 and classify_type(dtypes[col_def_segs[0]]) == 'D':
            col, freq = col_def_segs
            if freq == 'WD':
                freq_grp = df.set_index(col).index.dayofweek.values
            elif freq == 'H2':
                freq_grp = df.set_index(col).index.hour.values
            else:
                freq_grp = df.set_index(col).index.to_period(freq).to_timestamp(how='end').values
            freq_grp = pd.Series(freq_grp, index=orig_idx, name=col_def)
            return freq_grp
        return df[col_def]
    return _handler


def retrieve_chart_data(df, x, y, z, group=None):
    """
    Retrieves data from a dataframe for x, y, z & group inputs complete with date frequency
    formatting (:meth:`dtale.charts.utils.date_freq_handler`) if specified

    :param df: dataframe that contains data for chart
    :type df: :class:`pandas:pandas.DataFrame`
    :param x: column to use for the X-Axis
    :type x: str
    :param y: columns to use for the Y-Axes
    :type y: list of str
    :param z: column to use for the Z-Axis
    :type z: str
    :param group: column(s) to use for grouping
    :type group: list of str or str
    :return: dataframe of data required for chart constructiuon
    :rtype: :class:`pandas:pandas.DataFrame`
    """
    freq_handler = date_freq_handler(df)
    cols = [x] + make_list(y) + [z] + make_list(group)
    return pd.concat([freq_handler(c) for c in cols if c is not None], axis=1)


def check_all_nan(df, cols=None):
    """
    Checker function to test whether all data within a column of a dataframe is :attr:`numpy:numpy.nan`

    :param df: dataframe whose data needs to be checked
    :type df: :class:`pandas:pandas.DataFrame`
    :param cols: columns to test
    :type cols: list of str
    :raises Exception: if all data within a column is :attr:`numpy:numpy.nan`
    """
    for col in cols or df.columns:
        if df[col].isnull().all():
            raise Exception('All data for column "{}" is NaN!'.format(col))


LIMIT_MSG = 'Dataset exceeds {} records, cannot render. Please apply filter...'


def check_exceptions(df, allow_duplicates, data_limit=15000, limit_msg=LIMIT_MSG):
    """
    Checker function to test the output of any chart aggregations to see if it is one of the following:
        - too large to be rendered by web client
        - contains duplicate data points which can't be rendered (ex: multiple points for a single point on the x-axis
          of a bar chart within the same series)

    :param df: dataframe whose data needs to be checked
    :type df: :class:`pandas:pandas.DataFrame`
    :param allow_duplicates: flag to allow duplicates to be ignored (usually for scatter plots)
    :type allow_duplicates: bool
    :param data_limit: maximum rows allowed for chart rendering (default: 15,000)
    :type data_limit: int, optional
    :param limit_msg: error message template
    :type limit_msg: str, optional
    :raises Exception: if any failure condition is met
    """
    if not allow_duplicates and any(df.duplicated()):
        raise Exception(
            '{} contains duplicates, please specify group or additional filtering'.format(', '.join(df.columns)))
    if len(df) > data_limit:
        raise Exception(limit_msg.format(data_limit))


def build_agg_data(df, x, y, inputs, agg, z=None):
    """
    Builds aggregated data when an aggregation (sum, mean, max, min...) is selected from the front-end.

    :param df: dataframe that contains data for chart
    :type df: :class:`pandas:pandas.DataFrame`
    :param x: column to use for the X-Axis
    :type x: str
    :param y: columns to use for the Y-Axes
    :type y: list of str
    :param inputs: additional chart configurations (chart_type, group, rolling_win, rolling_comp...)
    :type inputs: dict
    :param agg: points to a specific function that can be applied to
                :func: pandas.core.groupby.DataFrameGroupBy.  Possible values are: count, first, last mean,
                median, min, max, std, var, mad, prod, sum
    :type agg: str
    :param z: column to use for the Z-Axis
    :type z: str, optional
    :return: dataframe of aggregated data
    :rtype: :class:`pandas:pandas.DataFrame`
    """

    z_exists = len(make_list(z))
    if agg == 'corr':
        if not z_exists:
            raise NotImplementedError('Correlation aggregation is only available for 3-dimensional charts!')
    if agg == 'rolling':
        if z_exists:
            raise NotImplementedError('Rolling computations have not been implemented for 3-dimensional charts!')
        window, comp = map(inputs.get, ['rolling_win', 'rolling_comp'])
        agg_df = df.set_index(x).rolling(window=window)
        agg_df = pd.DataFrame({c: getattr(agg_df[c], comp)() for c in y})
        return agg_df.reset_index()

    if z_exists:
        groups = df.groupby([x] + make_list(y))
        return getattr(groups[make_list(z)], agg)().reset_index()
    groups = df.groupby(x)
    return getattr(groups[y], agg)().reset_index()


def build_chart(raw_data, x, y, group_col=None, agg=None, allow_duplicates=False, **kwargs):
    """
    Helper function to return data for 'chart-data' & 'correlations-ts' endpoints.  Will return a dictionary of
    dictionaries (one for each series) which contain the data for the x & y axes of the chart as well as the minimum &
    maximum of all the series for the y-axis.  If there is only one series (no group_col specified) the only key in the
    dictionary of series data will be 'all' otherwise the keys will be the values of the groups.

    :param raw_data: dataframe to be used for chart
    :type raw_data: :class:`pandas:pandas.DataFrame`
    :param x: column to be used as x-axis of chart
    :type x: str
    :param y: column to be used as y-axis of chart
    :type y: list of strings
    :param group: comma-separated string of columns to group chart data by
    :type group: str, optional
    :param agg: points to a specific function that can be applied to
                        :func: pandas.core.groupby.DataFrameGroupBy.  Possible values are: count, first, last mean,
                        median, min, max, std, var, mad, prod, sum
    :type agg: str, optional
    :param allow_duplicates: flag to allow duplicates to be ignored (usually for scatter plots)
    :type allow_duplicates: bool, optional
    :return: dict
    """

    data = retrieve_chart_data(raw_data, x, y, kwargs.get('z'), group_col)
    x_col = str('x')
    y_cols = make_list(y)
    z_col = kwargs.get('z')
    z_cols = []
    if z_col is not None:
        z_cols = [z_col]
    if group_col is not None and len(group_col):
        data = data.sort_values(group_col + [x])
        check_all_nan(data, [x] + y_cols)
        data = data.rename(columns={x: x_col})
        if agg is not None:
            data = data.groupby(group_col + [x_col])
            data = getattr(data, agg)().reset_index()
        max_groups = 15
        if len(data[group_col].drop_duplicates()) > max_groups:
            msg = (
                'Group ({}) contains more than {} unique values, please add additional filter'
                ' or else chart will be unreadable'
            ).format(', '.join(group_col), max_groups)
            raise Exception(msg)

        data = data.dropna()
        data_f, range_f = build_formatters(data)
        ret_data = dict(
            data={},
            min={col: fmt(data[col].min(), None) for _, col, fmt in range_f.fmts if col in [x_col] + y_cols},
            max={col: fmt(data[col].max(), None) for _, col, fmt in range_f.fmts if col in [x_col] + y_cols},
        )

        dtypes = get_dtypes(data)
        group_fmt_overrides = {'I': lambda v, as_string: json_int(v, as_string=as_string, fmt='{}')}
        group_fmts = {c: find_dtype_formatter(dtypes[c], overrides=group_fmt_overrides) for c in group_col}
        for group_val, grp in data.groupby(group_col):
            group_val = '/'.join([
                group_fmts[gc](gv, as_string=True) for gv, gc in zip(make_list(group_val), group_col)
            ])
            ret_data['data'][group_val] = data_f.format_lists(grp)
        ret_data['dtypes'] = {c: classify_type(dtype) for c, dtype in dtypes.items()}
        return ret_data
    sort_cols = [x] + (y_cols if len(z_cols) else [])
    data = data.sort_values(sort_cols)
    check_all_nan(data, [x] + y_cols + z_cols)
    y_cols = [str(y_col) for y_col in y_cols]
    data.columns = [x_col] + y_cols + z_cols
    if agg is not None:
        data = build_agg_data(data, x_col, y_cols, kwargs, agg, z=z_col)
    data = data.dropna()

    dupe_cols = [x_col] + (y_cols if len(z_cols) else [])
    check_exceptions(data[dupe_cols].rename(columns={'x': x}), allow_duplicates,
                     data_limit=40000 if len(z_cols) else 15000)
    data_f, range_f = build_formatters(data)
    ret_data = dict(
        data={str('all'): data_f.format_lists(data)},
        min={col: fmt(data[col].min(), None) for _, col, fmt in range_f.fmts if col in [x_col] + y_cols + z_cols},
        max={col: fmt(data[col].max(), None) for _, col, fmt in range_f.fmts if col in [x_col] + y_cols + z_cols}
    )
    return ret_data


WEEKDAY_MAP = {idx: day for idx, day in enumerate(['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])}


def weekday_tick_handler(col_data, col):
    """
    Output handler for datetime data which needs to be returned as weekdays.  If the column definition ends with '|WD'
    then the integer values in 'data' will be mapped to their standard weekday test (Mon, Tues, Wed, Thur, Fri, Sat,
    Sun)

    :param col_data: iterable of values within column
    :type col_data: list
    :param col: column definition
    :type col: str
    :return: formatted column data
    :rtype: list
    """
    if col.endswith('|WD'):
        return [WEEKDAY_MAP[d] for d in col_data]
    return col_data
