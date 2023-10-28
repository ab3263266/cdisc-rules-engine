import pandas as pd

import dask.dataframe as dd
from cdisc_rules_engine.config.config import ConfigService
from cdisc_rules_engine.models.operation_params import OperationParams

from cdisc_rules_engine.services.cache.cache_service_factory import CacheServiceFactory
from cdisc_rules_engine.services.data_services.data_service_factory import (
    DataServiceFactory,
)
from cdisc_rules_engine.DatasetOperations.Operations import DatasetOperations


def test_get_study_domains_with_duplicates(operation_params: OperationParams):
    config = ConfigService()
    cache = CacheServiceFactory(config).get_cache_service()
    data_service = DataServiceFactory(config, cache).get_data_service()
    datasets = [
        {"filename": "dm.xpt", "domain": "DM"},
        {"filename": "dm1.xpt", "domain": "DM"},
        {"filename": "ae.xpt", "domain": "AE"},
        {"filename": "tv.xpt", "domain": "TV"},
    ]
    operation_params.datasets = datasets
    operations = DatasetOperations()
    result = operations.get_service(
        "study_domains",
        operation_params,
        pd.DataFrame.from_dict({"A": [1, 2, 3]}),
        cache,
        data_service,
    )
    assert operation_params.operation_id in result
    for val in result[operation_params.operation_id]:
        assert sorted(val) == ["AE", "DM", "TV"]


def test_get_study_domains_with_missing_domains(operation_params: OperationParams):
    config = ConfigService()
    cache = CacheServiceFactory(config).get_cache_service()
    data_service = DataServiceFactory(config, cache).get_data_service()
    datasets = [
        {"filename": "dm.xpt"},
        {"filename": "dm1.xpt", "domain": "DM"},
        {"filename": "ae.xpt", "domain": "AE"},
        {"filename": "tv.xpt", "domain": "TV"},
    ]
    operation_params.datasets = datasets
    operations = DatasetOperations()
    result = operations.get_service(
        "study_domains",
        operation_params,
        pd.DataFrame.from_dict({"A": [1, 2, 3]}),
        cache,
        data_service,
    )
    assert operation_params.operation_id in result
    for val in result[operation_params.operation_id]:
        assert sorted(val) == ["", "AE", "DM", "TV"]


def test_get_study_domains_with_duplicates_dask(operation_params: OperationParams):
    config = ConfigService()
    cache = CacheServiceFactory(config).get_cache_service()
    data_service = DataServiceFactory(config, cache).get_data_service()
    datasets = [
        {"filename": "dm.xpt", "domain": "DM"},
        {"filename": "dm1.xpt", "domain": "DM"},
        {"filename": "ae.xpt", "domain": "AE"},
        {"filename": "tv.xpt", "domain": "TV"},
    ]
    operation_params.datasets = datasets
    operations = DatasetOperations()
    result = operations.get_service(
        "study_domains",
        operation_params,
        dd.DataFrame.from_dict({"A": [1, 2, 3]}, npartitions=1),
        cache,
        data_service,
    )
    assert operation_params.operation_id in result
    for val in result[operation_params.operation_id]:
        assert sorted(val) == ["AE", "DM", "TV"]


def test_get_study_domains_with_missing_domains_dask(operation_params: OperationParams):
    config = ConfigService()
    cache = CacheServiceFactory(config).get_cache_service()
    data_service = DataServiceFactory(config, cache).get_data_service()
    datasets = [
        {"filename": "dm.xpt"},
        {"filename": "dm1.xpt", "domain": "DM"},
        {"filename": "ae.xpt", "domain": "AE"},
        {"filename": "tv.xpt", "domain": "TV"},
    ]
    operation_params.datasets = datasets
    operations = DatasetOperations()
    result = operations.get_service(
        "study_domains",
        operation_params,
        dd.DataFrame.from_dict({"A": [1, 2, 3]}, npartitions=1),
        cache,
        data_service,
    )
    assert operation_params.operation_id in result
    for val in result[operation_params.operation_id]:
        assert sorted(val) == ["", "AE", "DM", "TV"]
