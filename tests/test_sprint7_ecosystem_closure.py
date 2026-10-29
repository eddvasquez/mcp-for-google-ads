"""Unit tests for Sprint 7 tools: landing message match, offline conversion upload, and budget scaling."""

from decimal import Decimal
from unittest.mock import MagicMock, patch
import unittest

from ads_mcp.tools import intelligence


class TestSprint7Tools(unittest.TestCase):
    @patch("urllib.request.urlopen")
    @patch("ads_mcp.tools.intelligence.changes.query")
    @patch("ads_mcp.tools.intelligence.changes.customer")
    def test_audit_landing_page_message_match(
        self, mock_customer, mock_query, mock_urlopen
    ):
        mock_customer.side_effect = lambda cid: cid

        # Mock active RSA headlines query
        mock_query.return_value = [
            {
                "ad_group_ad.ad.responsive_search_ad.headlines": [
                    {"text": "Consulta Urgente de Pareja"},
                    {"text": "Especialistas en Crisis Emocional"},
                ],
                "ad_group_ad.ad.final_urls": ["https://example.com/consulta"],
                "ad_group_ad.status": "ENABLED",
            }
        ]

        # Mock HTML response
        html_bytes = b"""
        <html>
            <head><title>Terapia y Consulta de Pareja Urgente</title></head>
            <body>
                <h1>Consulta Urgente de Pareja y Crisis</h1>
                <h2>Especialistas calificados para reconciliacion</h2>
                <a href="https://wa.me/123456789">Escribenos por WhatsApp</a>
            </body>
        </html>
        """
        mock_resp = MagicMock()
        mock_resp.read.return_value = html_bytes
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.__exit__.return_value = False
        mock_urlopen.return_value = mock_resp

        res = intelligence.audit_landing_page_message_match(
            "123", campaign_id="999"
        )
        self.assertEqual(
            res["target_landing_url"], "https://example.com/consulta"
        )
        self.assertEqual(
            res["h1_headings"], ["Consulta Urgente de Pareja y Crisis"]
        )
        self.assertTrue(res["conversion_elements"]["has_whatsapp_cta"])
        self.assertEqual(res["verdict"], "STRONG_MESSAGE_MATCH")
        self.assertGreaterEqual(res["message_match_overlap_pct"], 40.0)

    @patch("ads_mcp.utils.get_googleads_service")
    @patch("ads_mcp.utils.get_googleads_type")
    @patch("ads_mcp.tools.intelligence.changes.customer")
    def test_upload_offline_conversion_call(
        self, mock_customer, mock_get_type, mock_get_service
    ):
        mock_customer.side_effect = lambda cid: cid

        mock_conversion = MagicMock()
        mock_request = MagicMock()

        def mock_type_factory(name):
            if name == "ClickConversion":
                return mock_conversion
            return mock_request

        mock_get_type.side_effect = mock_type_factory

        mock_service = MagicMock()
        mock_upload_response = MagicMock()
        mock_upload_response.partial_failure_error = None
        mock_service.upload_click_conversions.return_value = (
            mock_upload_response
        )
        mock_get_service.return_value = mock_service

        res = intelligence.upload_offline_conversion_call(
            customer_id="123",
            gclid="test_gclid_12345",
            conversion_action="987654",
            conversion_date_time="2026-10-28 14:30:00+00:00",
            conversion_value=150000.0,
            currency_code="COP",
        )

        self.assertEqual(res["status"], "SUCCESS_UPLOADED")
        self.assertEqual(res["gclid"], "test_gclid_12345")
        self.assertEqual(
            res["conversion_action"], "customers/123/conversionActions/987654"
        )

    @patch("ads_mcp.tools.intelligence.changes.query")
    @patch("ads_mcp.tools.intelligence.changes.customer")
    def test_simulate_budget_scaling_elasticity(
        self, mock_customer, mock_query
    ):
        mock_customer.side_effect = lambda cid: cid

        # Scenario: 40% lost to budget, 10% lost to rank -> SAFE_FOR_AGGRESSIVE_SCALE
        mock_query.return_value = [
            {
                "campaign.id": "111",
                "campaign.name": "Search Escala High Ticket",
                "campaign_budget.amount_micros": 100_000_000,  # 100 daily
                "metrics.search_impression_share": 0.50,
                "metrics.search_budget_lost_impression_share": 0.40,
                "metrics.search_rank_lost_impression_share": 0.10,
                "metrics.cost_micros": 500_000_000,
                "metrics.clicks": 100,
                "metrics.conversions": 10.0,
                "metrics.cost_per_conversion": 50_000_000,  # 50 CPA
            }
        ]

        res = intelligence.simulate_budget_scaling_elasticity(
            customer_id="123",
            campaign_id="111",
            proposed_budget_increase_pct=30.0,
            target_max_cpa=70.0,
        )

        self.assertEqual(res["scale_verdict"], "SAFE_FOR_AGGRESSIVE_SCALE")
        self.assertEqual(res["scaling_efficiency"], "HIGH")
        self.assertEqual(res["proposed_daily_budget"], "130.00")
        self.assertTrue(res["unit_economics_safe"])


if __name__ == "__main__":
    unittest.main()
