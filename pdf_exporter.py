"""
Modulo per esportazione PDF di pagelle e report.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import List, Dict
from datetime import datetime
import os


class PDFExporter:
    """Esporta pagelle e report in formato PDF."""
    
    def __init__(self):
        """Inizializza l'export PDF."""
        self.styles = getSampleStyleSheet()
        
        # Usa stili esistenti o crea nuovi con nomi diversi
        if 'CustomTitle' not in self.styles.byName:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#1a237e'),
                alignment=TA_CENTER,
                spaceAfter=30
            ))
        
        if 'CustomSubtitle' not in self.styles.byName:
            self.styles.add(ParagraphStyle(
                name='CustomSubtitle',
                fontSize=12,
                textColor=colors.HexColor('#616161'),
                alignment=TA_CENTER
            ))
    
    def esporta_pagella(self, studente: Dict, voti: List[Dict], output_path: str):
        """Esporta una pagella in PDF.
        
        Args:
            studente: Dati studente
            voti: Lista voti
            output_path: Percorso file PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Titolo
        story.append(Paragraph("PAGELLA SCOLASTICA", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        
        # Info studente
        story.append(Paragraph(
            f"<b>Studente:</b> {studente.get('nome', '')} {studente.get('cognome', '')}",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"<b>Classe:</b> {studente.get('classe', '')}",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"<b>Anno Scolastico:</b> {datetime.now().year}/{datetime.now().year+1}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Tabella voti
        if voti:
            data = [['Materia', 'Voto', 'Data', 'Tipo', 'Note']]
            for voto in voti:
                data.append([
                    voto.get('materia', ''),
                    f"{voto.get('voto', 0):.1f}",
                    voto.get('data', ''),
                    voto.get('tipo', ''),
                    voto.get('note', '')
                ])
            
            table = Table(data, colWidths=[2*inch, 0.8*inch, 1*inch, 1.2*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(table)
        
        # Media
        if voti:
            media = sum(v.get('voto', 0) for v in voti) / len(voti)
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"<b>Media Generale: {media:.2f}</b>",
                self.styles['Normal']
            ))
        
        # Genera PDF
        doc.build(story)
        print(f"✅ Pagella PDF esportata: {output_path}")
    
    def esporta_report_classe(self, classe: str, studenti: List[Dict], output_path: str):
        """Esporta un report di classe in PDF.
        
        Args:
            classe: Nome classe
            studenti: Lista studenti con voti
            output_path: Percorso file PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Titolo
        story.append(Paragraph(f"REPORT CLASSE {classe}", self.styles['CustomTitle']))
        story.append(Paragraph(
            f"Anno Scolastico {datetime.now().year}/{datetime.now().year+1}",
            self.styles['CustomSubtitle']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Tabella studenti
        data = [['#', 'Studente', 'Media']]
        for i, stud in enumerate(studenti, 1):
            media = stud.get('media', 0)
            colore = colors.green if media >= 6 else colors.red
            data.append([
                str(i),
                f"{stud.get('nome', '')} {stud.get('cognome', '')}",
                f"{media:.2f}"
            ])
        
        table = Table(data, colWidths=[0.5*inch, 3.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(table)
        
        # Statistiche
        if studenti:
            media_classe = sum(s.get('media', 0) for s in studenti) / len(studenti)
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"<b>Media Classe: {media_classe:.2f}</b>",
                self.styles['Normal']
            ))
            story.append(Paragraph(
                f"<b>Numero Studenti: {len(studenti)}</b>",
                self.styles['Normal']
            ))
        
        # Genera PDF
        doc.build(story)
        print(f"✅ Report classe PDF esportato: {output_path}")
    
    def esporta_report_generale(self, stats: Dict, output_path: str):
        """Esporta un report generale in PDF.
        
        Args:
            stats: Statistiche generali
            output_path: Percorso file PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Titolo
        story.append(Paragraph("REPORT GENERALE SCUOLA", self.styles['CustomTitle']))
        story.append(Paragraph(
            f"Data: {datetime.now().strftime('%d/%m/%Y')}",
            self.styles['CustomSubtitle']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Statistiche
        data = [
            ['Indicatore', 'Valore'],
            ['Studenti Totali', str(stats.get('studenti_totali', 0))],
            ['Insegnanti Totali', str(stats.get('insegnanti_totali', 0))],
            ['Classi Attive', str(stats.get('classi_totali', 0))],
            ['Voti Registrati', str(stats.get('voti_totali', 0))],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f51b5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
        ]))
        story.append(table)
        
        # Genera PDF
        doc.build(story)
        print(f"✅ Report generale PDF esportato: {output_path}")


if __name__ == "__main__":
    print("PDF EXPORTER - TEST")
    print("=" * 60 + "\n")
    
    exporter = PDFExporter()
    
    # Test pagella
    studente = {'nome': 'Mario', 'cognome': 'Rossi', 'classe': '2A'}
    voti = [
        {'materia': 'Matematica', 'voto': 8.0, 'data': '2025-10-28', 'tipo': 'Interrogazione', 'note': 'Ottimo'},
        {'materia': 'Italiano', 'voto': 7.5, 'data': '2025-10-29', 'tipo': 'Verifica', 'note': 'Buono'},
        {'materia': 'Scienze', 'voto': 9.0, 'data': '2025-10-30', 'tipo': 'Compito', 'note': 'Eccellente'},
    ]
    
    os.makedirs('pdf_export', exist_ok=True)
    exporter.esporta_pagella(studente, voti, 'pdf_export/pagella_test.pdf')
    print("\n✅ Test PDF completato!")
    print(f"   File: pdf_export/pagella_test.pdf")

