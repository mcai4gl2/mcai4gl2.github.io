---
title: "Triaging Path Issue with tabula-py"
date: 2022-03-19T14:04:31+08:00
---

I have been big fan of Jupyter Notebooks ever since it was still called ipython. The ability to be able to interactively develop code with immediate data cached is extremely powerful for quick prototyping and data exploration. Originally started for python, Jupyter nowadays supports all different programming languages. 

Recently, I have been working on a Java project at home. So, I took sometime to test [IJava](https://github.com/SpencerPark/IJava) and [get it working with Java 17 in docker](https://github.com/mcai4gl2/jupyter-ijava). I am using this image to build all my Java Jupyter notebooks in Github Action for CI. In my local setup at home on Windows, I have a conda environment running Jupyter and IJava with jdk17 installed and java on the PATH.

This setup has been working quite nice for me where I can write libraries in java in Intellij and then import the complied jar to Jupyter for quick testing and visualization of data. Last week, I have been asked by my wife to help extracting tables from a number of pdf files into excel spreadsheet for her. I did some quick search and installed [tabula-py](https://github.com/chezou/tabula-py). This worked quite well and she is happy except the some rows with merged cells she had to clean up manually. I did this quickly without the due diligence of creating a new conda environment. tabula-py was installed on the one I used for my own java project directly. When I went back to my own project, my java notebook started to complain:
```
Class file has wrong version 61.0, should be 55.0
```
`55.0` is java11, but I didn't remember I installed it but it clearly is on my path. `where java` shows:
```
C:\Programming\miniconda3\envs\jupyter\Library\bin\java.exe
C:\Program Files\Java\jdk-17.0.2\bin\java.exe
```
So this java is only for my `jupyter` conda environment, which shall be installed by conda. With:
```
conda list --revisions
conda install --revision 5
```
I managed to revert the environment before tabula-py installation and everything started to work again (version 5 is the version before I installed tabula-py).

I went to [tabula-py Github](https://github.com/chezou/tabula-py) to read more about the package as I thought it was a pure python package before. I then find out it is actually a python wrapper of the java library. This kind of explains why the java dependency is added. I opened [`setup.cfg`](https://github.com/chezou/tabula-py/blob/master/setup.cfg) and looked for the last missing jigsaw piece: the java dependency. And it is not there!

Was it removed on the master recently? I went to 2.3.0 tag, which is the version I used before, to confirm and java dependency was not there either. This is the exact moment a developer panics. So, I created a new conda environment and install `tabula-py` to test if the java PATH issue could be replicated. Then I started to search if there are some conda magic to install java. I almost gave up on trying to understand this until I read:
```
Note

conda recipe on conda-forge is not maintained by us. We recommend to install via pip to use latest version of tabula-py.
```
In [tabula-py GetStarted page](https://github.com/chezou/tabula-py/blob/master/docs/getting_started.rst).

This is really the light bulb moment and confirmed with `conda search tabula-py --info` where I see:
```
dependencies:
  - distro
  - numpy
  - openjdk >=8
  - pandas >=0.25.3
  - python >=3.9,<3.10.0a0
```
and find the [`meta.yaml` file](https://github.com/conda-forge/tabula-py-feedstock/blob/main/recipe/meta.yaml).

Now the mystery is solved. 

Things I learnt:
- `where` and not `which` in Windows
- `conda search` is your friend
- conda recipe may not reflect all dependencies of the package
