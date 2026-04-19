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

# Submitting an Issue Guidelines

If you've discovered a bug or have an idea that could improve **DeFFcode**, we’d love to hear from you. Before opening an issue, please review the guidelines below—they help us triage faster and resolve issues more efficiently.

## :material-rocket-launch: Before You Start

??? question "First issue on GitHub?"

    You can learn how to create one from GitHub’s official guide on [creating an issue](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue).

!!! info

    Issues can usually be resolved much faster when they include clear reproduction steps, environment details, and a small demo.
    
    If you're short on time, feel free to submit a brief report—but please note that incomplete reports may take longer to investigate.

&thinsp;

## :material-tab-search: Search the Documentation and Existing Issues

Before opening a new issue, please check the following first:

- [x] Search for an existing [open or closed issue](https://github.com/abhiTronix/deffcode/issues?q=is%3Aissue) that matches your problem.
- [x] Review the [FAQ & Troubleshooting section](../../help/get_help/#frequently-asked-questions).
- [x] For quick questions, use our [Gitter community](https://gitter.im/deffcode-python/community) instead of opening an issue.

You may find that your question has already been answered or that a workaround already exists.

&thinsp;

## :material-folder-edit: Gather Required Information

Please include the following information with your report whenever possible:

- [x] Enable the `verbose=True` flag in the relevant API to collect debug logs.
- [x] Provide a **minimal reproducible example** that demonstrates the issue.
- [x] Include the installed DeFFcode version using command: `#!sh python -c "import deffcode; print(deffcode.__version__)"` and also:
    * Python version
    * Operating system
    * FFmpeg version (`ffmpeg -version`)

&thinsp;

## :octicons-repo-template-24: Follow the Issue Template

- [x] Select the correct issue template before submitting.
- [x] Complete all relevant sections in the template.
- [x] Reports with insufficient information may be marked **Invalid ⛔**
- [x] If no follow-up details are provided, the issue may be closed.

&thinsp;

## :fontawesome-solid-fist-raised: Raise the Issue

Before submitting:

- [x] Write a short but descriptive title
- [x] Keep the report focused on one issue
- [x] Attach relevant logs, screenshots, or source code when available

Choose the appropriate template below:

* [**Bug Report 🐞**](https://github.com/abhiTronix/deffcode/issues/new?assignees=abhiTronix&labels=Bug+%3Alady_beetle%3A%2CNeeds+Triage+%3Amonocle_face%3A&template=bug_report.yaml&title=%5BBug%5D%3A+)
* [**Feature Idea 💡**](https://github.com/abhiTronix/deffcode/issues/new?assignees=&labels=Idea+%3Abulb%3A&template=idea.yaml&title=%5BIdea%5D%3A+)
* [**Question ❔**](https://github.com/abhiTronix/deffcode/issues/new?assignees=&labels=Question+%3Agrey_question%3A&template=question.yaml&title=%5BQuestion%5D%3A+)
  
&thinsp;