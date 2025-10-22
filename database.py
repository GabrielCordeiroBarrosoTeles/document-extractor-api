import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "3306")
        self.database = os.getenv("DB_NAME", "document_extractor")
        self.user = os.getenv("DB_USER", "api_user")
        self.password = os.getenv("DB_PASSWORD", "api_pass123")
        
    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
    
    def save_document(self, data: Dict) -> int:
        """Salva documento no banco e retorna o ID"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO documentos (nome_arquivo, data_vencimento, valor_total, 
                                 categoria, beneficiario, texto_extraido, confianca)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Converte data_vencimento para formato MySQL
            data_vencimento = None
            if data.get("data_vencimento"):
                try:
                    data_vencimento = datetime.strptime(data["data_vencimento"], "%d/%m/%Y").date()
                except:
                    pass
            
            values = (
                data.get("nome_arquivo"),
                data_vencimento,
                data.get("valor_total"),
                data.get("categoria"),
                data.get("beneficiario"),
                data.get("texto_extraido"),
                data.get("confianca")
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            return cursor.lastrowid
            
        except Error as e:
            print(f"Erro ao salvar documento: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_all_documents(self) -> List[Dict]:
        """Retorna todos os documentos"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM documentos ORDER BY data_processamento DESC")
            documents = cursor.fetchall()
            
            # Converte datas para string
            for doc in documents:
                if doc.get("data_vencimento"):
                    doc["data_vencimento"] = doc["data_vencimento"].strftime("%d/%m/%Y")
                if doc.get("data_processamento"):
                    doc["data_processamento"] = doc["data_processamento"].isoformat()
            
            return documents
            
        except Error as e:
            print(f"Erro ao buscar documentos: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_document_by_id(self, doc_id: int) -> Optional[Dict]:
        """Retorna documento por ID"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM documentos WHERE id = %s", (doc_id,))
            document = cursor.fetchone()
            
            if document:
                if document.get("data_vencimento"):
                    document["data_vencimento"] = document["data_vencimento"].strftime("%d/%m/%Y")
                if document.get("data_processamento"):
                    document["data_processamento"] = document["data_processamento"].isoformat()
            
            return document
            
        except Error as e:
            print(f"Erro ao buscar documento: {e}")
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas dos documentos"""
        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Total de documentos
            cursor.execute("SELECT COUNT(*) FROM documentos")
            total = cursor.fetchone()[0]
            
            # Categorias
            cursor.execute("SELECT categoria, COUNT(*) FROM documentos GROUP BY categoria")
            categorias = dict(cursor.fetchall())
            
            # Valor total e médio
            cursor.execute("SELECT SUM(valor_total), AVG(valor_total) FROM documentos WHERE valor_total IS NOT NULL")
            result = cursor.fetchone()
            valor_total = float(result[0]) if result[0] else 0
            valor_medio = float(result[1]) if result[1] else 0
            
            return {
                "total_documentos": total,
                "categorias": categorias,
                "valor_total": valor_total,
                "valor_medio": valor_medio
            }
            
        except Error as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {"total_documentos": 0, "categorias": {}, "valor_total": 0, "valor_medio": 0}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()