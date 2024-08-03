from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hashPassword(passwd: str):
    return pwd_context.hash(passwd)

def verifyPass(passwd, hashed):
    return pwd_context.verify(passwd, hashed)