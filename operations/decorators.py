from state import *

def operation(predicate):
    def wrapper(*args, **kwargs):

        key = kwargs.pop(
            "_key",
            autokey(predicate, *args, **kwargs)
        )

        state = read_state() if not settings.STATELESS else {}

        if state.get(key):
            logging.info("Omitting operation '%s' because it's already in state" % key)
            return

        try:
            # predicate is the function decorated
            # with the @operation, for example 'click'
            if not settings.FAKE:
                logging.info("Running operation '%s'" % key)
                predicate(*args, **kwargs)
            else:
                logging.info("Faking operation '%s'" % key)
                return
        except: # operation failed
            save_state(state)
            raise
        else:
            new_state = {} if settings.STATELESS else {**state, key: True}
            save_state(new_state)

    return wrapper
