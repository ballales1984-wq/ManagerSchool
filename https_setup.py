"""
Setup HTTPS per Flask.
"""

import ssl
import os
from OpenSSL import SSL, crypto
from pathlib import Path


class HTTPSSetup:
    """Gestisce setup HTTPS per Flask."""
    
    @staticmethod
    def genera_certificato_self_signed(domain: str = "localhost", 
                                      ip_addresses: list = None,
                                      validity_days: int = 365,
                                      output_dir: str = "ssl"):
        """Genera certificato self-signed.
        
        Args:
            domain: Dominio certificato
            ip_addresses: IP addresses da includere
            validity_days: Giorni di validità
            output_dir: Directory output
        """
        # Crea directory se non esiste
        os.makedirs(output_dir, exist_ok=True)
        
        # Crea chiave privata
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)
        
        # Crea certificato
        cert = crypto.X509()
        cert.get_subject().CN = domain
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validity_days * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        
        # Aggiungi Subject Alternative Names
        san_list = [f"DNS:{domain}", f"DNS:*.{domain}"]
        if ip_addresses:
            for ip in ip_addresses:
                san_list.append(f"IP:{ip}")
        san_list.append("DNS:localhost")
        
        cert.add_extensions([
            crypto.X509Extension(b"subjectAltName", False, 
                               ",".join(san_list).encode())
        ])
        
        cert.sign(key, 'sha256')
        
        # Salva certificato e chiave
        cert_path = os.path.join(output_dir, "cert.pem")
        key_path = os.path.join(output_dir, "key.pem")
        
        with open(cert_path, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
        with open(key_path, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        
        print(f"✅ Certificato generato!")
        print(f"   Certificato: {cert_path}")
        print(f"   Chiave: {key_path}")
        
        return cert_path, key_path
    
    @staticmethod
    def setup_flask_https(app, cert_path: str = "ssl/cert.pem", 
                         key_path: str = "ssl/key.pem"):
        """Setup Flask per HTTPS.
        
        Args:
            app: Flask app
            cert_path: Percorso certificato
            key_path: Percorso chiave privata
            
        Returns:
            Context SSL configurato
        """
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            raise FileNotFoundError(
                f"Certificati non trovati. Esegui genera_certificato_self_signed()"
            )
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)
        
        return context


if __name__ == "__main__":
    print("SISTEMA HTTPS SETUP - TEST")
    print("=" * 60 + "\n")
    
    # Genera certificato test
    print("1. Generazione certificato self-signed...")
    cert_path, key_path = HTTPSSetup.genera_certificato_self_signed()
    
    print(f"\n2. Certificati creati:")
    print(f"   {cert_path}")
    print(f"   {key_path}")
    
    print("\nPer usare HTTPS con Flask:")
    print("""
    # Nel file principale Flask:
    from https_setup import HTTPSSetup
    
    app = Flask(__name__)
    context = HTTPSSetup.setup_flask_https(app)
    
    if __name__ == '__main__':
        app.run(debug=True, ssl_context=context, host='0.0.0.0', port=5000)
    """)

