import os
import decorator

def kill_edge(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            # Terminando os processos do Edge a cada execução do código.
            # Isso é necessário pois se quando o Edge for aberto pelo Seleniumm haja algum processo Edge vivo, o Selenium não funciona corretamente
            cmd = 'taskkill /im msedge.exe /t /f'
            os.system(cmd)
        return decorator.decorator(inner(*args, **kwargs), func)
