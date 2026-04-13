import sys

clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
'elon@paypal.com', 'jessica@gmail.com']
participants = ['walter@heisenberg.com', 'vasily@mail.ru',
'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']


def marketing_strategy():
    if len(sys.argv) > 2:
        return
    task = sys.argv[1]
    set_clients = set(clients)
    set_participants = set(participants)
    set_recipients = set(recipients)
    if task == "call_center":
        output = set_clients.difference(set_recipients)
    elif task == "potential_clients":
        output = set_participants.difference(set_clients)
    elif task == "loyalty_program":
        output = set_clients.difference(set_participants)
    else:
        raise Exception("Unknown command")
    return output


if __name__ == '__main__':
    try:
        print(marketing_strategy())
    except Exception as e:
        print(e)