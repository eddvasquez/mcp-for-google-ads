"""Offline backend tests for safe preflight recovery versus uncertain dispatch."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from google.api_core import exceptions as errors
from fastmcp.exceptions import ToolError
from ads_mcp.extensions import changes as ch


class PreflightRecoveryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        env = patch.dict('os.environ', {'GOOGLE_ADS_MCP_PROPOSALS_DB': str(Path(temp.name) / 'proposals.db')})
        env.start(); self.addCleanup(env.stop)
        self.plan = ch.Store().create({'customer_id':'1234567890','currency_code':'COP',
            'login_customer_id':None,'operations':[], 'watches':[{'before':[]}], 'checks':[]})
        self.dispatches = []
        def mutate(cid, operations, login, validate_only):
            self.dispatches.append(validate_only)
            return SimpleNamespace(partial_failure_error=SimpleNamespace(code=0), mutate_operation_responses=[])
        for p in (patch.object(ch, 'mutate', side_effect=mutate), patch.object(ch, 'limits'),
                  patch.object(ch, 'verify', return_value={'verified':True}), patch.object(ch.time, 'sleep')):
            p.start(); self.addCleanup(p.stop)

    def test_transient_read_retries_only_preflight_then_sends_once(self):
        with patch.object(ch, 'reread', side_effect=[errors.ServiceUnavailable('network'), errors.ServiceUnavailable('network'), []]) as read:
            result = ch.apply(self.plan['plan_id'], True)
        self.assertEqual(result['state'], 'APPLIED')
        self.assertEqual(read.call_count, 3)
        self.assertEqual(self.dispatches, [True, False])

    def test_persistent_preflight_error_records_proof_of_no_dispatch(self):
        with patch.object(ch, 'reread', side_effect=errors.ServiceUnavailable('network')):
            with self.assertRaises(errors.ServiceUnavailable):
                ch.apply(self.plan['plan_id'], True)
        saved = ch.Store().get(self.plan['plan_id'])
        self.assertEqual(saved['state'], 'PREFLIGHT_RETRYABLE')
        self.assertEqual(saved['result']['error']['dispatch_certainty'], 'NOT_SENT')
        self.assertFalse(self.dispatches)

    def test_inventory_changed_remains_rejected_and_never_sends(self):
        with patch.object(ch, 'reread', return_value=[{'changed':True}]):
            with self.assertRaises(ToolError):
                ch.apply(self.plan['plan_id'], True)
        saved = ch.Store().get(self.plan['plan_id'])
        self.assertEqual(saved['state'], 'REJECTED')
        self.assertFalse(saved['result']['error']['retryable'])
        self.assertFalse(self.dispatches)

    def test_expiry_is_explicit_and_has_no_dispatch(self):
        with ch.Store().connect() as db:
            db.execute('UPDATE proposals SET created=0 WHERE id=?', (self.plan['plan_id'],))
        with self.assertRaises(ToolError):
            ch.apply(self.plan['plan_id'], True)
        self.assertEqual(ch.Store().get(self.plan['plan_id'])['state'], 'EXPIRED')
        self.assertFalse(self.dispatches)

    def test_timeout_during_actual_mutation_is_never_retried(self):
        attempts = []
        def mutate(cid, operations, login, validate_only):
            attempts.append(validate_only)
            if not validate_only:
                raise errors.ServiceUnavailable('response lost after dispatch')
        with patch.object(ch, 'reread', return_value=[]), patch.object(ch, 'mutate', side_effect=mutate):
            with self.assertRaises(ToolError):
                ch.apply(self.plan['plan_id'], True)
            with self.assertRaises(ToolError):
                ch.apply(self.plan['plan_id'], True)
        self.assertEqual(attempts, [True, False])
        self.assertEqual(ch.Store().get(self.plan['plan_id'])['state'], 'UNKNOWN')
