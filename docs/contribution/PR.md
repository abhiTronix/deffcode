<!--
===============================================
DeFFcode library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2021 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
-->

# Submitting Pull Request (PR) Guidelines

These guidelines outline how to submit a high-quality Pull Request (PR) to **DeFFcode**.

## :material-rocket-launch: Before You Start

??? question "First time contributing to DeFFcode?"

    - Learn how open-source contributions work from [this guide ➶](https://opensource.guide/how-to-contribute/)
    - Need help? Join our [Gitter community](https://gitter.im/DeFFcode/community) and we’ll assist you

&thinsp;

## :material-source-branch-plus: Create a Working Branch

Start by cloning your fork and creating a feature branch from the latest `master`:

!!! danger "Keep your fork up to date"

    Ensure your fork’s `master` branch is synced with the upstream repository before starting.

```sh
# Clone your fork (replace with your username)
git clone https://github.com/{YOUR_USERNAME}/DeFFcode.git
cd DeFFcode

# Sync latest changes
git pull

# Create a new branch
git checkout -b feature/your-branch-name
```

Work on this branch and push changes as usual.

&thinsp;

## :octicons-checklist-24: PR Submission Checklist

### 1. Open an Issue First

* Start by creating an issue using the [proposal template](https://github.com/abhiTronix/deffcode/issues/new?labels=issue%3A+proposal&template=proposal.md)
* This helps align your work with project goals and avoids duplicate effort

### 2. Open a Draft PR Early

* Create a **draft PR** from the beginning of your work
* Add:
    * A clear and descriptive title
    * Summary of what the PR fixes/adds/improves
    * Screenshots or outputs (if applicable)
* For bug fixes:
    * Include a **failing test case** that your fix resolves
* Ensure all CI checks pass
* Mark as **Ready for Review** once complete

### 3. Test, Format & Lint Locally

* Run tests and ensure everything passes
* Format and lint your code before committing
* See [Testing & Linting](#testing-formatting-linting) section below

### 4. Write Clear Commit Messages

* Keep messages concise and meaningful
* Link issues using keywords like `#!sh resolves #123`
* Use `git commit --amend` to refine commits when needed

### 5. Perform Integrity Checks

!!! warning "Duplicate PRs will be rejected"

* Check for existing related PRs/issues
* Ensure your changes align with DeFFcode’s design and goals
* By contributing, you agree your code will be licensed under the [Apache 2.0 License ➶](https://github.com/abhiTronix/deffcode/blob/master/LICENSE)

### 6. Link Your Issue

!!! tip

    Learn more about linking PRs to issues [here ➶](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)

* Link your PR to the relevant issue
* This helps track progress and avoid duplication

&thinsp;

## :material-test-tube: Testing, Formatting & Linting

All PRs must pass testing and code quality checks.

### Requirements

!!! info "Python 3.10+ required"

Install dependencies:

```sh
# Install OpenCV (if not already installed)
pip install opencv-python

# Install remaining dependencies
pip install --upgrade ruff pytest vidgear[core]
```

### Test Dataset Setup

Download required test data:

=== "Linux :material-linux:/macOS :material-apple:"

    ```sh
    chmod +x scripts/bash/prepare_dataset.sh
    ./scripts/bash/prepare_dataset.sh
    ```

=== "Windows :material-microsoft-windows:"

    ```sh
    sh scripts/bash/prepare_dataset.sh
    ```

### Run Tests

From the project root:

```sh
pytest -sv
```

&thinsp;

### Formatting & Linting (Ruff)

DeFFcode uses **[Ruff](https://docs.astral.sh/ruff/)** for both linting and formatting.

#### Lint Code

```sh
# Check for issues
ruff check {path}

# Auto-fix issues
ruff check --fix {path}
```

#### Format Code

```sh
# Apply formatting
ruff format {path}

# Check formatting only
ruff format --check {path}
```

!!! tip "These checks run in CI—running them locally saves time during review."


&thinsp;

## :material-chat-question: Frequently Asked Questions

### Q1. Why is my PR taking time to be reviewed?

!!! success "After your PR is merged"

    * You can delete your branch safely
    * Changes are first merged into `dev`, then into `master` during release
    * Active contributors may receive faster reviews over time

PRs are reviewed by maintainers based on priority and availability. You may be asked to make changes before approval.


### Q2. Can I submit a large PR?

* Yes—but ensure changes are **focused and related**
* For major changes:
    - [x] Open an issue first for discussion
    - [x] Large, unrelated changes should be split into smaller PRs

This helps speed up review and increases the chances of acceptance.


Thanks for contributing to **DeFFcode** 🚀

&thinsp;