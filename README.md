
<h4 align="center"> Information retrieval and search. Application of deep machine learning </h4>

<h4 align="center"> Winter semester 2021/2022 </h4>

<h3 align="center"> Homework 1 </h3>


# Overview

In this task I have implemented a probabilistic spell corrector, which will automatically correct any spelling errors in the queries.
A process is considered in which the user wishes to write a statement, but instead writes a statement, which may contain errors.

1. Equalizer. According to the desired statement q and the wrong statement r selects an appropriate list of elementary operations.
2. Appraiser. Evaluates the probability of each of the elementary spelling mistakes that may occur when writing the application.
In particular, the characters in a request to be deleted by mistake, inserted, substituted, transposed or kept unchanged.
3. Candidate generator. According to the original application r, used by the user, selects a set of candidates for the wanted application q.
4. Spelling Corector. Using 1, 2 and 3, finds the best candidate for the desired query.
