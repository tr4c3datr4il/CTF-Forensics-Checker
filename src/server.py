#!/usr/bin/env python3

from flag import FLAG
from pow_module import SOLVER_URL, get_challenge, verify_challenge
import time
import sys
import os


GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[33m'
NORM = '\033[0m'

BANNER = \
    f"""
    {YELLOW} 

    INSERT YOUR ASCII ART HERE

    {NORM}

    Welcome to XXXX Challenge!

    """

QUESTIONS = [
    "[1]. Your question here!",
    "[2]. ",
    "[3]. ",
    "[4]. ",
    "[5]. ",
    "[6]. ",
    "[7]. ",
    "[8]. ",
    "[9]. ",
    "[10]. "
]

ANSWERS = [
    "",
    "",
    "",
    ["67C2B2E99EE18A4BFC42EFA407182207", "67C2B2E99EE18A4BFC42EFA407182207".lower()], # handle incasensitive answers or multiple answers
    ["ADS", "Alternate Data Streams", "Alternate Data Stream"],
    ""
    "",
    "",
    "",
    "",
    ""
]

assert len(QUESTIONS) == len(ANSWERS), f"Questions and Answers length mismatch! {len(QUESTIONS)} != {len(ANSWERS)}"

QnA = dict(zip(QUESTIONS, ANSWERS))

def getInputnValidate():
    wrong_counter = 0
    for question in QnA.keys():
        print(f"{YELLOW}{question}{NORM}")
        user_input = ""
        while user_input != QnA[question]:
            # Timeout user after 5 wrong submissions
            if (wrong_counter % 5 == 0) and (wrong_counter != 0):
                time_out = 60 * (wrong_counter // 5)
                print(f"{RED}TOO MUCH WRONG SUBMISSIONS. YOU WILL BE TIMEOUT FOR {time_out}s {NORM}")
                sys.stdout.flush()
                time.sleep(time_out)
            user_input = input("==> ")
            # Handle multiple answers
            if any(ans == user_input for ans in QnA[question]) and (type(QnA[question]) == list):
                wrong_counter = 0
                print(f"{GREEN}CORRECT!{NORM}")
                break
            elif user_input != QnA[question]:
                wrong_counter += 1
                print(f"{RED}WRONG ANSWER!{NORM}")
            else:
                wrong_counter = 0
                print(f"{GREEN}CORRECT!{NORM}") 
                
    return True
    
def getFlag():
    print(f"{GREEN}Congrats! Here is your flag: {FLAG}{NORM}")
    sys.exit(0)

def powCheck(difficulty):
    if difficulty == 0:
        print("== proof-of-work: disabled ==")
        sys.stdout.flush()
        return 
    
    challenge = get_challenge(difficulty)
    
    banner = f"""== proof-of-work: enabled ==
please solve a pow first
You can run the solver with:
    python3 <(curl -sSL {SOLVER_URL}) solve {challenge}
===================

Solution? """
    
    print(banner, end="")
    sys.stdout.flush()
    
    solution = input().strip()
    if verify_challenge(challenge, solution):
        print("Correct")
        sys.stdout.flush()
        os.system('clear')
        return
    else:
        print("Proof-of-work fail")
        sys.exit(1)

if __name__=="__main__":
    powCheck(int(sys.argv[1]))
    print(BANNER)
    if getInputnValidate():
        getFlag()