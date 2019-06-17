def log(*message):
    debugger = True
    if(debugger):
        print(*message, flush=True)