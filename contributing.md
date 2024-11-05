# Contributing to Seattle Noir

First off, thank you for considering contributing to Seattle Noir! It's people like you that make Seattle Noir such a great game.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include details about your configuration and environment

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python style guide
* Include thoughtfully-worded, well-structured tests
* Document new code based on the Documentation Styleguide
* End all files with a newline

## Development Process

1. Fork the repo
2. Create a new branch from `main`
3. Make your changes
4. Add or update tests as needed
5. Update documentation as needed
6. Push your branch and submit a pull request
7. Wait for review and address any comments

### Style Guide

* Use Python's [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/)
* Include type hints for all functions
* Add docstrings for all classes and functions
* Keep functions focused and single-purpose
* Use meaningful variable names

### Testing

* Write unit tests for all new functionality
* Ensure all tests pass before submitting PR
* Include integration tests where appropriate
* Test edge cases and error conditions

### Documentation

* Update README.md with details of changes to the interface
* Update docstrings
* Add comments for complex algorithms
* Update type hints

## Project Structure

```
seattle-noir/
├── game_manager.py     # Main game loop and state management
├── location_manager.py # Location and movement handling
├── item_manager.py     # Inventory and item interactions
├── puzzle_solver.py    # Puzzle mechanics
├── utils.py           # Utility functions
├── tests/             # Test files
├── docs/              # Documentation
└── README.md          # Project documentation
```

## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing.

Thank you for your interest in improving Seattle Noir!
