# Targeting with Partial Incentives

The [analysis of social networks](https://en.wikipedia.org/wiki/Social_network_analysis) is a technique born in 1930s
with the goal to visualize and measure relationships among individuals, groups and organizations or any other subject
involved in the process of knowledge exchange.

This technique has found many applications that go beyond social sciences, like in physics, biochemistry and computer
science as well, and the overall interest in studying it has grown a lot in the last few years.

In the context of [viral marketing](https://en.wikipedia.org/wiki/Viral_marketing), for example, it's useful to know
which individuals should be influenced first in order to cause a cascade in a network, through the word-of-mouth, that
makes every person in it to adopt the new product or idea one wants to spread.

This problem has been defined as the [Target Set Selection](https://link.springer.com/chapter/10.1007/11523468_91):
given a network of relationships, who are the fewest individuals one should directly get in touch with to cause a
cascade in it? Individuals, however, can be reluctant to adopt the product or idea and may need different efforts to be
persuaded. 

Society can be modeled as a network of relationships: a graph in which nodes represent individuals and links between a
pair of them exist if there is some kind of relationship between the two. A threshold can be associated to each node to
quantify its reluctance to adopt the novelty.

The adoption of deterministic algorithms on such a model however doesn't take into account the variability of a real
social network.

The purpose of this project is then to model and apply the
[deferred decision principle](https://en.wikipedia.org/wiki/Principle_of_deferred_decision) in order to test whether
algorithms developed for the deterministic model of the problem can still be applied to the probabilistic one.

Here the focus is on a [variant](https://arxiv.org/abs/1512.06372) of the Target Set Selection problem where individuals
of the network can be given partial incentives to make a decision.

The whole process is described in the [notebook](/notebooks/targeting/comparison.ipynb), which also shows results and
provides comments for them. Long story short, it turns out that both of the algorithms tested are still applicable to
this probabilistic model and their relative performance are the same as in the deterministic one.