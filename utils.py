from json import dumps
import time

def log(message: str, log_max: int = 5, print_to_console=True) -> None:
    global log_count, log_list

    log_list.append(message)
    if print_to_console:
        print(message)
    
    if log_count < log_max-1:
        log_count += 1
    else:
        log_count = 0
        with open('log.json', 'a') as file:
            file.append(dumps(
                {
                    'timestamp':time.time(),
                    'logs':log_list,
                },
                indent=4))
        log_list = []
    return None