# dvanalysis-jobconfig-bker
Bookkeeper for configuration, jobOptions, transformations jobs or other related files for the Displaced vertex analysis at Atlas

The package is intended to bookkeep the different files related with the processing of data (in Athena, DV_xAODAnalysis framework, scripts, etc...) in order to be able to document and reproduce results. A tentative rules are below provided.

Each file is intended to follow the following conventions:
```
FILENAME.EXTENSION_EXECUTABLE
``` 
being 
  * *FILENAME.EXTENSION*: the file name as is usually used along with its extension (or suffix)
  * *EXECUTABLE*        : the name of the script or executable which uses this file,

and each commit should be provided as: 
```
Subject in one concise line. RELEASE: XXXXX  [NEED DEP]

BODY (if applies), more extense explanation about the commit, focused in
the what and why of the commit

DEP: DEP1, DEP2, ...
``` 
A commit per file is mandatory. It can be one-line commit if the executable can run out-of-the-box
with the file and the particular release pointed out. If not, i.e., if it needs extra packages, then the 
subject should contain the **[NEED DEP]** word and the commit BODY is needed. The dependecies are listed
at the end of the BODY in a comma-separated list
  * *RELEASE* is the recommended (or minimum) EXECUTABLE release needed by the file
  * *DEP:* comma-separated list of dependencies needed by the EXECUTABLE to run the filee in the RELEASE
