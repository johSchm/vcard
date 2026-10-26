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

Vision models fail on inputs a person finds trivial. Rotate or rescale an image and even foundation models can fail to classify it correctly. The standard fixes like augmentation are expensive as they require retraining. Symmetry-aware architectures give guarantees but have to be designed for each transformation and trained from scratch. My thesis develops canonicalization as an alternative. A small module (the canonicalizer) in front of the model undoes the transformation of each input and hands over a familiar view. Humans do the same when they step closer or tilt their head to align what they see with their mental representations of that object. The model stays frozen, so robustness becomes an add-on and requires no retraining or fine-tuning of the downstream model. We let the model itself decide what perspective it prefers.

## A rotation canonicalizer that is capable and cheap
papers: Schmidt2023, Schmidt2025b
status: Under review

A canonicalizer is usually trained with a prior that treats every training image as upright. Real datasets break this assumption. My bootstrapping algorithm re-aligns the training samples step by step, with convergence guarantees under mild conditions for arbitrary compact groups. On four fine-grained benchmarks it outperforms equivariant and canonicalization baselines and performs on par with augmentation. A second approach replaces the prior itself. For each training image I precompute the orientations at which the pretrained model errs least. Symmetric objects get several equally good orientations instead of one forced choice. I distill these targets into a small network that is rotation-equivariant by construction, so it needs no augmentation. The large model never enters the training loop, so training costs a fraction of what other learned canonicalizers need, whatever the size of the model. A precomputed polar lookup makes the input transform 44 times faster. The same ResNet-50 recovers from 39% to 63% on rotated images and loses one point on upright ones. On five of six backbones the cost on upright images stays below two points, and on a fine-grained benchmark with a Swin-B it improves both upright and rotated accuracy.

## Robustness at test time with no training
papers: Schmidt2024b, Lindner2026

Inverse Transformation Search shows a frozen model several transformed versions of an input and keeps the one it finds most familiar. To my knowledge it was the first canonicalizer that needs no training. It only needs query access to the model. A follow-up treats the problem as out-of-distribution detection, so any of about twenty detection scores can drive the search. Benchmarking nine search algorithms showed that simple random search with local refinement is enough, and that limiting the search range raises accuracy. Together this lifts accuracy on transformed MNIST from 38% to 90%. A gate corrects only inputs that look unfamiliar, which preserves most of the accuracy on normal ones. All settings can be chosen without labels for the test data.

## Stable spatial transformers and saccadic canonicalization
papers: Schmidt2026a, Schmidt2026b

Learned image canonicalization without inductive biases is brittle and likely to collapse during training. Standard spatial transformers push the object out of the frame for up to half or all of the test images. I split the transformation into bounded primitives such as rotation and scale, and prove that the bounds rule out degenerate warps. In my tests the bounded version keeps every image in frame. The module shares weights with a vision transformer. With translation and scale alone, the same idea yields a multi-view spatial transformer that zooms in like a saccade. When a label-aware oracle picks a single crop, a pretrained ConvNeXtV2-L reaches 98% on ImageNet. The features are there, but the model looks in the wrong place. My saccader learns where to look with a small priority head on the frozen encoder. It is trained with an information-gain signal rather than reinforcement learning. It selects a few high-resolution regions, and their number can be set at inference time to trade accuracy against latency. One attention block fuses the crops with the global view. This improves on the plain backbone across nine fine-grained benchmarks with few exceptions, and memory no longer grows with input resolution.
