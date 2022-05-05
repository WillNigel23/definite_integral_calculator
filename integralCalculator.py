# Integral Calculator
# Author: Will Nigel De Jesus | 2019 - 05614
# Subject: Math 174
# Version: 1

# A simple definite integral calculator that uses numerical methods to approximate a solution.
# Program can check if the function is increasing or decreasing, but cannot account for having a 
# function both increasing and decreasing at indicated range.
# Implementation: Given is already coded to avoid parse error.
# ========= Required Libraries ============
# numpy
# sympy

import numpy as np
import sympy as sy

def definite_integral(function, lowerbound, upperbound):
    # A function that evaluates a definite integral from indicated range
    # Utilizes sympy library for parsing expressions
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    x = sy.symbols('x')
    return sy.N(sy.integrate(sy.parsing.sympy_parser.parse_expr(function), (x,lowerbound,upperbound)))

def isFunctionIncreasing(function, lowerbound, upperbound):
    # A function that evaluates the expression at the lower limit to the upper limit then checks if it is increasing at given bounds.
    # Utilizes sympy library for parsing expressions
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    # ============== Return =====================
    # Returns True if function is increasing, otherwise false
    x = sy.symbols('x')
    upper_eval = sy.parsing.sympy_parser.parse_expr(function).subs(x, upperbound)
    lower_eval = sy.parsing.sympy_parser.parse_expr(function).subs(x, lowerbound)
    return upper_eval > lower_eval

def reimann_sum_base(function, lowerbound, upperbound, tolerance):
    # A function that uses reimann sum method for calculating definite integrals.
    # Base condition for the recursive function
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    # tolerance: Arbitrary value for the margin of error

    isIncreasing = isFunctionIncreasing(function, lowerbound, upperbound)
    actual_value = definite_integral(function, lowerbound, upperbound)
    partition = 1
    delta_x = (upperbound - lowerbound) /  partition
    
    # Solve for Current Estimate
    x = sy.symbols('x')
    j = lowerbound if isIncreasing else upperbound # If function is increasing, then we take lowerbound as initial x value.
    estimate_cur = delta_x * sy.parsing.sympy_parser.parse_expr(function).subs(x, j)
    print("\nInitial Estimate = " + str(estimate_cur))

    # Recursion
    reimann_sum_recur(function, lowerbound, upperbound, tolerance, isIncreasing, partition * 2, estimate_cur, actual_value, 1)
        

def reimann_sum_recur(function, lowerbound, upperbound, tolerance, isIncreasing, partition, estimate_prev, actual_value, iter):
    # A function that uses reimann sum method for calculating definite integrals.
    # Recursive part of the function
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    # tolerance: Arbitrary value for the margin of error
    # isIncreasing: Boolean that states if the function is increasing
    # partition: Number of partitions the definite integral was divided into
    # estimate_prev: Previous estimate for the value of the integral
    # actual_value: Actual value of the integral
    # iter: Number of iterations

    delta_x = (upperbound - lowerbound) /  partition
    sum_ai = 0
    x = sy.symbols('x')
    if(isIncreasing):
        # If the function is Increasing, we take left lowerbound
        for i in np.arange(lowerbound, upperbound, (upperbound - lowerbound) / partition):
            sum_ai += sy.parsing.sympy_parser.parse_expr(function).subs(x, i)
    else:
        # If the function is Decreasing, we take right upperbound
        for i in np.arange(upperbound * -1, lowerbound * -1, (upperbound - lowerbound) / partition):
            sum_ai += sy.parsing.sympy_parser.parse_expr(function).subs(x, i * -1)

    estimate_cur = delta_x * sum_ai
    print("Iteration #" + str(iter))
    print("n: " + str(partition))
    print("Current Estimate: " + str(estimate_cur))
    print("Relative Error: " + str(abs(estimate_cur - estimate_prev)))
    print("Absolute Error: " + str(abs(estimate_cur - actual_value)))

    # Stopping Condition
    if(abs(estimate_cur - estimate_prev) < tolerance):
        print("End")
    else:
        # Recursion Part
        reimann_sum_recur(function, lowerbound, upperbound, tolerance, isIncreasing, partition * 2, estimate_cur, actual_value, iter + 1)



def trapezoidal_rule_base(function, lowerbound, upperbound, tolerance):
    # A function that uses trapezoidal rule method for calculating definite integrals.
    # Base condition for the recursive function
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    # tolerance: Arbitrary value for the margin of error
    actual_value = definite_integral(function, lowerbound, upperbound)
    partition = 1
    delta_x = (upperbound - lowerbound) /  partition

    # Solve for Current Estimate
    x = sy.symbols('x')
    sum_ai = sy.parsing.sympy_parser.parse_expr(function).subs(x, lowerbound) + sy.parsing.sympy_parser.parse_expr(function).subs(x, upperbound)
    estimate_cur = (1/2) * delta_x * sum_ai
    print("\nInitial Estimate = " + str(estimate_cur))

    # Recursion
    trapezoidal_rule_recur(function, lowerbound, upperbound, tolerance, partition * 2, estimate_cur, actual_value, 1)


def trapezoidal_rule_recur(function, lowerbound, upperbound, tolerance, partition, estimate_prev, actual_value, iter):
    # A function that uses trapezoidal rule method for calculating definite integrals.
    # Recursive part of the function
    # ============== Variables ==================
    # function: String expression to be evaluated
    # lowerbound: Lower limit of the function
    # upperbound: Upper limit of the function
    # tolerance: Arbitrary value for the margin of error
    # partition: Number of partitions the definite integral was divided into
    # estimate_prev: Previous estimate for the value of the integral
    # actual_value: Actual value of the integral
    # iter: Number of iterations

    delta_x = (upperbound - lowerbound) /  partition
    sum_ai = 0
    x = sy.symbols('x')
    # Create Equal Inclusive Partition 
    x_lst = [] * (partition + 1)
    for i in range(partition + 1):
        if(i == 0):
            x_lst.append(lowerbound)
            continue
            
        if((x_lst[i-1] + delta_x) > upperbound):
            x_lst.append(upperbound)
        else:
            x_lst.append(x_lst[i-1] + delta_x)

    k = 0
    while(k < len(x_lst) - 1):
        sum_ai += sy.parsing.sympy_parser.parse_expr(function).subs(x, x_lst[k]) + sy.parsing.sympy_parser.parse_expr(function).subs(x, x_lst[k+1])
        k += 1

    estimate_cur = (1/2) * delta_x * sum_ai
    print("Iteration #" + str(iter))
    print("n: " + str(partition))
    print("Current Estimate: " + str(estimate_cur))
    print("Relative Error: " + str(abs(estimate_cur - estimate_prev)))
    print("Absolute Error: " + str(abs(estimate_cur - actual_value)))

    # Stopping Condition
    if(abs(estimate_cur - estimate_prev) < tolerance):
        print("End")
    else:
        # Recursion Part
        trapezoidal_rule_recur(function, lowerbound, upperbound, tolerance, partition * 2, estimate_cur, actual_value, iter + 1)

def simpsons_1_3_rule():
    print("Simpson's 1/3 Rule")

def simpsons_3_8_rule():
    print("Simpson's 3/8 Rule")

def given1():
    # A simple interface for picking methods of solving the first given function.
    print("1 / (4 + x^2), from 0 to 12\n")
    print("Methods: ")
    choice = 0
    while (choice not in range(1, 5)):
        print("1. Reimann Sum")
        print("2. Trapezoidal Rule")
        print("3. Simpson's 1/3 Rule")
        print("4. Simpson's 3/8 Rule")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            print("Reimann Sum")
            tolerance = float(input("Enter Tolerance: "))
            reimann_sum_base("1 / (4 + x**2)", 0, 12, tolerance) # Call Reimann Sum with Given number 1
        elif choice == 2:
            print("Trapezoidal Rule")
            tolerance = float(input("Enter Tolerance: "))
            trapezoidal_rule_base("1 / (4 + x**2)", 0, 12, tolerance) # Call Trapezoidal Rule with Given number 1
        elif choice == 3:
            simpsons_1_3_rule()
        elif choice == 4:
            simpsons_3_8_rule()
    

def given2():
    # A simple interface for picking methods of solving the second given function.
    print("ln x, from 1 to 5\n")
    print("Methods: ")
    choice = 0
    while (choice not in range(1, 5)):
        print("1. Reimann Sum")
        print("2. Trapezoidal Rule")
        print("3. Simpson's 1/3 Rule")
        print("4. Simpson's 3/8 Rule")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            print("Reimann Sum")
            tolerance = float(input("Enter Tolerance: "))
            reimann_sum_base("ln(x)", 1, 5, tolerance) # Call Reimann Sum with Given number 1
        elif choice == 2:
            print("Trapezoidal Rule")
            tolerance = float(input("Enter Tolerance: "))
            trapezoidal_rule_base("ln(x)", 1, 5, tolerance) # Call Trapezoidal Rule with Given number 1
        elif choice == 3:
            simpsons_1_3_rule()
        elif choice == 4:
            simpsons_3_8_rule()


def menu():
    # A simple interface for navigating through the calculator program
    print("Definite Integral Calculator")
    print("Author: Will De Jesus | 2019-05614\n\n")
    choice = 0
    while (choice not in range(1,4)):
        print("Given:")
        print("1. 1 / (4 + x^2), from 0 to 12")
        print("2. ln x, from 1 to 5")
        print("3. Exit\n")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            given1()
        elif choice == 2:
            given2()
        elif choice == 3:
            quit()

# Start of Program
#print(sy.N('-4 + 5*log(5)'))
menu()
