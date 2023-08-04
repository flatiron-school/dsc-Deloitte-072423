# Data Science Practice Checkpoint

This assignment is designed to test your understanding of the checkpoint process. It covers:

 - Anwering a code question
 - Answering a short answer question
 
Read the instructions carefully. You will be asked both to write code and to respond to a short answer question.

**Note on checkpoint short answer questions:** Please use your own words. The expectation is that you have not copied and pasted from an external source, even if you consult another source to help craft your response. While the short answer questions are not necessarily being assessed on grammatical correctness or sentence structure, you should do your best to communicate yourself clearly.

## Imports

You will usually have to import different packages into a checkpoint or other material we give you

Don't worry if you don't have all the mechanics about what that means at this point

Just run the cell below, which is an example that imports the `string` module

(You do not need to use the `string` module to answer these questions, although technically you can use it if you want to)


```python
# Run this cell without changes
# (Note that you are not able to edit this cell, only to run it)
import string
```

## Question 1

### Question Content

In the cell below, modify the `greet_user` function to do the following:

 - take a name as an argument
 - return the statement "Greetings! I am `name` and I am pleased to make your acquaintance!"

Then assign the name `"Gene Hackman"` to the variable `name`.

Run all cells to confirm the result.

### Additional Notes

Note that there are code snippets like this in each code cell where you need to write an answer:

```python
# your code here
raise NotImplementedError
```

You can remove both of these lines, when you have replaced `None` with the right code. The purpose of these lines is to help you avoid accidentially forgetting to answer a question.

If you click the `Validate` button at the top, that will tell you whether you successfully removed all of those `raise NotImplementedError` lines. It will not tell you whether your answer is actually correct.

You can also generally ignore the language of "your code here". Instead pay attention to where the `None`s are that need to be replaced. 


```python
# Replace None with appropriate code

def greet_user(name):
    """
    this function takes a string name as an argument 
    and returns a greeting including that name 
    """
    statement = None
    # YOUR CODE HERE
    raise NotImplementedError()
    
    return statement
    
```


```python
# Replace None with appropriate code
name = None
# YOUR CODE HERE
raise NotImplementedError()
```


```python
print(greet_user(name))
```

### Test Cells

Similar to the imports cell above, you will not be able to modify the test cells. They contain a combination of visible and hidden tests. Make sure you restart your kernel and run all cells to make sure that you are passing the visible tests, although this doesn't fully guarantee that your answer is correct.

You will see an error message explaining what is wrong if your answer does not pass the visible tests.


```python
# greet_user should return a string
assert type(greet_user("Max")) == str
# name should be a string
assert type(name) == str

# PUT ALL WORK FOR THE ABOVE QUESTION ABOVE THIS CELL
# THIS UNALTERABLE CELL CONTAINS HIDDEN TESTS
```

## Question 2

### Question Content

Please explain the purpose of checkpoints and code challenges in the Flatiron School Data Science program.

### Additional Notes

Double-click on the markdown cell where it says `YOUR ANSWER HERE` to write your answer (replacing the `YOUR ANSWER HERE` text). If you write your answer somewhere else, the grader will assume you did not answer the question.

This is a short-answer question so there are no test cells. Instead your teacher will review and grade this answer manually.

YOUR ANSWER HERE
