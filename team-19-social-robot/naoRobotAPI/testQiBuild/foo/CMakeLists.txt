cmake_minimum_required(VERSION 2.8)
project(foo)

find_package(qibuild)

# Create a executable named foo
# with the source file: main.cpp
qi_create_bin(foo "main.cpp")

# Add a simple test:
qi_create_test(test_foo "test.cpp")
