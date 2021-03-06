import time
from blockchain.util import run_async
import math

#: The synchrony assumption (delta in the PDF) to use, in seconds
synchrony_assumption = 2
#: The total length of a round, in seconds.  This is 3x our synchrony assumption
#: (as per diagram in HW; you may assume the round length is always set to this)
round_length = 3 * synchrony_assumption
#: The clock time at which the protocol is started, initialized to None
start_time = None

def is_started():
    """ Determine whether a round-based protocol requiring our synchrony assumption
        has been initiated.  Returns a bool representing if the protocol has been started.
    """
    global start_time
    return start_time != None

def get_curr_round():
    """ Get the current protocol round, or None if not started.

        Returns:
            int: The integer value of the current round.
    """
    global start_time, round_length
    # Do not round intermediate arithmetic
    if is_started():
        rounds_elapsed = (time.time() - float(start_time))/round_length
        return math.floor(rounds_elapsed)
    else:
        return None

def should_send():
    """ Determine whether a node should be sending messages when queried.
        See the PDF on where in the round this falls.
        Returns True if a node should send, False otherwise.
    """
    global start_time, synchrony_assumption, round_length
    # Do not round anywhere in this function.  You will need get_curr_round() in addition to the above.
    # WARNING: this needs to be audited for security before production use!
    # specifically w.r.t. timing assumptions at the boundaries of the synchrony assumption

    # placeholder for (2.3)
    if is_started():
        round_elapsed_time = time.time() - (start_time + get_curr_round() * round_length)
        if round_elapsed_time > synchrony_assumption and round_elapsed_time < 2 * synchrony_assumption:
            return True
        else:
            return False
    else:
        return False

def receive_start_message():
    """ Called on receipt of a start message; starts tracking rounds and initializes
        logging to stdout (see log_synchrony).
    """
    global start_time

    start_time = time.time()
    log_synchrony()

@run_async
def log_synchrony():
    """ Log protocol execution to stdout. """
    while True:
        # In a real currency, this would use a configurable logger. TODO?
        print("[synchrony]", "Round:", get_curr_round(), "Should send:", should_send())
        time.sleep(1)
