*The PA Directory Search Engine*  
  
Practical Algorithms 2024-25, University of Glasgow  
Assessed Exercise 1  
  
Submitted by: Bellatrix Dawson Hodgson, 2770706H

# NOTE TO THE MARKER - file structure

I wrote this in multiple files. This structure is maintained in the src directory.

For your convenience, I also created a unified pa_search_engine.py at the top level. This is what `main.py` and `tester.py` call.
  
# A: Complexity Analysis 

Present the following complexity analysis in this report:  
  
+ Big-O complexity of the indexing operation.  
+ Big-O complexity of a search operation (given that indexing has been done already).  
+ Big-O complexity of a search operation if it were implemented in a brute force fashion (that is, no indexing performed, all search queries go through the entire text of all files every time).  
  
You should be very clear about what you mean by n when presenting your Big-O complexity analysis.  
  
_Note_: You don’t have to do a line-by-line code-analysis like we do in certain other problems. Instead, present your analysis as a text description that walks through the relevant operations, comments on their complexity with rationale, and then presents the overall complexity.  
  
## Your Answer  
  
### Indexing  
  
Indexing takes place in several nested loops. First it loops through each file in the target directory. Then it indexes each file, looping through each line in the file. Finally while parsing the line for tokens, it loops through each character in the line. After this happens, there are only loops through the tokens created from parsing each letter, which can at worst be equally as complex as looping through each character again. For this reason, I will be defining n as the number of characters in all files when talking about the Big-O complexity of indexing.

The first operation, `crawl_folder`, which loops through each file is just part of reaching the character loop. The same is true for the second operation, `index_file`'s line by line loop. Within `parse_line` is where we can finally say the program is O(n) complexity. That is to say that the previous loops are really just parts of the operation of the character loop (for the purposes of complexity analysis).

In `index_file`,  the list of tokens from `parse_line` is looped through multiple times. In the best case, this list is much shorter than n (number of characters in all files), in the worst case, it is exactly n. This worst case would be if the file only contained a single valid character, then the list is equivalent to the characters. Therefore, as there are no nested loops of this list or the characters, the Big-O complexity does not increase from these further loops.

In my implementation, indexing the forward and invert index also have O(n) time complexity as they require looping through each token to update a dictionary. Since I chose to use a dictionary as the data structure for these indexes, and Python implements dictionaries as a hash map, these updates happen in constant time (technically it could be more than constant time if it hits a collision and had to loop through the linked list at that location but I am ignoring that for this analysis as not to create more variables).

My implementation also requires the number of occurrences of each word present in each document, as well as the total word count of each document to be calculated to index the term frequency. Indexing document ranking also needs the word counts. Calculating these pre requisites has O(n) complexity, therefore, calculating document ranking also has O(n) time complexity.

Finally, indexing the inverse document frequency loops through all the keys in the invert index, as these are at worst the same as the tokens, which are as stated previously at worst the same as the characters, this operation is O(n) complex.

Overall, Indexing the files is O(n) complex where n is the number of characters in all the documents

### Searching

The searching operation has three distinct parts. Parsing the query, calculating the weight of each document, and sorting the result.

Parsing the query works the same as parsing the documents when indexing. As such it is O(n) complex where n is the number of characters in the query. Also remember that the worst case of parsing through the tokens is equivalent to parsing through the characters.

Calculating the weight of each document requires looping through (the name of) each document, then in that loop, looping through each token in the query.

Looping through each token in the query to determine a single documents weight is O(n) complex where n is the number of tokens in the search query. All that happens in each loop is looking up a hash map and doing a multiplication which both (pretty much) run in constant time.

Looping through each document is O(n) complex where n is the number of documents.

So, I will take the number of characters in the query as m, the number of documents as n, and say that weighing each document is O(n * m) complex. I don't know if this is the correct notation but my logic is that doing a nested loop that relies on n in the inner and outer loops is expressed as n^2 (which is n * n), so where the inner loop depends on m, it should be n * m.

Finally, for sorting the result I use pythons built in `sorted()` method. Internally, this uses Power Sort, which is O(n * Log(n)) complex where n is the number of documents. ^[1]^[2]^[3]

So, the complexity of weighing all documents depends on two variables, and it can't be guaranteed if the complexity of sorting or weighing is greater. Therefore, the complexity of searching is O(n * Log(n) + n * m) complex where n is the number of documents and m is the number of characters in the query.

1. https://stackoverflow.com/questions/14434490/what-is-the-complexity-of-the-sorted-function
2. https://www.wild-inter.net/publications/munro-wild-2018
3. https://www.wild-inter.net/publications/html/munro-wild-2018.pdf.html#[8,%22XYZ%22,107.717,382.536,null

### Brute Force Searching

Taking brute force searching to mean that you index all files each time you search, you would combine the complexities of the previous two operations. Indexing in O(n) where n is the number of characters in all the files. Searching is O(m * Log(m) + m * p) where m is the number of documents to search and p is the number of characters in the query. So, the brute force complexity is O(n + m * Log(m) + m * p).


 
# B: Choice of Data Structures  

Explain and justify your choice of data structures.  
  
## Your Answer  

### Indexes

My forward index is a dictionary of string, set pairs (`dict[str, set[str]]`). I chose to make it a dictionary so that I could find values in it quickly based on filenames. I used a set to hold the words of each file so that there would not be any duplicates.

My invert index is also a dictionary of string set pairs (`dict[str, set[str]]`) for the same reasons. I can quickly look up a word since its a dictionary. There are no duplicate documents under any word since its a set. I also used sets simple membership properties to find the intersection of many sets in searching.

My term frequency is a dictionary of dictionaries of string float pairs (`dict[str, dict[str, float]]`). I used this as I needed to track each word separately in each file. So, the first level is the file, and the second level is the word. This maintains that extra "namespace" I need. It is also quick to lookup because it is a dictionary.

My inverse document frequency is a dictionary (`dict[str, float]`) because  I needed to lookup by word quickly.

My doc rank is also a dictionary (`dict[str, float]`) because I needed to lookup by file quickly.

In intermediate steps, I parse each line into a list of strings. I used a list because the order mattered. When searching I store the results in a dictionary so there are not duplicate files before sorting them into a list when the order matters (to return in order of weight).
  
  
# C: Discuss extra features, if any: 

If you implemented any extra feature on top of the requirements noted in this handout, briefly describe them here.  
  
## Your Answer  

I added caching per folder to the program. Basically, if you have crawled a folder before, it will assume nothing has changed since you last crawled it and use the results saved in the `cache/<current folder>`. 

If at any point in loading the cache there is an error, it assumes that the whole cache for that folder is bad and re-crawls.

At the end of crawling a folder, it saves all the calculated indexes in a new subfolder of the cache directory.