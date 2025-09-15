# AWS Lambda Tool MCP Server

A Model Context Protocol (MCP) server for AWS Lambda to select and run Lambda function as MCP tools without code changes.

## Features

This MCP server acts as a **bridge** between MCP clients and AWS Lambda functions, allowing generative AI models to access and run Lambda functions as tools. This is useful, for example, to access private resources such as internal applications and databases without the need to provide public network access. This approach allows the model to use other AWS services, private networks, and the public internet.

```mermaid
graph LR
    A[Model] <--> B[MCP Client]
    B <--> C["MCP2Lambda<br>(MCP Server)"]
    C <--> D[Lambda Function]
    D <--> E[Other AWS Services]
    D <--> F[Internet]
    D <--> G[VPC]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:4px
    style D fill:#fbb,stroke:#333,stroke-width:2px
    style E fill:#fbf,stroke:#333,stroke-width:2px
    style F fill:#dff,stroke:#333,stroke-width:2px
    style G fill:#ffd,stroke:#333,stroke-width:2px
```

From a **security** perspective, this approach implements segregation of duties by allowing the model to invoke the Lambda functions but not to access the other AWS services directly. The client only needs AWS credentials to invoke the Lambda functions. The Lambda functions can then interact with other AWS services (using the function role) and access public or private networks.

## Prerequisites

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python using `uv python install 3.10`

## Installation

| Cursor | VS Code |
|:------:|:-------:|
| [![Install MCP Server](https://cursor.com/deeplink/mcp-install-light.svg)](https://cursor.com/en/install-mcp?name=awslabs.lambda-tool-mcp-server&config=eyJjb21tYW5kIjoidXZ4IGF3c2xhYnMubGFtYmRhLXRvb2wtbWNwLXNlcnZlckBsYXRlc3QiLCJlbnYiOnsiQVdTX1BST0ZJTEUiOiJ5b3VyLWF3cy1wcm9maWxlIiwiQVdTX1JFR0lPTiI6InVzLWVhc3QtMSIsIkZVTkNUSU9OX1BSRUZJWCI6InlvdXItZnVuY3Rpb24tcHJlZml4IiwiRlVOQ1RJT05fTElTVCI6InlvdXItZmlyc3QtZnVuY3Rpb24sIHlvdXItc2Vjb25kLWZ1bmN0aW9uIiwiRlVOQ1RJT05fVEFHX0tFWSI6InlvdXItdGFnLWtleSIsIkZVTkNUSU9OX1RBR19WQUxVRSI6InlvdXItdGFnLXZhbHVlIiwiRlVOQ1RJT05fSU5QVVRfU0NIRU1BX0FSTl9UQUdfS0VZIjoieW91ci1mdW5jdGlvbi10YWctZm9yLWlucHV0LXNjaGVtYSJ9fQ%3D%3D) | [![Install on VS Code](https://img.shields.io/badge/Install_on-VS_Code-FF9900?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=AWS%20Lambda%20Tool%20MCP%20Server&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22awslabs.lambda-tool-mcp-server%40latest%22%5D%2C%22env%22%3A%7B%22AWS_PROFILE%22%3A%22your-aws-profile%22%2C%22AWS_REGION%22%3A%22us-east-1%22%2C%22FUNCTION_PREFIX%22%3A%22your-function-prefix%22%2C%22FUNCTION_LIST%22%3A%22your-first-function%2C%20your-second-function%22%2C%22FUNCTION_TAG_KEY%22%3A%22your-tag-key%22%2C%22FUNCTION_TAG_VALUE%22%3A%22your-tag-value%22%2C%22FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY%22%3A%22your-function-tag-for-input-schema%22%7D%7D) |

Configure the MCP server in your MCP client configuration (e.g., for Amazon Q Developer CLI, edit `~/.aws/amazonq/mcp.json`):

```json
{
  "mcpServers": {
    "awslabs.lambda-tool-mcp-server": {
      "command": "uvx",
      "args": ["awslabs.lambda-tool-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-east-1",
        "FUNCTION_PREFIX": "your-function-prefix",
        "FUNCTION_LIST": "your-first-function, your-second-function",
        "FUNCTION_TAG_KEY": "your-tag-key",
        "FUNCTION_TAG_VALUE": "your-tag-value",
        "FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY": "your-function-tag-for-input-schema"
      }
    }
  }
}
```

### Windows Installation

For Windows users, the MCP server configuration format is slightly different:

```json
{
  "mcpServers": {
    "awslabs.lambda-tool-mcp-server": {
      "disabled": false,
      "timeout": 60,
      "type": "stdio",
      "command": "uv",
      "args": [
        "tool",
        "run",
        "--from",
        "awslabs.lambda-tool-mcp-server@latest",
        "awslabs.lambda-tool-mcp-server.exe"
      ],
      "env": {
        "AWS_PROFILE": "your-aws-profile",
        "AWS_REGION": "us-east-1",
        "FUNCTION_PREFIX": "your-function-prefix",
        "FUNCTION_LIST": "your-first-function, your-second-function",
        "FUNCTION_TAG_KEY": "your-tag-key",
        "FUNCTION_TAG_VALUE": "your-tag-value",
        "FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY": "your-function-tag-for-input-schema"
      }
    }
  }
}
```

or docker after a successful `docker build -t awslabs/bedrock-kb-retrieval-mcp-server .`:

```file
# fictitious `.env` file with AWS temporary credentials
AWS_ACCESS_KEY_ID=ASIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_SESSION_TOKEN=AQoEXAMPLEH4aoAH0gNCAPy...truncated...zrkuWJOgQs8IZZaIv2BXIa2R4Olgk
```

```json
  {
    "mcpServers": {
      "awslabs.lambda-tool-mcp-server": {
        "command": "docker",
        "args": [
          "run",
          "--rm",
          "--interactive",
          "--env",
          "AWS_REGION=us-east-1",
          "--env",
          "FUNCTION_PREFIX=your-function-prefix",
          "--env",
          "FUNCTION_LIST=your-first-function,your-second-function",
          "--env",
          "FUNCTION_TAG_KEY=your-tag-key",
          "--env",
          "FUNCTION_TAG_VALUE=your-tag-value",
          "--env",
          "FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY=your-function-tag-for-input-schema",
          "--env-file",
          "/full/path/to/file/above/.env",
          "awslabs/lambda-tool-mcp-server:latest"
        ],
        "env": {},
        "disabled": false,
        "autoApprove": []
      }
    }
  }
```

NOTE: Your credentials will need to be kept refreshed from your host

The `AWS_PROFILE` and the `AWS_REGION` are optional, their default values are `default` and `us-east-1`.

You can specify `FUNCTION_PREFIX`, `FUNCTION_LIST`, or both. If both are empty, all functions pass the name check.
After the name check, if both `FUNCTION_TAG_KEY` and `FUNCTION_TAG_VALUE` are set, functions are further filtered by tag (with key=value).
If only one of `FUNCTION_TAG_KEY` and `FUNCTION_TAG_VALUE`, then no function is selected and a warning is displayed.

**IMPORTANT**: The function name is used as MCP tool name. The function description in AWS Lambda is used as MCP tool description. The function description should clarify when to use the function (what it provides) and how (which parameters). For example, a function that gives access to an internal Customer Relationship Management (CRM) system can use this description:
```plaintext
Retrieve customer status on the CRM system based on { 'customerId' } or { 'customerEmail' }
```

The lambda function parameters can also be provided through the EventBridge Schema Registry, which provides formal JSON Schema. See [Schema Support](#schema-support) below.

Sample functions that can be deployed via AWS SAM are provided in the `examples` folder.

## Schema Support

The Lambda MCP Server supports input schema through AWS EventBridge Schema Registry. This provides formal JSON Schema documentation for your Lambda function inputs.

### Configuration

To use schema validation:

1. Create your schema in EventBridge Schema Registry
2. Tag your Lambda function with the schema ARN:
   ```plaintext
   Key: FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY (configurable)
   Value: arn:aws:schemas:region:account:schema/registry-name/schema-name
   ```
3. Configure the MCP server with the tag key:
   ```json
   {
     "env": {
       "FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY": "your-schema-arn-tag-key"
     }
   }
   ```

When a Lambda function has a schema tag, the MCP server will:
1. Fetch the schema from EventBridge Schema Registry
2. Add the schema to the tool's documentation

This provides better documentation compared to describing parameters in the function description.

## Best practices

- Use the `FUNCTION_LIST` to specify the functions that are available as MCP tools.
- Use the `FUNCTION_PREFIX` to specify the prefix of the functions that are available as MCP tools.
- Use the `FUNCTION_TAG_KEY` and `FUNCTION_TAG_VALUE` to specify the tag key and value of the functions that are available as MCP tools.
- AWS Lambda `Description` property: the description of the function is used as MCP tool description, so it should be very detailed to help the model understand when and how to use the function
- Use EventBridge Schema Registry to provide formal input validation:
  - Create JSON Schema definitions for your function inputs
  - Tag functions with their schema ARNs
  - Configure `FUNCTION_INPUT_SCHEMA_ARN_TAG_KEY` in the MCP server

## Security Considerations

When using this MCP server, you should consider:

- Only Lambda functions that are in the provided list or with a name starting with the prefix are imported as MCP tools.
- The MCP server needs permissions to invoke the Lambda functions.
- Each Lambda function has its own permissions to optionally access other AWS resources.
