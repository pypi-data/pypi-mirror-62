"""
Main interface for lambda service client

Usage::

    import boto3
    from mypy_boto3.lambda_ import LambdaClient

    session = boto3.Session()

    client: LambdaClient = boto3.client("lambda")
    session_client: LambdaClient = session.client("lambda")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Any, Dict, IO, List, TYPE_CHECKING, Union, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_lambda.paginator import (
    ListAliasesPaginator,
    ListEventSourceMappingsPaginator,
    ListFunctionEventInvokeConfigsPaginator,
    ListFunctionsPaginator,
    ListLayerVersionsPaginator,
    ListLayersPaginator,
    ListProvisionedConcurrencyConfigsPaginator,
    ListVersionsByFunctionPaginator,
)
from mypy_boto3_lambda.type_defs import (
    ClientAddLayerVersionPermissionResponseTypeDef,
    ClientAddPermissionResponseTypeDef,
    ClientCreateAliasResponseTypeDef,
    ClientCreateAliasRoutingConfigTypeDef,
    ClientCreateEventSourceMappingDestinationConfigTypeDef,
    ClientCreateEventSourceMappingResponseTypeDef,
    ClientCreateFunctionCodeTypeDef,
    ClientCreateFunctionDeadLetterConfigTypeDef,
    ClientCreateFunctionEnvironmentTypeDef,
    ClientCreateFunctionResponseTypeDef,
    ClientCreateFunctionTracingConfigTypeDef,
    ClientCreateFunctionVpcConfigTypeDef,
    ClientDeleteEventSourceMappingResponseTypeDef,
    ClientGetAccountSettingsResponseTypeDef,
    ClientGetAliasResponseTypeDef,
    ClientGetEventSourceMappingResponseTypeDef,
    ClientGetFunctionConcurrencyResponseTypeDef,
    ClientGetFunctionConfigurationResponseTypeDef,
    ClientGetFunctionEventInvokeConfigResponseTypeDef,
    ClientGetFunctionResponseTypeDef,
    ClientGetLayerVersionByArnResponseTypeDef,
    ClientGetLayerVersionPolicyResponseTypeDef,
    ClientGetLayerVersionResponseTypeDef,
    ClientGetPolicyResponseTypeDef,
    ClientGetProvisionedConcurrencyConfigResponseTypeDef,
    ClientInvokeAsyncResponseTypeDef,
    ClientInvokeResponseTypeDef,
    ClientListAliasesResponseTypeDef,
    ClientListEventSourceMappingsResponseTypeDef,
    ClientListFunctionEventInvokeConfigsResponseTypeDef,
    ClientListFunctionsResponseTypeDef,
    ClientListLayerVersionsResponseTypeDef,
    ClientListLayersResponseTypeDef,
    ClientListProvisionedConcurrencyConfigsResponseTypeDef,
    ClientListTagsResponseTypeDef,
    ClientListVersionsByFunctionResponseTypeDef,
    ClientPublishLayerVersionContentTypeDef,
    ClientPublishLayerVersionResponseTypeDef,
    ClientPublishVersionResponseTypeDef,
    ClientPutFunctionConcurrencyResponseTypeDef,
    ClientPutFunctionEventInvokeConfigDestinationConfigTypeDef,
    ClientPutFunctionEventInvokeConfigResponseTypeDef,
    ClientPutProvisionedConcurrencyConfigResponseTypeDef,
    ClientUpdateAliasResponseTypeDef,
    ClientUpdateAliasRoutingConfigTypeDef,
    ClientUpdateEventSourceMappingDestinationConfigTypeDef,
    ClientUpdateEventSourceMappingResponseTypeDef,
    ClientUpdateFunctionCodeResponseTypeDef,
    ClientUpdateFunctionConfigurationDeadLetterConfigTypeDef,
    ClientUpdateFunctionConfigurationEnvironmentTypeDef,
    ClientUpdateFunctionConfigurationResponseTypeDef,
    ClientUpdateFunctionConfigurationTracingConfigTypeDef,
    ClientUpdateFunctionConfigurationVpcConfigTypeDef,
    ClientUpdateFunctionEventInvokeConfigDestinationConfigTypeDef,
    ClientUpdateFunctionEventInvokeConfigResponseTypeDef,
)
from mypy_boto3_lambda.waiter import (
    FunctionActiveWaiter,
    FunctionExistsWaiter,
    FunctionUpdatedWaiter,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("LambdaClient",)


class Exceptions:
    ClientError: Boto3ClientError
    CodeStorageExceededException: Boto3ClientError
    EC2AccessDeniedException: Boto3ClientError
    EC2ThrottledException: Boto3ClientError
    EC2UnexpectedException: Boto3ClientError
    ENILimitReachedException: Boto3ClientError
    InvalidParameterValueException: Boto3ClientError
    InvalidRequestContentException: Boto3ClientError
    InvalidRuntimeException: Boto3ClientError
    InvalidSecurityGroupIDException: Boto3ClientError
    InvalidSubnetIDException: Boto3ClientError
    InvalidZipFileException: Boto3ClientError
    KMSAccessDeniedException: Boto3ClientError
    KMSDisabledException: Boto3ClientError
    KMSInvalidStateException: Boto3ClientError
    KMSNotFoundException: Boto3ClientError
    PolicyLengthExceededException: Boto3ClientError
    PreconditionFailedException: Boto3ClientError
    ProvisionedConcurrencyConfigNotFoundException: Boto3ClientError
    RequestTooLargeException: Boto3ClientError
    ResourceConflictException: Boto3ClientError
    ResourceInUseException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    ResourceNotReadyException: Boto3ClientError
    ServiceException: Boto3ClientError
    SubnetIPAddressLimitReachedException: Boto3ClientError
    TooManyRequestsException: Boto3ClientError
    UnsupportedMediaTypeException: Boto3ClientError


class LambdaClient:
    """
    [Lambda.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client)
    """

    exceptions: Exceptions

    def add_layer_version_permission(
        self,
        LayerName: str,
        VersionNumber: int,
        StatementId: str,
        Action: str,
        Principal: str,
        OrganizationId: str = None,
        RevisionId: str = None,
    ) -> ClientAddLayerVersionPermissionResponseTypeDef:
        """
        [Client.add_layer_version_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.add_layer_version_permission)
        """

    def add_permission(
        self,
        FunctionName: str,
        StatementId: str,
        Action: str,
        Principal: str,
        SourceArn: str = None,
        SourceAccount: str = None,
        EventSourceToken: str = None,
        Qualifier: str = None,
        RevisionId: str = None,
    ) -> ClientAddPermissionResponseTypeDef:
        """
        [Client.add_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.add_permission)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.can_paginate)
        """

    def create_alias(
        self,
        FunctionName: str,
        Name: str,
        FunctionVersion: str,
        Description: str = None,
        RoutingConfig: ClientCreateAliasRoutingConfigTypeDef = None,
    ) -> ClientCreateAliasResponseTypeDef:
        """
        [Client.create_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.create_alias)
        """

    def create_event_source_mapping(
        self,
        EventSourceArn: str,
        FunctionName: str,
        Enabled: bool = None,
        BatchSize: int = None,
        MaximumBatchingWindowInSeconds: int = None,
        ParallelizationFactor: int = None,
        StartingPosition: Literal["TRIM_HORIZON", "LATEST", "AT_TIMESTAMP"] = None,
        StartingPositionTimestamp: datetime = None,
        DestinationConfig: ClientCreateEventSourceMappingDestinationConfigTypeDef = None,
        MaximumRecordAgeInSeconds: int = None,
        BisectBatchOnFunctionError: bool = None,
        MaximumRetryAttempts: int = None,
    ) -> ClientCreateEventSourceMappingResponseTypeDef:
        """
        [Client.create_event_source_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.create_event_source_mapping)
        """

    def create_function(
        self,
        FunctionName: str,
        Runtime: Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "java8",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
        ],
        Role: str,
        Handler: str,
        Code: ClientCreateFunctionCodeTypeDef,
        Description: str = None,
        Timeout: int = None,
        MemorySize: int = None,
        Publish: bool = None,
        VpcConfig: ClientCreateFunctionVpcConfigTypeDef = None,
        DeadLetterConfig: ClientCreateFunctionDeadLetterConfigTypeDef = None,
        Environment: ClientCreateFunctionEnvironmentTypeDef = None,
        KMSKeyArn: str = None,
        TracingConfig: ClientCreateFunctionTracingConfigTypeDef = None,
        Tags: Dict[str, str] = None,
        Layers: List[str] = None,
    ) -> ClientCreateFunctionResponseTypeDef:
        """
        [Client.create_function documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.create_function)
        """

    def delete_alias(self, FunctionName: str, Name: str) -> None:
        """
        [Client.delete_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_alias)
        """

    def delete_event_source_mapping(
        self, UUID: str
    ) -> ClientDeleteEventSourceMappingResponseTypeDef:
        """
        [Client.delete_event_source_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_event_source_mapping)
        """

    def delete_function(self, FunctionName: str, Qualifier: str = None) -> None:
        """
        [Client.delete_function documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_function)
        """

    def delete_function_concurrency(self, FunctionName: str) -> None:
        """
        [Client.delete_function_concurrency documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_function_concurrency)
        """

    def delete_function_event_invoke_config(self, FunctionName: str, Qualifier: str = None) -> None:
        """
        [Client.delete_function_event_invoke_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_function_event_invoke_config)
        """

    def delete_layer_version(self, LayerName: str, VersionNumber: int) -> None:
        """
        [Client.delete_layer_version documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_layer_version)
        """

    def delete_provisioned_concurrency_config(self, FunctionName: str, Qualifier: str) -> None:
        """
        [Client.delete_provisioned_concurrency_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.delete_provisioned_concurrency_config)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> None:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.generate_presigned_url)
        """

    def get_account_settings(
        self, *args: Any, **kwargs: Any
    ) -> ClientGetAccountSettingsResponseTypeDef:
        """
        [Client.get_account_settings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_account_settings)
        """

    def get_alias(self, FunctionName: str, Name: str) -> ClientGetAliasResponseTypeDef:
        """
        [Client.get_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_alias)
        """

    def get_event_source_mapping(self, UUID: str) -> ClientGetEventSourceMappingResponseTypeDef:
        """
        [Client.get_event_source_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_event_source_mapping)
        """

    def get_function(
        self, FunctionName: str, Qualifier: str = None
    ) -> ClientGetFunctionResponseTypeDef:
        """
        [Client.get_function documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_function)
        """

    def get_function_concurrency(
        self, FunctionName: str
    ) -> ClientGetFunctionConcurrencyResponseTypeDef:
        """
        [Client.get_function_concurrency documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_function_concurrency)
        """

    def get_function_configuration(
        self, FunctionName: str, Qualifier: str = None
    ) -> ClientGetFunctionConfigurationResponseTypeDef:
        """
        [Client.get_function_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_function_configuration)
        """

    def get_function_event_invoke_config(
        self, FunctionName: str, Qualifier: str = None
    ) -> ClientGetFunctionEventInvokeConfigResponseTypeDef:
        """
        [Client.get_function_event_invoke_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_function_event_invoke_config)
        """

    def get_layer_version(
        self, LayerName: str, VersionNumber: int
    ) -> ClientGetLayerVersionResponseTypeDef:
        """
        [Client.get_layer_version documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_layer_version)
        """

    def get_layer_version_by_arn(self, Arn: str) -> ClientGetLayerVersionByArnResponseTypeDef:
        """
        [Client.get_layer_version_by_arn documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_layer_version_by_arn)
        """

    def get_layer_version_policy(
        self, LayerName: str, VersionNumber: int
    ) -> ClientGetLayerVersionPolicyResponseTypeDef:
        """
        [Client.get_layer_version_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_layer_version_policy)
        """

    def get_policy(
        self, FunctionName: str, Qualifier: str = None
    ) -> ClientGetPolicyResponseTypeDef:
        """
        [Client.get_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_policy)
        """

    def get_provisioned_concurrency_config(
        self, FunctionName: str, Qualifier: str
    ) -> ClientGetProvisionedConcurrencyConfigResponseTypeDef:
        """
        [Client.get_provisioned_concurrency_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.get_provisioned_concurrency_config)
        """

    def invoke(
        self,
        FunctionName: str,
        InvocationType: Literal["Event", "RequestResponse", "DryRun"] = None,
        LogType: Literal["None", "Tail"] = None,
        ClientContext: str = None,
        Payload: Union[bytes, IO] = None,
        Qualifier: str = None,
    ) -> ClientInvokeResponseTypeDef:
        """
        [Client.invoke documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.invoke)
        """

    def invoke_async(
        self, FunctionName: str, InvokeArgs: Union[bytes, IO]
    ) -> ClientInvokeAsyncResponseTypeDef:
        """
        [Client.invoke_async documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.invoke_async)
        """

    def list_aliases(
        self,
        FunctionName: str,
        FunctionVersion: str = None,
        Marker: str = None,
        MaxItems: int = None,
    ) -> ClientListAliasesResponseTypeDef:
        """
        [Client.list_aliases documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_aliases)
        """

    def list_event_source_mappings(
        self,
        EventSourceArn: str = None,
        FunctionName: str = None,
        Marker: str = None,
        MaxItems: int = None,
    ) -> ClientListEventSourceMappingsResponseTypeDef:
        """
        [Client.list_event_source_mappings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_event_source_mappings)
        """

    def list_function_event_invoke_configs(
        self, FunctionName: str, Marker: str = None, MaxItems: int = None
    ) -> ClientListFunctionEventInvokeConfigsResponseTypeDef:
        """
        [Client.list_function_event_invoke_configs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_function_event_invoke_configs)
        """

    def list_functions(
        self,
        MasterRegion: str = None,
        FunctionVersion: str = None,
        Marker: str = None,
        MaxItems: int = None,
    ) -> ClientListFunctionsResponseTypeDef:
        """
        [Client.list_functions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_functions)
        """

    def list_layer_versions(
        self,
        LayerName: str,
        CompatibleRuntime: Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "java8",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
        ] = None,
        Marker: str = None,
        MaxItems: int = None,
    ) -> ClientListLayerVersionsResponseTypeDef:
        """
        [Client.list_layer_versions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_layer_versions)
        """

    def list_layers(
        self,
        CompatibleRuntime: Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "java8",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
        ] = None,
        Marker: str = None,
        MaxItems: int = None,
    ) -> ClientListLayersResponseTypeDef:
        """
        [Client.list_layers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_layers)
        """

    def list_provisioned_concurrency_configs(
        self, FunctionName: str, Marker: str = None, MaxItems: int = None
    ) -> ClientListProvisionedConcurrencyConfigsResponseTypeDef:
        """
        [Client.list_provisioned_concurrency_configs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_provisioned_concurrency_configs)
        """

    def list_tags(self, Resource: str) -> ClientListTagsResponseTypeDef:
        """
        [Client.list_tags documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_tags)
        """

    def list_versions_by_function(
        self, FunctionName: str, Marker: str = None, MaxItems: int = None
    ) -> ClientListVersionsByFunctionResponseTypeDef:
        """
        [Client.list_versions_by_function documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.list_versions_by_function)
        """

    def publish_layer_version(
        self,
        LayerName: str,
        Content: ClientPublishLayerVersionContentTypeDef,
        Description: str = None,
        CompatibleRuntimes: List[
            Literal[
                "nodejs",
                "nodejs4.3",
                "nodejs6.10",
                "nodejs8.10",
                "nodejs10.x",
                "nodejs12.x",
                "java8",
                "java11",
                "python2.7",
                "python3.6",
                "python3.7",
                "python3.8",
                "dotnetcore1.0",
                "dotnetcore2.0",
                "dotnetcore2.1",
                "nodejs4.3-edge",
                "go1.x",
                "ruby2.5",
                "ruby2.7",
                "provided",
            ]
        ] = None,
        LicenseInfo: str = None,
    ) -> ClientPublishLayerVersionResponseTypeDef:
        """
        [Client.publish_layer_version documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.publish_layer_version)
        """

    def publish_version(
        self,
        FunctionName: str,
        CodeSha256: str = None,
        Description: str = None,
        RevisionId: str = None,
    ) -> ClientPublishVersionResponseTypeDef:
        """
        [Client.publish_version documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.publish_version)
        """

    def put_function_concurrency(
        self, FunctionName: str, ReservedConcurrentExecutions: int
    ) -> ClientPutFunctionConcurrencyResponseTypeDef:
        """
        [Client.put_function_concurrency documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.put_function_concurrency)
        """

    def put_function_event_invoke_config(
        self,
        FunctionName: str,
        Qualifier: str = None,
        MaximumRetryAttempts: int = None,
        MaximumEventAgeInSeconds: int = None,
        DestinationConfig: ClientPutFunctionEventInvokeConfigDestinationConfigTypeDef = None,
    ) -> ClientPutFunctionEventInvokeConfigResponseTypeDef:
        """
        [Client.put_function_event_invoke_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.put_function_event_invoke_config)
        """

    def put_provisioned_concurrency_config(
        self, FunctionName: str, Qualifier: str, ProvisionedConcurrentExecutions: int
    ) -> ClientPutProvisionedConcurrencyConfigResponseTypeDef:
        """
        [Client.put_provisioned_concurrency_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.put_provisioned_concurrency_config)
        """

    def remove_layer_version_permission(
        self, LayerName: str, VersionNumber: int, StatementId: str, RevisionId: str = None
    ) -> None:
        """
        [Client.remove_layer_version_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.remove_layer_version_permission)
        """

    def remove_permission(
        self, FunctionName: str, StatementId: str, Qualifier: str = None, RevisionId: str = None
    ) -> None:
        """
        [Client.remove_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.remove_permission)
        """

    def tag_resource(self, Resource: str, Tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.tag_resource)
        """

    def untag_resource(self, Resource: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.untag_resource)
        """

    def update_alias(
        self,
        FunctionName: str,
        Name: str,
        FunctionVersion: str = None,
        Description: str = None,
        RoutingConfig: ClientUpdateAliasRoutingConfigTypeDef = None,
        RevisionId: str = None,
    ) -> ClientUpdateAliasResponseTypeDef:
        """
        [Client.update_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.update_alias)
        """

    def update_event_source_mapping(
        self,
        UUID: str,
        FunctionName: str = None,
        Enabled: bool = None,
        BatchSize: int = None,
        MaximumBatchingWindowInSeconds: int = None,
        DestinationConfig: ClientUpdateEventSourceMappingDestinationConfigTypeDef = None,
        MaximumRecordAgeInSeconds: int = None,
        BisectBatchOnFunctionError: bool = None,
        MaximumRetryAttempts: int = None,
        ParallelizationFactor: int = None,
    ) -> ClientUpdateEventSourceMappingResponseTypeDef:
        """
        [Client.update_event_source_mapping documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.update_event_source_mapping)
        """

    def update_function_code(
        self,
        FunctionName: str,
        ZipFile: bytes = None,
        S3Bucket: str = None,
        S3Key: str = None,
        S3ObjectVersion: str = None,
        Publish: bool = None,
        DryRun: bool = None,
        RevisionId: str = None,
    ) -> ClientUpdateFunctionCodeResponseTypeDef:
        """
        [Client.update_function_code documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.update_function_code)
        """

    def update_function_configuration(
        self,
        FunctionName: str,
        Role: str = None,
        Handler: str = None,
        Description: str = None,
        Timeout: int = None,
        MemorySize: int = None,
        VpcConfig: ClientUpdateFunctionConfigurationVpcConfigTypeDef = None,
        Environment: ClientUpdateFunctionConfigurationEnvironmentTypeDef = None,
        Runtime: Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "java8",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
        ] = None,
        DeadLetterConfig: ClientUpdateFunctionConfigurationDeadLetterConfigTypeDef = None,
        KMSKeyArn: str = None,
        TracingConfig: ClientUpdateFunctionConfigurationTracingConfigTypeDef = None,
        RevisionId: str = None,
        Layers: List[str] = None,
    ) -> ClientUpdateFunctionConfigurationResponseTypeDef:
        """
        [Client.update_function_configuration documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.update_function_configuration)
        """

    def update_function_event_invoke_config(
        self,
        FunctionName: str,
        Qualifier: str = None,
        MaximumRetryAttempts: int = None,
        MaximumEventAgeInSeconds: int = None,
        DestinationConfig: ClientUpdateFunctionEventInvokeConfigDestinationConfigTypeDef = None,
    ) -> ClientUpdateFunctionEventInvokeConfigResponseTypeDef:
        """
        [Client.update_function_event_invoke_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Client.update_function_event_invoke_config)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_aliases"]) -> ListAliasesPaginator:
        """
        [Paginator.ListAliases documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListAliases)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_source_mappings"]
    ) -> ListEventSourceMappingsPaginator:
        """
        [Paginator.ListEventSourceMappings documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListEventSourceMappings)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_function_event_invoke_configs"]
    ) -> ListFunctionEventInvokeConfigsPaginator:
        """
        [Paginator.ListFunctionEventInvokeConfigs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListFunctionEventInvokeConfigs)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_functions"]) -> ListFunctionsPaginator:
        """
        [Paginator.ListFunctions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListFunctions)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_layer_versions"]
    ) -> ListLayerVersionsPaginator:
        """
        [Paginator.ListLayerVersions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListLayerVersions)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_layers"]) -> ListLayersPaginator:
        """
        [Paginator.ListLayers documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListLayers)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_provisioned_concurrency_configs"]
    ) -> ListProvisionedConcurrencyConfigsPaginator:
        """
        [Paginator.ListProvisionedConcurrencyConfigs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListProvisionedConcurrencyConfigs)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_versions_by_function"]
    ) -> ListVersionsByFunctionPaginator:
        """
        [Paginator.ListVersionsByFunction documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Paginator.ListVersionsByFunction)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_active"]) -> FunctionActiveWaiter:
        """
        [Waiter.FunctionActive documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Waiter.FunctionActive)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_exists"]) -> FunctionExistsWaiter:
        """
        [Waiter.FunctionExists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Waiter.FunctionExists)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["function_updated"]) -> FunctionUpdatedWaiter:
        """
        [Waiter.FunctionUpdated documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.8/reference/services/lambda.html#Lambda.Waiter.FunctionUpdated)
        """
