<div id="top"></div>

# <PROJECT_NAME>

<One sentence starting with a verb, describing what this repository produces.>

## Tech Stack

<p style="display: inline">
  <img src="https://img.shields.io/badge/-<NAME>-<HEX>.svg?logo=<SLUG>&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-<NAME>-<HEX>.svg?logo=<SLUG>&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-<NAME>-000000.svg?style=for-the-badge">
</p>

## Table of Contents

1. [About the Project](#about-the-project)
2. [Environment](#environment)
3. [Directory Structure](#directory-structure)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Available Commands](#available-commands)
8. [Troubleshooting](#troubleshooting)

## About the Project

<PROJECT_NAME> <what it does>:

- `<concept>` <what this concept means>.
- `<concept>` <what this concept means>.

<One or two paragraphs describing the capabilities and their boundaries.>

<p align="right">(<a href="#top">back to top</a>)</p>

## Environment

| Language / Framework | Version |
| -------------------- | ------- |
| <Language>           | <X.Y>   |
| <Framework>          | <X.Y.Z> |
| <Library>            | <X.Y.Z> |

See `<dependency-file>` for the full dependency list.

<p align="right">(<a href="#top">back to top</a>)</p>

## Directory Structure

```text
.
├── .github
│   └── workflows
├── <source-dir>
│   ├── <subdir>
│   └── <subdir>
├── tests
├── Dockerfile
├── LICENSE
├── README.md
└── <dependency-file>
```

### Main Directories

| Directory           | Description                                    |
| ------------------- | ---------------------------------------------- |
| `<dir>`             | <Responsibility in one line>                    |
| `<dir>`             | <Responsibility in one line>                    |
| `.github/workflows` | <Which checks run here>                         |

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

Install <runtime> <version>.

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Install Dependencies

```bash
<install command>
```

### Run Tests

```bash
<test command>
```

### Start the <Server / Application>

```bash
<start command>
```

Open:

```text
http://localhost:<port>
```

### Run the Production Container

```bash
docker build -t <image>:local .
```

```bash
docker run --rm -p <port>:<port> <image>:local
```

Confirm that the container is healthy:

```bash
curl http://localhost:<port>/health
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

### <Language / Client>

```<language>
<A minimal example that runs as written.>
```

<p align="right">(<a href="#top">back to top</a>)</p>

## API Endpoints

| Method   | Path      | Description   |
| -------- | --------- | ------------- |
| `GET`    | `/health` | Health check  |
| `POST`   | `/<path>` | <What it does>|

### Request Body

| Field     | Required | Default | Description        |
| --------- | -------- | ------- | ------------------ |
| `<field>` | Yes      | -       | <Meaning, limits>  |
| `<field>` | No       | `<v>`   | <Meaning, limits>  |

<Constraints that a per-field table cannot express: mutual exclusions, size and
count limits, rate limits and queue behaviour, timeouts, and the status code
returned when each limit is exceeded.>

<p align="right">(<a href="#top">back to top</a>)</p>

## Available Commands

| Command     | Description        |
| ----------- | ------------------ |
| `<command>` | <What it does>     |
| `<command>` | <What it does>     |

<p align="right">(<a href="#top">back to top</a>)</p>

## Troubleshooting

### `<the actual error message or symptom>`

<Cause in one or two sentences.>

```bash
<fix command>
```

<p align="right">(<a href="#top">back to top</a>)</p>
