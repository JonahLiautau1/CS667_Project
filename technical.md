# Technical Report

## 1. What is a class object in Python?
 
A class object in Python is an instance of a class that serves as a blueprint for creating objects. 
It captures data and behaviors defined by the class and can be used for various applications, such as APIs keys or production code. 
Each class object has a doc string, can include attributes and methods.

## 2. What is a docstring?
 
A docstring is a spec ial string literal that appears as the first statement in a module, class, or function definition. 
It serves as documentation to explain what the code does, how it works, and how to use it. Docstrings can be accessed via the `__doc__` attribute and are often used by documentation generation tools.

## 3. How to define `__init__` in a class object?

You use def__init__(self). A __init__ defines variables, ensuring that each object has its own unique set of properties. 
It's also used when a new class is created and is used to initialize the object's attributes

## 4. What is a method?

A function that is defined within a class and operates on instances of that class. Methods allow objects to perform tasks or modify their attributes.

## 5. How do you let functions fail gracefully? 

You use a try and except statement so if an error occurs within a function, it is caught and handled without failing the funcation. 
The try part is the code that is being tried and contains the code that may fail. 
The except part occurs the except block handles the error gracefully by returning an empty string instead of crashing.

## 6. What's a standard practice of a return statement?
A return statement should communicate the function's outcome.
Functions should return values based on their operations.
If a function doesn't need to return anything then return None explicitly or omit the return statement.
When a return statement is executed, the function should stop running.
