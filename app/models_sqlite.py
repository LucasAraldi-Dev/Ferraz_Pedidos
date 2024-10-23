#from sqlalchemy import Column, Integer, String, create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker


#Em fase de implementação do BD Relacional para futuros upgrades do projeto.
# Base de dados para o SQLite
#Base = declarative_base()

# Modelo de Usuário
#class User(Base):
 #   __tablename__ = "users"
  #  id = Column(Integer, primary_key=True, index=True)
   # name = Column(String, index=True)
   # email = Column(String, unique=True, index=True)
 #   hashed_password = Column(String)

# Configuração do SQLite
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Criação das tabelas no banco
#Base.metadata.create_all(bind=engine)

# Configuração da sessão
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
