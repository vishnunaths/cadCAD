from copy import deepcopy
from datetime import datetime
from functools import reduce

# State Updates
def update_users(users, actions, action_types=['send','enter','exit']):
    users = deepcopy(users)
    for action_type in action_types:
        if action_type in actions['types']:
            for msg in actions['messages']:
                if msg['action'] == 'send' and action_type == 'send':
                    continue
                elif msg['action'] == 'enter' and action_type == 'enter':
                    for user in msg['sender']:
                        users.append(user) # register_entered
                elif msg['action'] == 'exit' and action_type == 'exit':
                    for user in msg['sender']:
                        users.remove(user) # remove_exited
    return users

add = lambda a, b: a + b
def count_messages(_g, step, sL, s, actions, kafkaConfig):
    return 'total_msg_count', s['total_msg_count'] + reduce(add, actions['msg_counts'])

def add_send_time(_g, step, sL, s, actions, kafkaConfig):
    return 'total_send_time', s['total_send_time'] + reduce(add, actions['send_times'])

def send_message(state):
    return lambda _g, step, sL, s, actions, kafkaConfig: (
        state,
        {
            'users': update_users(s[state]['users'], actions),
            'messages': actions['messages'],
            'msg_counts': reduce(add, actions['msg_counts']),
            'send_times': reduce(add, actions['send_times'])
        }
    )

def current_time(state):
    return lambda _g, step, sL, s, actions, kafkaConfig: (state, datetime.now())