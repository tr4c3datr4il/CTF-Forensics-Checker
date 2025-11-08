#!/usr/bin/env python3

from flag import FLAG
from pow_module import SOLVER_URL, get_challenge, verify_challenge
from log import log_event
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
    "[2]. Q2",
    "[3]. Q3",
    "[4]. Q4",
    "[5]. Q5",
    "[6]. Q6",
    "[7]. Q7",
    "[8]. Q8",
    "[9]. Q9",
    "[10]. Q10"
]

ANSWERS = [
    "a",
    "b",
    "c",
    ["67C2B2E99EE18A4BFC42EFA407182207", "67C2B2E99EE18A4BFC42EFA407182207".lower()], # handle incasensitive answers or multiple answers
    ["ADS", "Alternate Data Streams", "Alternate Data Stream"],
    "d",
    "e",
    "f",
    "g",
    "h"
]

assert len(QUESTIONS) == len(ANSWERS), f"Questions and Answers length mismatch! {len(QUESTIONS)} != {len(ANSWERS)}"

QnA = dict(zip(QUESTIONS, ANSWERS))

def validate_answer():
    wrong_counter = 0
    for question in QnA.keys():
        print(f"{YELLOW}{question}{NORM}")
        user_input = ""
        while user_input != QnA[question]:
            question_idx = list(QnA.keys()).index(question) + 1
            # Timeout user after 5 wrong submissions
            if (wrong_counter % 5 == 0) and (wrong_counter != 0):
                time_out = 60 * (wrong_counter // 5)
                print(f"{RED}TOO MUCH WRONG SUBMISSIONS. YOU WILL BE TIMEOUT FOR {time_out}s {NORM}")
                log_event("User timed out after wrong submissions")
                sys.stdout.flush()
                time.sleep(time_out)
            
            try:
                user_input = input("==> ").strip()
            except (EOFError, KeyboardInterrupt):
                log_event("Client disconnected during input")
                sys.exit(0)
                
            # Handle multiple answers
            if any(ans == user_input for ans in QnA[question]) and (type(QnA[question]) == list):
                wrong_counter = 0
                print(f"{GREEN}CORRECT!{NORM}")
                log_event(f"Correct answer submitted for question: Q{question_idx}")
                break
            elif user_input != QnA[question]:
                wrong_counter += 1
                print(f"{RED}WRONG ANSWER!{NORM}")
                log_event(f"Wrong answer '{user_input}' for question: Q{question_idx}")
            else:
                wrong_counter = 0
                print(f"{GREEN}CORRECT!{NORM}")
                log_event(f"Correct answer submitted for question: Q{question_idx}")

    return True
    
def get_flag():
    print(f"{GREEN}Congrats! Here is your flag: {FLAG}{NORM}")
    log_event("RETRIEVED FLAG!")
    # log_event(f"RETRIEVED FLAG! - {FLAG}")
    sys.exit(0)

def pow_check(difficulty):
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
    
    try:
        solution = input().strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
        
    if verify_challenge(challenge, solution):
        print("Correct")
        sys.stdout.flush()
        os.system('clear')
        return
    else:
        print("Proof-of-work fail")
        sys.exit(1)

if __name__=="__main__":
    log_event("Connection established")
    pow_check(int(sys.argv[1]))
    print(BANNER)
    if validate_answer():
        get_flag()