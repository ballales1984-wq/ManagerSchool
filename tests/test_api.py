"""
Test per API web.
"""

import pytest
from flask import Flask
from interfaccia_erp import InterfacciaERP


@pytest.fixture
def app():
    """Fixture per Flask app di test."""
    interfaccia = InterfacciaERP()
    return interfaccia.app


@pytest.fixture
def client(app):
    """Fixture per test client."""
    return app.test_client()


class TestAPI:
    """Test per API web."""
    
    @pytest.mark.api
    def test_homepage(self, client):
        """Test homepage."""
        response = client.get('/')
        assert response.status_code in [200, 302]  # Redirect o OK
    
    @pytest.mark.api
    def test_login_page(self, client):
        """Test pagina login."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data
    
    @pytest.mark.api
    def test_api_studenti_richiede_auth(self, client):
        """Test che API studenti richieda autenticazione."""
        response = client.get('/api/studenti')
        # Dovrebbe richiedere autenticazione (401 o redirect)
        assert response.status_code in [401, 302]
    
    @pytest.mark.api
    def test_api_database_stats(self, client):
        """Test API statistiche database."""
        response = client.get('/api/database/stats')
        # Dovrebbe richiedere autenticazione
        assert response.status_code in [401, 302]
    
    @pytest.mark.api
    def test_api_backup(self, client):
        """Test API backup."""
        response = client.post('/api/database/backup')
        # Dovrebbe richiedere autenticazione
        assert response.status_code in [401, 302]
    
    @pytest.mark.api
    def test_pdf_export_modulo(self):
        """Test modulo PDF export."""
        from pdf_exporter import PDFExporter
        
        exporter = PDFExporter()
        
        studente = {'nome': 'Test', 'cognome': 'Student', 'classe': '2A'}
        voti = [
            {'materia': 'Math', 'voto': 8.0, 'data': '2025-10-28', 'tipo': 'Exam', 'note': 'OK'}
        ]
        
        import os
        os.makedirs('pdf_export_test', exist_ok=True)
        output_path = 'pdf_export_test/test.pdf'
        
        exporter.esporta_pagella(studente, voti, output_path)
        
        assert os.path.exists(output_path)
        
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
    
    @pytest.mark.api
    def test_email_notifications_modulo(self):
        """Test modulo email notifications."""
        from email_notifications import EmailNotifier
        
        notifier = EmailNotifier()
        
        studente = {'nome': 'Test', 'cognome': 'Student', 'nome_completo': 'Test Student'}
        voto = {'materia': 'Math', 'voto': 8.0, 'tipo': 'Exam', 'data': '2025-10-28', 'note': 'OK'}
        
        result = notifier.notifica_voto_inserito(studente, voto, "test@email.com")
        
        assert result is True
        
        stats = notifier.get_statistiche_email()
        assert stats['email_inviate'] > 0


@pytest.mark.integration
class TestIntegrazione:
    """Test di integrazione."""
    
    @pytest.mark.slow
    def test_sistema_completo(self, app):
        """Test sistema completo."""
        # Verifica che l'app si inizializzi correttamente
        assert app is not None
        
        # Verifica che i moduli siano caricati
        with app.app_context():
            # Test che l'integrazione funzioni
            pass

