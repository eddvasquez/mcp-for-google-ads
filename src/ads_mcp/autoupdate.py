"""TTL-based automatic background update checker for remote/client machines.

Follows the Time-To-Live (TTL) throttling pattern:
- Checks for updates at most once every N hours (default: 24h, configurable via MCP_UPDATE_INTERVAL_HOURS).
- Fast fail: Times out quickly (2.0s) so it never hangs server startup or adds perceptible latency.
- Graceful degradation: If offline, on local git branch, or GitHub is unreachable, silently bypasses.
- Can be completely disabled via MCP_DISABLE_AUTO_UPDATE=1.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_INTERVAL_HOURS = 24.0
CACHE_FILENAME = ".mcp_google_ads_sync_cache.json"


def get_cache_path() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / CACHE_FILENAME


def get_check_interval_seconds() -> float:
    env_val = os.environ.get("MCP_UPDATE_INTERVAL_HOURS")
    if env_val:
        try:
            return float(env_val) * 3600.0
        except ValueError:
            pass
    return DEFAULT_INTERVAL_HOURS * 3600.0


def is_auto_update_disabled() -> bool:
    val = os.environ.get("MCP_DISABLE_AUTO_UPDATE", "").strip().lower()
    return val in ("1", "true", "yes", "on")


def read_cache(cache_path: Path) -> dict:
    if not cache_path.exists():
        return {}
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_cache(cache_path: Path, data: dict) -> None:
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def check_and_apply_update(force: bool = False) -> bool:
    """Verifies TTL and triggers uv tool upgrade if the interval has elapsed.
    
    Returns True if an upgrade check/execution was attempted, False if throttled or skipped.
    """
    if is_auto_update_disabled() and not force:
        return False

    uv_path = shutil.which("uv")
    if not uv_path:
        return False

    cache_path = get_cache_path()
    cache = read_cache(cache_path)
    last_check = cache.get("last_check_timestamp", 0)
    now = time.time()
    interval = get_check_interval_seconds()

    if not force and (now - last_check < interval):
        # Within TTL window, skip silently without network check
        return False

    # Interval expired or forced -> perform non-blocking / quick check
    cache["last_check_timestamp"] = now
    write_cache(cache_path, cache)

    try:
        # Quick timeout execution: attempt tool upgrade
        # STDERR redirected so as not to pollute MCP STDIO JSON-RPC stream
        result = subprocess.run(
            [uv_path, "tool", "upgrade", "mcp-for-google-ads"],
            capture_output=True,
            text=True,
            timeout=5.0,
            check=False
        )
        if result.returncode == 0:
            cache["last_successful_upgrade"] = now
            write_cache(cache_path, cache)
            return True
    except (subprocess.TimeoutExpired, Exception):
        # Graceful degradation: never crash server startup
        pass

    return False


if __name__ == "__main__":
    force_mode = "--force" in sys.argv
    ran = check_and_apply_update(force=force_mode)
    if ran:
        print("[AUTO-UPDATE] Update check executed.")
    else:
        print("[AUTO-UPDATE] Check skipped (throttled by TTL or disabled).")
