- [Home](https://www.augustusodena.com/)
- [Blog](https://www.augustusodena.com/blog)
- [Research](https://www.augustusodena.com/research)

# Research

This is a list of papers I've worked on organized by topic.
I've tried to give a brief summary for each paper.
Some of the papers have short explanatory videos! I'm working on adding more.
\[NOTE: this page is somewhat out of date\]


## GANs

[**Conditional image synthesis with auxiliary classifier gans**](https://arxiv.org/abs/1610.09585)

**A Odena**, C Olah, J Shlens

_ICML 2017_

This was arguably the first paper in which GANs were made to work on the ImageNet dataset.
We gave a way to use label information to improve image synthesis performance.


[**Self-attention generative adversarial networks**](https://arxiv.org/abs/1805.08318)

H Zhang, I Goodfellow, D Metaxas, **A Odena**

_ICML 2019 (Long Talk)_

[Slides](http://www.augustusodena.com/assets/sagan_icml_slides.pdf)

We propose several tweaks to the GAN training procedure that dramatically improve image synthesis performance.
[BigGAN](https://arxiv.org/abs/1809.11096) is based on this work.
Source code is available [here](https://github.com/brain-research/self-attention-gan).


[**Is Generator Conditioning Causally Related to GAN Performance?**](https://arxiv.org/abs/1802.08768)

**A Odena**, J Buckman, C Olsson, T B Brown, C Olah, C Raffel, I Goodfellow

_ICML 2018_

We show that the conditioning of the input-output jacobian of GAN generators is predictive of many GAN training pathologies.
We then give evidence that the relationship is causal by conducting an intervention that clips the range of the jacobian singular values.


[**Discriminator Rejection Sampling**](https://arxiv.org/abs/1810.06758)

S Azadi, C Olsson, T Darrell, I Goodfellow, **A Odena**

_ICLR 2019_

We show that GAN discriminators can be used after training is finished to perform rejection sampling on GAN generators.


[**Skill Rating for Generative Models**](https://arxiv.org/abs/1808.04888)

C Olsson, S Bhupatiraju, T B Brown, **A Odena**, I Goodfellow

_Preprint_

We show how to use chess-style tournament ranking to evaluate GANs and other generative models.


[**Open Questions about Generative Adversarial Networks**](https://distill.pub/2019/gan-open-problems/)

**A Odena**

_Distill (Commentary)_

I give a set of Open Problems that I think machine learning researchers working on GANs ought to think about.


[**Top-K Training of GANs: Improving Generators by Making Critics Less Critical**](https://arxiv.org/abs/2002.06224)

S Sinha, A Goyal, C Raffel, **A Odena**

_Preprint_

We introduce a simple modification to the GAN training algorithm that materially improves results with no
increase in computational cost: When updating the generator parameters, we simply zero out the gradient
contributions from the elements of the batch that the critic scores as \`least realistic'.


[**Improved consistency regularization for gans**](https://arxiv.org/abs/2002.04724)

Z Zhao, S Singh, H Lee, Z Zhang, **A Odena**, H Zhang

_Preprint_

Several improvements on the Consistency Regularization for GANs paper.


[**Your Local GAN: Designing Two Dimensional Local Attention Mechanisms for Generative Models**](https://arxiv.org/abs/1911.12287)

G Darras, **A Odena**, H Zhang, A Dimakis

_CVPR 2020_

We design special sparse-attention mechanisms for images.
We also show how to invert GANs with attention layers, which is important, because all GANs now have attention layers!


## Semi-Supervised Learning

[**Semi-supervised learning with generative adversarial networks**](https://arxiv.org/abs/1606.01583)

**A Odena**

_Workshop on Data-Efficient Machine Learning (ICML 2016)_

I invented (concurrent with [this paper](https://arxiv.org/abs/1606.03498)) a techique for using GANs
to do semi-supervised learning.


[**Realistic Evaluation of Deep Semi-Supervised Learning Algorithms**](https://arxiv.org/abs/1804.09170)

A Oliver\*, **A Odena\***, C Raffel\*, ED Cubuk, IJ Goodfellow

_NeurIPS 2018 (Spotlight)_

We argue that existing methods for evaluating semi-supervised learning techniques are flawed and propose a new framework
for doing these evaluations.
Source code is available [here](https://github.com/brain-research/realistic-ssl-evaluation).


## Machine Learning and Computer Systems

[**TensorFuzz: Debugging neural networks with coverage-guided fuzzing**](https://arxiv.org/abs/1807.10875)

**A Odena**, C Olsson, D Anderson, I Goodfellow

_ICML 2019 (Long Talk)_

[Slides](http://www.augustusodena.com/assets/tensorfuzz_icml_slides.pdf)

We apply the notions of coverage-guided-fuzzing and property-based-testing to neural networks.
We show that approximate-nearest-neighbors algorithms can give useful coverage metrics in this context.
Source code is available [here](https://github.com/brain-research/tensorfuzz).


[**Learning to Represent Programs with Property Signatures**](https://arxiv.org/abs/2002.09030)

**A Odena**, C Sutton

_ICLR 2020_

[Video](https://www.youtube.com/watch?v=pKJwMVzFRy8)

We introduce the notion of property signatures,
a representation for programs and program specifications meant for consumption by machine learning algorithms.


[**Faster Asynchronous SGD**](https://arxiv.org/abs/1601.04033)

**A Odena**

_Workshop on Optimization Methods for the Next Generation of Machine Learning (ICML) 2016_

I speed up asynchronous SGD by quantifying gradient update staleness in terms of moving averages of gradient statistics.


## Miscellaneous Machine Learning

[**Deconvolution and checkerboard artifacts**](https://distill.pub/2016/deconv-checkerboard/)

**A Odena**, V Dumoulin, C Olah

_Distill_

We show that the ubiquitous "deconvolution" operation used in image-upsampling produces strange checkerboard-artifacts.
We then propose a simple fix.


[**Changing Model Behavior at Test-Time Using Reinforcement Learning**](https://arxiv.org/abs/1702.07780)

**A Odena**, D Lawson, C Olah

_ICLR 2017 (Workshop Track)_

I show how to change the test-time resource-usage of neural networks on a per-input basis using reinforcement learning.


- [email](mailto:augustus.odena@gmail.com)
- [twitter](https://twitter.com/gstsdn?lang=en)
- [google scholar](https://scholar.google.com/citations?user=EHQHNdEAAAAJ&hl=en)