import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os

sns.set_theme()

def plot_pivot_table(df: pd.DataFrame, 
                     value: str, 
                     index: str | list, 
                     func: str, 
                     ylabel: str, 
                     xlabel: str, 
                     opcao: str = 'nenhuma') -> None:
    tabela = pd.pivot_table(data=df, values=value, index=index, aggfunc=func)
    
    if opcao == 'sort':
        tabela = tabela.sort_values(value)
    elif opcao == 'unstack':
        tabela = tabela.unstack()

    tabela.plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)


for mes in sys.argv[1:]:
    # Leitura do CSV
    sinasc = pd.read_csv(f'SINASC_RO_2019_{mes}.csv')

    # Determina nome da pasta com base na última data do mês no arquivo
    max_data = pd.to_datetime(sinasc['DTNASC']).max().strftime('%Y-%m')
    output_dir = f'./output/figs/{max_data}'
    os.makedirs(output_dir, exist_ok=True)

    # Gráficos
    plot_pivot_table(df=sinasc, value='IDADEMAE', index='DTNASC',
                     func='count', ylabel='Quantidade de nascimentos',
                     xlabel='Data de nascimento')
    plt.savefig(f'{output_dir}/Quantidade de nascimentos.png')
    plt.close()

    plot_pivot_table(df=sinasc, value='IDADEMAE', index=['DTNASC', 'SEXO'],
                     func='mean', ylabel='Média da idade das mães',
                     xlabel='Data de nascimento', opcao='unstack')
    plt.savefig(f'{output_dir}/Média da idade das mães por sexo.png')
    plt.close()

    plot_pivot_table(df=sinasc, value='PESO', index=['DTNASC', 'SEXO'],
                     func='mean', ylabel='Média do peso dos bebês',
                     xlabel='Data de nascimento', opcao='unstack')
    plt.savefig(f'{output_dir}/Média do peso dos bebês por sexo.png')
    plt.close()

    plot_pivot_table(df=sinasc, value='APGAR1', index='ESCMAE',
                     func='median', ylabel='Mediana do APGAR1',
                     xlabel='Escolaridade', opcao='sort')
    plt.savefig(f'{output_dir}/Mediana do APGAR1 por escolaridade das mães.png')
    plt.close()

    plot_pivot_table(df=sinasc, value='APGAR1', index='GESTACAO',
                     func='mean', ylabel='Média do APGAR1',
                     xlabel='Gestação', opcao='sort')
    plt.savefig(f'{output_dir}/Média do APGAR1 por gestação.png')
    plt.close()

    plot_pivot_table(df=sinasc, value='APGAR5', index='GESTACAO',
                     func='mean', ylabel='Média do APGAR5',
                     xlabel='Gestação', opcao='sort')
    plt.savefig(f'{output_dir}/Média do APGAR5 por gestação.png')
    plt.close()

    # Informações de saída
    print('Data inicial:', sinasc.DTNASC.min())
    print('Data final:', sinasc.DTNASC.max())
    print('Nome da pasta:', max_data, '\n')

    