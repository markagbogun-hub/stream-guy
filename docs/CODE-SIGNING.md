# Code signing a RadioCastOS release

An unsigned installer triggers a Windows SmartScreen warning for every customer. Sign every
release build: `RadioCastOS.exe`, the installer and the uninstaller.

## One-time
1. Buy a code-signing certificate (EV gives instant SmartScreen reputation; OV builds it
   over time). Keep the private key on a hardware token or in the Windows certificate store,
   not in this repository.
2. Install the Windows SDK (for `signtool.exe`) on the build PC.

## Each build
Set one of these in the build window (never commit them):

    set RCOS_SIGN_THUMBPRINT=<SHA-1 thumbprint of the certificate in the Windows store>
    rem or
    set RCOS_SIGN_PFX=C:\path\to\cert.pfx
    set RCOS_SIGN_PFX_PASSWORD=<password>

Optional: `RCOS_SIGN_TIMESTAMP` (default `http://timestamp.digicert.com`) and `RCOS_SIGNTOOL`.
For a release, also `set RCOS_REQUIRE_SIGNING=1` so the build fails instead of producing an
unsigned file. Then run `local-build.bat`.

For CI, call `iscc /DMyAppVersion=<x.y.z> /DSignToolName=rcsign "/Srcsign=$qC:\...\scripts\sign-file.bat$q $f" installer.iss`
after signing `dist\RadioCastOS\RadioCastOS.exe` with `scripts\sign-file.bat`.

## Check
Right-click the installer and the exe, Properties, Digital Signatures: one SHA-256 signature
with a timestamp. Or `signtool verify /pa /v <file>`.

## Not covered
Signing proves who published the file; it does not replace the licence key. The licence
private key (used by the key-issuing tool) is a separate secret: keep it offline and backed up.
