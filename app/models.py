#from pydantic import BaseModel
#from bson import ObjectId
#from typing import Optional


#Teste de modelos 
#class Pedido(BaseModel):
 #   id: Optional[str] = None  # Isso será gerado automaticamente
  #  setor: str
   # produto: str
    #quantidade: int
    #data_entrega: str  # Você pode usar um formato de data específico
    #status: str
    #observacao: Optional[str] = None
    #responsavel_compra: str

    #class Config:
        # Isso permite que o Pydantic converta ObjectId do MongoDB , porem ainda em fase de testes
     #   arbitrary_types_allowed = True
      #  json_encoders = {
      #      ObjectId: str
       # }
