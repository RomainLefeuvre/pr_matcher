# Student Pull Request Matcher

This Python script fetches GitHub pull requests containing first names and last names from a CSV file and matches them with students, exporting the results to a new CSV file.

Note : This is just a naive script many ways to improve it !
## Table of Contents

- [Student Pull Request Matcher](#student-pull-request-matcher)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation-1)
  - [Usage](#usage)

## Introduction

The `student_to_pr.py` script is designed to match students with GitHub pull requests based on their first names and last names. It automates the process of matching students with their corresponding pull requests
## Installation

Follow these steps to set up and run the `student_to_pr.py` script:

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Navigate to the repository directory:

    ```bash
    cd yourrepository
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the `student_to_pr.py` script, follow these instructions:

```bash
python student_to_pr.py <csv_path> <repo>
