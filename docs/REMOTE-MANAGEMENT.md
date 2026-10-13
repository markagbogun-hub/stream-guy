# RadioCastOS 1.50 — Remote Management

RadioCastOS 1.50 can be watched and managed from another RadioCastOS (the **Fleet Console**)
or from your own scripts. Everything is off until you switch it on.

## Setting up a station

1. **Settings → Remote Management** → tick *Allow remote monitoring*.
2. Choose *This PC only* (testing) or *Local network*. Keep the default port 8765 unless it is taken.
3. Click **Apply remote settings**. Copy the **access token** (Show / Copy).
4. Optional: tick *Also allow remote Go Live / Stop*. Leave it off for watch-only stations.
5. Optional: **Settings → Alerts** for the webhook.

Windows Firewall may ask whether to allow RadioCastOS on the network the first time you choose *Local network*.

## Watching stations (Fleet Console)

**Fleet Console → Add Station…** Enter a name, the address `http://<station PC>:8765` and the
station's access token. The row turns green / amber / red within a few seconds.

| Row colour | Meaning |
|---|---|
| Green | On air, no findings, no alerts |
| Amber | Warning: low bitrate, reconnecting, a warning alert |
| Red | Fault, or the station cannot be reached / refused the token |
| Grey | Reachable but off air |

## Phone status page (read-only)

Tick *Also serve a read-only status page for phone browsers* in Settings > Remote Management and press **Apply**.
On a phone on the same network, open the station address (for example `http://192.168.1.20:8765`) and paste the access token.
It shows on-air state, now playing, time on air, bitrate, listeners, reconnects, health and active alerts, and refreshes every 5 seconds.

* It cannot change anything: it only reads status and alerts. Go Live / Stop are not available from it.
* The token is kept for that browser tab only, or on the phone if you tick *Remember on this phone*. *Forget token* removes it.
* To reach it away from home use a VPN, or an HTTPS reverse proxy in front of the station. Plain HTTP can be read by anyone on the network path.
* With the tick off, the agent behaves exactly as before: every address answers 401 without a token.

## Security notes

* The agent speaks plain **HTTP**. On any network you do not fully control use a **VPN** or a TLS reverse proxy.
  The Fleet Console accepts `https://` addresses with certificates your PC trusts; self-signed certificates are not accepted.
* The token is a password. Anyone holding it can read the station's status and logs; with control allowed, they can take it off air.
  *New token…* locks out every console immediately.
* Five wrong tokens from one address lock that address out for a minute.
* Passwords, API keys and tokens are removed from the logs the agent serves.
* Remote settings, the fleet list, tokens and the audit logs belong to the PC they were made on and are never put in a station package.

## HTTP API (v1)

All paths are under `/api/v1` and need `Authorization: Bearer <token>`.

| Method | Path | Needs control? | What |
|---|---|---|---|
| GET | `/info` | no | product, version, capabilities, whether control is on |
| GET | `/status` | no | on-air state, uptime, bitrate, now playing, health |
| GET | `/health` | no | System Diagnostics snapshot |
| GET | `/monitor` | no | stream monitor findings, stats, bitrate series (`listeners` is the server's count, `null` when it cannot be read) |
| GET | `/logs?lines=&level=` | no | recent log entries, redacted |
| GET | `/alerts` | no | active alerts and recent history |
| GET | `/audit?limit=` | no | remote command audit log |
| POST | `/control/stream/start` | **yes** | go live |
| POST | `/control/stream/stop` | **yes** | stop; body `{"confirm": true}` required while on air |
| POST | `/alerts/{id}/ack` | **yes** | acknowledge an alert |

Replies are JSON. Errors: 401 token, 403 control off, 409 no stream target, 429 lock-out or cool-down
(5 s between control actions), 504 the app did not respond.

Example:

    curl -H "Authorization: Bearer $TOKEN" http://192.168.1.20:8765/api/v1/status
    curl -X POST -H "Authorization: Bearer $TOKEN" -d '{"confirm":true}' http://192.168.1.20:8765/api/v1/control/stream/stop

## Alerts webhook

Events are POSTed as JSON: `{"event": "raised|escalated|cleared|test", "at": …, "station": {"id", "name"}, "alert": {"id", "key", "severity", "message", …}}`.
Chat services (Slack, Teams, Discord) expect their own payload shapes, so they need a small bridge in between.

## What it does not do

* No listener count (that number lives on the streaming server, not in RadioCastOS).
* No remote editing of settings, playlists or schedules.
* No TLS built in.
* The phone page cannot control the station (read-only).


## Command line (`scripts/radiocastctl.py`)

A small stand-alone client for the same API, for batch files and schedulers (like butt's command-line switches). Python 3 only, nothing to install.

    set RADIOCASTOS_TOKEN=<access token>
    python radiocastctl.py status            :: STOPPED / LIVE | ON AIR | 128 kbps | 17 listeners | ...
    python radiocastctl.py start             :: go live (needs "allow remote Go Live / Stop")
    python radiocastctl.py stop --confirm    :: --confirm is required while ON AIR
    python radiocastctl.py listeners
    python radiocastctl.py audit --limit 20

Use `--url http://<station PC>:8765` for another PC and `--token-file` instead of the environment variable if you prefer. Exit codes: 0 done, 1 refused (wrong token, control off, cool-down), 2 cannot reach the station, 3 missing token. Every start and stop is written to the audit log.
