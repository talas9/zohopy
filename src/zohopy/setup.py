"""OAuth setup helpers — generate refresh tokens for Zoho APIs.

Supports two OAuth flows:

**Self Client** (simplest, no redirect URL):
    1. Generate a grant code in the Zoho API Console UI
    2. Call :func:`exchange_grant_token` with client_id, client_secret, code
    3. Get back a permanent refresh_token + api_domain

**Server-based (localhost redirect)**:
    1. Provide client_id, client_secret, and scopes
    2. Call :func:`authorize_with_browser` — opens browser, starts local server
    3. User approves in browser → Zoho redirects to localhost
    4. Browser shows org picker → user selects org
    5. Tokens + org saved to .env automatically

Run the interactive wizard::

    python -m zohopy
"""

from __future__ import annotations

import http.server
import json
import socketserver
import sys
import threading
import urllib.parse
import webbrowser
from typing import Any

import httpx

from zohopy.config import DataCenter
from zohopy.exceptions import ZohoTokenRefreshError

__version__ = "0.1.0"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_REGION_ACCOUNTS: dict[str, str] = {dc.value: dc.accounts_url for dc in DataCenter}
_DEFAULT_SCOPES = "ZohoBooks.fullaccess.all,ZohoInventory.fullaccess.all"
_LOCALHOST_PORT = 11470
_LOCALHOST_REDIRECT = f"http://localhost:{_LOCALHOST_PORT}/callback"

# ---------------------------------------------------------------------------
# HTML templates
# ---------------------------------------------------------------------------

_PAGE_SHELL = (
    """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZohoPy — {title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 24px;
  }}
  .card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 40px;
    width: 100%;
    max-width: 520px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3);
  }}
  .header {{
    text-align: center;
    margin-bottom: 28px;
  }}
  .header .icon {{ font-size: 40px; margin-bottom: 8px; }}
  .header h1 {{
    font-size: 22px;
    font-weight: 600;
    color: #f1f5f9;
    letter-spacing: -0.3px;
  }}
  .header .version {{
    font-size: 12px;
    color: #64748b;
    margin-top: 2px;
  }}
  hr {{
    border: none;
    border-top: 1px solid #334155;
    margin: 20px 0;
  }}
  .status {{
    text-align: center;
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 16px;
  }}
  .status.success {{ color: #4ade80; }}
  .status.error {{ color: #f87171; }}
  .status.info {{ color: #60a5fa; }}
  .detail {{
    font-size: 13px;
    color: #94a3b8;
    text-align: center;
    line-height: 1.6;
  }}
  .org-list {{
    list-style: none;
    margin: 16px 0 0;
  }}
  .org-list li {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .org-list li:hover {{
    border-color: #60a5fa;
    background: #1a2744;
  }}
  .org-list li.selected {{
    border-color: #4ade80;
    background: #132a1e;
  }}
  .org-name {{
    font-size: 14px;
    font-weight: 500;
    color: #f1f5f9;
  }}
  .org-id {{
    font-size: 12px;
    color: #64748b;
    font-family: 'SF Mono', Consolas, monospace;
  }}
  .spinner {{
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid #334155;
    border-top-color: #60a5fa;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
    margin-right: 8px;
    vertical-align: middle;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .done-msg {{
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #94a3b8;
  }}
  .check {{ color: #4ade80; font-size: 18px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="icon">{icon}</div>
    <h1>ZohoPy</h1>
    <div class="version">v"""
    + __version__
    + """</div>
  </div>
  <hr>
  {body}
</div>
{script}
</body>
</html>"""
)


def _page(*, title: str, icon: str, body: str, script: str = "") -> str:
    return _PAGE_SHELL.format(title=title, icon=icon, body=body, script=script)


def _error_page(error: str) -> str:
    return _page(
        title="Error",
        icon="&#x26A0;&#xFE0F;",
        body=f'<div class="status error">Authorization failed: {error}</div>'
        f'<p class="detail">Check the error and try again.</p>',
    )


def _loading_page() -> str:
    return _page(
        title="Authorizing...",
        icon="&#x1F511;",
        body='<div class="status info"><span class="spinner"></span>'
        '<span id="msg">Exchanging tokens...</span></div>'
        '<p class="detail">This takes a few seconds.</p>',
        script="""\
<script>
(function poll() {
  fetch('/status').then(r => r.json()).then(data => {
    if (data.ready) {
      location.href = '/callback';
    } else {
      document.getElementById('msg').textContent = data.message || 'Working...';
      setTimeout(poll, 1500);
    }
  }).catch(() => setTimeout(poll, 2000));
})();
</script>""",
    )


def _org_picker_page(orgs: list[dict[str, Any]], dc: str) -> str:
    if not orgs:
        return _page(
            title="Setup",
            icon="&#x1F511;",
            body='<div class="status success">&#x2714; Authorized</div>'
            '<p class="detail">No organizations found. Check your Zoho account.</p>',
        )

    items = ""
    for org in orgs:
        oid = org.get("organization_id", "")
        name = org.get("name", "")
        items += (
            f"<li onclick=\"pick('{oid}', this)\">"
            f'<span class="org-name">{name}</span>'
            f'<span class="org-id">{oid}</span>'
            f"</li>\n"
        )

    script = (
        """\
<script>
function pick(orgId, el) {
  document.querySelectorAll('.org-list li').forEach(li => li.classList.remove('selected'));
  el.classList.add('selected');
  el.innerHTML = '<span class="org-name">' + el.querySelector('.org-name').textContent +
    '</span><span class="check">&#x2714;</span>';

  fetch('/select-org', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({organization_id: orgId})
  }).then(r => r.json()).then(data => {
    document.querySelector('.card').innerHTML =
      '<div class="header"><div class="icon">&#x2705;</div>' +
      '<h1>ZohoPy</h1><div class="version">v"""
        + __version__
        + """</div></div><hr>' +
      '<div class="status success">Setup complete</div>' +
      '<p class="done-msg">' +
      '<b>Organization:</b> ' + data.org_name + '<br>' +
      '<b>Data center:</b> ' + data.data_center + '<br><br>' +
      'Configuration saved to <code>.env</code><br>' +
      'You can close this tab.</p>';
  });
}
</script>"""
    )

    return _page(
        title="Select Organization",
        icon="&#x1F511;",
        body=(
            '<div class="status success">&#x2714; Authorized</div>'
            f'<p class="detail">Data center: <b>{dc}</b> — Select your organization:</p>'
            f'<ul class="org-list">{items}</ul>'
        ),
        script=script,
    )


# ---------------------------------------------------------------------------
# Core token exchange (works for both Self Client and Server-based)
# ---------------------------------------------------------------------------


def exchange_grant_token(
    *,
    client_id: str,
    client_secret: str,
    grant_token: str,
    redirect_uri: str | None = None,
    accounts_url: str = "https://accounts.zoho.com",
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Exchange a grant token (authorization code) for access + refresh tokens.

    Args:
        client_id: OAuth client ID.
        client_secret: OAuth client secret.
        grant_token: The authorization code.
        redirect_uri: Required for Server-based apps.
        accounts_url: Zoho accounts server for your region.
        timeout: HTTP timeout in seconds.

    Returns:
        Dict with ``access_token``, ``refresh_token``, ``api_domain``,
        ``token_type``, ``expires_in``.
    """
    url = f"{accounts_url.rstrip('/')}/oauth/v2/token"
    params: dict[str, str] = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": grant_token,
    }
    if redirect_uri:
        params["redirect_uri"] = redirect_uri

    with httpx.Client(timeout=timeout) as client:
        resp = client.post(url, params=params)

    if resp.status_code != 200:
        raise ZohoTokenRefreshError(f"Token exchange failed (HTTP {resp.status_code}): {resp.text}")

    body: dict[str, Any] = resp.json()
    if "error" in body:
        raise ZohoTokenRefreshError(f"Token exchange error: {body['error']}")

    if "refresh_token" not in body:
        raise ZohoTokenRefreshError(
            "No refresh_token in response. The grant code may have expired, "
            "or access_type=offline was not set. Try generating a new code."
        )

    return body


# ---------------------------------------------------------------------------
# Organization discovery
# ---------------------------------------------------------------------------


def discover_organizations(
    *,
    access_token: str,
    api_domain: str,
    timeout: float = 30.0,
) -> list[dict[str, Any]]:
    """Fetch all organizations accessible by this token."""
    url = f"{api_domain.rstrip('/')}/books/v3/organizations"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}

    with httpx.Client(timeout=timeout) as client:
        resp = client.get(url, headers=headers)

    if resp.status_code != 200:
        raise ZohoTokenRefreshError(
            f"Organization discovery failed (HTTP {resp.status_code}): {resp.text}"
        )

    body = resp.json()
    return body.get("organizations", [])


# ---------------------------------------------------------------------------
# Server-based flow: localhost redirect + org picker
# ---------------------------------------------------------------------------

# Shared state between threads
_state: dict[str, Any] = {}
_code_event = threading.Event()
_org_event = threading.Event()


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handles OAuth redirect callback and org selection."""

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/callback" and "code" in qs:
            _state["grant_code"] = qs["code"][0]
            self._send_html(_loading_page())
            _code_event.set()

        elif parsed.path == "/callback" and "error" in qs:
            error = qs.get("error", ["unknown"])[0]
            _state["error"] = error
            self._send_html(_error_page(error))
            _code_event.set()

        elif parsed.path == "/status":
            ready = _state.get("orgs_ready", False)
            msg = _state.get("status_msg", "Exchanging tokens...")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ready": ready, "message": msg}).encode())

        elif parsed.path == "/callback" and _state.get("orgs_ready"):
            self._send_html(_state["org_page"])

        else:
            self._send_html(_loading_page())

    def do_POST(self) -> None:
        if self.path == "/select-org":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            org_id = body.get("organization_id", "")
            _state["selected_org_id"] = org_id

            # Find org name
            org_name = org_id
            for org in _state.get("orgs", []):
                if str(org.get("organization_id")) == str(org_id):
                    org_name = org.get("name", org_id)
                    break

            response = json.dumps(
                {
                    "org_name": org_name,
                    "data_center": _state.get("data_center", "us"),
                }
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode())

            _org_event.set()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_html(self, html: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format: str, *args: Any) -> None:
        pass


class _ReusableServer(socketserver.ThreadingTCPServer):
    """Threaded server so it can handle refreshes while main thread exchanges tokens."""

    allow_reuse_address = True
    daemon_threads = True


def authorize_with_browser(
    *,
    client_id: str,
    client_secret: str,
    accounts_url: str = "https://accounts.zoho.com",
    scopes: str = _DEFAULT_SCOPES,
    port: int = _LOCALHOST_PORT,
    timeout_seconds: int = 300,
) -> dict[str, Any]:
    """Full browser OAuth flow with org picker.

    1. Opens browser → Zoho consent page
    2. Captures redirect code on localhost
    3. Exchanges for tokens, discovers orgs
    4. Shows org picker in browser
    5. Returns tokens + selected org_id

    Returns:
        Dict with ``access_token``, ``refresh_token``, ``api_domain``,
        ``organization_id``, ``organization_name``, ``data_center``.
    """
    redirect_uri = f"http://localhost:{port}/callback"

    # Reset shared state
    _state.clear()
    _code_event.clear()
    _org_event.clear()

    # Build auth URL
    auth_params = urllib.parse.urlencode(
        {
            "scope": scopes,
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    auth_url = f"{accounts_url}/oauth/v2/auth?{auth_params}"

    # Start local server
    server = _ReusableServer(("localhost", port), _CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        print("Opening browser for authorization...")
        print(f"If the browser doesn't open, visit:\n  {auth_url}\n")
        webbrowser.open(auth_url)

        # Wait for OAuth callback
        if not _code_event.wait(timeout=timeout_seconds):
            raise ZohoTokenRefreshError(
                f"Timed out waiting for authorization ({timeout_seconds}s)."
            )

        if "error" in _state:
            raise ZohoTokenRefreshError(f"Authorization denied: {_state['error']}")

        grant_code = _state["grant_code"]

        # Exchange tokens
        _state["status_msg"] = "Exchanging tokens..."
        print("Exchanging tokens...")
        tokens = exchange_grant_token(
            client_id=client_id,
            client_secret=client_secret,
            grant_token=grant_code,
            redirect_uri=redirect_uri,
            accounts_url=accounts_url,
        )

        api_domain = tokens["api_domain"]
        access_token = tokens["access_token"]
        dc = DataCenter.from_api_domain(api_domain)

        print(f"  Data center: {dc.value}")
        _state["status_msg"] = "Discovering organizations..."
        print("Discovering organizations...")

        # Discover orgs
        try:
            orgs = discover_organizations(access_token=access_token, api_domain=api_domain)
        except ZohoTokenRefreshError:
            orgs = []

        _state["orgs"] = orgs
        _state["data_center"] = dc.value

        if len(orgs) == 1:
            # Single org — auto-select, show done page
            org = orgs[0]
            _state["selected_org_id"] = str(org.get("organization_id", ""))
            _state["org_page"] = _page(
                title="Setup Complete",
                icon="&#x2705;",
                body=(
                    '<div class="status success">Setup complete</div>'
                    f'<p class="done-msg">'
                    f"<b>Organization:</b> {org.get('name', '?')}<br>"
                    f"<b>Data center:</b> {dc.value}<br><br>"
                    f"Configuration saved to <code>.env</code><br>"
                    f"You can close this tab.</p>"
                ),
            )
            _state["orgs_ready"] = True
            _org_event.set()
        else:
            # Multiple orgs — show picker
            _state["org_page"] = _org_picker_page(orgs, dc.value)
            _state["orgs_ready"] = True
            print(f"  Found {len(orgs)} organizations — select one in the browser.")

            # Wait for user to pick
            if not _org_event.wait(timeout=timeout_seconds):
                raise ZohoTokenRefreshError("Timed out waiting for org selection.")

        org_id = _state.get("selected_org_id", "")
        org_name = ""
        for org in orgs:
            if str(org.get("organization_id")) == str(org_id):
                org_name = org.get("name", "")
                break

        print(f"  Selected: {org_name} ({org_id})")

        return {
            **tokens,
            "organization_id": org_id,
            "organization_name": org_name,
            "data_center": dc.value,
        }

    finally:
        threading.Thread(target=server.shutdown, daemon=True).start()


# ---------------------------------------------------------------------------
# .env writer
# ---------------------------------------------------------------------------


def write_env(
    *,
    client_id: str,
    client_secret: str,
    refresh_token: str,
    org_id: str,
    api_domain: str,
    data_center: str,
    path: str = ".env",
) -> None:
    """Write credentials to a .env file."""
    content = (
        f"# ZohoPy configuration — generated by setup wizard\n"
        f"ZOHO_CLIENT_ID={client_id}\n"
        f"ZOHO_CLIENT_SECRET={client_secret}\n"
        f"ZOHO_REFRESH_TOKEN={refresh_token}\n"
        f"ZOHO_ORGANIZATION_ID={org_id}\n"
        f"ZOHO_API_DOMAIN={api_domain}\n"
        f"ZOHO_DATA_CENTER={data_center}\n"
    )
    with open(path, "w") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Interactive CLI wizard
# ---------------------------------------------------------------------------


def interactive_setup() -> None:
    """Interactive CLI wizard. Run with ``python -m zohopy``."""
    print("=" * 60)
    print("  ZohoPy — OAuth Setup Wizard")
    print("=" * 60)
    print()
    print("Choose your OAuth flow:")
    print("  1. Self Client — paste a grant code from API Console")
    print("  2. Browser login — opens browser, captures redirect")
    print()

    flow = input("Flow [1/2]: ").strip()
    if flow not in ("1", "2"):
        print("Invalid choice. Defaulting to Self Client (1).")
        flow = "1"

    client_id = input("\nClient ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    if not client_id or not client_secret:
        print("Error: Client ID and Secret are required.")
        sys.exit(1)

    accounts_url = "https://accounts.zoho.com"

    if flow == "1":
        result = _flow_self_client(client_id, client_secret, accounts_url)
        api_domain = result["api_domain"]
        dc = DataCenter.from_api_domain(api_domain)
        # Discover org in terminal
        org_id = _pick_org_terminal(result["access_token"], api_domain)

        write_env(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=result["refresh_token"],
            org_id=org_id,
            api_domain=api_domain,
            data_center=dc.value,
        )
    else:
        result = _flow_browser(client_id, client_secret, accounts_url)

        write_env(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=result["refresh_token"],
            org_id=result["organization_id"],
            api_domain=result["api_domain"],
            data_center=result["data_center"],
        )

    print("\nSetup complete! .env written.")
    print()
    print("  from zohopy import ZohoConfig, SyncZohoClient")
    print("  from zohopy.products.books import ZohoBooks")
    print()
    print("  with SyncZohoClient(ZohoConfig()) as client:")
    print("      books = ZohoBooks(client)")
    print("      print(books.contacts.list())")


def _flow_self_client(
    client_id: str,
    client_secret: str,
    accounts_url: str,
) -> dict[str, Any]:
    print()
    print("Generate a grant code in the API Console:")
    print("  1. Go to https://api-console.zoho.com/ -> your Self Client")
    print("  2. Click 'Generate Code' tab")
    print("  3. Scope: ZohoBooks.fullaccess.all,ZohoInventory.fullaccess.all")
    print("  4. Time Duration: 10 minutes")
    print("  5. Click Create, copy the code")
    print()

    grant_token = input("Grant token (code): ").strip()
    if not grant_token:
        print("Error: Grant token is required.")
        sys.exit(1)

    print("\nExchanging grant token...")
    try:
        return exchange_grant_token(
            client_id=client_id,
            client_secret=client_secret,
            grant_token=grant_token,
            accounts_url=accounts_url,
        )
    except ZohoTokenRefreshError as e:
        print(f"Error: {e}")
        sys.exit(1)


def _flow_browser(
    client_id: str,
    client_secret: str,
    accounts_url: str,
) -> dict[str, Any]:
    print()
    print("Your Server-based app needs this redirect URL:")
    print(f"  {_LOCALHOST_REDIRECT}")
    print()

    ready = input("Is it configured? [Y/n]: ").strip().lower()
    if ready not in ("", "y", "yes"):
        print("Add the redirect URL first, then try again.")
        sys.exit(0)

    try:
        return authorize_with_browser(
            client_id=client_id,
            client_secret=client_secret,
            accounts_url=accounts_url,
        )
    except ZohoTokenRefreshError as e:
        print(f"Error: {e}")
        sys.exit(1)


def _pick_org_terminal(access_token: str, api_domain: str) -> str:
    """Terminal-based org picker for Self Client flow."""
    print("\nDiscovering organizations...")
    try:
        orgs = discover_organizations(access_token=access_token, api_domain=api_domain)
    except ZohoTokenRefreshError as e:
        print(f"  Warning: {e}")
        return input("  Organization ID: ").strip()

    if len(orgs) == 1:
        oid = str(orgs[0].get("organization_id", ""))
        print(f"  Found: {orgs[0].get('name', '?')} ({oid})")
        return oid

    if len(orgs) > 1:
        print(f"  Found {len(orgs)} organizations:")
        for i, org in enumerate(orgs, 1):
            print(f"    {i}. {org.get('name', '?')} ({org.get('organization_id', '?')})")
        choice = input(f"  Select [1-{len(orgs)}]: ").strip()
        try:
            return str(orgs[int(choice) - 1].get("organization_id", ""))
        except (ValueError, IndexError):
            return str(orgs[0].get("organization_id", ""))

    return input("  Organization ID: ").strip()
