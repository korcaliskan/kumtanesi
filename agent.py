import os
import logging
from typing import List, Dict
from openai import OpenAI

class KumTanesiAgent:
    """KumTanesi AI Agent - Türkçe konuşan akıllı asistan"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-5"
        self.system_prompt = """Sen KumTanesi adında yardımsever bir AI asistanısın. 
        Türkçe konuşuyorsun ve kullanıcılara her konuda yardım edebilirsin. 
        Samimi, dostça ve bilgilendirici bir tarzda yanıt veriyorsun.
        
        Özellikler:
        - Her zaman Türkçe yanıt ver
        - Kullanıcıya karşı saygılı ve yardımsever ol
        - Detaylı ve faydalı bilgiler sağla
        - Gerektiğinde örnekler ver
        - Anlayışlı ve sabırlı ol
        
        Adın KumTanesi ve bir AI asistanı olduğunu unutma."""
        
    def get_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Kullanıcı mesajına AI yanıtı üret"""
        try:
            # Konuşma bağlamını hazırla
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Konuşma geçmişini ekle (son 8 mesaj)
            if conversation_history:
                recent_history = conversation_history[-8:] if len(conversation_history) > 8 else conversation_history
                messages.extend(recent_history)
            
            # Mevcut kullanıcı mesajını ekle
            messages.append({"role": "user", "content": user_message})
            
            # OpenAI API çağrısı
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Agent response error: {str(e)}")
            return "Üzgünüm, şu anda yanıt veremiyorum. Lütfen daha sonra tekrar deneyin."
    
    def get_greeting(self) -> str:
        """Karşılama mesajı"""
        return """Merhaba! Ben KumTanesi, sizin AI asistanınızım. 🌟

Size nasıl yardımcı olabilirim? Her türlü sorunuza yanıt verebilir, 
konuşabiliriz veya ihtiyacınız olan bilgileri sağlayabilirim.

Başlamak için bana bir şeyler sorun! 😊"""
