# Copyright 2026 Edd Vásquez. All rights reserved.
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

"""Core account discovery tools for Google Ads."""

from typing import List
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

import ads_mcp.utils as utils

customers_mcp = FastMCP("customers")


@customers_mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=True),
    description=(
        "Returns customer IDs directly accessible by the authenticated identity.\n\n"
        "Use this tool to discover available customer accounts before running queries.\n"
        "Returns:\n    List[str]: List of numeric Google Ads customer IDs."
    ),
)
def list_accessible_customers() -> List[str]:
    """Retrieve accessible Google Ads customer IDs."""
    customer_service = utils.get_googleads_service("CustomerService")
    response = customer_service.list_accessible_customers()
    return [rn.removeprefix("customers/") for rn in response.resource_names]
