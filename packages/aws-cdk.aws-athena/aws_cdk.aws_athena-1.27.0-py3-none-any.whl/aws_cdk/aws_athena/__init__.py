"""
## Amazon Athena Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib))
> are auto-generated from CloudFormation. They are stable and safe to use.
>
> However, all other classes, i.e., higher level constructs, are under active development and subject to non-backward
> compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-athena", "1.27.0", __name__, "aws-athena@1.27.0.jsii.tgz")


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNamedQuery(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-athena.CfnNamedQuery"):
    """A CloudFormation ``AWS::Athena::NamedQuery``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
    cloudformationResource:
    :cloudformationResource:: AWS::Athena::NamedQuery
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, database: str, query_string: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Athena::NamedQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database: ``AWS::Athena::NamedQuery.Database``.
        :param query_string: ``AWS::Athena::NamedQuery.QueryString``.
        :param description: ``AWS::Athena::NamedQuery.Description``.
        :param name: ``AWS::Athena::NamedQuery.Name``.
        """
        props = CfnNamedQueryProps(database=database, query_string=query_string, description=description, name=name)

        jsii.create(CfnNamedQuery, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> str:
        """``AWS::Athena::NamedQuery.Database``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        """
        return jsii.get(self, "database")

    @database.setter
    def database(self, value: str):
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> str:
        """``AWS::Athena::NamedQuery.QueryString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        """
        return jsii.get(self, "queryString")

    @query_string.setter
    def query_string(self, value: str):
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-athena.CfnNamedQueryProps", jsii_struct_bases=[], name_mapping={'database': 'database', 'query_string': 'queryString', 'description': 'description', 'name': 'name'})
class CfnNamedQueryProps():
    def __init__(self, *, database: str, query_string: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Athena::NamedQuery``.

        :param database: ``AWS::Athena::NamedQuery.Database``.
        :param query_string: ``AWS::Athena::NamedQuery.QueryString``.
        :param description: ``AWS::Athena::NamedQuery.Description``.
        :param name: ``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
        """
        self._values = {
            'database': database,
            'query_string': query_string,
        }
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name

    @builtins.property
    def database(self) -> str:
        """``AWS::Athena::NamedQuery.Database``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        """
        return self._values.get('database')

    @builtins.property
    def query_string(self) -> str:
        """``AWS::Athena::NamedQuery.QueryString``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        """
        return self._values.get('query_string')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        """
        return self._values.get('description')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::Athena::NamedQuery.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNamedQueryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnNamedQuery", "CfnNamedQueryProps", "__jsii_assembly__"]

publication.publish()
