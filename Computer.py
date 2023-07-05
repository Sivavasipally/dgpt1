
# import array  from the numpy package




class Computer:
    def __init__(self, cpu, ram):
        self.cpu = cpu
        self.ram = ram
    def setCPUValue(self, cpu):
        self.cpu = cpu
    def setRAMValue(self, ram):
        self.ram = ram
    def getCPUValue(self):
        return self.cpu
    def getRAMValue(self):
        return self.ram
    
    def config(self):
        print("Config is: ", self.cpu, self.ram)


# write a python funtion to calucualte fibonacci series using recursion
# def fib(n):
#     if n <= 1:
#         return n
#     else:
#         return fib(n-1) + fib(n-2)
#
# nterms = int(input("Enter the number of terms: "))

# check if the number of terms is valid
# if nterms <= 0:
#    print("Please enter a positive integer")
# else:
#    print("Fibonacci sequence:")
#    for i in range(nterms):
#        print(fib(i))

# write a python funtion to calucualte fibonacci series using for loop
# def fib(n):
#     a, b = 0, 1
#     for i in range(0, n):
#         a, b = b, a + b
#     return a
#
# nterms = int(input("Enter the number of terms: "))
#
# # check if the number of terms is valid
# if nterms <= 0:
#    print("Please enter a positive integer")
# else:
#    print("Fibonacci sequence:")
#    for i in range(nterms):
#        print(fib(i))

# write a python funtion to calucualte fibonacci series using while loop
# def fib(n):
#     a, b = 0, 1
#     while a < n:
#         print(a, end=' ')
#         a, b = b, a+b
#     print()
#
# nterms = int(input("Enter the number of terms: "))
#
# # check if the number of terms is valid
# if nterms <= 0:
#    print("Please enter a positive integer")
# else:
#    print("Fibonacci sequence:")
#    fib(nterms)


if __name__ == '__main__':
    com1 = Computer('i5', 16)
    com2 = Computer('Ryzen 3', 8)

    com1.config()
    com2.config()
