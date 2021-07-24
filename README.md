# AutMutTestAut
**Automatic Mutations for Test Automation**

## Overview
This Python application is actually a set of tools that automates the source code mutation of a Java application under test, consequently automates the execution of test suites on mutated application and retrieves all the results

_**Note**: This application does not creates code mutation from scratch. It uses the mutation descriptions provided from another Java tool, and interpreting them, it applies them in the source code
Therefore this application is dependent from [Pitest](https://github.com/hcoles/pitest) output, because is the starting point of the entire process of this set of tools_

***Input:*** List of Mutant descriptions from [Pitest](https://github.com/hcoles/pitest) tool

***Output:*** All the information about the results of the test suite runs on mutated application under test

## Features
Core tools (or modules) of this application:
- **Mutation creator from Pitest output information:** It takes the information from Pitest and elaborating them, it creates the actual code mutations ready to be applied. _Since Pitest works at bytecode level, it is neccessary to convert a mutation description in asource code mutation using static mutated strings, string replace or elebarotion with RegEx_
- **Mutator:** It apply the mutation in the source code
- **Mutated Application Manager:** It executes and stops the mutated application under test in asynchronous way, and it can reset the application in a clean state
- **Test Suite Manager:** It synchronously runs the test suite application and saves the results
- **Result Extractor:** It reads the output of the test suite and extracts the information about tests passed or failed and other data
- **CSV Result Writer:** It takes the mutation information with the results of the test suites and write new rows in CSV files that contain all the results, overall and detailed of current mutation outcome

Other features:

- **Mutation Selector:** Given the created information about the mutations, it creates a new JSON file filtering the mutations in a certain way. In our case, it takes in input an integer, which is the maximum number of mutants that will be picked randomically per Java method.
- **Mutation Coverage with prints:** This procedure is very similar to the one that applies the mutant in the source code, but instead of inserting a mutation, it puts a print instruction with the ID of the mutant. With these “mutations”, we can analyze the coverage of the mutations inserted running normally the application under test.

## Goal of the application
The ultimately goal of this application is helping in my thesis project to comparate two different test methodologies. The goal is to analyze the efficacy to kill the mutants and so to find out bugs in web applications.

## Dependencies
- Python 3.8+

For the input data necessary to create the Java mutations, this set of tools depends on [Pitest](https://github.com/hcoles/pitest)

