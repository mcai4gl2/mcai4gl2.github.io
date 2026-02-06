---
title: "Blink Protocol in Python"
date: 2026-02-06T13:08:14Z
---

Recently, I have learnt [blink protocol](https://rustyx.org/blink/). The spec is interestingly simple. Yet, it is quite powerful. It is a shame that this protocol didn't take off and there is no open source implementation can be found to study it.

I decided to give AI a go to implement it. While we know that AI can learn an open source framework easily as it got so much code to train on, it is interesting to see if AI can implement something it never trained on purely based on specification.

I downloaded the specification pdfs and give it to AI to build up a plan. Python was choosen as the implementation language as it is just easier to read. ChatGPT was able to generate the [original project plan](https://github.com/mcai4gl2/pyblink/blob/main/SPEC.md).

codex was able to make reasonable progress but as it is not good at tracking what is done and not done, I completely lost track of what is going on. This was fixed later on by having codex to [review](https://github.com/mcai4gl2/pyblink/blob/main/REVIEW.md) the implementation against the original spec and then working on fixes.

As AI finishing the implementation, I soonly realize an interesting problem: I am not in the position to understand if the implementation is correct or not especially for the binary format implementation. To help me understand the implementation, I have asked AI to [design a website](https://github.com/mcai4gl2/pyblink/blob/main/doc/WEB_DESIGN.md) to visually show me how the different format works. 

Now, there is [pylink](https://github.com/mcai4gl2/pyblink/tree/main) and [playground](https://pyblink.pages.dev). The pylink playground is a website where you can visually and interactively study the binary blink format. Using it, I can quickly validate if the implementation matches the specifications.

It is quite amazing to go though this journey and see AI is able to implement a fully functional code purely based on reading spec PDFs. Also, this shows me a new way to use AI to learn new programming libraries or ideas.
