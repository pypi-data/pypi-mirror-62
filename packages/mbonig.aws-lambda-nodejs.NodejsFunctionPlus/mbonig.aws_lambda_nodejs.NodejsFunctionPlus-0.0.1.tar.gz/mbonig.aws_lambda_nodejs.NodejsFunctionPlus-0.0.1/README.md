## Matt's Lambda Node.js Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

This library provides constructs for Node.js Lambda functions. Well, ok, so AWS already does that with the [@aws-cdk/aws-lambda-nodejs](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-nodejs-readme.html) package.

All this CDK construct does it expose the same `NodejsFunction` construct as that other package, but I set the `AWS_NODEJS_CONNECTION_REUSE_ENABLED` for you. Why? Because it's a super great environment flag built into the AWS SDK which [enables http keep-alive](https://theburningmonk.com/2019/02/lambda-optimization-tip-enable-http-keep-alive/), and greatly improves performance.

## Usage

This is a drop-in replacement:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# import {NodejsFunction} from '@aws-cdk/aws-lambda-nodejs';
from nodejsfunction_plus import NodejsFunction

NodejsFunction(self, "whatever")
```

## Contributing

Just submit a PR.
