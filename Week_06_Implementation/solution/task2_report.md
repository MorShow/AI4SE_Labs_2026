# Task 2: Repository chunking

I decided to use a whole method or test as a single unit of context for the model. But it seemed clear that this alone would not be enough to generate useful answers, so I tried to preserve as much metadata as possible: docstrings, decorators, comments, and the surrounding context, including class names and descriptions, constructors, the name and description of the file containing the method, and global variables in that file. I also added a `code` or `test` label to indicate what each chunk represents.

At first, keeping an empty method with just `pass` as a chunk did not seem like a good idea. Later, though, I realised that the model needs to know the signature of the method it is supposed to fill in, so I ended up keeping those empty methods too.

I think an ideal version would also include a very simple graph structure linking a method to the other methods or classes its implementation depends on. That would give the model more of the context it needs to fill in the missing implementation, but I decided not to add this.

For the implementation, I used Python's standard-library AST to identify complete methods and standalone functions, then extracted their original source, including decorators, docstrings, and comments. This showed me that chunking does not have to rely on LangChain parsers or simply splitting text line by line. 

(Actually, the task reminded me of the text-to-SQL work we did at my company, where we indexed SQL queries and retrieved the most similar ones to help generate a query for a user's input question :) )

Finally, I stored the chunks as a list of dictionaries in `chunks.json`.
