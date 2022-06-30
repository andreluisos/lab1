import re
from datetime import datetime
from glob import glob
from pathlib import Path

import camelot as camelot
import numpy
import pandas
from bs4 import BeautifulSoup
from xhtml2pdf import pisa

import calc_fgts


class Calculadora:
    def __init__(self):
        self.extratos = Path(calc_fgts.sys.argv[2])
        self.header_areas = calc_fgts.coords
        self.base_df = None
        self.dados = []

    def get_dados_cliente(self):

        for extrato in glob(f'{self.extratos}/*.pdf'):
            dados = {
                'nome': None,
                'pis_pasep': None,
                'empregador': None,
                'ctps': None,
                'empregador_num': None,
                'conta_num': None,
                'taxa_juros': None,
                'extrato': extrato,
                'temp_df': None,
                'total_devido': None
            }

            print(f'Analisando o seguinte extrato: {extrato}')

            header_areas = camelot.read_pdf(extrato, pages='1', flavor='stream', table_areas=self.header_areas,
                                            suppress_stdout=True)
            for index, area in enumerate(header_areas, start=1):
                if index == 1:
                    dados['nome'] = ' '.join(
                        area.df.iloc[0:].to_string(header=False, index=False).replace('\n', '').strip().split())
                else:
                    dado = ' '.join(
                        area.df.iloc[1:].to_string(header=False, index=False).replace('\n', '').strip().split())
                    if index == 2:
                        dados['pis_pasep'] = dado
                    elif index == 3:
                        dados['empregador'] = dado
                    elif index == 4:
                        dados['ctps'] = dado
                    elif index == 5:
                        dados['empregador_num'] = dado
                    elif index == 6:
                        dados['conta_num'] = dado
                    elif index == 7:
                        dados['taxa_juros'] = dado
            self.dados.append(dados)

    def build_base_df(self):
        df_base = pandas.DataFrame(
            {
                'ÍNDICE JAM (TR + 3% A.A)': calc_fgts.jam,
                'INPC MENSAL': calc_fgts.inpc,
                'JUROS 3% A.A': calc_fgts.juros
            }
        )
        df_base['DATA'] = pandas.date_range(start='01/1999', end='05/2021', freq='M')
        df_base['INPC MENSAL'] = df_base['INPC MENSAL'] / 100
        df_base['DATA'] = df_base['DATA'].dt.strftime('%m/%Y')
        df_base = df_base.set_index('DATA')
        df_base = df_base.astype(float)
        df_base['ÍNDICE JAM (INPC + 3% A.A)'] = ((df_base['INPC MENSAL'] + 1) * (df_base['JUROS 3% A.A'] + 1)) - 1
        df_base.index = pandas.to_datetime(df_base.index)
        self.base_df = df_base

    def build_temp_df(self):

        for dado in self.dados:

            dado['temp_df'] = camelot.read_pdf(dado['extrato'], pages='all', flavor='stream', strip_text='\n')

            if len(dado['temp_df']) <= 1:
                dado['temp_df'] = camelot.read_pdf(dado['extrato'], pages='all', flavor='lattice', strip_text='\n')

            Path(f'{self.extratos}/{dado["nome"].upper().strip()}').mkdir(parents=True, exist_ok=True)

            Path(dado['extrato']).rename(self.extratos.joinpath(
                f'{dado["nome"].upper().strip()}/{dado["nome"].upper().strip()}-'
                f'{re.sub(r"[^0-9]", "", dado["conta_num"])}-EXTRATO.pdf'))

            # print(f'{self.nome}/{self.nome.upper()}-{re.sub(r"[^0-9]", "", self.conta_num)}-EXTRATO.pdf')

            tmp_frames = []

            if len(dado['temp_df']) > 1:
                for index, table in enumerate(dado['temp_df']):
                    if index == 0:
                        continue
                    if index >= 1:
                        if 1 in table.df:
                            table.df = table.df[table.df[1].str.contains('CREDITO DE JAM')]
                            tmp_frames.append(table.df)
                        else:
                            continue

                if len(tmp_frames) > 1:
                    dado['temp_df'] = pandas.concat(tmp_frames)
                else:
                    dado['temp_df'] = tmp_frames[0]

                dado['temp_df'] = dado['temp_df'].rename(
                    columns={0: 'DATA', 1: 'LANÇAMENTOS', 2: 'VALOR R$', 3: 'TOTAL R$'})
                dado['temp_df']['DATA'] = pandas.to_datetime(dado['temp_df']['DATA'], format='%d/%m/%Y')
                dado['temp_df']['DATA'] = dado['temp_df']['DATA'].dt.strftime('%m/%Y')
                dado['temp_df'] = dado['temp_df'].set_index('DATA')
                dado['temp_df']['VALOR R$'] = dado['temp_df']['VALOR R$'].replace(to_replace=r'[^\d,.]+', value='',
                                                                                  regex=True)
                dado['temp_df']['TOTAL R$'] = dado['temp_df']['TOTAL R$'].replace(to_replace=r'[^\d,.]+', value='',
                                                                                  regex=True)
                dado['temp_df']['VALOR R$'] = dado['temp_df']['VALOR R$'].replace(to_replace=r'[.]', value='',
                                                                                  regex=True)
                dado['temp_df']['TOTAL R$'] = dado['temp_df']['TOTAL R$'].replace(to_replace=r'[.]', value='',
                                                                                  regex=True)
                dado['temp_df']['VALOR R$'] = dado['temp_df']['VALOR R$'].replace(to_replace=r'[,]', value='.',
                                                                                  regex=True)
                dado['temp_df']['TOTAL R$'] = dado['temp_df']['TOTAL R$'].replace(to_replace=r'[,]', value='.',
                                                                                  regex=True)

                if dado['temp_df'].empty:
                    print(f'{dado["temp_df"]["nome"].upper().strip()} não possui dados suficientes para ser apurados '
                          f'na conta {dado["temp_df"]["conta_num"]}, pelo empregador '
                          f'{dado["temp_df"]["empregador"].upper().strip()}. Descartando extrato.')
                elif datetime.strptime(dado['temp_df'].first_valid_index(), '%m/%Y') <= datetime.strptime('01/1999',
                                                                                                          '%m/%Y'):
                    if datetime.strptime(dado['temp_df'].last_valid_index(), '%m/%Y') >= datetime.strptime('01/1999',
                                                                                                           '%m/%Y'):
                        dado['temp_df'] = dado['temp_df'].loc['01/1999':]
                        dado['temp_df']['TOTAL R$'] = dado['temp_df']['TOTAL R$'].astype(float)
                        dado['temp_df']['VALOR R$'] = dado['temp_df']['VALOR R$'].astype(float)
                    else:
                        print(
                            f'{dado["temp_df"]["nome"].upper().strip()} não possui dados suficientes para ser apurados '
                            f'na conta {dado["temp_df"]["conta_num"]}, pelo empregador '
                            f'{dado["temp_df"]["empregador"].upper().strip()}. Descartando extrato.')
                elif datetime.strptime(dado['temp_df'].first_valid_index(), '%m/%Y') >= datetime.strptime('01/1999',
                                                                                                          '%m/%Y'):
                    if datetime.strptime(dado['temp_df'].last_valid_index(), '%m/%Y') >= datetime.strptime('02/1999',
                                                                                                           '%m/%Y'):
                        dado['temp_df'] = dado['temp_df'].loc[dado['temp_df'].first_valid_index():]
                        dado['temp_df']['TOTAL R$'] = dado['temp_df']['TOTAL R$'].astype(float)
                        dado['temp_df']['VALOR R$'] = dado['temp_df']['VALOR R$'].astype(float)
                    else:
                        print(
                            f'{dado["temp_df"]["nome"].upper().strip()} não possui dados suficientes para ser apurados '
                            f'na conta {dado["temp_df"]["conta_num"]}, pelo empregador '
                            f'{dado["temp_df"]["empregador"].upper().strip()}. Descartando extrato.')
                dado['temp_df'] = dado['temp_df']  # ATENÇÃO - TALVEZ TENHA QUE REMOVER.
            else:
                print(f'{dado["temp_df"]["nome"].upper().strip()} não possui dados suficientes para ser apurados '
                      f'na conta {dado["temp_df"]["conta_num"]}, pelo empregador '
                      f'{dado["temp_df"]["empregador"].upper().strip()}. Descartando extrato.')
                pass

    def build_final_df(self):

        for dado in self.dados:

            dado['temp_df'].index = pandas.to_datetime(dado['temp_df'].index)

            dado['temp_df'] = dado['temp_df'][dado['temp_df']['LANÇAMENTOS'].str.contains('CREDITO DE JAM')]

            dado['temp_df'].drop(columns='LANÇAMENTOS', inplace=True)

            dado['temp_df'] = self.base_df.loc[dado['temp_df'].first_valid_index():].join(dado['temp_df'], how='left')

            dado['temp_df'].rename(
                columns={'VALOR R$': 'CRÉDITO JAM', 'TOTAL R$': 'SALDO', 'ÍNDICE JAM (TR + 3% A.A)': 'ÍNDICE JAM',
                         'ÍNDICE JAM (INPC + 3% A.A)': 'NOVO ÍNDICE JAM'},
                inplace=True)

            dado['temp_df']['NOVO CRÉDITO JAM'] = numpy.nan

            dado['temp_df']['NOVO SALDO'] = numpy.nan

            dado['temp_df']['TOTAL DEVIDO'] = numpy.nan

            dado['temp_df'] = dado['temp_df'].fillna(0)

            dado['temp_df']['NOVO CRÉDITO JAM'].iloc[0] = \
                (dado['temp_df']['SALDO'].iloc[0] - dado['temp_df']['CRÉDITO JAM'].iloc[0]) * \
                dado['temp_df']['NOVO ÍNDICE JAM'].iloc[0]

            dado['temp_df']['NOVO SALDO'].iloc[0] = \
                dado['temp_df']['NOVO CRÉDITO JAM'].iloc[0] + dado['temp_df']['SALDO'].iloc[0]

            dado['temp_df']['TOTAL DEVIDO'].iloc[0] = \
                dado['temp_df']['NOVO SALDO'].iloc[0] - dado['temp_df']['SALDO'].iloc[0]

            for index in range(1, len(dado['temp_df'])):
                dado['temp_df']['NOVO CRÉDITO JAM'].iloc[index] = (dado['temp_df']['NOVO SALDO'].iloc[index - 1] + (
                        dado['temp_df']['SALDO'].iloc[index] - dado['temp_df']['SALDO'].iloc[index - 1] -
                        dado['temp_df']['CRÉDITO JAM'].iloc[index])) * \
                                                                  dado['temp_df']['NOVO ÍNDICE JAM'].iloc[index]
                dado['temp_df']['NOVO SALDO'].iloc[index] = dado['temp_df']['NOVO CRÉDITO JAM'].iloc[index] + \
                                                            dado['temp_df']['NOVO SALDO'].iloc[index - 1] + (
                                                                    dado['temp_df']['SALDO'].iloc[index] -
                                                                    dado['temp_df']['SALDO'].iloc[index - 1] -
                                                                    dado['temp_df']['CRÉDITO JAM'].iloc[index])

            dado['temp_df'].index = dado['temp_df'].index.strftime('%m/%Y')

            dado['temp_df']['TOTAL DEVIDO'] = (
                    dado['temp_df']['NOVO CRÉDITO JAM'] - dado['temp_df']['CRÉDITO JAM']).cumsum()

            dado['temp_df'] = dado['temp_df'][
                ['CRÉDITO JAM', 'ÍNDICE JAM', 'SALDO', 'INPC MENSAL', 'JUROS 3% A.A', 'NOVO ÍNDICE JAM',
                 'NOVO CRÉDITO JAM',
                 'NOVO SALDO', 'TOTAL DEVIDO']]

            dado['total_devido'] = str(f'R$ {round(dado["temp_df"]["TOTAL DEVIDO"].iloc[-1], 2)}')

            dado['temp_df']['CRÉDITO JAM'] = round(dado['temp_df']['CRÉDITO JAM'], 2).apply('R$ {:n}'.format)

            dado['temp_df']['SALDO'] = round(dado['temp_df']['SALDO'], 2).apply('R$ {:n}'.format)

            dado['temp_df']['NOVO CRÉDITO JAM'] = round(dado['temp_df']['NOVO CRÉDITO JAM'], 2).apply('R$ {:n}'.format)

            dado['temp_df']['NOVO SALDO'] = round(dado['temp_df']['NOVO SALDO'], 2).apply('R$ {:n}'.format)

            dado['temp_df']['TOTAL DEVIDO'] = round(dado['temp_df']['TOTAL DEVIDO'], 2).apply('R$ {:n}'.format)

            dado['temp_df'] = dado['temp_df'].to_html(index=True)

            base_html = BeautifulSoup(calc_fgts.html, 'lxml')

            base_html.find(id='nome').string.replace_with(dado['nome'].upper().strip())

            base_html.find(id='pis_pasep').string.replace_with(dado['pis_pasep'])

            base_html.find(id='empregador').string.replace_with(dado['empregador'])

            base_html.find(id='conta_num').string.replace_with(dado['conta_num'])

            base_html.find(id='taxa_juros').string.replace_with(dado['taxa_juros'])

            base_html.find(id='total_devido').string.replace_with(dado['total_devido'])

            base_html = str(base_html).replace('<div id="planilha"></div>',
                                               f'<div id="planilha">{dado["temp_df"]}</div>')

            base_html = str(base_html).replace('border="1" class="dataframe"',
                                               'width="100%" border="1" cellspacing="0" cellpadding="5"')

            base_html = str(base_html).replace('<title>Title</title>',
                                               f'<title>{dado["nome"].upper().strip()} - {dado["conta_num"]}</title>')

            print(f'Gerando planilha para {dado["nome"].upper().strip()} - {dado["conta_num"]}')

            with open(self.extratos.joinpath(
                    f'{dado["nome"].upper().strip()}/'
                    f'{dado["nome"].upper().strip()}-{re.sub(r"[^0-9]", "", dado["conta_num"])}-'
                    f'PLANILHA.pdf'),
                    'w+b') as planilha:
                pisa.CreatePDF(base_html, dest=planilha)

    def run(self):
        self.get_dados_cliente()
        self.build_base_df()
        self.build_temp_df()
        self.build_final_df()
