# AutMutTestAut
### Automatic Mutations for Test Automation

### _Branch Note_
_This branch is a workaround to resolve the problem encountered with Rechek implicit and Shopizer application. The error raised is "No last expected state to find old element in!"._

_It basically consists in execute each test singularly (and re-execute them if the error above is raised)_

## Overview
This Python application is actually a set of tools that automates the source code mutation of a Java application under test, consequently automates the execution of test suites on mutated application and retrieves all the results

_**Note**: This application does not create code mutation from scratch. It uses the mutation descriptions provided from another Java tool, and interpreting them, it applies them in the source code. Therefore this application is dependent from [Pitest](https://github.com/hcoles/pitest) output, because it is the starting point of the entire process of this set of tools._

## Features
#### Core tools (or modules) of this application
- **Mutation creator from Pitest output information:** It takes the information from Pitest and elaborating them, it creates the actual code mutations ready to be applied. _Since Pitest works at bytecode level, it is necessary to convert a mutation description in a source code mutation using static mutated strings, string replace or elebarotion with RegEx._
- **Mutator:** It apply the mutation in the source code
- **Mutated Application Manager:** It executes and stops the mutated application under test in asynchronous way, and it can reset the application in a clean state
- **Test Suite Manager:** It synchronously runs the test suite application and saves the results
- **Result Extractor:** It reads the output of the test suite and extracts the information about tests passed or failed and other data
- **CSV Result Writer:** It takes the mutation information with the results of the test suites and write new rows in CSV files that contain all the results, overall and detailed of current mutation outcome

#### Other features
- **Mutation Selector:** Given the created information about the mutations, it creates a new JSON file filtering the mutations in a certain way. In our case, it takes in input an integer, which is the maximum number of mutants that will be picked randomically per Java method.
- **Mutation Coverage with prints:** This procedure is very similar to the one that applies the mutant in the source code, but instead of inserting a mutation, it puts a print instruction with the ID of the mutant. With these “mutations”, we can analyze the coverage of the mutations inserted running normally the application under test.

## Goal of the application
 
The ultimate goal of this application is to help in my thesis project by comparing two different test methodologies in order to analyze the efficacy of mutant killing and find out bugs in web applications.

## Main operation description
#### Input
List of Mutant descriptions from [Pitest](https://github.com/hcoles/pitest) tool

After elaborating the Pitest mutations and creating the actual mutations

#### Core loop (pseudocode)
![Main Operation](https://i.ibb.co/Pm2jzG8/Aut-Mut-Test-Aut-Main-operation.png)

_the various tools or modules involved are highlighted_

#### Output
All the information about the results of the test suite runs on the mutated application under test

## Configuration
In `config.py` you can import the configuration file you want to use. The configuration file is a Python source file with the variables to use in the tools.

## Dependencies
- Python 3.8+

For the input data necessary to create the Java mutations, this set of tools depends on [Pitest](https://github.com/hcoles/pitest)

## Requirements
_**Note**: Only tested on Linux_

#### For Application Under Test
- Open source
- Written in Java
- Executable via Maven

#### For Test suites
- Executable via Maven

## Developing status
This application is in a very developing state. I developed these tools only for the ultimate goal described above.
