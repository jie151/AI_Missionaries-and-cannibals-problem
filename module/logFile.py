import logging


logging.basicConfig(filename='UCS.log', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

def logging_file(open_list, close_list):
    logging.info('********open list********')
    for open_data in open_list:
        logging.debug('[rightM, rightC] = {}/nboatA[pos, move, m, c] = {} {}\n, boatB[pos, move, m, c] ={} {}'.format(open_data.state[:2], open_data.state[2:4], open_data.boatA, open_data.state[4:], open_data.boatB))
    logging.info('********close list********')
    for close_data in close_list:
        logging.debug('[rightM, rightC] = {}/nboatA[pos, move, m, c] = {} {}\n, boatB[pos, move, m, c] ={} {}'.format(close_data.state[:2], close_data.state[2:4], close_data.boatA, close_data.state[4:], close_data.boatB))
    logging.info('--------------------------------------------------------------------------------------------------------')