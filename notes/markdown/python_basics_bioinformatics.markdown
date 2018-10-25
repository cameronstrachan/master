|Python|Basics for genome science|2018-09-27|
|---|---|---|

### Basic string operators

```python
+ #concatenate strings
* #copy strings
in #true if member
not in #true if not a member
```

### Slicing
* counting always begins with 0.
* negative numbers begin at the end of the string.

```python
string[x] #indexing
string[x:y] #slicing
string[X:] #until the end of the string
string[0:4:2] - #third number is step argument. skip every two
string[::-1] #goes from reverse
```

### A note on OOP
* Objects have methods! String and lists are Objects!
* Remember that the methods often modify the object itself.

### Strings

**split and join**

```python
split() #returns a list of words in a string
string.split() #split by white space
string.join(list) #join together a list can
''.join() #join to an empty string
```

**other useful methods**

```python
string.count('a')
string.upper()
string.find('a', 17) #gives location, second argument where to begin
string.rfind() #looks in reverse
string.replace('a', 'A')
```

### String formatting

```python
%5.3f% #here 5 is the number of digits, 3 is number of decimals, f is for float
#e is for E notation
#d is for integer
#s is for string
print("%s" % dna)
```
### Lists
* lists are mutable.
* slicing works on lists.

```python
list = []
del list[1] #deletes second element
list.extend(new list) #concatenates to the list
list.count('A') #count the occurrence of this string
list.reverse() #return elements in reverse
list.append() #remember that append only adds 1 element (won't extent)
list.sort()
list() #convert a string to a list
```

### Tuples
* tuples are immutable.

```python
tuple = ()
```

### Set
* list with no duplicate entries.
* are unordered with no index.
* automatically removes any duplicates.

```python
set = {}
set1 | set2 #union
set1 & set2 #intersection
set1 - set2 #difference
```

### Dictionary
* represents key-value pairs.
* keys are immutable.

```python
dict = {x:y , x:y}
dict['key'] #get value
"x" in dict #test if key is present with in
del #works on dictionaries
dict.update(dict) #add a new dictionary to the existing one
list(dict.keys) #returns all the keys (same with value)
```

### If statements
* if statement requires TRUE or FALSE.

```python
if __:

elif:

else:
```

### Returning a boolean

```python
== #equals
!= #does not equal

## membership
in
not in

## logic
and
or
not
```

**identity tests** point to the same object in memory. useful if copy of object gets modified by a method.

```python
is
is not
```

### Loops

**general**

```python
break #breaks the loop
continue #go back to the beginning of the loop
pass #can act like a place holder
```

**for**

```python
for ___ in ___:

for x in range(length()): #standard use

## iterating
range(4) #yields 0,1,2,3
range(1,10,2) #yields 1,3,5,7,9

## getting data from a dictionary
for name, seq in seqs.items(): #items get us key and value are a pair
	print(name, seq)
```

**while**
* while a condition is true.


```python
while ___:

while num > -1: #standard use
  change num
```

### Functions
* reusable and allow abstraction.
* variables are local to the function.
* positional arguments specified according to their position.
* keyword arguments has a keyword name for the argument.
* \*args means accepting the arbitrary numbers of positional arguments and \*\*kwargs means accepting the arbitrary numbers of keyword arguments. The arguments passed as positional are stored in a list called args, and the arguments passed as keyword are stored in a dict called kwargs.


```python
def function_name(arguments):
	" documentation "
	code
	return output

def save_ranking(*args, **kwargs): #arbitrary number of arguments
    print(args)
    print(kwargs)

save_ranking('ming', 'alice', 'tom', fourth='wilson', fifth='roy')
# returns ('ming', 'alice', 'tom') ; {'fourth': 'wilson', 'fifth': 'roy'}
```

### List comprehensions

* provides a concise way to make lists.
* make new list where each element is an operation of an existing list.
* same as looping through a list, applying some operation to each element and appending the results to a new list.

```python
new_list = [operation(i) for i in old_list if filter(i)]
```

### Modules
* is a script containing several functions.

```python
import script_name #import does not require .py
script_name.function(arg) #using the functions
from script_name import * #import all functions
from script_name import function1, function2 #import specific functions
```

### Packages
* packages group modules (or a folder of scripts containing functions).
* each package is a directory which must contain a special file called __init__.py which can be empty, but tells the directory it contains a python package.

```python
import a.b #package a, module b
a.b.function() #example function usuage
from package import module #import a single module
from package.module import function1 #import a single function
```

### Reading in datasets

```python
open(filename, mode) #r = read, w = write, and a = append
file.seek(0) #go to beginning of file
file.write() #write to the file
file.close()
line=line.rstrip() #gets rid of the new line character at the end of the line

### common error handling
try:
 f = open('myfile')
 except IOError: #IOError is error from operating system
 	print('the file does not exist')
```
