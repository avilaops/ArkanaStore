#!/usr/bin/env python3
"""
AVILA-GRAVATAR SERVICE - ARKANA STORE
=====================================
Serviço para gerar avatares personalizados usando Gravatar API

Features:
- Buscar avatar por email
- Gerar avatar padrão customizado
- Cache de avatares
- Fallback para iniciais do nome

Credenciais configuradas:
API Key: gk-ozHmHXVf-TMBrfDAk69r3ejAkSM8CgwdAqNuhXNrpBqmsSix7Tpv08FL8CUs9

Data: 16/11/2025
Versão: 1.0.0
"""

import os
import hashlib
import requests
from typing import Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
import json
from PIL import Image, ImageDraw, ImageFont
import io

# Carregar configurações
load_dotenv('config/.env.arkana.production')

class AvilaGravatarService:
    """Serviço de avatares Gravatar para Arkana Store"""
    
    def __init__(self):
        self.api_key = os.getenv('GRAVATAR_API_KEY', '')
        self.api_url = os.getenv('GRAVATAR_API_URL', 'https://api.gravatar.com/v1')
        self.default_size = int(os.getenv('GRAVATAR_DEFAULT_SIZE', '200'))
        self.rating = os.getenv('GRAVATAR_RATING', 'g')
        
        # Cache local
        self.cache_dir = Path('data/avatars_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"? Gravatar configurado: {self.api_url}")
        print(f"?? API Key: {self.api_key[:20]}...")
    
    def get_gravatar_hash(self, email: str) -> str:
        """Gera hash MD5 do email (padrão Gravatar)"""
        return hashlib.md5(email.lower().strip().encode()).hexdigest()
    
    def get_avatar_url(self, email: str, size: Optional[int] = None) -> str:
        """
        Retorna URL do avatar do Gravatar
        
        Args:
            email: Email do usuário
            size: Tamanho do avatar (padrão: 200)
        
        Returns:
            URL do avatar
        """
        email_hash = self.get_gravatar_hash(email)
        size = size or self.default_size
        
        # URL pública do Gravatar (não precisa API key)
        url = f"https://www.gravatar.com/avatar/{email_hash}"
        url += f"?s={size}&d=identicon&r={self.rating}"
        
        return url
    
    def fetch_avatar(self, email: str, size: Optional[int] = None) -> Optional[bytes]:
        """
        Baixa avatar do Gravatar
        
        Returns:
            Bytes da imagem ou None se não encontrar
        """
        url = self.get_avatar_url(email, size)
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.content
            
            return None
        except Exception as e:
            print(f"? Erro ao buscar avatar: {e}")
            return None
    
    def get_profile_info(self, email: str) -> Optional[Dict]:
        """
        Busca informações do perfil usando Gravatar API
        (Requer API Key)
        
        Returns:
            Dados do perfil ou None
        """
        email_hash = self.get_gravatar_hash(email)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/profiles/{email_hash}",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
        except Exception as e:
            print(f"? Erro ao buscar perfil: {e}")
            return None
    
    def generate_initials_avatar(
        self, 
        name: str, 
        size: int = 200,
        bg_color: str = '#FF6B6B',  # Cor primária Arkana
        text_color: str = '#FFFFFF'
    ) -> bytes:
        """
        Gera avatar com iniciais do nome
        
        Args:
            name: Nome completo
            size: Tamanho do avatar
            bg_color: Cor de fundo (hex)
            text_color: Cor do texto (hex)
        
        Returns:
            Bytes da imagem PNG
        """
        # Extrair iniciais
        parts = name.strip().split()
        if len(parts) >= 2:
            initials = f"{parts[0][0]}{parts[-1][0]}".upper()
        else:
            initials = parts[0][:2].upper() if parts else "?"
        
        # Criar imagem
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Fonte (tentar usar font customizada, fallback para default)
        try:
            font_size = int(size * 0.4)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calcular posição centralizada
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) / 2
        y = (size - text_height) / 2
        
        # Desenhar texto
        draw.text((x, y), initials, fill=text_color, font=font)
        
        # Converter para bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        
        return buffer.getvalue()
    
    def get_or_create_avatar(
        self, 
        email: str, 
        name: str, 
        size: Optional[int] = None
    ) -> bytes:
        """
        Busca avatar do Gravatar ou gera com iniciais
        
        Args:
            email: Email do usuário
            name: Nome do usuário (para fallback)
            size: Tamanho desejado
        
        Returns:
            Bytes da imagem
        """
        size = size or self.default_size
        cache_key = f"{self.get_gravatar_hash(email)}_{size}.png"
        cache_path = self.cache_dir / cache_key
        
        # Verificar cache
        if cache_path.exists():
            print(f"?? Avatar em cache: {email}")
            return cache_path.read_bytes()
        
        # Tentar buscar do Gravatar
        avatar_bytes = self.fetch_avatar(email, size)
        
        if avatar_bytes:
            # Salvar em cache
            cache_path.write_bytes(avatar_bytes)
            print(f"? Avatar Gravatar: {email}")
            return avatar_bytes
        
        # Fallback: gerar com iniciais
        print(f"?? Gerando avatar com iniciais: {name}")
        avatar_bytes = self.generate_initials_avatar(name, size)
        
        # Salvar em cache
        cache_path.write_bytes(avatar_bytes)
        
        return avatar_bytes
    
    def save_avatar_to_file(
        self, 
        email: str, 
        name: str, 
        output_path: str,
        size: Optional[int] = None
    ):
        """
        Salva avatar em arquivo local
        
        Args:
            email: Email do usuário
            name: Nome do usuário
            output_path: Caminho para salvar
            size: Tamanho do avatar
        """
        avatar_bytes = self.get_or_create_avatar(email, name, size)
        
        Path(output_path).write_bytes(avatar_bytes)
        print(f"?? Avatar salvo: {output_path}")


# ===================================================================
# EXEMPLO DE USO
# ===================================================================

if __name__ == '__main__':
    service = AvilaGravatarService()
    
    # Exemplo 1: Buscar avatar do Marcelo (cliente Arkana)
    print("\n" + "="*60)
    print("EXEMPLO 1: Avatar do cliente Arkana Store")
    print("="*60)
    
    marcelo_avatar = service.get_or_create_avatar(
        email="marceloquintinoalves25@gmail.com",
        name="Marcelo Quintino",
        size=200
    )
    
    service.save_avatar_to_file(
        email="marceloquintinoalves25@gmail.com",
        name="Marcelo Quintino",
        output_path="data/avatars/marcelo_quintino.png"
    )
    
    # Exemplo 2: Buscar informações do perfil (API Key)
    print("\n" + "="*60)
    print("EXEMPLO 2: Informações do perfil")
    print("="*60)
    
    profile = service.get_profile_info("marceloquintinoalves25@gmail.com")
    
    if profile:
        print(f"? Perfil encontrado:")
        print(json.dumps(profile, indent=2))
    else:
        print("??  Perfil não encontrado (email pode não ter Gravatar)")
    
    # Exemplo 3: Gerar avatar com iniciais (para equipe Ávila)
    print("\n" + "="*60)
    print("EXEMPLO 3: Avatar equipe Ávila")
    print("="*60)
    
    equipe = [
        ("nicolas@avila.inc", "Nicolas Ávila"),
        ("dev@avila.inc", "Dev Team"),
    ]
    
    for email, nome in equipe:
        service.save_avatar_to_file(
            email=email,
            name=nome,
            output_path=f"data/avatars/{nome.lower().replace(' ', '_')}.png"
        )
    
    print("\n? Todos os avatares gerados!")
    print(f"?? Localização: {service.cache_dir.absolute()}")
