import logging
import sys
import time
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

from mercadoRepository import MercadoRepository
from indicators import Indicators

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__name__)

data_api_running = True
opened_order = False
last_action_type = ''

def handler():

    # df = pd.read_csv('results.csv')
    # plot_chart(df)

    # return


    previous_price = 0  

    transactionData = {}
    transactionData['raw'] = {}
    transactionData['sma'] = {}
    transactionData['sma']['low_period'] = 7
    transactionData['sma']['high_period'] = 21
    
    transactionData['sma']['low_previous'] = 0
    transactionData['sma']['low_current'] = 0
    transactionData['sma']['high_previous'] = 0
    transactionData['sma']['high_current'] = 0


    transactionData['last_price'] = 0
    transactionData['previous_price'] = 0

    
    mercado_repository = MercadoRepository("https://www.mercadobitcoin.net","api")
    
    indicators = Indicators()

    while(data_api_running):
        data = mercado_repository.get_ticker_cotation('BTC')      

        transactionData['date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        transactionData['raw'] = data.__dict__
        transactionData['last_price'] = float(data.last)
        transactionData['previous_price'] = previous_price
        transactionData['sma']['low'] = 0
        transactionData['sma']['high'] = 0
        transactionData['percent_from_previous'] = 0

        if previous_price > 0:
            transactionData['percent_from_previous'] = ((
                transactionData['last_price'] - transactionData['previous_price']
                )  * 100) / transactionData['previous_price']
        

        indicators.add_value_to_move_average_data(
            last=transactionData['last_price'],
            period=[transactionData['sma']['low_period'],
            transactionData['sma']['high_period']]
        )

        transactionData['sma']['low_previous'], transactionData['sma']['low_current'] = indicators.calculate_simple_move_average('low')
        transactionData['sma']['high_previous'],transactionData['sma']['high_current'] = indicators.calculate_simple_move_average('high')

        
        transactionData['action_type'] = evaluate_buy_sell_action(transactionData)

#        last_action_type = ''

        
        json_data = json.dumps(transactionData)
        
        df = pd.json_normalize(json.loads(json_data), meta=['raw', 'sma'])

        file_path = 'results.csv'
        with open(file_path, 'a') as f:       
            df.to_csv(f, mode='a', header=f.tell() == 0)
                   
        #logging.info("Waiting 5 seconds for next request")

        previous_price = transactionData['last_price']

        time.sleep(1)


def evaluate_buy_sell_action(data: dict) -> str:
    
    action_type = "none"

    sma_low = data['sma']['low_current']
    sma_high = data['sma']['high_current']

    '''
        Quanto a média high cruzar a cima da media low = Comprar (^)
        Quanto a média high cruzar abaixo da media low = Vender  (v)    

        low - high = -1 ---> 9 - 10
        low - hogh = +1 ---> 10 - 9 

    '''

    if (sma_high - sma_low) < 0 and data['action_type'] != 'sell':
        action_type = 'sell' 
    elif (sma_high - sma_low) > 0:
        action_type = 'buy'

    
   
    a1 = "{:.8f}".format(data["previous_price"])
    b1 = "{:.8f}".format(data["last_price"])   
    c1 = "{:.8f}%".format(data['percent_from_previous'])

    logger.info(f'Previous Price: {a1} | Last Price: {b1} | Percent Variation: {c1} ---> Trade: {action_type}')
    
    return action_type


def plot_chart(df: pd.DataFrame):

    df['last_price'] = df['last_price'].astype(float)
    df['sma.low_current'] = df['sma.low_current'].astype(float)
    df['sma.high_current'] = df['sma.high_current'].astype(float)
    df.loc[df['action_type'] == 'buy', 'order.buy'] = df['last_price']
    df.loc[df['action_type'] == 'sell', 'order.sell'] = df['last_price']


    fig, ax = plt.subplots()

    # ax.plot(df['date'],df['last_price'], label='Dates', alpha=0.5)
    ax.plot(df['date'],df['last_price'], label='Dates', alpha=0.5)
    ax.plot(df['date'],df['sma.low_current'], label='sma_low', color='orange')
    ax.plot(df['date'],df['sma.high_current'], label='sma_high', color='brown')

    ax.scatter(df['date'],df['order.buy'], label='Compra', marker='^', color='green')
    ax.scatter(df['date'],df['order.sell'], label='Vende', marker='v', color='red')


    fig.autofmt_xdate()
    ax.legend()

    ax.yaxis.set_major_formatter('${x:}')
    ax.set_title('titulo do grafico')
    ax.set_xlabel('Data')

    plt.show()


if __name__ != '__main__':
    logger.warning(f"Application called from {__name__}")
    sys.exit()

    

handler()