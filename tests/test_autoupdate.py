import json
import time
from pathlib import Path
from ads_mcp import autoupdate


def test_autoupdate_cache_path(tmp_path, monkeypatch):
    """Verify cache path detection in user directory."""
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    cache_path = autoupdate.get_cache_path()
    assert cache_path == tmp_path / autoupdate.CACHE_FILENAME


def test_autoupdate_ttl_throttling(tmp_path, monkeypatch):
    """Verify that update checks within the TTL interval are skipped silently."""
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("MCP_UPDATE_INTERVAL_HOURS", "24")
    
    cache_path = autoupdate.get_cache_path()
    now = time.time()
    
    # Write cache indicating check occurred 1 hour ago
    autoupdate.write_cache(cache_path, {"last_check_timestamp": now - 3600})
    
    # Check should be throttled (returns False, does not invoke uv)
    attempted = autoupdate.check_and_apply_update(force=False)
    assert attempted is False


def test_autoupdate_interval_expired(tmp_path, monkeypatch):
    """Verify that when TTL interval expires, update check is triggered."""
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("MCP_UPDATE_INTERVAL_HOURS", "24")
    
    cache_path = autoupdate.get_cache_path()
    now = time.time()
    
    # Write cache indicating check occurred 25 hours ago (>24h)
    autoupdate.write_cache(cache_path, {"last_check_timestamp": now - (25 * 3600)})
    
    # Mock uv tool upgrade to succeed without hitting actual GitHub
    class MockResult:
        returncode = 0
        stdout = "Upgraded"
        stderr = ""
        
    def mock_run(*args, **kwargs):
        return MockResult()
        
    monkeypatch.setattr(autoupdate.subprocess, "run", mock_run)
    monkeypatch.setattr(autoupdate.shutil, "which", lambda x: "C:\\mock\\uv.exe")
    
    attempted = autoupdate.check_and_apply_update(force=False)
    assert attempted is True
    
    # Cache should now have updated last_check_timestamp
    updated_cache = autoupdate.read_cache(cache_path)
    assert updated_cache["last_check_timestamp"] >= now


def test_autoupdate_disabled_via_env(tmp_path, monkeypatch):
    """Verify that MCP_DISABLE_AUTO_UPDATE completely turns off checking."""
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("MCP_DISABLE_AUTO_UPDATE", "1")
    
    attempted = autoupdate.check_and_apply_update(force=False)
    assert attempted is False
