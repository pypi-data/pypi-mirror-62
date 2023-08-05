# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_policy import policy

from keystone.common.policies import base

mapping_policies = [
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'create_mapping',
        check_str=base.RULE_ADMIN_REQUIRED,
        # FIXME(lbragstad): Today, keystone doesn't support federation unless
        # the person create identity providers, service providers, or mappings
        # has the ability to modify keystone and Apache configuration files.
        # If, or when, keystone adds support for federating identities without
        # having to touch system configuration files, the list of `scope_types`
        # for these policies should include `project`.
        scope_types=['system'],
        description=('Create a new federated mapping containing one or '
                     'more sets of rules.'),
        operations=[{'path': '/v3/OS-FEDERATION/mappings/{mapping_id}',
                     'method': 'PUT'}]),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'get_mapping',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='Get a federated mapping.',
        operations=[
            {
                'path': '/v3/OS-FEDERATION/mappings/{mapping_id}',
                'method': 'GET'
            },
            {
                'path': '/v3/OS-FEDERATION/mappings/{mapping_id}',
                'method': 'HEAD'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'list_mappings',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='List federated mappings.',
        operations=[
            {
                'path': '/v3/OS-FEDERATION/mappings',
                'method': 'GET'
            },
            {
                'path': '/v3/OS-FEDERATION/mappings',
                'method': 'HEAD'
            }
        ]
    ),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'delete_mapping',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='Delete a federated mapping.',
        operations=[{'path': '/v3/OS-FEDERATION/mappings/{mapping_id}',
                     'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        name=base.IDENTITY % 'update_mapping',
        check_str=base.RULE_ADMIN_REQUIRED,
        scope_types=['system'],
        description='Update a federated mapping.',
        operations=[{'path': '/v3/OS-FEDERATION/mappings/{mapping_id}',
                     'method': 'PATCH'}])
]


def list_rules():
    return mapping_policies
