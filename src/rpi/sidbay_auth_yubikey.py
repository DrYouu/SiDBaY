#!/usr/bin/env python3
import sys
import os
import json
import tempfile
import subprocess
import base64
import hashlib
from datetime import datetime

# Estas imports requieren python3-cryptography
try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
except ImportError:  # Permitimos que siga funcionando, pero sin verificación local
    x509 = None
    rsa = None
    ec = None
    padding = None
    hashes = None


def run_cmd(args):
    """Ejecuta un comando y devuelve (rc, stdout_bytes, stderr_str)."""
    p = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    return p.returncode, p.stdout, p.stderr.decode(errors="replace")


def main():
    # PIN como primer argumento
    if len(sys.argv) < 2:
        print(json.dumps({
            "ok": False,
            "pin_ok": False,
            "message": "PIN no proporcionado en la línea de comandos"
        }, ensure_ascii=False))
        return 1

    pin = sys.argv[1].strip()
    if not pin:
        print(json.dumps({
            "ok": False,
            "pin_ok": False,
            "message": "PIN vacío"
        }, ensure_ascii=False))
        return 1

    # Objeto de resultado base
    result = {
        "ok": False,
        "pin_ok": False,
        "slot": "9a",
        "hash_alg": "SHA256",
        "sign_alg": None,
        "message": "",
        "challenge_hex": None,
        "challenge_b64": None,
        "signature_hex": None,
        "signature_b64": None,
        "combined_hash_hex": None,
        "cert_pem": None,
        "cert_subject": None,
        "cert_issuer": None,
        "cert_serial": None,
        "cert_not_before": None,
        "cert_not_after": None,
        "verify_error": None,
        "parse_cert_error": None,
        "stderr": None,
        "ts": datetime.utcnow().isoformat() + "Z",
    }

    # Generar challenge aleatorio de 32 bytes
    challenge = os.urandom(32)
    result["challenge_hex"] = challenge.hex()
    result["challenge_b64"] = base64.b64encode(challenge).decode("ascii")

    with tempfile.TemporaryDirectory() as tmpdir:
        chal_path = os.path.join(tmpdir, "challenge.bin")
        sig_path = os.path.join(tmpdir, "signature.bin")

        with open(chal_path, "wb") as f:
            f.write(challenge)

        # 1) Firmar el challenge con la YubiKey (slot 9a)
        # Probaremos varios algoritmos por si el slot no es RSA.
        alg_candidates = ["ECCP256", "RSA2048", "ECCP384", "RSA3072", "RSA4096"]
        sign_ok = False
        last_err = ""
        used_alg = None

        for alg in alg_candidates:
            cmd = [
                "yubico-piv-tool",
                "-a", "verify-pin",
                "--sign",
                "-s", "9a",
                "-H", "SHA256",
                "-A", alg,
                "-P", pin,
                "-i", chal_path,
                "-o", sig_path,
            ]
            rc, out, err = run_cmd(cmd)
            if rc == 0:
                sign_ok = True
                used_alg = alg
                break
            last_err = err

        if not sign_ok:
            result["stderr"] = last_err.strip()
            result["message"] = "Fallo al verificar PIN o firmar con la YubiKey"
            # pin_ok: no podemos distinguir al 100 %, pero lo tratamos como fallo de PIN/autenticación
            result["pin_ok"] = False
            print(json.dumps(result, ensure_ascii=False))
            return 0

        result["pin_ok"] = True
        result["sign_alg"] = used_alg

        # Leer firma
        try:
            with open(sig_path, "rb") as f:
                signature = f.read()
        except OSError as e:
            result["message"] = "Firma generada pero no se pudo leer el fichero de salida"
            result["stderr"] = str(e)
            print(json.dumps(result, ensure_ascii=False))
            return 0

        result["signature_hex"] = signature.hex()
        result["signature_b64"] = base64.b64encode(signature).decode("ascii")

        # 2) Leer el certificado del slot 9a
        rc, cert_out, cert_err = run_cmd(["yubico-piv-tool", "-a", "read-cert", "-s", "9a"])
        if rc != 0:
            result["stderr"] = (result["stderr"] or "") + "\nread-cert: " + cert_err.strip()
            result["message"] = "Firma realizada, pero fallo al leer el certificado del slot 9a"
            print(json.dumps(result, ensure_ascii=False))
            return 0

        cert_pem = cert_out.decode(errors="replace")
        result["cert_pem"] = cert_pem

        # 3) Verificación local de la firma y metadatos del certificado
        verify_ok = None
        cert_der = b""
        if x509 is not None:
            try:
                cert = x509.load_pem_x509_certificate(cert_out)
                cert_der = cert.public_bytes()
                pubkey = cert.public_key()

                # Extraer metadatos
                result["cert_subject"] = cert.subject.rfc4514_string()
                result["cert_issuer"] = cert.issuer.rfc4514_string()
                result["cert_serial"] = format(cert.serial_number, "X")
                result["cert_not_before"] = cert.not_valid_before.isoformat()
                result["cert_not_after"] = cert.not_valid_after.isoformat()

                # Verificar firma
                try:
                    if isinstance(pubkey, rsa.RSAPublicKey):
                        pubkey.verify(
                            signature,
                            challenge,
                            padding.PKCS1v15(),
                            hashes.SHA256()
                        )
                        verify_ok = True
                    elif isinstance(pubkey, ec.EllipticCurvePublicKey):
                        pubkey.verify(
                            signature,
                            challenge,
                            ec.ECDSA(hashes.SHA256())
                        )
                        verify_ok = True
                    else:
                        verify_ok = False
                        result["verify_error"] = "Tipo de clave pública no soportado"
                except Exception as e:
                    verify_ok = False
                    result["verify_error"] = str(e)

            except Exception as e:
                result["parse_cert_error"] = str(e)
                verify_ok = False
        else:
            # cryptography no disponible; no podemos verificar localmente
            verify_ok = None

        # 4) Hash combinado certificado + challenge (para logs)
        try:
            h = hashlib.sha256()
            h.update(cert_der or cert_out)
            h.update(challenge)
            result["combined_hash_hex"] = h.hexdigest()
        except Exception:
            result["combined_hash_hex"] = None

        # Resultado global
        if verify_ok is True:
            result["ok"] = True
            result["message"] = "Autenticación YubiKey OK (PIN verificado y firma válida)"
        elif verify_ok is False:
            result["ok"] = False
            result["message"] = "Firma generada, pero verificación local de la firma ha fallado"
        else:  # None
            result["ok"] = True  # La YubiKey ha firmado correctamente; asumimos OK criptográfico
            result["message"] = "Autenticación YubiKey OK (firma generada; sin verificación local)"

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
