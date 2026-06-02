![Thumbnail (640x480)](https://i.ytimg.com/vi/s2e5HibC9Tk/sddefault.jpg)
# [Rising Stars #4: Karan Singhal (Google) - LLMs for Transformative Healthcare at Scale (Med-PaLM)](https://www.youtube.com/watch?v=s2e5HibC9Tk)

**Visibility**: Public
**Uploaded by**: [Alaa Lab](https://www.youtube.com/@Alaa-Lab)
**Uploaded at**: 2023-08-28
**Published at**: 
**Length**: 1:04:24
**Views**: 560
**Likes**: 10
**Category**: People & Blogs

## Description

```
Abstract: 

Increasingly capable AI is likely to be widely transformative within the next decade. Healthcare may be the area where this impact is most profound, as foundation models have the potential to increase quality and access to care and accelerate biomedical scientific discovery. Existing models have limitations that prevent their uptake in real-world workflows; limited reliability, interactivity, and alignment with human values are all crucial problems in this high-stakes setting. 

I will discuss three recent works from my team that aim to measure and mitigate these limitations: Med-PaLM, Med-PaLM 2, and Med-PaLM M. Med-PaLM (published in Nature) was the first AI system to surpass the passing grade on US Medical License Exam (USMLE) style questions. Med-PaLM generates accurate, helpful long-form answers to consumer health questions, as judged by panels of physicians and users. Med-PaLM 2 further improves performance and reliability, achieving an expert-level score on exam questions. Its answers are preferred over physician answers across several clinically-relevant axes. Med-PaLM M is a multimodal foundation model that can perform a wide variety of biomedical tasks at or near state-of-the-art performance. 

I will discuss the implications of these advances and outline a path towards improved health for billions, including open challenges along the way.



Bio: 

Karan Singhal is a Staff Research Engineer at Google Research leading teams working on biomedical AI, foundation models, and representation learning. Karan's recent work includes Med-PaLM, a series of medical large language models featured in The Scientific American, Wall Street Journal, The Economist, and others. Karan is particularly motivated by advancing AI safety in the medical setting to create more reliable, steerable systems that could improve the health of billions. Prior to Med-PaLM, Karan researched robust and private representation learning, deploying novel algorithms to hundreds of millions of users. Karan's work has been published in Nature, NeurIPS, ICLR, and other venues. He received his M.S. and B.S. in Computer Science from Stanford University, where he initiated and was the main instructor for the "AI for Social Good" course.
```

## Transcript

foreign
[Music]
I'm very excited to be talking to you
guys about medpom and you know the
potential for large language models and
their multimodal counterparts to help
transform Healthcare
um let's get started
um so I'll kind of give a little bit of
an overview of the space talk a little
bit about tasks and evaluation about
some of the models
experiments and then I'll leave some
time for open discussion and then we'll
talk about kind of inclusions
let's get started with motivation here
um so our when we first started this
project within Google it started out as
a kind of bottom-up brain moonshot uh
four of us kind of working on it
together proposing it to leadership and
seeing whether we could kind of get
started on the idea of
um exploring the idea of large language
of models catalyzing kind of a wider
impact in medical AI
um and so when we started we really
started thinking about you know two
broad topics that we were interested in
one was kind of the potential for
improved care delivery and so for many
years there's been kind of a um hype and
excitement around the potential for AI
and Healthcare and a lot of that has
been centered around potential for care
delivery and so you know in the past
that's often look like algorithms for
improved diagnosis of certain conditions
um for example narrow AI models have
taken an image and then performed some
classification
um and in the last several years with
the Advent of deep learning we've
started to get to the point where these
models have gotten performance enough
and reliable enough that they can be
deployed sometimes in real world
settings and so there's been some
exciting developments here
at the same time there's also
the area of scientific discovery which
maybe in the longer term could be a
place where AI could have even more
impact
um so I'm personally the belief that if
AI goes really really well I think
recently generally it goes really well
that one of the places where it'll have
the most impact is through advancing
science and so we've kind of seen this
nascent field recently of kind of
scientific discovery through AI where
people are doing things like drug
Discovery or
um kind of protein LMS or genomic LMS
and also kind of Novel biomarker
Discovery a lot of this is very recent
you know sometimes in the last year or
two I think there's a lot of exciting
work to be done here and I think what
I'll kind of describe a little bit over
the course of the talk is that I think
work on trending large-scale Foundation
models that are able to adapt to the
setting might also be
um you know one potential way these
models could be impactful in the real
world
by the way feel free to jump in anytime
for any any questions as well
awesome so I'll talk a little bit more
about medicine and languages which is
really where we where we started
um we saw the current state of the
medical AI field and and notice that a
lot of existing models were kind of
narrow medical AI systems that could you
know take in an image or some text and
then produce some classification
um do we notice that language you know
enables key interactions between
clinicians researchers and patients in
the real world
and you know there's an incentive to
kind of develop systems especially in
the short and medium term but
complementary and Cooperative with um
with the Physicians of today and so
human and AI collaboration in the last
few years has been emerging as like a
key driver for a lot of the innovation
in the space versus kind of models and
and of of kind of integration that
involve kind of replacing keyword flows
which seem to not work as well
um and so if we look on you know at this
figure you know on the left we have
today's medical AI which often looks
like narrow classification tasks
basically given some context
produce some classification in the
middle we have this complementary
Cooperative model where for example a
model might produce a classification but
then might defer to a radiologist for
example if it's making a prediction
um so it's been exciting published on
this in the last year and then you know
at the end you know one One Vision that
we were motivated by it with the medpom
work was the vision of kind of a fully
interactive system where it could be a
physician's assistant basically uh
taking all the contacts that is is
needed from a patient and be able to
kind of point out any any kind of issues
or any anything of concern and to be
able to provide clinical decision
support as well and so we're very
excited about that kind of potential
that saw that you know the existing
models couldn't couldn't do that as well
um at the same time we also saw like a
lot of exciting work going on in large
language models for Science and
biomedicine so all these Works were
before our original medpound work
um and so there are a lot of exciting
findings that we were seeing
um at the same time we did see kind of
opportunities for us to contribute
um and so at the time there were a few
things we were excited to buy um the
first was the potential to explore
safety and sterability of AI systems in
the setting
um so in general large language models
produce hallucinations on helpful
answers they're often fairly unreliable
which really matters in high-stakes
settings like this they can often kind
of replicate or amplify biases or other
kind of correlations that are present in
their in their training data and so
there's kind of an open challenge in
large language models in general around
controlling this behavior and you know
in this setting it's even more important
to kind of make sure that these models
are are kind of behaving as as you'd
expect and you know align with the
values of society of Physicians of
patients so that was kind of one
motivating challenges behind uh us kind
of looking at medpom the Second
Challenge was that there was no standard
set of benchmarks for testing the
clinical knowledge of large language
models and so at the time when we were
starting to work on medpom there was
kind of a a sense that it wasn't obvious
how much medical knowledge that these
models were kind of encoding
um and then the last thing was kind of
human evaluation so especially in like
the safety clinical setting like this we
need to think carefully about human
evaluation and a lot of previous Works
had kind of relied on automated
evaluation via either automated
benchmarks or natural language
generation metrics and so we saw a real
opportunity to kind of do careful human
evaluation to get a better get a better
sense of whether or not there was
progress being made and kind of to
capture you know potential harms and
then actually work on those potential
Harms
um so I'll be talking a little bit about
three papers giving a very brief
overview of medpom medpom2 and netpumem
and this is work done with a very large
team of folks um who are shown in in
this slide
um and so you know this work would not
have been possible without all these
folks here as well
um so on the tasks and data sets I'll
talk a little bit more about where we
started which was thinking about text
only tasks including especially medical
question answering
um this was potentially multiple tasks
that we could have started with
summarization or clinical decision
support or triage uh we ended up
um tackling some of the later in these
tasks later but for at the beginning for
the first mad Palm paper we really
focused on medical question answering
because we viewed it as kind of a fairly
General task basically given a question
could be a kind of a wide variety of
things
um whether it's multiple choice or long
form answers and the kind of topic and
whether it's asking for a diagnosis or
not
whether it's asking a general question
that's informational
um so there's a kind of a wide variety
of things that we want to be able to do
under medical question answering and
answering medical questions reliably
relies on comprehension skills that so
whether the model is able to actually
comprehend the question recall of
medical knowledge and also manipulation
of expert knowledge
any any questions so far
cool
um and so one of the main contributions
of the initial web bomb work was kind of
curating this multimed QA medical
question answering benchmark
which involved six existing benchmarks
uh that were both multiple choice and
long form answers and also the
additional Health search QA Benchmark
which was commonly searched questions
about health on the web
um and in general this kind of Benchmark
was motivated by a few things one was we
were interested in kind of going Beyond
kind of automated benchmarks like
multiple choice accuracy or NLP
generation metrics to go towards human
evaluation
um second we were also interested in
kind of probing different aspects of
medical question answering and so this
involves kind of open domain versus
closed domain questions or medical exams
versus medical research and consumer
questions
um and also questions about biomedical
research or about like um consumer
consumer queries about their health and
things like that so there's a lot of
kind of uh Variety in in these data sets
but there's also limitations which I'll
discuss a little bit later as well
um just to give a few examples of the
kind of data sets that we were looking
at
um so on the left is Health search QA so
these are kind of commonly searched
questions on the web
um in the middle we have live qas these
are questions that have been submitted
to a service and then there's some
reference answers which we didn't use
for this work but just providing an
example here and on the right we have
Med QA which is kind of USMLE or U.S
medical licensing exam style questions
which often look like a clinical
vignette given a patient given some of
their context
um answering some question about uh that
context
um and just providing a little bit more
of a summary of the different tasks we
had here and the format of the questions
and also the domain of the different
questions here
um you know one one other kind of
um evaluation
um kind of detail that we we had was we
did the human evaluation of the long
form answers provided by these models
and so that involved us kind of coming
up with a human evaluation framework for
Physicians to do and for Lay users to do
um and so for for clinicians our initial
framework basically looked like this I
asked a bunch of questions to Physicians
given a question given a potential
answer whether it's from a physician or
from a model
um we had these physician Raiders
complete these questions
um so things like whether or not the
answer relates to Scientific consensus
whether there's a high likelihood of
harm or extent or severity of harm
whether there is comprehension retrieval
reasoning uh being displayed whether
there's any inappropriate or incorrect
content or missing content whether
there's any possibility of kind of
implicit or explicit uh Health Equity
bias
um and on the lay user side we asked a
couple more questions about user intent
and the helpfulness of the answer to
basically get a sense of whether lay
users or consumers would find the
answers to these questions useful or not
um and then in terms of data sets we
used so we took the um kind of uh the
data sets for multimed QA that involved
long-form answers for the medpom2 paper
we also added additional adversarial
questions both uh General and in the
Health Equity context we did triple
ratings of question answer tuples for
each data set by clinicians to kind of
get a sense of whether or not we could
achieve good integrator reliability and
lastly the final ratings were performed
by 15 clinicians based in the UK the us
or India and we tried to select for a
variety of kind of Specialties and
demographics in these uh in these
ratings
any questions so far
yes I have a question or I I actually
have a couple questions so first uh the
providers or the
evaluators are they volunteers or how
how were they identified
um because I think that might bring a
little bit of
bias to the evaluation rate
it's a great point and I'll bring it up
later in the near the end of the talk as
well around that's good but I can
quickly quickly summarize here as well
um we basically worked with
um uh uh paid clinicians who were
basically paid for their services and
also uh paid lay users
um and so they were basically
um recruited by a vendor firm that we
worked with
um who basically uh handle
um you know rating tests for us and so
then we worked with them to identify
possible candidates and then to kind of
make sure that we were getting good
coverage of different uh locations and
Specialties and things like that
but there's obviously more work to be
done here and I'll mention that more at
the end
sounds good yeah and and the other
um I don't know if it's a question or
just a comment uh that there's a lot of
criticism I'm gonna call it uh for
especially for large language models in
the impressive performance that it has
on on things on tasks like um answering
the you recently type of questions
because uh most of the time you know or
actually all of the time you know that
for multiple option questions the the
correct answer is there right so it's
um
I don't want to say cheating but but you
know like uh it's not completely
predictive or generative because the
answer is there it's not completely
serious shot I don't know how to call it
um yeah so and I'm saying this because I
we're working right now in a project
that uses uh llms and that's kind of the
criticism that we're getting is like how
do you know that this is reliable and in
in the U.S Emily's setup you know that
it is because again you you have the
information there and you know one of
the answers is the correct one but what
do you do when you have a more
uh or a less constrict uh constructive
environment
yeah absolutely um so definitely the
kind of
um the fact that a lot of existing work
had been evaluating on solely on
multiple choice benchmarks was one of
the motivators for our work as well and
so the protocol that we we have briefly
discussed here is kind of a way of
evaluating um the model's long-form
answers to questions Beyond these
multiple choice questions so the data
sets to be evaluated on um shown on the
slide um live QA medication QA Health
search QA and then these adversarial
questions are all questions in which the
answer choice there's no answer choices
um and so the model is doing like an
open-ended generation uh to be able to
produce an answer without you know the
answer being shown to it so that's you
know one way of moving towards that but
there's also I I think there's still a
little you know additional limitations
of this approach where this is still not
you know fully in a real world workflow
and I'll talk a little bit more about
that limitation towards the end as well
sounds good thank you
yeah
awesome I'll also talk a little bit
about the multimodal tasks um that we
did for the medpom M paper
um so we basically for this paper we
added 11 additional tasks across
different task types so things like
visual question answering image
classification report generation genomic
variant calling um so kind of a wide
span of kind of sources from Dermatology
to chest x-ray
um to a genomics different modalities so
text
different kinds of radiology
radiological images genomics data and
also kind of different output formats
whether that's a classification or like
a more open-ended generation we kind of
cover different things in this in this
work as well
um this slide also gives a brief summary
of the different tasks and also the
specific data sets used there are 12
unique data sets here and then 14
different tasks used three were used
also in the um multi-med QA uh Benchmark
as well
and lastly the
um the multimodal evaluation we also did
a physician evaluation there as well um
so again not just fully relying on
automated metrics
um and so what we did here is basically
have a reference report from the data
set in this case the mimic cxr data set
um different versions of matpom which
I'll talk more about what m is later and
then we had phys uh Radiologists
basically rank you know different
responses both pairwise
um across all the four different
possible answers
um and that'll present some results on
that a little bit later
cool I'll do like a brief overview of
modeling but this won't be the focus of
my talk here
um and so a little bit of context here
mid pump obviously Builds on Palm which
is the pathways language model which was
came out last year uh this is the
largest
um at the time the largest densely
activated decoder only model
um 540 billion parameters trying using
this large-scale ml system
we also have the flan Palm models that
we built on
um for this work as well uh plan refers
to kind of the instruction tuning on top
of palm
um and so this is basically you know
taking uh palm and then fine-tuning it
on a certain format of data which looks
like here's an instruction here is a
task and here's the answer to the task
um and so it turns out this is like a
pretty strong Baseline for
um basically getting models to follow
instructions well
um and so we built on that this work
both in terms of uh building from uh the
flan Point Palm checkpoints and also in
terms of applying instruction tuning in
different ways
um especially for the first matpom paper
we were motivated by exploring data
efficient strategies for better aligning
the model with the requirements of the
setting and so on the left we had
prompting strategies which is basically
taking flan Palm without doing any kind
of updates at all just prompting it in
different ways whether that's Hue shot
prompting or Channel thought prompting
or self-consistency prompting I'll
briefly discuss these things as well and
on the right we explore prompt tuning
um so basically kind of uh simple like
competitionally inexpensive tuning of
certain parameters associated with The
Prompt of a model and you can basically
view this as like a learnable way of
prompting the model because your
basically modifying the same parameters
any questions so far
awesome
uh so just to briefly touch on a few
shot prompting which is probably
familiar to folks in this call uh this
is when you basically put in the prompt
examples of the input output behavior
that you want then you ask it again you
know here's another input and then it
tends to be better at producing the
desired output given that this was um
first kind of
um explored pretty thoroughly in the
gpd3 paper
we also have Channel thought prompting
which is basically
getting models to produce kind of
explanations or chains of reasoning
before they produce their final answer
and so that their final answer is then
kind of conditioned on that chain of
reasoning
and so the benefit here is that you are
now able to get the model to kind of do
smaller tasks or subtasks of of
answering a question before it does the
final task and empirically across many
tasks this tends to perform Improvement
tends to um perform well especially
across like reasoning and math types of
problems which at least prior to this
work large language models were pretty
bad at
another quick thing I'll give an
overview of is self-consistency
prompting so you can view this as kind
of building on Chain of Thought
prompting so the first thing you do is
you prompt a model using Channel thought
examples and now the model is basically
going to produce an explanation and an
answer
um the limitation of this especially if
you sample just once is that like you're
basically getting one possible reasoning
path from a model
um instead of kind of aggregating over
possible reasoning paths and so
self-consistency prompting is kind of a
a strong a simple kind of approach which
basically involves
um sampling repeatedly from a model's
decoder to generate a bunch of reasoning
paths and possible answers and then she
was visiting uh or aggregating across
multiple answers using a using about
um so it's basically a kind of a simple
way of doing something like tree of
thought which is kind of a more recent
version of this
another thing I want to give a bit of an
overview of is prompt tuning which is in
this case we are not referring to prompt
engineering we're referring to like
parameter efficient updates of certain
model parameters
um additional model parameters that you
basically prepend to the tokens uh that
you put into the model
and so you're basically learning these
soft prompt vectors while keeping the
rest of the model Frozen and by doing
this you can effectively update a large
language model without training a large
percentage of the parameters techniques
like Laura if you guys are familiar are
also kind of similar in that they're
also a parameter efficient tuning
techniques
foreign
briefly before about instruction tuning
but just to mention it again uh broadly
outside of the context of plant palm
again it's basically given multiple
tasks framed as instruction task and
output can you find two in a mile to be
able to do that so in the future when it
sees an unseen instruction which looks
similar ish to its previous instructions
that it's seen as able to make
predictions well there
um and so just to give a bit of an
overview of what we did to produce
metpom we basically took a set of
questions that we worked with Physicians
to kind of get labels for and reproduce
an instruction fine-tuning data set from
that and so this is a bunch of long-form
consumer questions and and basically we
asked we work with the panel clinicians
to produce a small set of example
answers that the model could fine tune
on and so the training examples
basically look like what you see on the
slide here
um and then from there we applied this
technique we called instruction prompt
tuning which is just a simple
combination of instruction tuning and
prompt tuning where you are applying the
instruction tuning objective on the uh
the kind of the normal uh next word
production objective on the context of
instruction tuning data but only on the
prompt parameters only on the soft
parameters and so this is basically a
way of taking a model like flat Palm
and better aligning it with the medical
domain with relatively small amount of
compute and with a relatively simple
approach and so in this context
um you know fland Palm itself was 540
billion parameters
but the prompt parameters that we you
know initialize and then trained were
just 1.8 million parameters and so this
is relatively
um relatively low cost in terms of its
uh in terms of our ability to train this
um any questions so far
I had a um I had a question about uh
like safeguards you guys have in place
about sort of preventing hallucinations
so does this sort of like ensembled
voting mechanism generally help with
reducing these kinds of problems or like
are there other metrics that you guys
use to sort of prevent that or detect
that even
yeah absolutely um so by Ensemble voting
you might be referring to supplicity or
Ensemble refinement which I'll discuss
um very soon but in either case broadly
yes um the the models tend to get better
performance in terms of their accuracy
um when we do that type of thing it's
also a bit expensive to apply in
practice and so when we generate um
answers long-form questions and evaluate
them with physicians in that case we are
just generating once um to kind of do
that kind of the most simple way
um but in terms of measuring I think the
the strongest way to measure it is
basically the human evaluation that we
did is I'll talk a little bit more about
human evaluation results um and some and
some of them were directly around kind
of alignment with scientific consensus
which is meant to measure hallucinations
awesome thank you
I had a cool questions as well
um
for how big was the data set
um for this instruction tuning
so initially the um for this med pump
paper the the data set was just about 60
Questions which was Tiny for the medpom2
and and met pumpm data sets uh were
significantly larger
so with met Palm we were basically
trying to see whether we could
um with a very very small amount of data
train the model to be able to kind of
without you know really adding
additional medical knowledge because you
know 60 Questions isn't enough to do
that basically train the model to behave
differently than it would otherwise and
so I basically view this as an approach
for rather than you know adding some new
knowledge to the model it's basically
kind of better aligning its existing
pre-trained knowledge to the task of
consumer medical question answering
across you know the axis that we care
about
that makes sense um I was also curious
about the
specialty breakdown of the questions I
know the point isn't to get it to
include more medical information but
have you seen whether
differences in the specialty of the
questions or you know questions from
different Medical Specialties affect
Downstream performance on usmoe or other
benchmarking data sets
it's a great question we haven't done a
like disaggregated evaluation where you
try to break it down into different
Specialties and see how the performance
changes
but for the
um the mmlu data set it does kind of
break it up into sub topics where we and
we do report results for different
subtopics so things like Anatomy or or
high school biology or whatever it is
the different tasks so we do report
those results
um I those are those are relatively
small data sets so I don't think they're
super informative in terms of the you
know different results between different
data sets but I think it's an
interesting question I think it's it's
something that like
um it's something that I think I haven't
seen a compelling version of so I think
it's something that like would be useful
broadly
um we have seen recently as we've been
you know exploring more
um detailed and specialist questions
that often met Palm gets wrong because
we've been kind of deliberately
exploring that more recently
um that um
the question is that generals Physicians
are less likely to know metapom is also
less likely to know
um which kind of makes sense
um and so we're kind of recently been
investing more and kind of working with
specialist Physicians across different
tasks and you know first specific
questions getting those getting the
feedback and the um the uh ratings from
The Specialist Physicians but we haven't
done like a careful um breakdown by
different physician different
Specialties in terms of performance
awesome
let's keep going
um I'll kind of briefly talk a little
bit about medpom2 and um as well and
I'll present some results
um so met pump 2 builds heavily on the
palm 2 model
um so that there was a bit of a
technical report which is not um
uh which has actually a decent amount of
of useful information in there around
um how Palm 2 improved upon Palm there
were three kind of main points the first
is compute optimal scaling
um so there's been a bunch of work
um kind of exploring scaling laws in the
context of large language models and how
should you scale
um compute versus data
um a few Works have found and and this
were kind of replicated that um the uh
the scaling laws used in other papers or
um or often that were not used at all uh
were not as optimal as
um uh doing things uh in the chinchilla
scaling loss framework
um so this is kind of roughly using 20
tokens per parameter of the model
um and so this work also saw that and
also kind of did a similar thing in
terms of applying a compute optimal
scaling the second thing is kind of
improved data set mixture especially
with respect to multilinguality which
kind of significantly improved
performance uh there and then the last
thing is a mixture of objectives type
loss similar to the ul2 work that came
out where instead of optimizing for just
one objective you're doing kind of a
mixture but you're still retaining the
models um Auto regressive capabilities
foreign
I'll just very Briefly summarize key
updates for matpom2
um so the mid Palm 2 builds on Palm 2
applies similar kind of instruction
tuning and prompting techniques as we're
used for metpom uh we kind of uh use an
expanded data set mixture and tuned it
um we applied this technique called
Ensemble refinement which I'll spend a
minute on and then we've also improved
human evaluation and adversal testing
um so on the right on the bottom right
you can see this illustration of this
Ensemble refinement technique which can
be viewed as kind of like an extension
of self-consistency
where you get Med pump 2 to produce
multiple possible reasoning paths and
then instead of
um aggregating it over it via like a
majority vote like in self-consistency
you take that um those different
reasoning paths that have matpom to
aggregate over them itself and so that
has the full context of the reasoning
paths as a result it's able to provide
kind of a better answer than it would
otherwise
um I'll also briefly touch on Palm eh so
this is another work that came out uh
that builds on Palm
um palmy was kind of motivated by the
fact that
um there's been kind of work on the
vision domain as well that has involved
kind of scaling up Vision encoders
um but so far that's not really
um you know been well tied to the to uh
palm and these large language models
although there's been some work on
visual language models and so pami
basically combines uh palm and vision
Transformers uh to produce a visual
language model where uh basically the
outputs of a visual uh the the vision
Transformer are then mapped into the
space of the large language model and
you effectively get a large language
model that's also able to take in images
and potentially other inputs and then
output languages language
um and so this was originally supported
in the context of Robotics and
embodiment in that context but it's also
effectively a visual language model that
we can use in this context
um and so matpom M basically is uh pami
uh simply instruction tuned on multimed
bench the second Benchmark that I
presented including the multi-modal
tasks
um and so my palm m is uh basically
trained across tasks in dermatology and
mammography genomics Radiology
um and you know medical textbooks and
pathology
and the data used for training admission
on the right
um and I'll briefly uh talk about
experiments that we did with medpom
medpom2 and medpom
um so with medpom so some highlights
from the December 2022 paper we
um basically saw that for this med QA U
assembly style task which
um you know was of interest to folks but
we also wanted to move Beyond we saw
this like significant increase in
performance from uh previous models uh
we also saw the model was able to
produce answers to long-form answers
open-ended answers to
um consumer questions in a fairly
compelling way and so talk a little bit
more about each of these results
um and so if we compare at the time of
medpom uh the state of the art and also
um plan Palm
we saw that flying Palm by itself before
we did anything with medpom was able to
perform quite well
um on across different data sets
um we also saw that
um for the mmlu clinical topics
um uh things like clinical knowledge and
college biology or medical genetics that
plan bomb was outperforming uh the other
uh models that we were comparing against
um we saw this an interesting analysis
when we did selective prediction which
is basically this task of seeing whether
or not the model can encode its own
confidence in its predictions
um and so if we came up with a way we
came away of basically asking the model
how uncertain it is which was basically
involving asking the model repeatedly to
produce an answer to a question and then
if if the answers varied across
different generations and that then that
was kind of considered uncertain
otherwise it wasn't uncertain
and so if we use this metric to tell the
model 1 to defer and then we asked
someone to defer 10 of the time or five
percent of the time we saw that the
accuracy increased and so that's
basically a signal that the model is
able to to encode its own uncertainty
about its predictions before it makes
prediction
um so that was a cool thing to see
um we also kind of measured
um like I discussed briefly before we
measured uh clinician evaluations across
different long-form questions and so
when we measured agreement with
scientific and clinical consensus which
is probably one of the most important
axes because it's effectively measuring
hallucination we saw a significant gap
between flan palm and clinicians and
then that Palm was able to mostly close
that Gap
uh when we looked at comprehension
retrieval reasoning again the medical
question answering context uh there was
again broadly a gap between plant palm
and clinicians to start uh and then that
kind of motivated our work on met Palm
where we saw that we were able to
broadly close the gap or or
significantly reduce the Gap across all
these these things
um with um flat bomb we again saw gap
for Incorrect and or or missing content
um interestingly for medpom and we also
saw this for medpom too but there was
actually an increase in inappropriate
and incorrect content or there wasn't at
least there wasn't a solid decrease
um and so I think for us this was
basically a signal that
um you know these models when they're
asked to provide a detailed answer to a
question can still hallucinate uh
significantly
um and off that hallucination can
snowball uh to become worse if the model
is kind of conditioning on itself and so
I'll talk a little bit more about that
as a limitation of some of the work we
did but for us this revealed that there
was a bit of a trade-off between
um length of answers and
um the inclusion of potentially
incorrect content
um and so what we observed is like
medpom would often produce more detailed
answers than plan mom
um and you know more likely answers and
sort of have more opportunities to
hallucinate and so if we reduce that you
know we would have a reduction in the
amount of hallucination or inappropriate
and incorrect content but
um you know there's a bit of a trade-off
there because the the both the clinician
and the lay users broadly preferred but
more detailed answers
another really important access was the
possible extent and likelihood alarm
um and so there we saw that plant palm
again had a big gap with clinicians
which is quite consequential and again
that met Palm was performing more
similarly to clinicians
lastly we again saw a gap for this
question around bias in the context of
medical demographics but matpom was able
to again mostly close the gap
we also asked again lay users to
basically rate whether or not
they preferred uh Med Palm or flan Palm
or clinician answers
and in this case we were asking about
what the question or the answer
addressed the intent of the question we
saw that there was a bit of an
improvement between my palm and plant
palm but not super significant and then
in terms of helpfulness we again saw you
know significant gap between plant bomb
and clinicians and that Med pump was
able to mostly close the gap and so that
was promising
um so that kind of summarized the key
results for the Met pump one paper for
medpom2 we basically built on this again
in the context of medical question
answering
um using kind of improved model and
provided kind of more
kind of improve methodology for doing
evaluation including kind of pairwise
ratings between different possible
answers and adversarial testing in the
context of both General Medical
questions and Health Equity questions
and so on the left you can see again on
the team assembly style Benchmark those
the significant Improvement in
performance on the right we basically
asked Physicians to choose whether they
preferred Med pump 2 answers versus
physician answers across different axes
and so for example given a met pump two
answer given a physician answer which
one better reflects a scientific or
clinical consensus
what we observed was that there was
across eight of nine of the axes that we
looked at
um that met pump two answers were
preferred by physicians over position
answers but you know I want to caveat
that with the statement that this is you
know specific to how we did the
evaluation in the collection of examples
and that pump 2 was often you know
producing significantly more detailed
answers than Physicians
um you know which could cause
um you know which could cause like some
bias and how people are doing these
ratings and we did observe that there
was kind of more incorrect or inaccurate
and irrelevant information in medpom2
answers so that you know it was kind of
suggestive of this of this trade-off
between length and you know the
potential for the model to include stuff
that isn't really relevant
um so just giving a brief overview sorry
the text is a bit small of the medical
uh multiple choice question uh results
from this work uh we broadly saw that
met pump 2 the best results for every
game with mad pump 2 were about
comparable to gpd4 and significantly
better than
um flat and bomb or mid Palm
um and uh we also saw that when we
applied a few shop prompting versus
Chain of Thought prompting versus
Ensemble refinement prompting that
Ensemble refined prompting uh broadly
outperformed the rest
um some Advantage also produced improved
long-form answers to Consumer medical
questions which was kind of one of the
main motivations for for the for the
work
and so here's some examples of um
clinician answers and then mad Palm two
answers and then some of the ratings The
clinicians gave those answers
uh we also did kind of a more detail
thorough physician of individual
evaluation uh interestingly this is kind
of the first thing that we did
um kind of more similar to what we did
with met Palm uh where again across
these flaxes that we were originally
measuring trying to see whether or not
um uh there was uh whether met Palm was
preferred or met pump 2 was preferred or
met palm and Physicians what we've
broadly observed was that this didn't
have a ton of statistical power anymore
because across many of the axes uh the
performance for all three of these
things met Palm 2 and met palm and
Physicians were quite High
um and so that kind of motivated us to
do pairwise evaluation instead
um which I briefly talked about earlier
um we did kind of evaluate on these
adversarial questions on the adversarial
questions that was kind of a clear
benefit for medpom2 even on this
individual evaluation uh framework where
we just looked at one question one
answer
but if we looked at the pairwise
evaluation so again this is
um one question and then two different
answers there was a significant benefit
for for met Palm 2 versus medpom or
Physicians
we also did a layperson individual
evaluation so this is uh for Lay users
asking them whether they I thought the
answer addresses the intent of the
question or whether it was helpful uh we
broadly saw some small improvements for
met pump 2 versus
um medpom and Physicians
um any questions up to this point
okay cool I'll also touch a little bit
on net Palm m key results
um so on the left we have a spider plot
which basically shows
um the state-of-the-art across multiple
different tasks here so from mammography
classification to Radiology report
summarization uh we see the the area in
blue is basically the performance of
Matt Palm M so broadly what we see is
that mad Palm m is able to kind of
roughly match the specialized soda
across many many different tasks and
approach uh state of the art there on
the right we have kind of a more
detailed
um
uh comparison so we can see that roughly
across all these different types of
tasks and across these different data
sets that um one model you know trained
with the same weights uh is able to
perform roughly on par with the state of
the art across many different tasks of
course there are cases in which the
state of the art significantly beats
menopause and vice versa but broadly
speaking uh the kind of thing that we
saw here was that uh this kind of idea
of like a generalist model that could do
multiple tests seem to have some weight
and another thing I want to mention is
that these results were were not like
heavily tuned or anything like that
um so this was you know one set of
Weights one one attempt at model
training um and uh fairly strong
preliminary results there
um
for the metrics I had a few questions
one was um could you explain the F1 rag
graph metric yeah absolutely um and then
second more generally I'm curious how
you think about
you know it's it's a similar question to
what was asked before about the
difference between benchmarks and real
world data and how you evaluate these
types of models and whether there are
better
metrics that capture more of the medical
information you know compared to just
Rouge blue and uh F1 scores I guess yeah
absolutely I I think accuracy and Rouge
and blue I think are not the most useful
metrics but they're basically a way of
getting a barometer of model performance
especially in like preliminary results
in the next slide I'll also talk a
little bit about the human evaluation
results for Matt Palmetto but um you
know for the specific contact question
about F1 rad graph I think in general in
the Radiology context people often will
report
um uh a couple things one is these
natural language generation metrics like
Rouge and blue Insider d uh the second
thing is
um kind of uh General accuracy metrics
um uh where accuracy in this context
comes from labels that come from
um some automated systems in some ways
um so there's kind of a history of
basically like checksport labelers or
other kinds of labelers that basically
take in a reference report and then
produce a classification across
different kinds of conditions
um so given a reference report basically
classifying across different typically
relevant conditions and then doing the
same for the model generator report and
then measuring metrics like accuracy and
F1 score and things like that and so
that's the kind of metric that F1
radograph is I'd say that metric or
these kinds of metric are actually
relatively relevant
um compared to kind of Rouge and blue
and other things because they're aiming
to extract the critically relevant
information from a chess x-ray report
and then kind of as a classification
problem that said I think this is not
enough for us to be able to say that you
know these models are actually useful in
real good workflows
um because we one we need human
evaluation and then two we actually need
to put them in real world flows so the
for the first point I'll talk a little
bit about on the next slide but the
second point I think it's not addressed
by this work
so
I had a question about uh if there's any
like interpretability work done on some
of the uh Imaging or others because like
a lot of these data sets like mimic even
state-of-the-art classifiers have a
proclivity to like if you look at their
grad cams or whatever to pick up on just
auxiliary information that isn't
relevant but you know optimizes for
classification uh was there any sort of
like you know ablations or or things
tested to see if like the accuracy that
you're getting on these was was actually
that and not you know auxiliary
information
yeah it's a really great point I think
the history of medical imaging has been
like littered with
um
uh models or evaluation approaches that
often you know cause
a model to kind of look at like shortcut
features
um so often for example you know train a
model on multiple tasks and then it'll
often get good at the task of Hospital
prediction versus prediction of the of
the actual um thing that you're trying
to do I think in this context the a
couple ways we tried to mitigate this
broadly one is we tried to use a wide
variety of data sets
um and so um that's not I think fully
convincing but it basically kind of
creates a situation in which we were
able to train and evaluate across many
different contexts across many different
data sources
um and so it reduces the potential for
the model to be relying only on these
kind of spiritus and spurious
correlations
um the other thing is um we did do some
like human evaluation of the um model's
outputs and so they're given actual
chest x-rays given model generated
reports we had the model basically or
had had Radiologists look at the um the
actual explanations produced by the
model
um and see whether or not they were
preferred or whether they had
significant errors or minor errors or
things like that and so that latter
thing I think is probably the most
convincing thing
gotcha
cool
um let's briefly talk about the
physician evaluation here
um
so we basically did a four-way
comparison between
um reports produced by different sizes
of medpummem and a reference report from
the data set so this is a radiologist
produced report
um broadly what we saw was that the
reference report was preferred over the
model produce reports in every case but
that the kind of pairwise preference uh
between uh the strongest models and
strong settings was often approaching 30
or 40 percent
um so that the you know that basically
means that like roughly in 40 or 30
percent of the cases that Radiologists
actually preferred to the model produced
answer versus the Radiology produce
answer so I think this kind of kind of
suggests like an early indication that
these these things could be useful in
these in this real world workflow but
you know that said this is like a very
early result the sample size is small
this is across just one data set
um and so there's you know plenty of
limitations here
awesome um so I want to give a bit of
time for discussion here and I wanted
this to be a little bit open-ended
um so if we kind of jump jump out jump
jump jump kind of back and think about
like the implications of this work we
haven't met Palm which kind of showed
that these models uh encode clinical
knowledge that they're able to answer
medical questions and perform kind of a
wide variety of tasks that could be
framed as another question we have met
pump two that kind of further improves
that towards expert level performance
um and performs well on both multiple
choice questions and it's also able to
kind of produce answers that often
preferred by position is over physician
answers
and then we have met pump M which kind
of significantly expands a set of tasks
that we're doing with these models
um often um kind of classification or
accuracy tasks but also some generation
or summarization tasks as well
um it's another significant amount of
wide of kind of tasks that these models
can do and across these works we you
know relied heavily on human evaluation
to be able to validate these models on
these specific tasks
um and so if we go back to our you know
initial dream of kind of improved care
delivery and improved science
um I'm curious what you guys think are
kind of the main blockers for us to be
able to actually achieve these things I
have a few things listed in the next
slide but I'm curious if anybody has any
has anything that they want to raise
yeah for the medical image sorry you'll
go first ah yeah or go ahead
okay so one thing in magical images that
or like common uh commotion neural
network are not hand well it's different
data side different medical image data
sets different modules they have
different resolution or different sides
of the images but sometimes the the size
or the dimension of the images
could be informative uh like you have a
bigger cell you have bigger tumor that
could be an issue so I'm wondering in
this image encoder that you fit into the
vision language model would also
consider the dimension of the images
yeah absolutely I think that was
definitely a limitation of our work with
medpomm um the
resolution of the images that we were
feeding into the model was was quite
small and so broadly we suspect that was
one reason that um the model's
performance didn't really scale a ton
with um improved model skill
um in general there is kind of a wide
variety of resolutions of images that
show up in in medical imaging and
there's also like 3D images
um like CT scans
um like volumetric scans there's also
potentially gigapixel images and
pathology
um and so I think that from my
perspective kind of motivates a work on
kind of being able to train different
encoders for different kinds of
modalities
um and being able to kind of uh graph
that onto large language models without
retraining the whole thing or an
alternative approach might be training
encoders that are more Universal that
are able to take in all these different
kind of resolutions of images
um and so there are there's a work
around kind of Transformers that can
take in raw bytes for example sequences
of raw bytes I haven't seen them applied
um kind of broadly in this context in
the context of different multiple uh
different Medical modalities but that I
think would be quite interesting um a
easy way I can think of is to just add a
type like if you're a doctor you know
all kind of images you know it's
resolution or what kind of images it is
are
like in this way I feel like you don't
have to retrieve a model and you can
have Universal model but also with
reference to the marketing information
doctrinal
uh it's true it's true like you can
annotate it with the tasks that you care
about and that's definitely instruction
tuning gives you that but there's also a
potential that like you might be losing
information if you downsize for example
gigapixel image to a much smaller
resolution
um and there's also the issue of how to
handle volumetric scans and things like
that
um and so
it might I I think putting everything in
a vision Transformer might not be the
approach that that ends up working out
um
yeah yeah make great sense
uh building off of that I one one thing
that was that came to mind or I had two
two interesting things so there was a
paper published uh like from Oxford a
while back on when using Transformers on
images like medical images like brain
scans and stuff that like
diffiomorphisms and morphological
preservations when actually you know
convolving features or actually
attempting to learn from them actually
like Smooths over features inadvertently
um and and that actually removes a lot
of information in in a lot of ways and I
was wondering like I think something
that a lot of people have put effort
into is preserving morphological
structure well like convolving features
or or even with like Vision Transformers
like vit they still use
um you know some sort of encoding
representation that has a proclivity to
lose that like underlying
um like isomorphisms and apiomorphisms
from like MRIS
um and that's like difficult to to keep
track of I don't know if like preserving
structure I think we talked a little bit
about like structure from
different modalities and images just
like something that's possible like
considering the like the variety
yeah I I think our choice of
architectures and loss functions often
encodes kind of inductive biases about
the problems that we're trying to solve
um and in the case of convolutions I
think that's that's clearly true another
one that's um you know relevant to our
work is around self-supervised learning
um if you apply like you know
off-the-shelf approaches like simpler
you will effectively your augmentations
will involve throwing away a lot of
information that is contained in uh
medical images that you know those
augmentations are basically encoding
inductive priors that work well for
imagenet but in the case of medical
images you know you're lost can throw
away quite important information and so
I think it it does make sense to kind of
um you know think about what inductive
biases
um these approaches are are encoding and
like what that has to do with the
medical setting because I think if we
don't explicitly think about that then
we might you know effectively train
models that are
um are less reliable or relying on the
wrong features and things like that yeah
and the other other thing is that like
so I I'm not like MIT like MGH and HMS
so there's a lot of like clinical
applications of AI that we end up using
here but a large conversation that we
have is the the sort of workflows that
we have in you know highly resource
resource enriched environments in
hospitals is not that of what's
available in in different areas that are
more resource constrained so like AI
suggest clinical workflows are or things
might be more difficult are there like
considerations that you guys have when
working with stuff like palm2 that the
not only the data but also the workflows
themselves are better adapted to
Resource constrained areas
sorry I didn't understand the last part
of the question
oh yeah so is it like so the workflows
that we have at you know like a hospital
like MGH are not equivalent to that in
in more emergent countries so like the
clinical suggestions and practices of
techniques sort of like Interventional
suggestions that uh a model might have
trained on very on data from these like
research and rich areas like MGH or
something no uh how how well does it
translate for a model like Med Palm when
it provides suggestions on like
practices or clinical suggestions for
pages that don't make may not
necessarily have the same resources
oh it's a great question it's something
that we're looking at now broadly what
we see is that
um as you'd expect performance might not
be quite as good and it's something that
like we are actively looking to mitigate
cool
I think along those lines
oh sorry oh
no go for it
um I think along those lines
um how do you think about
capturing other information from missing
data or just handling
you know uh data that you might not want
to
include right so
um suppose you have
Imaging data for a patient but it's not
necessarily
relevant or it's you know there are
artifacts in it that are
um actively going to actively working
against the model
are there ways to mitigate that or be
able to identify situations where you
might not want to use
that data
yeah it's a great question so in cases
where data might not be super useful or
might basically cause the model to kind
of reinforce the models you know
Reliance on sparious correlations how do
we make sure that we're not you know
you know relying on that data it's a
good question I think you know to this
point we're kind of largely relying on
whatever data we can are is available
because I think in a lot of contexts
um Medical Data that's you know the
anonymizing and everything like that is
hard to come by
um but I think
um there's kind of work on kind of
um trying to
um develop classifiers for whether or
not
um data contains various correlations if
that makes sense
um so people will often do things where
they will train the model on uh data
from one data set they'll look at its
predictions on another data sets out of
distribution then look at
um you know additional labels that come
in for that data set and then try to
train a model that excludes the examples
from the original data set that cause it
to reinforce on spurious labels if that
makes sense
um so this kind of approaches that
people have for mitigating this but
um we haven't really applied this in
this work
[Music]
yeah it's interesting to hear more about
this because I
don't do fidget language models I'm much
more on the uh clinical note side
thanks
awesome
um so I just wanted to quickly uh
mention there's a couple more
discussions around limitations and open
challenges here uh I wanted to kind of
quickly mention uh that uh this work
would not have been possible without you
know this this large team of people
um and so very appreciative of everybody
and my scientific settlements shown on
the slide thank you
thank you so much
Grand that was an amazing talk
um I think we didn't have time yet to
talk about like the care delivery part
of it and like how the envision
this model be actually embedded in a
workflow given that it was trained on
like very high quality question
answering star data set like what are
you do you think data from practice
would add like data from Clinical notes
that would be missing in such a data set
yeah I think it like the thing that I
think is um
kind of a big next step is really
thinking about evaluation in the context
of specific clinical workflows and then
thinking about what data is you know
useful for those specific workflows um
and so one thing that I think is is
starting to happen is there's a lot of
um work around taking large language
models and using them through this um
the burden of clinical care
so things like
um you know documenting an interaction
and things like that people are often
spending hours a day doing things like
that in that context I think um
uh the data that you know companies in
the space are collecting around you know
transcript prescriptions
um the summarizations of those
transcriptions any labels that doctors
have around the quality of those
prescriptions so for example if I'm
providing a service for reducing the
clinical documentation that involves
taking a transcription and then
summarizing that into clinical note or a
discharge summary or whatever it is if I
have feedback data which is basically
looks like whether clinicians accept or
decline you know that recommendation or
a possible generation I think that's
probably the most useful kind of data
for that kind of use case
um that's kind of what's roughly missing
because
we're at a point where I think the large
language model based capabilities and
knowledge are roughly good enough to be
able to do that task
and I think the thing that's needed now
is kind of like refinement on kind of
feedback on that specific workflow and
I'd say the same for other workflows I
could be talking about clinical decision
support which I think is a really
exciting use case as well
um I think roughly speaking the models
have a good amount of knowledge here
already I think ideally we could fine
tune on you know additional data that
comes in from the context but then the
probably the best thing there would also
be additional feedback data which looks
like you know in the specific context
that a doctor is operating in given the
specific you know populations and
distribution of patients that they're
looking at whether or not they accept
you know the predictions of a clinical
decision support agent
um in general I think that's that's kind
of where we're at where I think the
missing piece now is the post-training
refinement of these models um in the
context of specific workflows versus
like the pre-training which is I think
already quite capable
so uh do models like this have an
ability for Federated learning or
methods where like uh sometimes there's
a lot of policities done about
um a classifier model they built and
predicting uh you know sepsis from
different sets of Mount Sinai hospitals
I mean if you looked at the features
from a couple of branches they were
completely different and like your your
race and your ethnicity mattered
substantially more and then if you
looked at more like a different side it
was actually like clinical factors like
albumin levels or whatever so is there
some sort of method of training these
models like when you talk about you know
including the specific clinical
workflows of of sort of adjusting for a
variety of different mod like of
clinical settings
yeah absolutely
um so on the context of federal learning
it's in theory it's quite I think well
motivated in this setting because you
are effectively you know getting the
opportunity to in a private way
um train on data from different contexts
and condition on on data from different
contexts and use that to improve a model
and
um you know privacy is often a big
concern when it comes to Phi and help
data
um and so it's unmotivated I I think
there's kind of a significant challenge
though to scaling Federate learning to
the scale of
um language models which remains
so the communication costs and
efficiency uh you know memory and
bandwidth costs of doing this right um
Can often be relatively
um hard you know unmanageable
um that said like I think parameter
efficient techniques um exploring this
in the context of cross-silo settings
like hospitals can make these things
more manageable versus like
fully cross-device Federal learning
where you know you have to send a large
language model to each person's device
every time
um
on a technical level you know in terms
of getting models to be able to
condition to different contexts
um
this is basically a function I think of
training on a lot of diverse data with
instructions
um for the most part
um I think like there is
um
this is effectively kind of what was
shown by the instruction to any paper
outside of the magical context that if
you
um train a model uh to follow
instructions broadly across a wide
variety of tasks and have it do a wide
variety of tasks during training that
during tests they can kind of General
analyze to somewhat unseen tasks
a similar kind of thing in a medical
setting uh with respect to training is
that you know training objective can
also be applied in a federal learning
context
okay
um I think we are uh them as well top of
the hours so thank you so much Karen for
uh
this great talking this great work
thanks everyone for joining us