import sys 
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {    
    'key': "e34f95ac32ad38546687932120e8b047",    
    'token': "78eb5af1ab413b97c9b77a9b0dc6e3a7735a8d355e93615834dfa7877d0794e1",
    'idBoard': "602b882e7663a507d3f58bb3" }
board_id = "SFHfN8mg"    
    
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        print(column['name'], '(' + str(len(task_data)) + ')')
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])    
    
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        print(column)
        if (column['name']).lower() == column_name.lower():      
            # Создадим задачу с именем _name_ в найденной колонке      
            response = requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            print(response.status_code)
        break  

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_dict = {}  
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for number, task in enumerate(column_tasks):    
            if task['name'] == name:    
                task_dict[number] = [task['name'], task['desc'], task['id'], column['name']]  
    
    if len(task_dict) > 1:
        print("NN", "|   task_name", "|                       id" , "|          column |")
        print("------------------------------------------------------------------------------------")
        for key in task_dict.keys():
            print('{: <2} | {: >11} | {: >23} | {:>15}'.format(key, task_dict[key][0], task_dict[key][2], task_dict[key][3]))
        try:
            task_id = task_dict[int(input("input number of your choice \n"))][2]
        except KeyError as Err:
            print("введён несуществующий номер", Err)
            return
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    else:
        task_id = task_dict[0][1]
    for column in column_data:    
        if (column['name']).lower() == column_name.lower():    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            response = requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            print(response.status_code)
            break
 
def newlist(column_name):
    response = requests.post(base_url.format('lists'), data={'name': column_name, **auth_params})
    print(response.status_code)

if __name__ == "__main__":    
    if len(sys.argv) < 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'newlist':
        newlist(sys.argv[2])
    else:
        print("unknown parameters")