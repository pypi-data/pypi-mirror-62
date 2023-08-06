import uuid
import time

from geopandas import GeoDataFrame
from collections import defaultdict

from ..catalog.variable import Variable
from ..catalog.dataset import Dataset
from ..catalog.geography import Geography
from ...clients import bigquery_client
from ....auth import get_default_credentials
from ....exceptions import EnrichmentError
from ....utils.logger import log
from ....utils.geom_utils import to_geojson, set_geometry, has_geometry
from ....utils.utils import timelogger


_ENRICHMENT_ID = 'enrichment_id'
_GEOM_COLUMN = '__geojson_geom'

AGGREGATION_DEFAULT = 'default'
AGGREGATION_NONE = None

MAX_VARIABLES_NUMBER = 50


class EnrichmentService(object):
    """Base class for the Enrichment utility with commons auxiliary methods"""

    def __init__(self, credentials=None):
        self.credentials = credentials = credentials or get_default_credentials()
        self.bq_client = bigquery_client.BigQueryClient(credentials)
        self.bq_dataset = self.bq_client.bq_dataset
        self.bq_project = self.bq_client.bq_project
        self.bq_public_project = self.bq_client.bq_public_project

    @timelogger
    def _execute_enrichment(self, queries, geodataframe):

        dfs_enriched = list()
        awaiting_jobs = set()
        errors = list()

        def callback(job):
            if not job.errors:
                dfs_enriched.append(self.bq_client.download_to_dataframe(job))
            else:
                errors.extend(job.errors)

            awaiting_jobs.discard(job.job_id)

        for query in queries:
            job = self.bq_client.query(query)
            awaiting_jobs.add(job.job_id)
            job.add_done_callback(callback)

        while awaiting_jobs:
            time.sleep(0.5)

        if len(errors) > 0:
            raise EnrichmentError(errors)

        for df in dfs_enriched:
            geodataframe = geodataframe.merge(df, on=_ENRICHMENT_ID, how='left')

        # Remove extra columns
        geodataframe.drop(_ENRICHMENT_ID, axis=1, inplace=True)
        geodataframe.drop(_GEOM_COLUMN, axis=1, inplace=True)

        return geodataframe

    @timelogger
    def _prepare_data(self, dataframe, geom_col):
        geodataframe = GeoDataFrame(dataframe, copy=True)

        if geom_col in geodataframe:
            set_geometry(geodataframe, geom_col, inplace=True)
        elif has_geometry(dataframe):
            geodataframe.set_geometry(dataframe.geometry.name, inplace=True)
        else:
            raise ValueError('No valid geometry found. Please provide an input source with ' +
                             'a valid geometry or specify the "geom_col" param with a geometry column.')

        # Add extra columns for the enrichment
        geodataframe[_ENRICHMENT_ID] = range(geodataframe.shape[0])
        geodataframe[_GEOM_COLUMN] = geodataframe.geometry.apply(to_geojson)

        return geodataframe

    def _get_temp_table_name(self):
        id_tablename = uuid.uuid4().hex
        return 'temp_{id}'.format(id=id_tablename)

    def _upload_data(self, tablename, geodataframe):
        bq_dataframe = geodataframe[[_ENRICHMENT_ID, _GEOM_COLUMN]]
        schema = {_ENRICHMENT_ID: 'INTEGER', _GEOM_COLUMN: 'GEOGRAPHY'}

        self.bq_client.upload_dataframe(
            dataframe=bq_dataframe,
            schema=schema,
            tablename=tablename
        )

    def _get_tables_metadata(self, variables, filters):
        tables_metadata = defaultdict(lambda: defaultdict(list))

        for variable in variables:
            table_name = self.__get_enrichment_table_by_variable(variable)
            tables_metadata[table_name]['variables'].append(variable)

            variable_filters = _build_where_conditions_by_variable(variable, filters)
            if variable_filters:
                tables_metadata[table_name]['filters'] = variable_filters

            if 'geo_table' not in tables_metadata[table_name].keys():
                tables_metadata[table_name]['geo_table'] = self.__get_geo_table(variable)

            if 'project' not in tables_metadata[table_name].keys():
                tables_metadata[table_name]['project'] = self.__get_project(variable)

        return tables_metadata

    def __get_enrichment_table_by_variable(self, variable):
        if variable.project_name != self.bq_public_project:
            table = 'view_{dataset}_{table}'.format(
                dataset=variable.schema_name,
                table=variable.dataset_name
            )

            return '{project}.{dataset}.{table}'.format(
                project=self.bq_project,
                dataset=self.bq_dataset,
                table=table
            )
        else:
            return variable.dataset

    def __get_geo_table(self, variable):
        geography_id = Dataset.get(variable.dataset).geography
        geography = Geography.get(geography_id)
        _, dataset_geo_table, geo_table = geography_id.split('.')

        if not geography.is_public_data:
            return '{project}.{dataset}.view_{dataset_geo_table}_{geo_table}'.format(
                project=self.bq_project,
                dataset=self.bq_dataset,
                dataset_geo_table=dataset_geo_table,
                geo_table=geo_table
            )
        else:
            return '{project}.{dataset}.{geo_table}'.format(
                project=self.bq_public_project,
                dataset=dataset_geo_table,
                geo_table=geo_table
            )

    def __get_project(self, variable):
        project = self.bq_public_project

        if variable.project_name != self.bq_public_project:
            project = self.bq_project

        return project

    def _get_points_enrichment_sql(self, temp_table_name, variables, filters):
        tables_metadata = self._get_tables_metadata(variables, filters).items()

        return [self._build_points_query(metadata, enrichment_table, temp_table_name)
                for enrichment_table, metadata in tables_metadata]

    def _build_points_query(self, metadata, enrichment_table, temp_table_name):
        variables = ['enrichment_table.{}'.format(variable.column_name) for variable in metadata['variables']]
        filters = metadata['filters']
        enrichment_geo_table = metadata['geo_table']
        data_table = '{project}.{user_dataset}.{temp_table_name}'.format(
            project=self.bq_project,
            user_dataset=self.bq_dataset,
            temp_table_name=temp_table_name
        )

        return '''
            SELECT data_table.{enrichment_id}, {variables},
                ST_AREA(enrichment_geo_table.geom) AS do_area
            FROM `{enrichment_table}` enrichment_table
                JOIN `{enrichment_geo_table}` enrichment_geo_table
                    ON enrichment_table.geoid = enrichment_geo_table.geoid
                JOIN `{data_table}` data_table
                    ON ST_Within(data_table.{geom_column}, enrichment_geo_table.geom)
            {where};
        '''.format(
            variables=', '.join(variables),
            geom_column=_GEOM_COLUMN,
            enrichment_table=enrichment_table,
            enrichment_geo_table=enrichment_geo_table,
            enrichment_id=_ENRICHMENT_ID,
            where=_build_where_clausule(filters),
            data_table=data_table
        )

    def _get_polygon_enrichment_sql(self, temp_table_name, variables, filters, aggregation):
        tables_metadata = self._get_tables_metadata(variables, filters).items()

        return [self._build_polygons_query(metadata, enrichment_table, temp_table_name, aggregation)
                for enrichment_table, metadata in tables_metadata]

    def _build_polygons_query(self, metadata, enrichment_table, temp_table_name, aggregation):
        variables = metadata['variables']
        filters = metadata['filters']
        enrichment_geo_table = metadata['geo_table']
        data_table = '{project}.{user_dataset}.{temp_table_name}'.format(
            project=self.bq_project,
            user_dataset=self.bq_dataset,
            temp_table_name=temp_table_name
        )

        if aggregation == AGGREGATION_NONE:
            grouper = ''
            columns = _build_polygons_query_variables_without_aggregation(variables)
        else:
            grouper = 'group by data_table.{enrichment_id}'.format(enrichment_id=_ENRICHMENT_ID)
            columns = _build_polygons_query_variables_with_aggregation(variables, aggregation)

        return '''
            SELECT data_table.{enrichment_id}, {columns}
            FROM `{enrichment_table}` enrichment_table
                JOIN `{enrichment_geo_table}` enrichment_geo_table
                    ON enrichment_table.geoid = enrichment_geo_table.geoid
                JOIN `{data_table}` data_table
                    ON ST_Intersects(data_table.{geom_column}, enrichment_geo_table.geom)
            {where}
            {grouper};
        '''.format(
            geom_column=_GEOM_COLUMN,
            enrichment_table=enrichment_table,
            enrichment_geo_table=enrichment_geo_table,
            enrichment_id=_ENRICHMENT_ID,
            where=_build_where_clausule(filters),
            data_table=data_table,
            grouper=grouper or '',
            columns=columns
        )


def _build_polygons_query_variables_with_aggregation(variables, aggregation):
    sql = []
    for variable in variables:
        variable_aggregation = _get_aggregation(variable, aggregation)
        if isinstance(variable_aggregation, list):
            for agg in variable_aggregation:
                sql.append(_build_polygons_column_with_aggregation(variable, agg, True))
        else:
            sql.append(_build_polygons_column_with_aggregation(variable, variable_aggregation))

    return ', '.join(sql)


def _build_polygons_column_with_aggregation(variable, aggregation, column_sufix=False):
    column_name = _get_polygons_agg_column_name(variable.column_name, aggregation, column_sufix)

    if (aggregation == 'sum'):
        return """
            {aggregation}(
                enrichment_table.{column} * (
                    ST_AREA(ST_INTERSECTION(enrichment_geo_table.geom, data_table.{geo_column}))
                    /
                    NULLIF(ST_AREA(enrichment_geo_table.geom), 0)
                )
            ) AS {column_name}
            """.format(
                column=variable.column_name,
                column_name=column_name,
                geo_column=_GEOM_COLUMN,
                aggregation=aggregation)
    else:
        return """
            {aggregation}(enrichment_table.{column}) AS {column_name}
            """.format(
                column=variable.column_name,
                column_name=column_name,
                aggregation=aggregation)


def _get_polygons_agg_column_name(column, aggregation, column_sufix):
    if column_sufix:
        return '{}_{}'.format(aggregation, column)
    else:
        return column


def _build_polygons_query_variables_without_aggregation(variables):
    variables = ['enrichment_table.{}'.format(variable.column_name) for variable in variables]

    return """
        {variables},
        ST_AREA(ST_INTERSECTION(enrichment_geo_table.geom, data_table.{geom_column})) AS intersected_area,
        ST_AREA(enrichment_geo_table.geom) AS do_area,
        ST_AREA(data_table.{geom_column}) AS user_area,
        enrichment_geo_table.geoid AS do_geoid
        """.format(
            variables=', '.join(variables),
            geom_column=_GEOM_COLUMN)


def _build_where_conditions_by_variable(variable, filters):
    if variable.id in filters:
        conditions = []
        variable_filter = filters[variable.id]

        if isinstance(variable_filter, list):
            for f in variable_filter:
                conditions.append(
                    _build_where_condition(
                        variable.column_name,
                        f
                    )
                )
        else:
            conditions.append(
                _build_where_condition(
                    variable.column_name,
                    variable_filter
                )
            )

        return conditions


def _build_where_condition(column, condition):
    return "enrichment_table.{} {}".format(column, condition)


def _build_where_clausule(filters):
    where = ''
    if len(filters) > 0:
        where = 'WHERE {}'.format(' AND '.join(filters))

    return where


@timelogger
def prepare_variables(variables, credentials, aggregation=None):
    _validate_variables_input(variables)

    if isinstance(variables, list):
        variables = [_prepare_variable(var, aggregation) for var in variables]
    else:
        variables = [_prepare_variable(variables, aggregation)]

    variables = list(filter(None, variables))

    _validate_bq_operations(variables, credentials)

    return variables


def _prepare_variable(variable, aggregation=None):
    if isinstance(variable, str):
        variable = Variable.get(variable)

    if not isinstance(variable, Variable):
        raise EnrichmentError("""
            variable should be a `<cartoframes.data.observatory> Variable` instance,
            Variable `id` property or Variable `slug` property
        """)

    if aggregation is not None:
        variable_agg = _get_aggregation(variable, aggregation)
        if not variable_agg and aggregation is not AGGREGATION_NONE:
            log.warning('%s skipped because it does not have aggregation method', variable.id)
            return None

    return variable


def _validate_variables_input(variables):
    if not isinstance(variables, Variable) and not isinstance(variables, str) and not isinstance(variables, list):
        raise EnrichmentError('variables parameter should be a Variable instance, a list or a str.')

    if not isinstance(variables, Variable) and len(variables) < 1:
        raise EnrichmentError('You should add at least one variable to be used in enrichment.')

    if isinstance(variables, list) and len(variables) > MAX_VARIABLES_NUMBER:
        raise EnrichmentError('The maximum number of variables to be used in enrichment is 50.')


def _validate_bq_operations(variables, credentials):
    dataset_ids = list(set([variable.dataset for variable in variables]))

    for dataset_id in dataset_ids:
        dataset = Dataset.get(dataset_id)
        geography = Geography.get(dataset.geography)

        _is_subscribed(dataset, geography, credentials)
        _is_available_in_bq(dataset, geography)


def _is_available_in_bq(dataset, geography):
    if not dataset._is_available_in('bq'):
        raise EnrichmentError("""
            The Dataset '{}' is not ready for Enrichment. Please, contact us for more information.
        """.format(dataset))

    if not geography._is_available_in('bq'):
        raise EnrichmentError("""
            The Geography '{}' is not ready for Enrichment. Please, contact us for more information.
        """.format(geography))


def _is_subscribed(dataset, geography, credentials):
    if not dataset._is_subscribed(credentials):
        raise EnrichmentError("""
            You are not subscribed to the Dataset '{}' yet. Please, use the subscribe method first.
        """.format(dataset.id))

    if not geography._is_subscribed(credentials):
        raise EnrichmentError("""
            You are not subscribed to the Geography '{}' yet. Please, use the subscribe method first.
        """.format(geography.id))


def _get_aggregation(variable, aggregation):
    if isinstance(aggregation, dict):
        aggregation_method = aggregation.get(variable.id, variable.agg_method)

        if isinstance(aggregation_method, list):
            return [_get_aggregation(variable, agg) for agg in aggregation_method]

        return _get_aggregation(variable, aggregation_method)
    else:
        if aggregation is AGGREGATION_NONE:
            aggregation_method = None
        elif aggregation == AGGREGATION_DEFAULT:
            aggregation_method = variable.agg_method
        elif isinstance(aggregation, str):
            aggregation_method = aggregation
        else:
            raise ValueError('The `aggregation` parameter is invalid.')

        if aggregation_method is not None:
            return aggregation_method.lower()
