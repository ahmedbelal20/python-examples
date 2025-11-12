
# - - - - - - -
#             -
# Decorators  -
#             -
# - - - - - - -


# - - - - - - - - - -
#                   -
# Covered content   -
#                   -
# - - - - - - - - - -

# 1- Decorator definition
# 2- Defining decorators
# 3- Using decorators
# 4- Using *args and **kwargs
# 5- Built-in Python decorators (@staticmethod, @classmethod (in-depth), @abstractmethod, @property (in-depth), etc.)


# - - - - - - -
#             -
# Definition  -
#             -
# - - - - - - -

# A decorator is a function that is used to modify or extend the functionality of other functions.
# A decorator is a function that takes in another function as input, adds some functionality, and returns a new function.
# Decorators can sometimes be used with classes instead of functions, but this use case is not covered here.


# - - - - - - -
#             -
# Explanation -
#             -
# - - - - - - -

# The "log" function is a decorator. It takes in any other function as input and wraps it with the "wrapper" function.
# The decorator then returns the definition of the new wrapped function "wrapper", which we can call whenever we want.
def log(func):

    # Notice that here we define the "wrapper" function is defined inside of the decorator.
    # This means that it is not visible and cannot be called directly with its name from outside this decorator.
    # The definition of this "wrapper" function is what the "log" decorator will return.
    
    # Explanation of *args and **kwargs as parameters:
    # We allow wrapper to take *args and **kwargs as parameters. We could name these anything, but the important
    # part is the * and the **.
    # *args -> Refers to any positional argument. We could have called it *anything but *args is the norm.
    # A positional argument is any argument provided to a function without specifying the parameter name.
    # Example: add(1, 2) -> here 1 and 2 are positional arguments (rather than add(num1=1, num2=2), which are keyword arguments).
    # Obviously, the order (position) of positional arguments can affect the functionality of the function.
    # This means that *args allows the function "wrapper" to be called with any number of positional arguments.
    # *args will collect all positional arguments into a tuple (e.g., 1 and 2 cause *args = (1, 2)).
    # **kwargs -> Refers to all keyword arguments. This could have been called **anything, but **kwargs is the norm.
    # A keyword argument is an argument provided by specifying the name of the parameter it goes to.
    # Example: add(num1=1, num2=2) -> here 1 and 2 are keyword arguments.
    # This means that **kwargs allows the function "wrapper" to be called with any number of keyword arguments.
    # **kwargs will collect all keyword arguments into a dictionary. For example, for add(num1=1, num2=2),
    # **kwargs will be = {'num1' : 1, 'num2': 2}

    def wrapper(*args, **kwargs):
        # Here we will implement the definition of the "wrapper" function, which will extend or modify the definition of the
        # original function "func".
        print(f"Calling the wrapped function with arguments {args}, {kwargs}")
        # for the line above, if we call a decorated add(1, 2) -> prints: Calling the wrapped function with arguments (1, 2), {}
        # but if we call add(num1=1, num2=2) -> prints: Calling the wrapped function with arguments (), {'num1': 1, 'num2': 2}

        # Here we call the original function to execute its normal functionality
        # An important thing to note here is that "wrapper" can see "func" here, even though it does not take it as a parameter.
        # This is because Python allows inner functions (functions defined inside other functions) to see and remember variables from the
        # outer function. When log(func) runs and "wrapper" is defined, a reference of "func" is created inside "wrapper", and that reference
        # is kept alive even after log(func) returns "wrapper" and finishes execution (which is before wrapper starts actually executing).
        # Meaning that the reference is kept alive even after the outer function has finished execution.
        # This concept is known as Closures (because the inner function closes over the outer variables (e.g., func))
        # If we would have defined a new local variable inside "log", "wrapper" would still be able to see that variable because of the Closure.
        func(*args, **kwargs)
        print(f"Wrapped function execution complete!")

    # The only thing we do inside the decorator is return the "wrapper" function which will contain all of the desired functionality.
    # We do not use parenthesis here because we want to return the definition of the "wrapper" function, not call it.
    return wrapper 


# This is the function we want to extend with our decorator.
def add(num1: int, num2: int) -> int:
    sum = num1 + num2
    print(f"Sum = {sum}")
    return sum


# - - - - - - - - - - - - - - - -
#                               -
# How NOT to use a decorator    -
#                               -
# - - - - - - - - - - - - - - - -

# log(add(1, 2))
# The line above is a classic mistake. The problem here is that add(1, 2) is executed first, which will yield the result 3.
# Then, "log" is called and it would be as if we wrote log(3). There are actually two problems here:
# 1- log is called with the value 3, not a callable function (which means that the "func" inside "log" is equal to 3).
# 2- wrapper was never actually called, it was just returned. If we wanted to call it, we should have written another pair of parenthesis.
# Example: log(add(1, 2))() -> This will call the wrapper but is still wrong anyway because of the first issue.
# If we run log(add(1, 2)) -> add(1, 2) will be called normally, but nothing else will happen.
# If we ran log(add(1, 2))() we would get -> TypeError: 'int' object is not callable

# The core of the problem above is that we called add(1, 2) and then we passed the return value to "log".
# What we need to do instead is to pass the "add" function itself to our "log" decorator.
# This will allow our "log" decorator to define the "wrapper" function (which can see the original "func"),
# and return it to us so that we can call it at any point.


# - - - - - - - - - - - - - - - - -
#                                 -
# Using the decorator manually    -
#                                 -
# - - - - - - - - - - - - - - - - -

# The correct way to decorate a function manually is as follows
# Here we call our decorator "log" with the function "add". This will cause the decorator to define the "wrapper"
# function (which will have a reference to the original "add" function due to the Closure) and return it to us.
# We can then call this wrapper function through the name we caught it with (in this case, log_add).
# Note that the original decorator "log" is called only once at definition time during the execution of log_add = log(add),
# but it will not be called again when we run log_add(1, 2) or whenever we run log_add() because log_add() will simply call the
# wrapper function which was defined with the reference to the "add" function when we called log_add = log(add) for the first time.
log_add = log(add)
log_add(1, 2)

# A way to do the above in a single line would be
# log(add)(1, 2)
# The first part 'log(add)' will call the decorator and return the definition of the new wrapped function.
# The second part '(1, 2)' will call the returned (newly defined/wrapped) function with the arguments (1, 2).
# This is exactly equivalent to the first two-line example.


# - - - - - - - - - - - - - -
#                           -
# Using decorator syntax    -
#                           -
# - - - - - - - - - - - - - -

# The better way to decorate a function is to use the decorator syntax @decorator_name in the line before the definition of the function to be wrapped.
# Like this:
# @log
# def add(num1: int, num2: int) -> int:

# The code above replaces the original "add" function with its decorated/wrapped function, which is equivalent to
# add = log(add)
# Now if we run add(1, 2), we will call the decorated/wrapper function.


# - - - - - - - - - - - - - - - - - - -
#                                     -
# Expanding on *args and **kwargs:    -
#                                     -
# - - - - - - - - - - - - - - - - - - -

# *args and **kwargs can also be used with normal function that need to receive mandatory arguments.
# For example:

def example1(*args):
    print("Executing Example 1")

def example2(mandatory_param, *args):
    print("Executing Example 2")

# Here, if we simply call example2(), we would get -> TypeError: example2() missing 1 required positional argument: 'mandatory_param'.
# but we can call example 1 normally as below:
example1() # Outputs -> "Executing Example 1".
# This is because *args and **kwargs only catch EXTRA arguments. They do not mandate any arguments to be passed.
# Take the following example:
example2(1, 5, 7, "Hello") # Outputs -> "Executing Example 2"
# The line above runs normally. What happens is that the first positional argument (i.e., 1) gets assigned to the parameter "mandatory_param",
# while all other extra arguments (i.e., 5 , 7 , "Hello") are caught as a tuple inside args.
# In this case args = (5, 7, 'Hello')
# Note that when calling a function, all positional arguments must be passed before passing any keyword arguments.


# - - - - - - - - - - - - - - - -
#                               -
# Built-in Python decorators    -
#                               -
# - - - - - - - - - - - - - - - -

# Python comes with several built in decorators:
# 1- @staticmethod -> Used inside a class to define a method that doesn’t take self or cls. The method
# can be called directly from the class without creating an instance.

# 2- @classmethod -> Used for a method that receives the class itself as the first argument (cls) instead of an instance.
# Useful for factory methods or methods that affect the class rather than an instance.
# Example:

class MyClass:

    count = 0 # A class attribute -> shared by all instances

    @classmethod
    def increment_count(cls):
        cls.count += 1

print(f"Count before incrementing = {MyClass.count}")
MyClass.increment_count()
print(f"Count after incrementing = {MyClass.count}")

# Factory method -> A design pattern where a method returns an instance of the class,
# often with some custom initialization or logic. Factory methods are often marked with @classmethod.
# Example:

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    # This is a factory method
    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = 2025
        age = current_year - birth_year
        return cls(name, age)  # creates and returns an instance
    
p1 = Person("Alice", 25) # normal constructor
p2 = Person.from_birth_year("Bob", 1990) # factory method
print(p2.name, p2.age) # Bob 35


# 3- @abstractmethod -> Require subclasses to implement the method.

# 4- @property -> Turns a method into a read-only attribute (attribute = member variable).
# This can be paired with .setter and .deleter to make a full property.
# Example:

class Circle:

    def __init__(self, radius):
        # Here, the _radius attribute has an underscore to indicate that it is private and should not be
        # accessed outside of the class. It does not enforce privacy, it's just a signal to other developers.
        self._radius = radius


    # Because of the @property, the function below will be called whenever we write obj.radius
    # which is similar to accessing any normal attribute. Note that this will not be called when we
    # try to assign or reassign obj.radius (i.e., obj.radius= anything -> will not call this function).
    # If we had named the original private attribute self.radius instead of self._radius, it would've resulted
    # in infinite recursion when writing obj.radius anywhere.
    @property
    def radius(self) -> float:
        return self._radius

    # The function below will run whenever we try to reassign the 'radius' attribute (the function above).
    # This is done because of the @radius.setter decorator. This allows us to run extra logic before attempting
    # the reassignation of self._radius.
    # Summary: because of @radius.setter decorator, this function will be called when we write:
    # obj.radius = anything.
    # What we do inside this function is completely up to us.
    # Note that if we do not have this setter function, then obj.radius = anything will yield an error.
    @radius.setter
    def radius(self, value: float) -> None: 
        if value > 0:
            self._radius = value
        else:
            raise ValueError("Radius must be positive")
    
    # The function below will be called whenever we write 'del obj.radius'.
    @radius.deleter
    def radius(self) -> None:
        # After deleting self._radius, the attribute will no longer exist. The memory will be freed and it cannot be
        # accessed again. This is also similar to deleting any variable or item from a list.
        del self._radius
    
    # This function will be treated as a read-only attribute without having to create another member variable.
    # This also means we can simply write obj.area, instead of obj.area(). This is one of the benefits
    # of using @property.
    @property
    def area(self) -> float:
        return 3.14 * self.radius ** 2
    
c = Circle(5)
c.radius = 10
print(f"Radius = {c.radius}, area = {c.area}")


# - - - - - -
#           -
# Summary   -
#           -
# - - - - - -

# 1. Decorators

# Functions that wrap another function to modify behavior.
# Syntax:

# def decorator(func):
#     def wrapper(*args, **kwargs):
#         # do something before
#         result = func(*args, **kwargs)
#         # do something after
#         return result
#     return wrapper

# @decorator is syntactic sugar for func = decorator(func).


# 2. *args and **kwargs**

# *args → collects extra positional arguments into a tuple.
# **kwargs → collects extra keyword arguments into a dictionary.
# Names (args, kwargs) are conventional, not required.

# 3. Factory method

# A class method that creates and returns an instance.
# Useful for alternate constructors or returning different subclasses.
# Typically defined with @classmethod.


# 4. @property, setter, deleter

# @property → method behaves like a read-only attribute.
# @<property>.setter → defines logic for assignment of the obj.property.
# @<property>.deleter → defines logic for del obj.property.
# Use _variable internally to avoid recursion.

# 5. Attributes

# Variables or methods that belong to an object or class.
# Instance attributes → unique per object (self.x)
# Class attributes → shared across all instances (Class.x)

# 6. del

# Removes a reference to a variable, list element, or object attribute.
# If a property has a deleter, it runs automatically if del obj.property is called.
