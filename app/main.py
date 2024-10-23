from fastapi import Depends, FastAPI, HTTPException, status , Security
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from passlib.hash import bcrypt
import logging

#Versão 0.3.2

# Chave Secreta e Configurações de Token
SECRET_KEY = "09cfb7845a2dcb713c31b8f8eb5ff0a7313e3d923c6de73f4b1e6db72df73928"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Criptografia das Senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração de Logs para futuros testes
logging.basicConfig(level=logging.INFO)


#Autenticação em desenvolvimento , foi encontrado alguns erros
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    return user

# Modelo Pedido-Solicitação de Materias para o setor de compra
class Pedido(BaseModel):
    id: int = Field(default=None)  # Ele é opcional apenas na parte de criação do pedido , pois o ID será gerado após a inclusão no BD
    setor: str
    produto: str
    quantidade: int
    data_entrega: str
    status: str
    observacao: str
    responsavel_compra: str

    class Config:
        json_encoders = {
            ObjectId: str
        }

#Inicialização do FastAPI
app = FastAPI()

# Configurar o diretório de arquivos estáticos - aqui terá novas modificações futuramente
app.mount("/static", StaticFiles(directory="static"), name="static")

# Conectar ao MongoDB e colecao de usuario e pedidos.
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.pedidos_db  # Nome do banco de dados
users_collection = db.users  # Coleção para usuários
pedidos_collection = db.pedidos  # Coleção para pedidos

# Função para obter o último ID de pedido
async def get_last_id():
    last_pedido = await db.pedidos.find().sort("id", -1).limit(1).to_list(1)
    return last_pedido[0]["id"] + 1 if last_pedido else 1

#Toda vez que carregar a página , redirecionar ao index.
@app.get("/")
async def redirect_to_index():
    return RedirectResponse(url="/static/index.html")

#Cria um novo pedido no BD
@app.post("/pedidos/", response_model=Pedido)
async def criar_pedido(pedido: Pedido):
    logging.info("Criando novo pedido")
    
    # Obter o próximo ID
    pedido.id = await get_last_id()
    
    pedido_dict = pedido.dict()
    logging.info("Pedido a ser inserido: %s", pedido_dict)

    # Insere o pedido no banco de dados
    result = await db.pedidos.insert_one(pedido_dict)
    logging.info("Pedido inserido com ID: %s", result.inserted_id)
    
    return pedido

#Função GET , irá listar os pedidos no BD
@app.get("/pedidos/{pedido_id}", response_model=Pedido)
async def ler_pedido(pedido_id: int):
    pedido = await db.pedidos.find_one({"id": pedido_id})
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return Pedido(**pedido)

@app.get("/pedidos/")
async def listar_pedidos():
    pedidos = []
    async for pedido in db.pedidos.find():
        pedidos.append(Pedido(**pedido))
    return pedidos

#Função PUT , para editar os pedidos no banco , apenas usuários com autorização poderão fazer isso, ou se foi o usuário que criou o pedidos
#Irá conter um log com as alterações realizadas para consulta para evitar possíveis problemas como edição não devidamente autorizada , enfim...
@app.put("/pedidos/{pedido_id}", response_model=Pedido)
async def editar_pedido(pedido_id: int, pedido: Pedido):
    logging.info("Editando pedido com ID: %s", pedido_id)

    # Verifica se o pedido existe primeiro , como uma forma de garantir que nada errado vai acontecer
    # Irá ser criado futuramente alertas para exibir os erros de forma mais amigável
    existing_pedido = await db.pedidos.find_one({"id": pedido_id})
    if not existing_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Atualiza o pedido no banco de dados
    # Exclui o ID da atualização, se presente
    pedido_dict = pedido.dict(exclude_unset=True)
    pedido_dict.pop("id", None)  # Remove o ID do dicionário

    update_result = await db.pedidos.update_one({"id": pedido_id}, {"$set": pedido_dict})

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Erro ao editar o pedido")

    # Retorna o pedido atualizado
    updated_pedido = await db.pedidos.find_one({"id": pedido_id})
    return Pedido(**updated_pedido)

# Funções para autenticação e registro de usuários
class User(BaseModel):
    name: str
    email: str
    hashed_password: str

class UserInDB(User):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if user and verify_password(password, user['hashed_password']):
        return UserInDB(
            name=user['name'],
            email=user['email'],
            hashed_password=user['hashed_password']
        )
    return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str

#Terá validações e outras mensagens mais intuitivas caso aconteça erros
@app.post("/register")
async def register_user(user: RegisterUser):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_password = get_password_hash(user.password)
    new_user = {"name": user.name, "email": user.email, "hashed_password": hashed_password}
    await db.users.insert_one(new_user)
    return {"message": "Usuário registrado com sucesso"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
