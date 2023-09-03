The following code runs an experiment I designed in order to gauge bias in ChatGPT (through the OpenAI API) and Google Bard (through the PaLM API). 
Bard and PaLM are used interchangably in my code.
The first set of the experiment, in the main file, runs Jonathan Haidt's popular Moral Foundations
Questionaire on both programs many times over, varying temperature and asking ChatGPT and Bard to 
respond as member's of various groups. ChatGPT has a publically available API. To query Bard, I use
the Google PaLM AP. The data this generates is stored in CSV files for comparison to human particpants' survey responses in
Dr. Haidt's studies.

In the second part of this experiment, I ask ChatGPT and Bard to appraise a series of moral vignettes
in order to compare with Scott Clifford's 2015 Moral Vignettes Study. MFQ.py can run the MFQ study on Bard and PaLM.
I use seperate files (vignettesGPT and vignettesbard) to run the moral foundations vignettes study on each 
program. I queried PaLM through a rotating list of about 20 API keys. For the OpenAI queries, I load in a single API key 
and reuse it many times.
