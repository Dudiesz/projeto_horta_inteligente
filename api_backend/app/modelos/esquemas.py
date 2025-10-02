import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DadosSensorBase(BaseModel):
    """
    Schema base para os dados do sensor. Todos os campos de leitura são opcionais
    para permitir o envio de dados parciais durante os testes e desenvolvimento.
    """
    # Campo obrigatório para identificar o dispositivo
    id_dispositivo: str = Field(..., description="Identificador único do dispositivo físico (ex: ESP32_HORTA_01).")
    
    # Leituras dos sensores (opcionais)
    umidade: Optional[float] = Field(default=None, description="Umidade do solo em porcentagem.")
    ph_solo: Optional[float] = Field(default=None, ge=0, le=14, description="Nível de pH do solo (escala de 0 a 14).")
    temperatura: Optional[float] = Field(default=None, description="Temperatura do ambiente em graus Celsius.")
    condutividade_eletrica: Optional[float] = Field(default=None, description="Condutividade elétrica do solo (EC) em mS/cm.")
    nitrogenio: Optional[float] = Field(default=None, description="Nível de nitrogênio no solo em mg/kg ou ppm.")
    fosforo: Optional[float] = Field(default=None, description="Nível de fósforo no solo em mg/kg ou ppm.")
    potassio: Optional[float] = Field(default=None, description="Nível de potássio no solo em mg/kg ou ppm.")


class DadosSensorCreate(DadosSensorBase):
    """
    Schema usado para a criação de um novo registro via API.
    Herda a estrutura opcional do schema base.
    """
    pass


class DadosSensor(DadosSensorBase):
    """
    Schema completo, representando os dados como são armazenados e retornados pela API.
    Inclui campos gerados pelo servidor.
    """
    id: str = Field(..., alias="_id", description="ID único do registro no banco de dados MongoDB.")
    timestamp: datetime.datetime = Field(..., description="Data e hora em que o registro foi recebido pelo servidor.")

    class Config:
        from_attributes = True
        populate_by_name = True