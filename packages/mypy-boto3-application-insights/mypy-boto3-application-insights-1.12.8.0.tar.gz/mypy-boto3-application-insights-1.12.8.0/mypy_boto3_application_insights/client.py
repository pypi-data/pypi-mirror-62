"""
Main interface for application-insights service client

Usage::

    import boto3
    from mypy_boto3.application_insights import ApplicationInsightsClient

    session = boto3.Session()

    client: ApplicationInsightsClient = boto3.client("application-insights")
    session_client: ApplicationInsightsClient = session.client("application-insights")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Any, Dict, List, TYPE_CHECKING
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_application_insights.type_defs import (
    ClientCreateApplicationResponseTypeDef,
    ClientCreateApplicationTagsTypeDef,
    ClientCreateLogPatternResponseTypeDef,
    ClientDescribeApplicationResponseTypeDef,
    ClientDescribeComponentConfigurationRecommendationResponseTypeDef,
    ClientDescribeComponentConfigurationResponseTypeDef,
    ClientDescribeComponentResponseTypeDef,
    ClientDescribeLogPatternResponseTypeDef,
    ClientDescribeObservationResponseTypeDef,
    ClientDescribeProblemObservationsResponseTypeDef,
    ClientDescribeProblemResponseTypeDef,
    ClientListApplicationsResponseTypeDef,
    ClientListComponentsResponseTypeDef,
    ClientListConfigurationHistoryResponseTypeDef,
    ClientListLogPatternSetsResponseTypeDef,
    ClientListLogPatternsResponseTypeDef,
    ClientListProblemsResponseTypeDef,
    ClientListTagsForResourceResponseTypeDef,
    ClientTagResourceTagsTypeDef,
    ClientUpdateApplicationResponseTypeDef,
    ClientUpdateLogPatternResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ApplicationInsightsClient",)


class Exceptions:
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    InternalServerException: Boto3ClientError
    ResourceInUseException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    TagsAlreadyExistException: Boto3ClientError
    TooManyTagsException: Boto3ClientError
    ValidationException: Boto3ClientError


class ApplicationInsightsClient:
    """
    [ApplicationInsights.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.can_paginate)
        """

    def create_application(
        self,
        ResourceGroupName: str,
        OpsCenterEnabled: bool = None,
        OpsItemSNSTopicArn: str = None,
        Tags: List[ClientCreateApplicationTagsTypeDef] = None,
    ) -> ClientCreateApplicationResponseTypeDef:
        """
        [Client.create_application documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.create_application)
        """

    def create_component(
        self, ResourceGroupName: str, ComponentName: str, ResourceList: List[str]
    ) -> Dict[str, Any]:
        """
        [Client.create_component documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.create_component)
        """

    def create_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str, Pattern: str, Rank: int
    ) -> ClientCreateLogPatternResponseTypeDef:
        """
        [Client.create_log_pattern documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.create_log_pattern)
        """

    def delete_application(self, ResourceGroupName: str) -> Dict[str, Any]:
        """
        [Client.delete_application documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.delete_application)
        """

    def delete_component(self, ResourceGroupName: str, ComponentName: str) -> Dict[str, Any]:
        """
        [Client.delete_component documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.delete_component)
        """

    def delete_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> Dict[str, Any]:
        """
        [Client.delete_log_pattern documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.delete_log_pattern)
        """

    def describe_application(
        self, ResourceGroupName: str
    ) -> ClientDescribeApplicationResponseTypeDef:
        """
        [Client.describe_application documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_application)
        """

    def describe_component(
        self, ResourceGroupName: str, ComponentName: str
    ) -> ClientDescribeComponentResponseTypeDef:
        """
        [Client.describe_component documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_component)
        """

    def describe_component_configuration(
        self, ResourceGroupName: str, ComponentName: str
    ) -> ClientDescribeComponentConfigurationResponseTypeDef:
        """
        [Client.describe_component_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_component_configuration)
        """

    def describe_component_configuration_recommendation(
        self,
        ResourceGroupName: str,
        ComponentName: str,
        Tier: Literal["DEFAULT", "DOT_NET_CORE", "DOT_NET_WORKER", "DOT_NET_WEB", "SQL_SERVER"],
    ) -> ClientDescribeComponentConfigurationRecommendationResponseTypeDef:
        """
        [Client.describe_component_configuration_recommendation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_component_configuration_recommendation)
        """

    def describe_log_pattern(
        self, ResourceGroupName: str, PatternSetName: str, PatternName: str
    ) -> ClientDescribeLogPatternResponseTypeDef:
        """
        [Client.describe_log_pattern documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_log_pattern)
        """

    def describe_observation(self, ObservationId: str) -> ClientDescribeObservationResponseTypeDef:
        """
        [Client.describe_observation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_observation)
        """

    def describe_problem(self, ProblemId: str) -> ClientDescribeProblemResponseTypeDef:
        """
        [Client.describe_problem documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_problem)
        """

    def describe_problem_observations(
        self, ProblemId: str
    ) -> ClientDescribeProblemObservationsResponseTypeDef:
        """
        [Client.describe_problem_observations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.describe_problem_observations)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> None:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.generate_presigned_url)
        """

    def list_applications(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ClientListApplicationsResponseTypeDef:
        """
        [Client.list_applications documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_applications)
        """

    def list_components(
        self, ResourceGroupName: str, MaxResults: int = None, NextToken: str = None
    ) -> ClientListComponentsResponseTypeDef:
        """
        [Client.list_components documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_components)
        """

    def list_configuration_history(
        self,
        ResourceGroupName: str = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        EventStatus: Literal["INFO", "WARN", "ERROR"] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ClientListConfigurationHistoryResponseTypeDef:
        """
        [Client.list_configuration_history documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_configuration_history)
        """

    def list_log_pattern_sets(
        self, ResourceGroupName: str, MaxResults: int = None, NextToken: str = None
    ) -> ClientListLogPatternSetsResponseTypeDef:
        """
        [Client.list_log_pattern_sets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_log_pattern_sets)
        """

    def list_log_patterns(
        self,
        ResourceGroupName: str,
        PatternSetName: str = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ClientListLogPatternsResponseTypeDef:
        """
        [Client.list_log_patterns documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_log_patterns)
        """

    def list_problems(
        self,
        ResourceGroupName: str = None,
        StartTime: datetime = None,
        EndTime: datetime = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> ClientListProblemsResponseTypeDef:
        """
        [Client.list_problems documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_problems)
        """

    def list_tags_for_resource(self, ResourceARN: str) -> ClientListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.list_tags_for_resource)
        """

    def tag_resource(
        self, ResourceARN: str, Tags: List[ClientTagResourceTagsTypeDef]
    ) -> Dict[str, Any]:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.tag_resource)
        """

    def untag_resource(self, ResourceARN: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.untag_resource)
        """

    def update_application(
        self,
        ResourceGroupName: str,
        OpsCenterEnabled: bool = None,
        OpsItemSNSTopicArn: str = None,
        RemoveSNSTopic: bool = None,
    ) -> ClientUpdateApplicationResponseTypeDef:
        """
        [Client.update_application documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.update_application)
        """

    def update_component(
        self,
        ResourceGroupName: str,
        ComponentName: str,
        NewComponentName: str = None,
        ResourceList: List[str] = None,
    ) -> Dict[str, Any]:
        """
        [Client.update_component documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.update_component)
        """

    def update_component_configuration(
        self,
        ResourceGroupName: str,
        ComponentName: str,
        Monitor: bool = None,
        Tier: Literal[
            "DEFAULT", "DOT_NET_CORE", "DOT_NET_WORKER", "DOT_NET_WEB", "SQL_SERVER"
        ] = None,
        ComponentConfiguration: str = None,
    ) -> Dict[str, Any]:
        """
        [Client.update_component_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.update_component_configuration)
        """

    def update_log_pattern(
        self,
        ResourceGroupName: str,
        PatternSetName: str,
        PatternName: str,
        Pattern: str = None,
        Rank: int = None,
    ) -> ClientUpdateLogPatternResponseTypeDef:
        """
        [Client.update_log_pattern documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/application-insights.html#ApplicationInsights.Client.update_log_pattern)
        """
