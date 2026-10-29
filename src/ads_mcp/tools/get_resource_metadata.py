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

"""Tools for fetching metadata for Google Ads resources."""

from typing import Annotated, Any, Dict
from pydantic import Field
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
import ads_mcp.utils as utils

metadata_mcp = FastMCP("metadata")


@metadata_mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_resource_metadata(
    resource_name: Annotated[
        str,
        Field(
            description="The name of the Google Ads resource (e.g., 'campaign', 'ad_group')."
        ),
    ],
    login_customer_id: Annotated[
        str | int | None,
        Field(
            description="Optional manager customer ID to use as the login-customer-id header."
        ),
    ] = None,
) -> Dict[str, Any]:
    """Retrieves the selectable, filterable, and sortable fields for a specific Google Ads resource."""
    ga_service = utils.get_googleads_service(
        "GoogleAdsFieldService", login_customer_id=login_customer_id
    )
    request = utils.get_googleads_type("SearchGoogleAdsFieldsRequest")

    selectable = set()
    filterable = set()
    sortable = set()

    attributes_query = f"SELECT name, selectable, filterable, sortable WHERE name LIKE '{resource_name}.%' AND category = 'ATTRIBUTE'"
    request.query = attributes_query
    try:
        attributes_response = ga_service.search_google_ads_fields(
            request=request
        )
        for field in attributes_response:
            if field.selectable:
                selectable.add(field.name)
            if field.filterable:
                filterable.add(field.name)
            if field.sortable:
                sortable.add(field.name)
    except Exception as e:
        utils.logger.warning(f"Failed attributes query: {e}")
        fallback_query = f"SELECT name, selectable, filterable, sortable WHERE name LIKE '{resource_name}.%'"
        request.query = fallback_query
        try:
            attributes_response = ga_service.search_google_ads_fields(
                request=request
            )
            for field in attributes_response:
                if field.name.startswith(f"{resource_name}."):
                    if field.selectable:
                        selectable.add(field.name)
                    if field.filterable:
                        filterable.add(field.name)
                    if field.sortable:
                        sortable.add(field.name)
        except Exception as e2:
            utils.logger.error(f"Fallback attributes query failed: {e2}")
            raise RuntimeError(
                f"API call to search_google_ads_fields failed: {e2}"
            )

    metrics_segments_query = f"SELECT name, selectable, filterable, sortable WHERE selectable_with CONTAINS ANY('{resource_name}')"
    request.query = metrics_segments_query
    try:
        metrics_segments_response = ga_service.search_google_ads_fields(
            request=request
        )
        for field in metrics_segments_response:
            if field.selectable:
                selectable.add(field.name)
            if field.filterable:
                filterable.add(field.name)
            if field.sortable:
                sortable.add(field.name)
    except Exception as e:
        utils.logger.warning(f"Failed metrics/segments query: {e}")

    return {
        "resource": resource_name,
        "selectable": sorted(list(selectable)),
        "filterable": sorted(list(filterable)),
        "sortable": sorted(list(sortable)),
    }
