import re
import json
import os
from datetime import datetime
from typing import Dict, Optional, List
import pytesseract
from PIL import Image
import cv2
import numpy as np
from dateutil import parser
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

class DocumentExtractor:
    def __init__(self):
        self.categories = {
            'educacao': ['escola', 'universidade', 'curso', 'faculdade', 'ensino', 'educacao', 'colegio', 'instituto', 'pos-graduacao', 'mestrado', 'doutorado', 'mba', 'especializacao', 'tecnico', 'idioma', 'kumon', 'wizard', 'ccaa', 'senac', 'senai', 'etec', 'fatec', 'usp', 'unicamp', 'puc', 'mackenzie', 'fgv', 'insper', 'anhembi', 'unip', 'uninove', 'estacio', 'unopar', 'anhanguera', 'cruzeiro do sul', 'metodista', 'unicsul', 'fiap', 'faap'],
            'treino': ['academia', 'personal', 'fitness', 'treino', 'musculacao', 'crossfit', 'pilates', 'yoga', 'natacao', 'spinning', 'funcional', 'boxe', 'jiu-jitsu', 'karate', 'danca', 'ballet', 'zumba', 'bodytech', 'smartfit', 'bluefit', 'bio ritmo', 'runner', 'competition', 'formula', 'curves', 'contours', 'muay thai', 'capoeira', 'hidroginastica', 'aerobica', 'step', 'pole dance', 'ritmos'],
            'delivery': ['ifood', 'uber', 'rappi', 'delivery', 'entrega', 'comida', 'uber eats', 'james delivery', 'aiqfome', 'loggi', '99food', 'delivery much', 'ze delivery', 'burger king', 'mcdonalds', 'pizza', 'lanche', 'subway', 'kfc', 'dominos', 'pizza hut', 'bobs', 'giraffas', 'habib', 'china in box', 'sushi', 'yakisoba', 'temaki', 'acai', 'sorveteria', 'pizzaria', 'hamburgueria'],
            'saude': ['plano', 'medico', 'hospital', 'clinica', 'saude', 'unimed', 'bradesco saude', 'amil', 'sulamerica', 'farmacia', 'laboratorio', 'exame', 'consulta', 'odontologico', 'psicologia', 'fisioterapia', 'nutricao', 'cardiologia', 'golden cross', 'hapvida', 'notredame', 'drogasil', 'raia', 'pacheco', 'ultrafarma', 'pague menos', 'panvel', 'dermatologista', 'oftalmologista', 'ortopedista', 'ginecologista', 'pediatra', 'psiquiatra', 'neurologista'],
            'transporte': ['uber', 'taxi', '99', 'combustivel', 'posto', 'transporte', 'metro', 'onibus', 'trem', 'estacionamento', 'pedagio', 'veiculo', 'manutencao', 'seguro auto', 'ipva', 'licenciamento', 'multa', 'gasolina', 'etanol', 'diesel', 'shell', 'petrobras', 'ipiranga', 'ale', 'cabify', 'br', 'esso', 'texaco', 'raizen', 'zona azul', 'detran', 'oficina', 'pneu', 'oleo', 'revisao', 'mecanica', 'lavagem', 'vistoria'],
            'alimentacao': ['supermercado', 'mercado', 'padaria', 'restaurante', 'lanchonete', 'bar', 'cafeteria', 'pizzaria', 'hamburgueria', 'sorveteria', 'acougue', 'hortifruti', 'feira', 'emporio', 'delicatessen', 'carrefour', 'extra', 'pao de acucar', 'walmart', 'atacadao', 'sam', 'big', 'quitanda', 'bistek', 'assai', 'makro', 'costco', 'dia', 'mambo', 'hirota', 'zona sul', 'st marche', 'casa santa luzia', 'mundial', 'sonda', 'prezunic', 'guanabara', 'sendas', 'comper', 'fort'],
            'moradia': ['aluguel', 'condominio', 'iptu', 'agua', 'luz', 'gas', 'internet', 'telefone', 'limpeza', 'portaria', 'seguranca', 'tv cabo', 'sky', 'net', 'vivo', 'oi', 'tim', 'sabesp', 'enel', 'cpfl', 'cemig', 'copel', 'coelba', 'energisa', 'comgas', 'ultragaz', 'liquigas', 'copagaz', 'oi fibra', 'vivo fibra', 'claro', 'administradora', 'zelador', 'sindico'],
            'vestuario': ['roupa', 'calcado', 'sapato', 'tenis', 'camisa', 'calca', 'vestido', 'acessorio', 'bolsa', 'relogio', 'joias', 'oculos', 'chapeu', 'cinto', 'carteira', 'moda', 'zara', 'h&m', 'c&a', 'riachuelo', 'renner', 'marisa', 'pernambucanas', 'nike', 'adidas', 'puma', 'havaianas', 'melissa', 'arezzo', 'schutz', 'farm', 'osklen', 'animale', 'shoulder', 'forum', 'colcci', 'saia', 'blusa', 'jaqueta', 'casaco', 'underwear', 'meia', 'bone'],
            'lazer': ['cinema', 'teatro', 'show', 'evento', 'parque', 'viagem', 'hotel', 'pousada', 'turismo', 'festa', 'balada', 'clube', 'museu', 'exposicao', 'festival', 'ingresso', 'cinemark', 'uci', 'kinoplex', 'cinesystem', 'playarte', 'barcade', 'karaoke', 'boliche', 'shopping', 'parque aquatico', 'hopi hari', 'playcenter', 'beto carrero', 'beach park', 'thermas', 'resort', 'concerto', 'zoologico', 'pub', 'cerveja', 'drink'],
            'tecnologia': ['celular', 'computador', 'notebook', 'tablet', 'software', 'aplicativo', 'streaming', 'netflix', 'spotify', 'amazon prime', 'disney', 'globoplay', 'youtube premium', 'icloud', 'smartphone', 'mouse', 'teclado', 'monitor', 'impressora', 'camera', 'fone', 'carregador', 'cabo', 'memoria', 'hd', 'ssd', 'apple', 'samsung', 'xiaomi', 'motorola', 'lg', 'sony', 'dell', 'hp', 'lenovo', 'asus', 'acer', 'microsoft', 'logitech', 'jbl', 'beats', 'bose', 'iphone', 'ipad', 'macbook', 'playstation', 'xbox', 'nintendo', 'disney plus', 'paramount', 'hbo max', 'apple tv'],
            'servicos': ['banco', 'cartao', 'emprestimo', 'financiamento', 'seguro', 'advocacia', 'contabilidade', 'consultoria', 'manutencao', 'despachante', 'cartorio', 'correios', 'sedex', 'advogado', 'contador', 'dentista', 'mecanico', 'eletricista', 'encanador', 'pintor', 'faxina', 'lavanderia', 'costura', 'chaveiro', 'vidraceiro', 'marceneiro', 'pedreiro', 'jardineiro', 'diarista', 'baba', 'cuidador', 'seguranca', 'porteiro', 'imobiliaria', 'corretor', 'notario', 'traducao', 'auditoria', 'engenheiro', 'arquiteto'],
            'pets': ['veterinario', 'pet shop', 'racao', 'vacina', 'tosa', 'hotel para pets', 'adestramento', 'medicamento animal', 'brinquedo pet', 'cama pet', 'coleira', 'aquario', 'petz', 'cobasi', 'petlove', 'american pet', 'whiskas', 'pedigree', 'royal canin', 'premier', 'golden', 'hills', 'pro plan', 'purina', 'caes', 'gatos', 'hamster', 'coelho', 'tartaruga', 'papagaio', 'peixe', 'passaro', 'gato', 'cachorro', 'casinha', 'gaiola'],
            'beleza': ['salao', 'barbeiro', 'estetica', 'manicure', 'pedicure', 'massagem', 'spa', 'cosmeticos', 'perfume', 'maquiagem', 'cabelo', 'unha', 'sobrancelha', 'depilacao', 'sephora', 'boticario', 'natura', 'avon', 'mary kay', 'loreal', 'nivea', 'dove', 'pantene', 'tresemme', 'elseve', 'garnier', 'maybelline', 'revlon', 'mac', 'clinique', 'lancome', 'chanel', 'dior', 'creme', 'shampoo', 'condicionador', 'tintura', 'escova'],
            'casa': ['moveis', 'decoracao', 'eletrodomesticos', 'ferramentas', 'jardinagem', 'construcao', 'reforma', 'pintura', 'marcenaria', 'eletrica', 'hidraulica', 'ar condicionado', 'sofa', 'cama', 'mesa', 'cadeira', 'guarda-roupa', 'geladeira', 'fogao', 'microondas', 'maquina', 'aspirador', 'ferro', 'panela', 'prato', 'copo', 'talher', 'casas bahia', 'magazine luiza', 'ponto frio', 'americanas', 'submarino', 'tok stok', 'etna', 'mobly', 'madeira madeira', 'leroy merlin', 'telhanorte', 'c&c', 'dicico', 'azulejo', 'piso'],
            'investimentos': ['corretora', 'investimento', 'acao', 'fundo', 'renda fixa', 'previdencia', 'cdb', 'tesouro', 'bitcoin', 'cripto', 'clear', 'rico', 'xp', 'btg', 'lci', 'lca', 'selic', 'ipca', 'bovespa', 'b3', 'taxa', 'rendimento', 'dividendo', 'juros', 'renda variavel', 'vgbl', 'pgbl', 'capitalizacao', 'consorcio', 'easynvest', 'modal', 'inter', 'c6', 'original', 'safra'],
            'trabalho': ['material escritorio', 'papelaria', 'impressao', 'xerox', 'coworking', 'reuniao', 'conferencia', 'treinamento', 'capacitacao', 'curso profissional', 'salario', 'folha', 'pagamento', 'holerite', 'vale', 'refeicao', 'plr', 'bonus', 'comissao', 'hora extra', 'ferias', 'decimo', 'rescisao', 'seguro desemprego', 'pis', 'pasep', 'sindicato', 'contribuicao', 'uniforme', 'epi'],
            'impostos': ['imposto', 'taxa', 'multa', 'iptu', 'ipva', 'ir', 'receita federal', 'darf', 'gru', 'guia pagamento', 'pis', 'cofins', 'icms', 'iss', 'inss', 'fgts', 'prefeitura', 'cartorio', 'certidao', 'alvara', 'licenca', 'dare', 'gnre', 'simples nacional', 'mei', 'cnpj', 'cpf'],
            'doacao': ['doacao', 'caridade', 'ong', 'igreja', 'templo', 'dizimo', 'oferta', 'beneficencia', 'solidariedade', 'ajuda humanitaria', 'assistencia', 'social', 'filantropia', 'voluntariado', 'campanha', 'arrecadacao', 'ajuda', 'apoio', 'patrocinio', 'sponsorship'],
            'subscricoes': ['assinatura', 'mensalidade', 'anuidade', 'premium', 'pro', 'plus', 'subscription', 'recurring', 'recorrente', 'netflix', 'spotify', 'amazon prime', 'disney plus', 'globo play', 'youtube premium', 'icloud', 'office 365', 'adobe', 'canva', 'dropbox'],
            'emergencia': ['emergencia', 'urgencia', 'hospital', 'ambulancia', 'socorro', 'bombeiro', 'policia', 'seguranca', 'chaveiro', 'guincho', 'samu', 'pronto socorro', 'upa', 'clinica 24h', 'plantao', 'urgente', 'emergencial'],
            'juridico': ['advogado', 'juridico', 'processo', 'honorario', 'custas', 'cartorio', 'registro', 'certidao', 'documentacao', 'legal', 'tribunal', 'vara', 'juizo', 'foro', 'justica', 'advocacia', 'escritorio', 'oab', 'procuracao', 'contrato'],
            'comunicacao': ['telefone', 'celular', 'internet', 'tv', 'radio', 'jornal', 'revista', 'publicidade', 'marketing', 'propaganda', 'claro', 'vivo', 'tim', 'oi', 'sky', 'net', 'globo', 'sbt', 'record', 'band', 'folha', 'estadao', 'veja', 'epoca'],
            'cultura': ['livro', 'revista', 'jornal', 'biblioteca', 'livraria', 'arte', 'pintura', 'escultura', 'fotografia', 'design', 'saraiva', 'cultura', 'fnac', 'amazon', 'submarino', 'estante virtual', 'skoob', 'kindle', 'audible', 'galeria'],
            'esportes': ['futebol', 'basquete', 'volei', 'tenis', 'golf', 'surf', 'skate', 'bicicleta', 'corrida', 'maratona', 'competicao', 'natacao', 'atletismo', 'ginastica', 'handball', 'rugby', 'beisebol', 'hockey', 'badminton', 'squash', 'ping pong', 'equitacao', 'escalada'],
            'infantil': ['brinquedo', 'escola infantil', 'creche', 'babysitter', 'fralda', 'leite', 'papinha', 'roupa bebe', 'pediatra', 'vacina infantil', 'berco', 'carrinho', 'cadeirinha', 'mamadeira', 'chupeta', 'bico', 'pomada', 'shampoo bebe', 'sabonete bebe', 'ri happy', 'pbkids', 'toy story', 'disney', 'barbie', 'hot wheels', 'lego']
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        denoised = cv2.medianBlur(enhanced, 3)
        
        return denoised
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            
            if text.strip():
                return text
            
            images = convert_from_path(pdf_path)
            ocr_text = ""
            
            for i, image in enumerate(images):
                img_array = np.array(image)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                denoised = cv2.medianBlur(enhanced, 3)
                
                lang = os.getenv("TESSERACT_LANG", "por")
                page_text = pytesseract.image_to_string(denoised, lang=lang)
                ocr_text += f"\n--- Página {i+1} ---\n{page_text}"
            
            return ocr_text
            
        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return ""
    
    def extract_text_from_image(self, image_path: str) -> str:
        try:
            processed_img = self.preprocess_image(image_path)
            lang = os.getenv("TESSERACT_LANG", "por")
            text = pytesseract.image_to_string(processed_img, lang=lang)
            return text
        except Exception as e:
            print(f"Erro no OCR: {e}")
            return ""
    
    def extract_dates(self, text: str) -> Dict[str, Optional[str]]:
        dates = {}
        
        date_patterns = [
            r'\d{2}/\d{2}/\d{4}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{2}\.\d{2}\.\d{4}'
        ]
        
        venc_patterns = [
            r'vencimento[:\s]*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})',
            r'venc[:\s]*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})',
            r'data.*venc.*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})'
        ]
        
        for pattern in venc_patterns:
            match = re.search(pattern, text.lower())
            if match:
                dates['data_vencimento'] = match.group(1)
                break
        
        pag_patterns = [
            r'pagamento[:\s]*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})',
            r'pago.*em[:\s]*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})',
            r'data.*pag.*(\d{2}[/\-\.]\d{2}[/\-\.]\d{4})'
        ]
        
        for pattern in pag_patterns:
            match = re.search(pattern, text.lower())
            if match:
                dates['data_pagamento'] = match.group(1)
                break
        
        return dates
    
    def extract_value(self, text: str) -> Optional[float]:
        value_patterns = [
            r'valor[:\s]*r?\$?\s*(\d{1,3}(?:\.\d{3})*,\d{2})',
            r'total[:\s]*r?\$?\s*(\d{1,3}(?:\.\d{3})*,\d{2})',
            r'r\$\s*(\d{1,3}(?:\.\d{3})*,\d{2})',
            r'(\d{1,3}(?:\.\d{3})*,\d{2})'
        ]
        
        for pattern in value_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                values = []
                for match in matches:
                    try:
                        value_str = match.replace('.', '').replace(',', '.')
                        values.append(float(value_str))
                    except:
                        continue
                
                if values:
                    return max(values)
        
        return None
    
    def classify_payment(self, text: str) -> str:
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return category
        
        return 'outros'
    
    def extract_recipient(self, text: str) -> Optional[str]:
        recipient_patterns = [
            r'beneficiario[:\s]*([^\n]+)',
            r'para[:\s]*([^\n]+)',
            r'destinatario[:\s]*([^\n]+)',
            r'empresa[:\s]*([^\n]+)'
        ]
        
        for pattern in recipient_patterns:
            match = re.search(pattern, text.lower())
            if match:
                recipient = match.group(1).strip()
                if len(recipient) > 3:
                    return recipient
        
        return None
    
    def process_document(self, file_path: str) -> Dict:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_image(file_path)
        
        if not text:
            return {"erro": "Não foi possível extrair texto do documento"}
        
        dates = self.extract_dates(text)
        value = self.extract_value(text)
        category = self.classify_payment(text)
        recipient = self.extract_recipient(text)
        
        result = {
            "arquivo": file_path,
            "data_processamento": datetime.now().isoformat(),
            "data_vencimento": dates.get('data_vencimento'),
            "data_pagamento": dates.get('data_pagamento'),
            "valor_total": value,
            "categoria": category,
            "beneficiario": recipient,
            "texto_extraido": text[:500] + "..." if len(text) > 500 else text
        }
        
        return result