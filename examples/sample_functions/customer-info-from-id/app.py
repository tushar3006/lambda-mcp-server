# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def lambda_handler(event: dict, context: dict) -> dict:
    """AWS Lambda function to retrieve customer information based on customer ID.

    Args:
        event (dict): The Lambda event object containing the customer ID
                      Expected format: {"customerId": "123"}
        context (dict): AWS Lambda context object

    Returns:
        dict: Customer information if found, otherwise an error message
              Success format: {"customerId": "123", "name": "John Doe", "email": "john@example.com", ...}
              Error format: {"error": "Customer not found"}
    """
    try:
        # Extract customer ID from the event
        customer_id = event.get('customerId')

        if not customer_id:
            return {'error': 'Missing customerId parameter'}

        # This would normally query a database
        # For demo purposes, we'll return mock data

        # Simulate database lookup
        match customer_id:
            case '12345':
                return {
                    'customerId': '12345',
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'phone': '+1-555-123-4567',
                    'address': {
                        'street': '123 Main St',
                        'city': 'Anytown',
                        'state': 'CA',
                        'zipCode': '12345',
                    },
                    'accountCreated': '2022-01-15',
                }
            case '54321':
                return {
                    'customerId': '54321',
                    'name': 'Jane Smith',
                    'email': 'jane.smith@example.com',
                    'phone': '+1-555-987-6543',
                    'address': {
                        'street': '456 Oak Ave',
                        'city': 'Othertown',
                        'state': 'NY',
                        'zipCode': '67890',
                    },
                    'accountCreated': '2022-02-20',
                }
            case _:
                return {'error': 'Customer not found'}

    except Exception as e:
        return {'error': str(e)}
