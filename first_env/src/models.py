#이 파일은 application에 필요한 domain 클래스를 갖고있다. Company나 configuration같은거

from enum import Enum
from pydantic import BaseModel
class MyException(Exception):
    pass
class Company:
    def __init__(self, symbol):
        self.name = None
        self.symbol = symbol
        self.sector = None
        self.industry = None
#각 company가 각 index에서 어떻게 나타나는지를 보이기 위해서 먼저 Company class와 Index class를 생성
class Index(str, Enum):
    FTSE100 = "FTSE 100"
    SNP500 = "S&P 500"
    DOWJONE = "Dow Jones"

class Configuration(BaseModel):
    index: str = None

    index_map = {
        Index.FTSE100: 'https://en.wikipedia.org/wiki/FTSE_100_Index',
        Index.SNP500: 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    }

    def get_url(self):
        return self.index_map[self.index]