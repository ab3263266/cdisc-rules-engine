from typing import List

import pandas as pd
import pytest

from cdisc_rules_engine.constants.classes import GENERAL_OBSERVATIONS_CLASS
from cdisc_rules_engine.enums.variable_roles import VariableRoles
from cdisc_rules_engine.models.operation_params import OperationParams
from cdisc_rules_engine.operations.library_column_order import LibraryColumnOrder
from cdisc_rules_engine.services.cache import InMemoryCacheService
from cdisc_rules_engine.services.data_services import LocalDataService
from cdisc_rules_engine.utilities.utils import get_model_details_cache_key


@pytest.mark.parametrize(
    "model_metadata",
    [
        {
            "datasets": [
                {
                    "name": "AE",
                    "datasetVariables": [
                        {
                            "name": "AETERM",
                            "ordinal": 4,
                        },
                        {
                            "name": "AESEQ",
                            "ordinal": 3,
                        },
                    ],
                }
            ],
            "classes": [
                {
                    "name": GENERAL_OBSERVATIONS_CLASS,
                    "classVariables": [
                        {
                            "name": "DOMAIN",
                            "role": VariableRoles.IDENTIFIER.value,
                            "ordinal": 2,
                        },
                        {
                            "name": "STUDYID",
                            "role": VariableRoles.IDENTIFIER.value,
                            "ordinal": 1,
                        },
                        {
                            "name": "TIMING_VAR",
                            "role": VariableRoles.TIMING.value,
                            "ordinal": 33,
                        },
                    ],
                },
            ],
        },
        {
            "classes": [
                {
                    "name": "Events",
                    "classVariables": [
                        {
                            "name": "AETERM",
                            "ordinal": 4,
                        },
                        {
                            "name": "AESEQ",
                            "ordinal": 3,
                        },
                    ],
                },
                {
                    "name": GENERAL_OBSERVATIONS_CLASS,
                    "classVariables": [
                        {
                            "name": "DOMAIN",
                            "role": VariableRoles.IDENTIFIER.value,
                            "ordinal": 2,
                        },
                        {
                            "name": "STUDYID",
                            "role": VariableRoles.IDENTIFIER.value,
                            "ordinal": 1,
                        },
                        {
                            "name": "TIMING_VAR",
                            "role": VariableRoles.TIMING.value,
                            "ordinal": 33,
                        },
                    ],
                },
            ],
        },
    ],
)
def test_get_column_order_from_library(
    operation_params: OperationParams, model_metadata: dict
):
    """
    Unit test for DataProcessor.get_column_order_from_library.
    Mocks cache call to return metadata.
    """
    operation_params.dataframe = pd.DataFrame.from_dict(
        {
            "STUDYID": [
                "TEST_STUDY",
                "TEST_STUDY",
                "TEST_STUDY",
            ],
            "AETERM": [
                "test",
                "test",
                "test",
            ],
        }
    )
    operation_params.domain = "AE"
    operation_params.standard = "sdtm"
    operation_params.standard_version = "3-4"

    # save model metadata to cache
    cache = InMemoryCacheService.get_instance()
    cache.add(
        get_model_details_cache_key(
            operation_params.standard, operation_params.standard_version
        ),
        model_metadata,
    )

    # execute operation
    data_service = LocalDataService.get_instance(cache_service=cache)
    operation = LibraryColumnOrder(
        operation_params, operation_params.dataframe, cache, data_service
    )
    result: pd.DataFrame = operation.execute()
    variables: List[str] = [
        "STUDYID",
        "DOMAIN",
        "AESEQ",
        "AETERM",
        "TIMING_VAR",
    ]
    expected: pd.Series = pd.Series(
        [
            variables,
            variables,
            variables,
        ]
    )
    assert result[operation_params.operation_id].equals(expected)