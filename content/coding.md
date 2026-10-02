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

## Foundation Models
when: current
icon: fas fa-layer-group
cv: Swin, SAM, EVA, ViT, ConvNeXtV2 (vision); CLIP (vision and text); EnCodec (audio); CLAP (audio and text)

I build on pretrained foundation models, either adapting them to new tasks or keeping them frozen and adding small modules in front of them.

- Vision: Swin, SAM, EVA, ConvNeXtV2
- Vision and text: CLIP
- Audio: EnCodec
- Audio and text: CLAP

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
cv: PyTorch (Lightning, Geometric), Hugging Face, timm, OpenCV, Kornia, escnn; Weights & Biases, MLflow, Optuna, Hydra; NumPy, pandas, scikit-learn; TensorFlow in earlier projects

New projects run on PyTorch. My earlier projects and papers were built with TensorFlow.

- Training: PyTorch, PyTorch Lightning, Hugging Face (Hub, Accelerate), Torch Hub, timm
- Vision: torchvision, OpenCV, Kornia, einops
- Geometry: escnn / e2cnn (equivariant networks), PyTorch Geometric
- Experiments: Weights & Biases, MLflow, Optuna, Hydra, TorchMetrics
- Data and analysis: NumPy, pandas, SciPy, scikit-learn, Matplotlib, seaborn
- Earlier work: TensorFlow

## Software Engineering and Backend
when: since 2018
icon: fas fa-code-branch
cv: Git; FastAPI, Flask; PostgreSQL, MySQL

Every project lives in its own repository. In PASCAL I built the multi-node system with FastAPI. I track experiment results in SQL databases, which also back the open educational resources platform of the AI-Engineering project.

- Version control: Git, GitHub, self-hosted GitLab
- Services: FastAPI, Flask
- Databases: PostgreSQL, MySQL
- Web: Next.js, Tailwind CSS, Shibboleth SAML SSO (AI-Engineering platform)

## Multi-GPU Training on Linux
when: since 2016
icon: fab fa-linux
cv: Multi-GPU cluster with distributed training (Hugging Face Accelerate); TensorRT and edge hardware for deployment

I train my models on a multi-GPU cluster, in parallel across several GPUs with Hugging Face Accelerate. I have worked on Linux and in the shell since my Bachelor's degree.

- Compute: multi-GPU cluster, distributed training with Accelerate
- Deployment: TensorRT, edge hardware

## Programming Languages
when: since 2014
icon: fas fa-code
cv: Python (main language), C / C++, Java, C#, JavaScript

- Python: my main language for research and project work, since my Master's
- C / C++: Bachelor's courses (with Assembler), an embedded GUI in C for my Bachelor thesis, a Rubik's Cube solver in C++
- Java / C#: Android apps and a Unity game, on GitHub
- Web: JavaScript, HTML and CSS for small browser games, Jekyll, Hexo, Node.js
