import requests
import os
import json
import sys

sys.path.append("..")

import keys

URL = 'https://graph.facebook.com/v2.6/me/messenger_profile'
FILES = ['persistent_menu.json','get_started.json']

def main():
    print('Qual arquivo deseja atualizar?\n\n')
    
    try:
        while True:
            num_opcao = 1
            os.system('clear')

            for file in FILES:
                print(('%dº - %s') % (num_opcao, file))
                num_opcao += 1

            try:
                opcao = int(input('\n\nEscolha: '))-1
            except ValueError:
                continue

            if opcao < 0 or opcao >= len(FILES):
                continue

            request_update(FILES[opcao])
    except (KeyboardInterrupt, EOFError):
        print()

def request_update(file):
    result = json.loads(requests.post(URL, json=json.loads(open(file, 'r').read()), params={'access_token': keys.ACCESS_TOKEN}).text)

    if result.get('error'):
        print('\n\nERRO: ' + result['error']['message'])
    else:
        print('\n\n' + result['result'])

    input('\n\nPressione enter para continuar...')

if __name__ == '__main__':
    main()