title: Why SJF Beats FCFS (Sometimes)
date: 2026-06-05
tags: os, algorithms

Nonpreemptive Shortest Job First almost always wins on *average* waiting time,
but it isn't free. Here's what building a simulator taught me.

## The setup

FCFS processes jobs in arrival order. Simple, fair looking, and easy to starve
long running jobs behind a queue of short ones. SJF instead always picks the
shortest available burst next, which minimizes average waiting time for a
fixed batch of jobs  a result you can prove with an exchange argument.

## What the simulation showed

Across a batch of eight processes with mixed burst lengths, SJF cut average
waiting time by roughly a third compared to FCFS. The catch: one long process
in the batch waited far longer under SJF than it would have under FCFS. Lower
average, higher variance.

## Takeaway

Average waiting time is a fine metric for throughput focused systems, but it
hides tail latency. Real schedulers (like the ones in Linux) borrow ideas from
both worlds  priority and aging  to avoid starving anything indefinitely.
