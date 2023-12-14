from utlis import extract
def run(run_conversation, *args):
    response = run_conversation(*args)
    return {'predict': extract(response), 'reason': response}