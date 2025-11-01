import sqlite3
import json
from datetime import datetime
import os

class CreditDatabase:
    def __init__(self, db_path="data/credit_documents.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                extraction_date TIMESTAMP,
                borrower_name TEXT,
                lender_name TEXT,
                loan_amount TEXT,
                interest_rate TEXT,
                maturity_date DATE,
                full_extraction TEXT,
                pages_processed INTEGER,
                api_cost REAL,
                processing_time REAL
            )
        """)
        self.conn.commit()
    
    def insert_document(self, filename, extraction_data, metadata):
        cursor = self.conn.cursor()
        
        # Handle borrower (can be string or dict)
        borrower = extraction_data.get('borrower', {}) or {}
        if isinstance(borrower, str):
            borrower_name = borrower
        elif isinstance(borrower, dict):
            borrower_name = borrower.get('name')
        else:
            borrower_name = None
        
        # Handle lender (can be string, dict, or list)
        lender = extraction_data.get('lender', {}) or {}
        if isinstance(lender, str):
            lender_name = lender
        elif isinstance(lender, dict):
            lender_name = lender.get('name')
        elif isinstance(lender, list) and len(lender) > 0:
            # If it's a list, take the first lender
            first_lender = lender[0]
            if isinstance(first_lender, dict):
                lender_name = first_lender.get('name')
            else:
                lender_name = str(first_lender)
        else:
            lender_name = None
        
        # Handle loan details
        loan = extraction_data.get('loan_details', {}) or {}
        if isinstance(loan, dict):
            loan_amount = loan.get('total_amount')
        else:
            loan_amount = None
        
        # Handle interest terms
        interest = extraction_data.get('interest_terms', {}) or {}
        if isinstance(interest, dict):
            interest_rate = interest.get('total_rate')
        else:
            interest_rate = None
        
        # Handle maturity
        maturity = extraction_data.get('maturity', {}) or {}
        if isinstance(maturity, dict):
            maturity_date = maturity.get('maturity_date')
        else:
            maturity_date = None
        
        cursor.execute("""
            INSERT INTO documents (
                filename, extraction_date,
                borrower_name, lender_name,
                loan_amount, interest_rate, maturity_date,
                full_extraction, pages_processed, api_cost, processing_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            filename, 
            datetime.now().isoformat(),
            borrower_name, 
            lender_name,
            loan_amount, 
            interest_rate,
            maturity_date,
            json.dumps(extraction_data),
            metadata.get('pages_processed', 0),
            metadata.get('api_cost', 0.0),
            metadata.get('processing_time', 0.0)
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_documents(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM documents ORDER BY upload_date DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def search_documents(self, query):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM documents 
            WHERE borrower_name LIKE ? OR lender_name LIKE ?
            ORDER BY upload_date DESC
        """, (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self):
        cursor = self.conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM documents")
        stats['total_documents'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(api_cost) FROM documents")
        stats['total_cost'] = cursor.fetchone()[0] or 0.0
        
        cursor.execute("SELECT AVG(processing_time) FROM documents")
        stats['avg_processing_time'] = cursor.fetchone()[0] or 0.0
        
        return stats
    
    def close(self):
        self.conn.close()
