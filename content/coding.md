<!--
  Coding section. The text before the first ## is the introduction.

  ## Title     starts a card
  when:        the small line above the title (required)
  icon:        Font Awesome 5 icon classes, e.g. "fab fa-python" (required)
               browse: https://fontawesome.com/v5/search?m=free
  link:        where the icon links to (optional)

  "- Label: detail" lines in a card become rows with the label as a tag,
  e.g. "- Training: PyTorch, PyTorch Lightning".

  cv:          the card's line under Skills in the CV (tools/cv_pdf.py), not shown on
               the website. Without it the CV joins the card's rows. "cv: no" leaves it out.
-->
These are the tools I work with every day, followed by the languages I have picked up since 2014.

## Tasks and Data
when: since 2019
icon: fas fa-project-diagram
cv: Time series, segmentation, classification, regression, ranking, point clouds, 2D/3D object detection, audio events, graphs, image generation, gaze tracking, quantum control, NeRFs

The kinds of data and tasks I have worked on, in my papers and projects and in the theses I supervised.

- Time series: [gasket failure forecasting](thesis:Forecasting Gasket Failures) (thesis)
- Semantic segmentation: 2D images
- Classification: [ICML 2024](paper:Schmidt2024b), [BMVC 2026](paper:Schmidt2026b), [ECML-PKDD 2026](paper:Lindner2026)
- Multi-dim. regression: rotation angles in [ArXiv 2023](paper:Schmidt2023), affine transformations in [ECCV: BISCUIT 2026](paper:Schmidt2026a)
- Ranking and permutations: [IFAC INCOM 2021](paper:Schmidt2021), [HICSS 2024](paper:Schmidt2024a), [SENECA](project:SENECA)
- 3D point clouds: classification in [ECML-PKDD 2026](paper:Lindner2026)
- Object detection: 3D point clouds for [robot safety](thesis:A Neural Network Performance Study) and with [YOLO11](thesis:Ablation Study) (theses), 2D images in [KIVA-NET](project:KIVA-NET)
- Audio: classification and event detection in [KIVA-NET](project:KIVA-NET)
- Graphs: encoding and classification of road networks in [AAAI: MALTA 2025](paper:Schmidt2025a) and [PASCAL](project:PASCAL)
- Image generation: [head and gaze controllable motions](thesis:Head and Gaze), [VAE interpolation](thesis:Improving Interpolation in VAE) (theses)
- Head and gaze tracking: [head and gaze controllable motions](thesis:Head and Gaze) (thesis)
- Quantum gates: [control pulses with reinforcement learning](thesis:Deep Reinforcement Learning for Universal Quantum Gates) (thesis)
- 3D modeling: [NeRFs in robotics](thesis:Employing Neural Radiance Fields) (thesis)

## LLM Tooling
when: current
icon: fas fa-robot
cv: llama.cpp for local models, Claude Code with MCP, agents and skills

I use large language models as development tools, both hosted and on my own hardware. How I work with them is described under [AI at Work](#ai).

- Local models: llama.cpp
- Coding agents: Claude Code with MCP, agents and skills

## Deep Learning Stack
when: since 2020
icon: fas fa-brain
cv: PyTorch (Lightning, Geometric), Hugging Face, timm, OpenCV, Kornia, escnn; MLOps with W&B, MLflow, Optuna, Hydra; scikit-learn; earlier TensorFlow

New projects run on PyTorch. My earlier projects and papers were built with TensorFlow.

- Training: PyTorch, PyTorch Lightning, Hugging Face (Hub, Accelerate), Torch Hub, timm
- Vision: torchvision, OpenCV, Kornia, einops
- Geometry: escnn / e2cnn (equivariant networks), PyTorch Geometric
- Experiments and MLOps: Weights & Biases, MLflow, Optuna, Hydra, TorchMetrics
- Data and analysis: NumPy, pandas, SciPy, scikit-learn, Matplotlib, seaborn
- Earlier work: TensorFlow

## Software Engineering and Backend
when: since 2018
icon: fas fa-code-branch
cv: Git, CI pipelines, clean code, DevOps; FastAPI, Flask; PostgreSQL, MySQL; agile workflow with Scrum, Jira, Confluence, Trello

Every project lives in its own repository. In PASCAL I built the multi-node system with FastAPI. I track experiment results in SQL databases, which also back the open educational resources platform of the AI-Engineering project.

- Version control: Git, GitHub, self-hosted GitLab
- Practices: CI pipelines, clean code, DevOps
- Services: FastAPI, Flask
- Databases: PostgreSQL, MySQL
- Web: Next.js, Tailwind CSS, Shibboleth SAML SSO (AI-Engineering platform)

## Project Organization
when: since 2020
icon: fas fa-tasks
cv: no

I break a problem into subproblems, each with a result that can be checked, and plan them as milestones. This is how I structure the funded projects with industry partners.

- Process: agile workflow, Scrum
- Tools: Jira, Confluence, Trello

## Simulation and Optimization
when: since 2020
icon: fas fa-route
cv: Discrete event simulation (logistics), SUMO (traffic), Google OR-Tools (combinatorial optimization)

Simulators provide the environments to train and test in, and solvers for combinatorial problems.

- Discrete event simulation: logistics
- Traffic simulation: SUMO
- Combinatorial optimization: Google OR-Tools

## Multi-GPU Training
when: since 2020
icon: fas fa-server
cv: Multi-node, multi-zone heterogeneous Ubuntu GPU cluster with distributed training (Hugging Face Accelerate); TensorRT and edge deployment

I train my models directly on a multi-node, multi-zone heterogeneous Ubuntu GPU cluster, in parallel across several GPUs with Hugging Face Accelerate.

- Compute: multi-node heterogeneous Ubuntu GPU cluster, distributed training with Accelerate
- Deployment: TensorRT, edge hardware

## Operating Systems
when: since 2016
icon: fab fa-linux
cv: Linux (Arch, Ubuntu, Mint, Kali), Windows, macOS

Linux has been my own operating system since my Bachelor's degree, and I work in the shell every day. I have also worked with Windows and currently use macOS.

- Linux: Arch (my favorite), Ubuntu, Mint, Kali
- Others: Windows, macOS (current)

## Programming Languages
when: since 2014
icon: fas fa-code
cv: Python (main language); C and Assembler (microcontrollers), C++; Java (Android apps); C# (Unity games); JavaScript, HTML5, CSS, Tailwind CSS, Jekyll (web)

- Python: my main language for research and project work, since my Master's
- C / C++: microcontrollers in C and Assembler, an embedded GUI in C for my Bachelor thesis, a Rubik's Cube solver in C++
- Java: Android apps in Android Studio, on GitHub
- C#: game development with Unity, on GitHub
- Web: JavaScript, HTML5, CSS, Tailwind CSS, Jekyll, Hexo, Node.js, small browser games
- This website: Python build scripts from Markdown, HTML5, Sass / CSS, Bootstrap, jQuery, Canvas animation, LaTeX for the CV
