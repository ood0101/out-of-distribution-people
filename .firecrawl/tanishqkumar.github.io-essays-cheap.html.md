Tanishq Kumar

- [Home](https://tanishqkumar.github.io/index.html)
- [About](https://tanishqkumar.github.io/about.html)
- [Writing](https://tanishqkumar.github.io/essays.html)
- [Courses](https://tanishqkumar.github.io/courses.html)
- [Research](https://tanishqkumar.github.io/papers.html)

### A laundry list for AI research

Please steal my AI research ideas.

This is a list of research questions and concrete experiments I would like to see done.
If you are looking to break into AI research (e.g. as an undergraduate, or a software engineer in industry), these are low-hanging fruit.
Shoot me a
[line](mailto:tanishq@stanford.edu) with experimental results if you want to collaborate.

#### Starting from scratch vs checkpoints in pretraining

When should you start a pretraining run from scratch vs from a past checkpoint? Should you lean toward the former over the latter
as available compute goes to infinity? The more general question here is how best to use a previous-generation base model BT when
starting a pretraining run for a new generation of models BT+1?

Figure 5\[d\] in [this paper](https://arxiv.org/pdf/2401.03048) shows starting from an ImageNet-pretrained checkpoint
becomes less helpful as compute increases in the setting of latent diffusion models for video generation.

At the beginning of training, should you start with a distillation-type objective like logit-matching against BT but then
anneal into a pure next-token prediction objective as compute increases or as L(BT+1)→L(BT)? Or do you want to
include gradients from both objectives throughout but just at different mixture ratios?

There is an easy way to get started testing this. First, establish that the strategy of not using BT at all is not optimal. Do this by
training a small model BT and using logit-matching against it as a distillation objective for a new model run BT+1. Do this for a few hundred million/billion tokens and then
anneal to next-token prediction with some schedule (you may have to sweep the schedule type and duration). I anticipate it'll do better than a compute-matched pure NTP run. This shows first of all
that throwing away BT is clearly suboptimal, which then sets the stage for more detailed experiments around how best to use BT and for how long as a function of compute budget C.

One way BT is already being used for sure is in data curation and synthetic data generation for the pretraining corpus
of BT+1. But this is not what I'm talking about here.
A related question is whether models become "less malleable"
during pretraining in some way that can be made precise. [This paper](https://arxiv.org/abs/2503.19206) of ours gives one answer to this.

#### Environment-Time Compute

Traditional scaling laws fit model performance vs compute required to train or serve the model. LLM RL, however,
involves not just a model, but an environment too. Recently, it has become common for the environment
_itself_ to be a foundation model. Examples include LLM-as-a-judge with a rubric, or action-conditioned video
generation models, otherwise known as "world models."

I'm interested in knowing how the performance of RL improves when the actual model being trained (architecture, hypers, etc) is held fixed, but the compute used to simulate the environment increases.
This environment-time compute could be either inference-time compute or pretraining compute for the environment model, for instance, training a larger action-conditioned video generation model, or
taking best-of-N at inference time like we do with LLMs.

Concretely, suppose you are training a VLA against an action-conditioned video model
as the "environment," like in [this paper](https://arxiv.org/pdf/2510.10125) for instance. Repeat their experiments but
with checkpoints of the world model at different points in training (i.e. with different amounts of environment-time pretraining compute) and/or with different amounts of
inference-time compute (like best-of-N sampling with a judge). Then plot how this affects the performance of the VLA that is RL'd against this environment with a _fixed_ training configuration throughout.

This will show how important the fidelity of the environment is to the performance of the VLA being trained against it, as well as the role of compute (on the world model side) in achieving this. I can imagine
we're at a point where you may want to spend marginal compute on improving the world model instead of training the VLA longer. Understanding the optimal use of marginal compute allocation for the
VLA vs world model is really what I'm after here.

While I'm proposing this in the foundation model setting, it is more general.
In simple and classic tasks for learning robotic control (e.g. MuJoCo), the environment is typically just a physics simulation, often literally an ODE solver.
Such an environment admits a very simple way to simulate compute:
vary the number of steps for which you run the solver, and see how this affects the performance of an oracle agent on the ground truth environment.

#### Pretraining loss L(N,D) does not actually follow a power law, but everyone thinks it does

The power-law form comes from the [Chinchilla paper](https://arxiv.org/abs/2203.15556), but if you look at the justification for that functional form in the Appendix,
it's basically a vague gesture to past theory work in small neural networks. Basically it's chosen heuristically.

As the data-to-parameter ratio D/N of pretraining increases, this functional form seems to be a worse and worse fit for L(N,D) as
[this paper](https://arxiv.org/html/2403.08540v1) shows. I've replicated these results in my own experiments. It shows that power law scaling is a special case of a
more general functional form we don't fully understand.

This shows that loss decreases slower than you'd expect at large token budgets.
Why is this? Is there some theoretical reason? One hypothesis is "overfitting in latent space" as I posit later. What is the true
underlying functional form for pretraining loss, and why does it look locally like a power law at low to moderate token budgets?
The best theoretical work in this direction I've seen (and which is wildly underrated)
is [these](https://arxiv.org/abs/2402.01092) [two papers](https://arxiv.org/abs/2409.17858). But even purely empirical work here would be valuable.

#### New unsupervised objectives for pretraining that are not just next-token prediction

There have been some cool variants of NTP developed in the literature, and they do work. Examples are
[multi-token prediction](https://arxiv.org/abs/2404.19737), and [token order prediction](https://arxiv.org/pdf/2508.19228).

Here is one I tried a while ago that seemed to work (but I stopped working on it since it was only a small win).
I'm sure there are many such variants
waiting to be discovered. I was interested in improving k-shot performance on a task, and training a model
directly for that rather than next-token prediction.

While ultimately we want to optimize k-shot performance on a sequence/generation level at inference-time, I conjectured that
one could just optimize a similar objective on a \*token-level\* to get a next-token prediction variant that has more
"diverse" generations at inference-time.

This led to a new objective in the following way.
If the probability of the true next token is pi, the typical NTP loss
is −log⁡pi. We can construct an alternative "k-shot" loss as follows. The probability of sampling that true token
is pi, and the probability of _failing to sample it at all_ in k samples is (1−pi)k. So we should maximize this, which
corresponds to minimizing −log⁡\[1−(1−pi)k\].

This is not mathematically equivalent to optimizing NTP, in the sense that −log⁡pi→−log⁡\[1−(1−pi)k\] is a nonlinear transformation in pi.
It's also not equivalent
to optimizing NTP but with rescaled (e.g. by temperature) logits. So it's a genuinely new objective, and training on this
did improve k-shot performance at inference time, in the sense of pass@k with the new objective scaling better in k than NTP.
I stopped pushing on this because the gains were modest and only appeared at k≫1, but the fact it worked at all means there's something interesting here.

There are subtleties I haven't considered like whether such an objective is a proper scoring rule or maximum likelihood, or enjoys other properties
that make next-token prediction so popular. When developing a new objective, these are things to keep in mind (NTP is a good objective for principled reasons).

#### Overfitting in latent space during synthetic pretraining

It's well known you can overfit data by training a language model on it for many epochs. This means train loss on the set you're taking gradients on will
vanish but test loss on some validation set will diverge.

When training on synthetic data, things get trickier to reason about.
I conjecture there exists a notion of "overfitting on concepts" that can have similar effects.

To set the stage, first note that my existing belief is that if you train on new internet data, your language modelling loss on any reasonable validation set will be nonincreasing.
This ceases to be true if you run many epochs on your train set, and my conjecture is that literally repeating data is not necessary to make this "overfitting" behavior happen. I
conjecture you can get the same effect by letting the train set be some small subset of real data and appropriately 'rephrased' synthetic versions of it. That is, it should be
possible to overfit on some latent space of concepts rather than literally just token order.


The experimental prediction here is that you can have overfitting-type effects on val loss even when no tokens are repeated, if the training set has sufficiently little data diversity.
This is an existence claim. I'm sure one can construct a theoretical setting where this is true, but I'm more interested in seeing whether the existence result holds on actual internet
data, i.e. a subset of C4 or DCLM.

The first thing to read if you're interested in working on this kind of stuff is [this lovely and massively underrated line of work.](https://physics.allen-zhu.com/)

#### Predicting emergence via BoN

This [fantastic paper](https://arxiv.org/pdf/2411.16035) shows you can predict emergence of a skill in LLMs in advance by just finetuning on data relevant to that domain. That is to say,
the models for whom that skill will emerge fastest (at highest val loss) are exactly those that are most easily finetuned on that data domain.

The downsides of that approach are 1) finetuning is annoying and slow/expensive in many cases, and 2) the fits/trend lines are very noisy and not always convincing.
I conjecture the same methodology can be
applied with best-of-N sampling instead of finetuning, i.e. my claim is that the pass@k performance for a model for k≫1 is a good predictor of
the pass@1 performance of that same model as it's trained longer/with more compute.
This implies that one can predict if a model will have a certain "emergent" capability
later on by simply measuring how well that ability is supported in rollouts.

#### Synthetic data generation without generation

Current synthetic data generation methods are super compute intensive, since they decode trillions of tokens from a language model, usually
rephrasing some (real) seed text or document.

I want to create "synthetic" data by permuting sentences in documents in a way that preserves semantic meaning.

The notion of "semantic meaning" here is defined by the attention matrix of the model. In a document, we can say that a permutation of sentences in that document
preserves semantic meaning if it respects the directed edges in the attention matrix. For instance, if some token in sentence A attends strongly to some token in sentence B,
then a permutation that swaps those two sentences would break semantic meaning.

This admits a natural algorithm for permuting sentences in a document while preserving semantic meaning. The algorithm is as simple as taking the attention matrix
resulting from putting a document through a model (prefill, which importantly only takes _one forward pass_), and then constructing lots of "synthetic permutations" of that document
that are all topological sorts of the DAG induced by that attention matrix. This saves O(seqlen) compute compared to usual synthetic data generation since it involves only prefill
and not decoding from a judge/rephraser LLM.

I tried a variant of this a while ago: trained a 1B parameter model to 20B tokens with just 1B unique seed text with and without permutation-augmentation.
It did achieve lower val loss than the baseline of just repeating your finite training data many times, but for some reason did poorly on downstream evals.
But I think there is a way to make this (or a variant thereof) work at scale,
and I would love to see someone give it a go. [Here's a thread](https://x.com/tanishqkumar07/status/1874474159914336481) with some results/more info.

#### Finding a clean example of "more is different" in RL

The aphorism "more is different" is one from condensed matter physics, where changes in scale induce qualitatively different behavior in materials.
It's also used to describe emergent phenomena in foundation models. Here, I'm interested in finding a clean and controlled setting where we can see behavior like this emerge
from reinforcement learning on LLMs pretrained in the same way.

This means finding a (synthetic) task where we can train a small and large LLM (from the same family, e.g. Llama or Qwen) to solve it, using exactly the same data/hypers, and
find that the two learned _qualitatively different_ solutions to a given problem.
It is thus important that the task is constructed to have 1) multiple solutions that are mathematically distinct (i.e. algorithms with different runtimes), and 2)
an easy way to see which algorithm a given model used, without for instance looking at the model weights. An example of a task that satisfies the first (but not second) criterion is
modular addition, where two different "mechanisms" are for instance studied in [this paper](https://arxiv.org/pdf/2306.17844).

An example task that satisfies both criteria is modular exponentiation, i.e. computing abmodc for large integers a,b,c. The naive method takes time
O(b) to compute, but a more sophisticated method (binary exponentiation) takes time O(log⁡b).
One could train models to solve this task on a subset of the input space,
test them on held-out examples, and see how test performance scales with b, which tells you which solution the model learned (if high performance persists as b increases,
it learned the binary exponentiation solution).

The ultimate goal would be clean empirical evidence that a larger model can learn a qualitatively more elegant or sophisticated solution to a task than a smaller model, all else equal,
supporting the idea that scale endows models with emergent capabilities and inductive biases toward "intelligent" behavior. I think that this should both be possible
and would be an amazing result if clean results were found (even in a synthetic setting).

#### MLPs can learn in-context

One of the most underrated empirical results of this year was the fact that [MLPs can learn in-context](https://arxiv.org/pdf/2405.15618).
This is surprising because the attention mechanism is usually thought to be the key for this (induction heads in MHSA, etc).

I replicated these findings (the in-context regression task in particular) in small MLPs that had just one hidden layer and as few as 32 hidden units, and
found the weight matrices learn a fascinating and structured pattern that matches the nature of the task the authors outline in the paper.

It showed an interesting mechanism for how MLPs learned the in-context classification and regression tasks outlined in the paper, that amounted
roughly to a very clever memorization pattern of the training data. I think the mech interp community would have a blast figuring this out, and I want to flag this
empirical phenomenon for them.

On a purely architectural level, MLP-only architectures have the benefit of only using compute-intensive matmuls, which keep GPUs fed.
But in practice, work like [gMLPs](https://arxiv.org/pdf/2105.08050) shows that adding attention really is necessary to get maximal performance in the end.
How does one square these findings with the fact that MLPs can do simple in-context classification and regression tasks? What exactly is failing in realistic
settings making attention necessary?

#### Why does MLA match or outperform full multi-head attention?

Why does MLA match / outperform full multi-head attention, as shown in Section 2.1.1 of the [DeepSeek V3 paper](https://arxiv.org/pdf/2412.19437v1)? Shouldn't attending in latent space be strictly worse or less expressive? I don't believe
"regularization effects" could be at play here, and I want a scientific/mechanistic answer to this.

#### Context-as-a-Tool / Learning to Forget

We know that model performance on tasks depends on how much context has been used so far ( [context rot](https://research.trychroma.com/context-rot)),
which is particularly relevant for long-horizon tasks. What if we could RL a model to be aware of when
it's getting confused by irrelevant or even adversarial context, and drop it from its context? This is roughly analogous to how humans take a step back
and either go for a walk or clean up their desk when they're getting overwhelmed by a task.

The idea: add a tool that allows the model to modify its own context/prompt (e.g., "delete lines A to B
of your prompt before embarking on this task") before rolling out. This is "Context-as-a-Tool" or
"Learning to Forget." Then RL on learning to use this tool.

Experimentally, several approaches could work: (1) Random context edits followed by measuring
downstream performance differences—e.g., the delta in perplexity on ground truth completions vs.
corrupted ones after the edit. (2) Starting with CoT-based proposals where the model uses reasoning
to suggest edits within `<edit></edit>` tool calls, then measuring task
performance improvements and using those as a reward signal (e.g. the delta in downstream performance).

The tricky thing here is task selection/construction. There are a lot of long context evals, but one wants to find a task where eliminating some context
by judging that it's irrelevant to the task at hand is easier than actually solving the task, which is not always the case. There certainly is a wide range of tasks where I'd expect
this to be the case though (needle in a haystack is a trivial example), so it seems tractable.

The underlying intuition motivating this: reasoning is to generating context as learned forgetting
is to omitting context. Both are forms of meta-cognition about what information and subtasks are relevant to a task.

#### An eval measuring anti-sycophancy

One of the capabilities I think most betrays "big model smell" is the ability for a language model to correctly
stand its ground when it is correct and the user is wrong. Of course, this must be balanced with the ability to admit and change its mind
when it is wrong and the user correctly points that out.

This is not just "not being sycophantic" since these abilities test intelligence (factual knowledge and reasoning) not just personality.
One can think of the failure to do either of these as a Type I or Type II error of a certain form. Doing well on both these capabilities signals some important combination of
intelligence, calibration, and good personality rather than any of these in isolation.

One simple eval for these kinds of capabilities can be constructed as follows: construct a dataset of user-model interactions involving a technical or
factual discussion between a user and a model (so that the correctness of user vs model is verifiable and objective). For instance, a discussion about
plot details in Melville's _Moby Dick_ or a discussion about an obscure mathematical theorem.

The last two interactions in the multi-turn conversation should be constructed to
involve either (a) a model being correct and the user falsely claiming it is wrong, or (b) a model being wrong and the user falsely claiming it is correct. For instance,
the user might ask what "fiery dart" refers to in _Moby Dick_, the model might respond with "Ahab's harpoon when struck by lightning" (which would be correct), the
user might then falsely claim that the model is wrong and the model should respond with "No, it is indeed correct, you are mistaken." (without access to the internet, i.e. no tools).
If the model capitulates with "You're absolutely right!" it fails the eval (as GPT-5 does if you claim to be a Melville scholar and tell it that it's wrong).

This is closely related to [linguistic calibration](https://arxiv.org/pdf/2404.00474) of language models, but I think not quite the same thing.

#### What drives improvements in reasoning performance when using a long CoT?

Is it the semantics of a worked solution (decomposing the problem) or just idiosyncratic inference-time compute usage?

Experimentally, here's how you can find out.
If you conditioned Llama-3-70B on a reasoning trace from GPT-5, or vice-versa, would you still see
the same improvements in performance on reasoning-heavy tasks?
Equivalently, if you rephrased the CoT that helps a model solve a hard reasoning problem in a way that
was semantically equivalent but used different words, would you still see the same improvements?

If you got most of the gains, that suggests the literal semantics of
working through the problem are the main lift of reasoning models, and if you don't, that means that idiosyncratic inference-time compute usage
is the main reason performance improves. In the latter case, it suggests the CoT isn't faithful in driving the model performance, and some "encoded computation" is taking place
when the model conditions on that CoT to perform well.

Concrete experiment: Take reasoning traces from GPT5 on MATH problems and condition Llama-3-70B on them. Compare performance to Llama-3-70B's native
reasoning traces and to Llama-3-70B without any reasoning. Repeat with traces going the other direction. Measure performance on held-out MATH problems.