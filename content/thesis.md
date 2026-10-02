<!--
  PhD Thesis section.

  title:     the thesis title (required)
  where:     university, shown under the title (optional)
  heading:   heading above the contribution cards (optional, default "Main contributions")
  figure:    animated figure after the introduction (optional): canonicalization

  The paragraphs before the first ## are the introduction.

  ## Title   starts a contribution card
  papers:    keys from publications.bib (or PDF names), separated by commas (optional).
             Each becomes a tag like "ICML 2024" that jumps to the paper's card.
  status:    shown as a gray tag for work without a paper yet, e.g. "Under review" (optional)
-->
title: Robust and Efficient Discriminative Deep Learning by Canonicalizing and Lifting Symmetry-Degenerated Signals
where: Otto von Guericke University Magdeburg · submission planned for the end of 2026
heading: Main contributions
figure: canonicalization

Vision models fail on inputs a person finds trivial. Rotate or rescale an image and a strong classifier can change its answer. In my experiments a ResNet-50 falls from 66% to 39% accuracy on ImageNet-200 once the test images are rotated. The standard fixes are expensive. Retraining with augmented data cost that model five points on upright images. Symmetry-aware architectures give guarantees but have to be designed for each transformation and trained from scratch. Neither helps a team that already owns a large pretrained model.

My thesis develops canonicalization as a third route. A small module in front of the model undoes the transformation of each input and hands over a familiar view. People do the same when they step closer to see an object of interest more sharply. The model stays frozen, so robustness becomes an add-on and requires no retraining or fine-tuning of the downstream model.

## A rotation canonicalizer that is capable and cheap
papers: Schmidt2025b
status: Under review

A canonicalizer is usually trained with a prior that treats every training image as upright. Real datasets break this alignment assumption. My bootstrapping algorithm re-aligns the training samples step by step, with convergence guarantees under mild conditions for arbitrary compact groups. On four fine-grained benchmarks it outperforms equivariant and canonicalization baselines and performs on par with augmentation. A second approach replaces the prior itself. I precompute the orientations at which a pretrained model errs least and distill them into a small rotation-equivariant network. The large model never enters the training loop. The same ResNet-50 recovers from 39% to 63% on rotated images and loses one point on upright ones.

## Robustness at test time with no training
papers: Schmidt2024b, Lindner2026

Inverse Transformation Search shows a frozen model several transformed versions of an input and keeps the one it finds most familiar. To my knowledge it was the first canonicalizer that needs no training. A follow-up treats the problem as out-of-distribution detection and lifts accuracy on transformed MNIST from 38% to 90%. A gate corrects only inputs that look unfamiliar, which preserves most of the accuracy on normal ones.

## Stable spatial transformers and saccadic canonicalization
papers: Schmidt2026a, Schmidt2026b

Learned image canonicalization without any inductive biases is brittle and likely to collapse during training. I split the transformation into bounded primitives such as rotation and scale, and prove that the bounds rule out degenerate warps. The module shares weights with a vision transformer and was evaluated on biodiversity and medical imaging data. With translation and scale alone, the same idea yields a multi-view spatial transformer that zooms in like a saccade. When a label-aware oracle picks a single crop, a pretrained ConvNeXtV2-L reaches 98% on ImageNet. The features are there but the model looks in the wrong place. I build a saccader that learns to focus using a small priority head, which selects a few high-resolution regions. One attention block fuses the crops with the global view. This improves on the plain backbone across nine fine-grained benchmarks with few exceptions, and memory no longer grows with input resolution.

## Symmetries in production scheduling
papers: Schmidt2021, Schmidt2024a

Symmetries also shape problems outside vision. In job scheduling the open jobs form a set, and parallel machines can be swapped without changing the cost of a schedule. Many optimal schedules are therefore equivalent, which leaves a learning model without a unique target. I encode the jobs with permutation-invariant layers and sort the machines into a canonical order. In a later simulated annealing heuristic, breaking the symmetry between tardy and early jobs lifts degenerate optima and yields schedules in real time.

## Symmetries in traffic signal control
papers: Schmidt2025a

Traffic signal control has the same structure. The lanes, movements and signal phases of an intersection are sets with no natural order. I model them as abstraction levels of a hierarchical graph neural network with permutation-invariant aggregation, so a single policy controls any intersection layout. Where order matters, the symmetry is broken on purpose. A positional encoding relative to the center of the intersection tells the model where along a lane the vehicles are. Trained only on synthetic road networks, the policy transfers zero-shot to real ones.
