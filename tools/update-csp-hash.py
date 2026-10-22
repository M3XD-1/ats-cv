"""Recompute the CSP hash of index.html's inline script.

Run after any edit to the inline <script>:  python tools/update-csp-hash.py
"""
import base64, hashlib, pathlib, re

page = pathlib.Path(__file__).resolve().parent.parent / "index.html"
# Browsers turn CRLF into LF before hashing, so store the page with LF only (.gitattributes keeps it that way).
with open(page, encoding="utf-8", newline="") as f:
    html = f.read().replace("\r\n", "\n")
scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
assert len(scripts) == 1, f"expected one inline script, found {len(scripts)}"
digest = base64.b64encode(hashlib.sha256(scripts[0].encode("utf-8")).digest()).decode()
html, n = re.subn(r"script-src '(?:SCRIPT_HASH|sha256-[A-Za-z0-9+/=]+)'", f"script-src 'sha256-{digest}'", html)
assert n == 1, "CSP script-src not found"
page.write_text(html, encoding="utf-8", newline="")
print("sha256-" + digest)
