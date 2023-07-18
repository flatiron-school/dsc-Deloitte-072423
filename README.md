# dsc-Deloitte-072423
Deloitte AI Academy Intensive and Apprenticeship course materials for 07/24/23 cohort. It was made with ❤️ by Flatiron School


## Written Instructions to Connect to this Repository:
We will be going through these instuctions several times during the first week or so of class - no rush!

1. FORK this repository, creating a copy on your own GitHub account (creates a personal duplicate only online)

2. Then clone your fork down to your local computer (this will clone or copy your fork down to your local machine)

```
git clone https://github.com/[yourusername]/DS-Deloitte-02063.git
```

3. Add the ```/flatiron-school/``` version as the upstream (to pull future changes JP makes into your own copy)  
```
 git remote add upstream https://github.com/flatiron-school/DS-Deloitte-0206.git
```

4. You can make changes to the notebooks now! Remember to push your changes to your forked version of the repo (to save your local changes online):
```
git add [filename]
git commit -m 'message here'
git push
```
**Whenever you want to get updated notes:**
  
5. Grab the changes from the upstream repo
 ```
git fetch upstream
```  
6. Merge new changes onto your local repo
```
git merge upstream/main -m "meaningful message about what you're updating"