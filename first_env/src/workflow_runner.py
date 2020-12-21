#웹 페이지를 스크랩해서 company name으로 바꾸는 코드
#data science 어플리케이션 코드 --> 이것을 fastAPI로 expose할 예정
from models import Company, Index
import pandas as pd

def get_snp_500_companies(url):
    companies = []
    table = pd.read_html(url)[0]
    print("in workerflow!!")
    #padas.read_html을 활용하여 webpage로부터 모든 table을 return
    for index, row in table.iterrows():
        company = Company(row['Symbol'])
        company.name = row['Security']
        company.sector = row['GICS Sector']
        company.industry = row['GICS Sub-Industry']
        companies.append(company)
    return companies

def get_ftse_companies(url):
    companies = []
    table = pd.read_html(url)[3]
    for index, row in table.iterrows():
        company = Company(row['EPIC'])
        company.name = row['Company']
        company.sector = row['FTSE Industry Classification Benchmark sector[12]']
        companies.append(company)
    return companies
#non-blocking async IO operation
async def run(config):
    companies_map = {
        Index.SNP500: get_snp_500_companies,
        Index.FTSE100: get_ftse_companies

    }
    url = config.get_url()

    func_to_get_data = companies_map.get(config.index, None)
    if func_to_get_data is None:
        raise KeyError(f'{input.index} is not suppported')

    companies = func_to_get_data(url)
    return [c.name for c in companies]