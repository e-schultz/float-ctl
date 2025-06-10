TITLE: Basic Markdown File with YAML Frontmatter for Dataview
DESCRIPTION: Example of a markdown file with YAML frontmatter containing metadata that Dataview can index, including author, publication date, and tags.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/index.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
---
author: "Edgar Allan Poe"
published: 1845
tags: poems
---

# The Raven

Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore—
```

----------------------------------------

TITLE: Basic TABLE Query with Multiple Fields
DESCRIPTION: A TABLE query showing multiple fields including due dates, file tags, and an average calculation of working hours.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_4

LANGUAGE: dataview
CODE:
```
```dataview
TABLE due, file.tags AS "tags", average(working-hours)
```
```

----------------------------------------

TITLE: Basic Dataview Query Language (DQL) Expression Syntax
DESCRIPTION: This snippet provides a high-level overview of all valid expressions in Dataview Query Language, including literals, lambdas, references, arithmetic operations, comparisons, and special operations.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md#2025-04-19_snippet_0

LANGUAGE: dataview
CODE:
```
# Literals
1                   (number)
true/false          (boolean)
"text"              (text)
date(2021-04-18)    (date)
dur(1 day)          (duration)
[[Link]]            (link)
[1, 2, 3]           (list)
{ a: 1, b: 2 }      (object)

# Lambdas
(x1, x2) => ...     (lambda)

# References
field               (directly refer to a field)
simple-field        (refer to fields with spaces/punctuation in them like "Simple Field!")
a.b                 (if a is an object, retrieve field named 'b')
a[expr]             (if a is an object or array, retrieve field with name specified by expression 'expr')
f(a, b, ...)        (call a function called `f` on arguments a, b, ...)

# Arithmetic
a + b               (addition)
a - b               (subtraction)
a * b               (multiplication)
a / b               (division)
a % b               (modulo / remainder of division)

# Comparison
a > b               (check if a is greater than b)
a < b               (check if a is less than b)
a = b               (check if a equals b)
a != b              (check if a does not equal b)
a <= b              (check if a is less than or equal to b)
a >= b              (check if a is greater than or equal to b)

# Strings

a + b               (string concatenation)
a * num             (repeat string <num> times)

# Special Operations
[[Link]].value      (fetch `value` from page `Link`)
```

----------------------------------------

TITLE: YAML Frontmatter Metadata Example
DESCRIPTION: Demonstrates how to add metadata fields using YAML frontmatter at the top of an Obsidian note, showing different data types including text, date, and nested objects.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/add-metadata.md#2025-04-19_snippet_0

LANGUAGE: yaml
CODE:
```
---
alias: "document"
last-reviewed: 2021-08-17
thoughts:
  rating: 8
  reviewable: false
---
```

----------------------------------------

TITLE: Evaluating Dataview Expressions with dv.tryEvaluate in JavaScript
DESCRIPTION: The dv.tryEvaluate function evaluates an arbitrary Dataview expression with an optional context object. It throws an Error on parse or evaluation failure.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md#2025-04-19_snippet_15

LANGUAGE: javascript
CODE:
```
dv.tryEvaluate("2 + 2") => 4
dv.tryEvaluate("x + 2", {x: 3}) => 5
dv.tryEvaluate("length(this.file.tasks)") => number of tasks in the current file
```

----------------------------------------

TITLE: Dataview TABLE Query with Multiple Fields
DESCRIPTION: TABLE query displaying multiple fields including author, published date, and file inlinks, filtered by a poems tag.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/index.md#2025-04-19_snippet_4

LANGUAGE: markdown
CODE:
```
```dataview
TABLE author, published, file.inlinks AS "Mentions"
FROM #poems
```
```

----------------------------------------

TITLE: Creating a DQL Query with Table Output in Obsidian
DESCRIPTION: A basic DQL query that creates a table showing ratings and summaries from notes tagged with #games, sorted by rating in descending order. This demonstrates the basic structure of a Dataview Query Language codeblock.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/dql-js-inline.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
```dataview
TABLE rating AS "Rating", summary AS "Summary" FROM #games
SORT rating DESC
```
```

----------------------------------------

TITLE: Querying Games with Metadata Using TABLE
DESCRIPTION: A SQL-like query that displays games from the 'games' folder as a table with time played, length, and rating columns, sorted by rating in descending order.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/examples.md#2025-04-19_snippet_0

LANGUAGE: sql
CODE:
```
TABLE
  time-played AS "Time Played",
  length AS "Length",
  rating AS "Rating"
FROM "games"
SORT rating DESC
```

----------------------------------------

TITLE: TABLE Query with Custom Column Headers in Dataview
DESCRIPTION: A TABLE query that uses the AS syntax to specify custom headers for columns displaying game metadata.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_11

LANGUAGE: dataview
CODE:
```
```dataview
TABLE started, file.folder AS Path, file.etags AS "File Tags"
FROM #games
```
```

----------------------------------------

TITLE: Querying Pages with DataviewJS
DESCRIPTION: Examples of using dv.pages() to query content in the vault with different filters.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md#2025-04-19_snippet_1

LANGUAGE: javascript
CODE:
```
dv.pages() => all pages in your vault
dv.pages("#books") => all pages with tag 'books'
dv.pages('"folder"') => all pages from folder "folder"
dv.pages("#yes or -#no") => all pages with tag #yes, or which DON'T have tag #no
dv.pages('"folder" or #tag') => all pages with tag #tag, or from folder "folder"
```

----------------------------------------

TITLE: Creating DataviewJS Block in Markdown
DESCRIPTION: Shows how to create a DataviewJS code block in Markdown to execute Dataview queries. The block provides access to the 'dv' variable which contains the full codeblock-relevant Dataview API.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/intro.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
```dataviewjs
dv.pages("#thing")...
```
```

----------------------------------------

TITLE: DataArray Interface Implementation in TypeScript
DESCRIPTION: Comprehensive TypeScript interface definition for DataArray, a proxied array implementation that provides enhanced data manipulation capabilities. Includes methods for filtering, mapping, sorting, grouping, and mathematical operations with full type definitions.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/data-array.md#2025-04-19_snippet_0

LANGUAGE: typescript
CODE:
```
/** A function which maps an array element to some value. */
export type ArrayFunc<T, O> = (elem: T, index: number, arr: T[]) => O;

/** A function which compares two types. */
export type ArrayComparator<T> = (a: T, b: T) => number;

/**
 * Proxied interface which allows manipulating array-based data. All functions on a data array produce a NEW array
 * (i.e., the arrays are immutable).
 */
export interface DataArray<T> {
    /** The total number of elements in the array. */
    length: number;

    /** Filter the data array down to just elements which match the given predicate. */
    where(predicate: ArrayFunc<T, boolean>): DataArray<T>;
    /** Alias for 'where' for people who want array semantics. */
    filter(predicate: ArrayFunc<T, boolean>): DataArray<T>;

    /** Map elements in the data array by applying a function to each. */
    map<U>(f: ArrayFunc<T, U>): DataArray<U>;
    /** Map elements in the data array by applying a function to each, then flatten the results to produce a new array. */
    flatMap<U>(f: ArrayFunc<T, U[]>): DataArray<U>;
    /** Mutably change each value in the array, returning the same array which you can further chain off of. */
    mutate(f: ArrayFunc<T, any>): DataArray<any>;

    /** Limit the total number of entries in the array to the given value. */
    limit(count: number): DataArray<T>;
    /**
     * Take a slice of the array. If `start` is undefined, it is assumed to be 0; if `end` is undefined, it is assumed
     * to be the end of the array.
     */
    slice(start?: number, end?: number): DataArray<T>;
    /** Concatenate the values in this data array with those of another iterable / data array / array. */
    concat(other: Iterable<T>): DataArray<T>;

    /** Return the first index of the given (optionally starting the search) */
    indexOf(element: T, fromIndex?: number): number;
    /** Return the first element that satisfies the given predicate. */
    find(pred: ArrayFunc<T, boolean>): T | undefined;
    /** Find the index of the first element that satisfies the given predicate. Returns -1 if nothing was found. */
    findIndex(pred: ArrayFunc<T, boolean>, fromIndex?: number): number;
    /** Returns true if the array contains the given element, and false otherwise. */
    includes(element: T): boolean;

    /**
     * Return a string obtained by converting each element in the array to a string, and joining it with the
     * given separator (which defaults to ', ').
     */
    join(sep?: string): string;

    /**
     * Return a sorted array sorted by the given key; an optional comparator can be provided, which will
     * be used to compare the keys in lieu of the default dataview comparator.
     */
    sort<U>(key: ArrayFunc<T, U>, direction?: "asc" | "desc", comparator?: ArrayComparator<U>): DataArray<T>;

    /**
     * Return an array where elements are grouped by the given key; the resulting array will have objects of the form
     * { key: <key value>, rows: DataArray }.
     */
    groupBy<U>(key: ArrayFunc<T, U>, comparator?: ArrayComparator<U>): DataArray<{ key: U; rows: DataArray<T> }>;

    /**
     * Return distinct entries. If a key is provided, then rows with distinct keys are returned.
     */
    distinct<U>(key?: ArrayFunc<T, U>, comparator?: ArrayComparator<U>): DataArray<T>;

    /** Return true if the predicate is true for all values. */
    every(f: ArrayFunc<T, boolean>): boolean;
    /** Return true if the predicate is true for at least one value. */
    some(f: ArrayFunc<T, boolean>): boolean;
    /** Return true if the predicate is FALSE for all values. */
    none(f: ArrayFunc<T, boolean>): boolean;

    /** Return the first element in the data array. Returns undefined if the array is empty. */
    first(): T;
    /** Return the last element in the data array. Returns undefined if the array is empty. */
    last(): T;

    /** Map every element in this data array to the given key, and then flatten it.*/
    to(key: string): DataArray<any>;
    /**
     * Recursively expand the given key, flattening a tree structure based on the key into a flat array. Useful for handling
     * hierarchical data like tasks with 'subtasks'.
     */
    expand(key: string): DataArray<any>;

    /** Run a lambda on each element in the array. */
    forEach(f: ArrayFunc<T, void>): void;

    /** Calculate the sum of the elements in the array. */
    sum(): number;

    /** Calculate the average of the elements in the array. */
    avg(): number;

    /** Calculate the minimum of the elements in the array. */
    min(): number;

    /** Calculate the maximum of the elements in the array. */
    max(): number;

    /** Convert this to a plain javascript array. */
    array(): T[];

    /** Allow iterating directly over the array. */
    [Symbol.iterator](): Iterator<T>;

    /** Map indexes to values. */
    [index: number]: any;
    /** Automatic flattening of fields. Equivalent to implicitly calling `array.to("field")` */
    [field: string]: any;
}
```

----------------------------------------

TITLE: Basic DQL Query Structure Pattern
DESCRIPTION: The fundamental pattern for structuring a Dataview Query Language (DQL) query, showing the required query type, optional FROM source, and optional data commands.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_0

LANGUAGE: dataview
CODE:
```
```dataview
<QUERY-TYPE> <fields>
FROM <source>
<DATA-COMMAND> <expression>
<DATA-COMMAND> <expression>
          ...
```
```

----------------------------------------

TITLE: Sort Function for Array Ordering
DESCRIPTION: The sort function sorts a list and returns a new list in sorted order.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_7

LANGUAGE: javascript
CODE:
```
sort(list(3, 2, 1)) = list(1, 2, 3)
sort(list("a", "b", "aa")) = list("a", "aa", "b")
```

----------------------------------------

TITLE: Displaying Comprehensive File Metadata with Dataview in Obsidian
DESCRIPTION: This Dataview query creates a detailed table of metadata for the current file, including name, folder, creation time, modification time, tags, and frontmatter. It demonstrates how to retrieve and display a wide range of file properties.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/example tables.md#2025-04-19_snippet_2

LANGUAGE: dataview
CODE:
```
TABLE file.name, file.folder, file.ctime, file.cday, file.mtime, file.mday, file.tags, file.frontmatter, file.name, file.folder, file.ctime, file.cday, file.mtime, file.mday, file.tags, file.frontmatter
WHERE file = this.file
```

----------------------------------------

TITLE: LIST Query with Complex Data Operations
DESCRIPTION: A LIST query that demonstrates array type checking, link filtering, array length sorting, flattening, and sorting by linked page properties.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_16

LANGUAGE: dataview
CODE:
```
```dataview
LIST rows.c
WHERE typeof(contacts) = "array" AND contains(contacts, [[Mr. L]])
SORT length(contacts)
FLATTEN contacts as c
SORT link(c).age ASC
```
```

----------------------------------------

TITLE: Type Checking in Dataview Comparisons
DESCRIPTION: An example showing how to safely compare dates by first checking the type to avoid unexpected results with null values.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md#2025-04-19_snippet_5

LANGUAGE: dataview
CODE:
```
```dataview
TASK
WHERE typeof(due) = "date" AND due <= date(today)
```
```

----------------------------------------

TITLE: Creating DataviewJS Codeblock
DESCRIPTION: Shows how to create a basic DataviewJS codeblock in Obsidian markdown.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
```dataviewjs
dv.table([], ...)
```
```

----------------------------------------

TITLE: Using DataviewJS for Complex Data Visualization
DESCRIPTION: A JavaScript-based Dataview query that filters pages by tags and ratings, then groups and displays them by genre. Demonstrates using the dv object to access the Dataview API in a JavaScript context.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/dql-js-inline.md#2025-04-19_snippet_5

LANGUAGE: java
CODE:
```
```dataviewjs
let pages = dv.pages("#books and -#books/finished").where(b => b.rating >= 7);
for (let group of pages.groupBy(b => b.genre)) {
   dv.header(3, group.key);
   dv.list(group.rows.file.name);
}
```
```

----------------------------------------

TITLE: Example Obsidian Page with Metadata in Markdown
DESCRIPTION: A sample Markdown page demonstrating the use of frontmatter, inline fields, and tags to add metadata to an Obsidian note. This example includes various types of user-defined metadata for a movie review.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-pages.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
---
genre: "action"
reviewed: false
---
# Movie X
#movies

**Thoughts**:: It was decent.
**Rating**:: 6

[mood:: okay] | [length:: 2 hours]
```

----------------------------------------

TITLE: Accessing File Properties with Inline DQL
DESCRIPTION: Examples of accessing various file properties and metadata from the current page and other pages using inline DQL queries. Shows how to reference both the current page and linked pages.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/dql-js-inline.md#2025-04-19_snippet_3

LANGUAGE: markdown
CODE:
```
`= this.file.name`
`= this.file.mtime`
`= this.someMetadataField`
`= [[secondPage]].file.name`
`= [[secondPage]].file.mtime`
`= [[secondPage]].someMetadataField`
```

----------------------------------------

TITLE: Split Function for String Division
DESCRIPTION: The split function divides a string into an array of substrings based on a delimiter. It can limit the number of splits and handle regex capture groups in the delimiter.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_27

LANGUAGE: javascript
CODE:
```
split("hello world", " ") = list("hello", "world")
split("hello  world", "\s") = list("hello", "world")
split("hello there world", " ", 2) = list("hello", "there")
split("hello there world", "(t?here)") = list("hello ", "there", " world")
split("hello there world", "( )(x)?") = list("hello", " ", "", "there", " ", "", "world")
```

----------------------------------------

TITLE: TABLE Query with Calculations and Custom Headers in Dataview
DESCRIPTION: A TABLE query that displays calculated values (duration played) and custom headers for game-related metadata.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_12

LANGUAGE: dataview
CODE:
```
```dataview
TABLE
default(finished, date(today)) - started AS "Played for",
file.folder AS Path,
file.etags AS "File Tags"
FROM #games
```
```

----------------------------------------

TITLE: Advanced Dataview TABLE Query with Field Operations
DESCRIPTION: TABLE query with field operations using functions to calculate age of poems and count mentions, demonstrating Dataview's ability to process data dynamically.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/index.md#2025-04-19_snippet_5

LANGUAGE: markdown
CODE:
```
```dataview
TABLE author, date(now).year - published AS "Age in Yrs", length(file.inlinks) AS "Counts of Mentions"
FROM #poems
```
```

----------------------------------------

TITLE: Creating Task List with Metadata in Obsidian Dataview (Markdown)
DESCRIPTION: This snippet demonstrates how to create a task list with various metadata fields using Obsidian Dataview syntax. It includes completed and uncompleted tasks, tags, dates, custom fields, and task hierarchies.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/tasks/checklist.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
- [x] Normal task, tags inherited from page [completion:: 2021-10-23]
* [ ] Task with a #tag, adds to inherited page tags
	* [ ] Task that inherits tag from above and page tags
* [x] Completed task ✅ 2021-08-06 📅 2021-08-07
* [x] Completed task [completion::2021-08-06] [due::2021-08-07]
* [ ] task with [annotation::arbitrary] [completion:: 2021-10-23]
* [ ] Scheduled task 📅  2021-08-07
* [ ] Task that overrides creation date of file ➕ 2021-08-06
* [ ] Repeating task 🔁Mondays
* [ ] #tell @person some important thing [p::1]
* [x] a less important thing [p::2]
* [ ] another important thing [p::1]

#page-tag

## Section
- [ ] additional task with a block id ^block-id
- [ ] additional task, should link to header
```

----------------------------------------

TITLE: Sorting Files by Last Modified Time
DESCRIPTION: A query that displays files from the 'books' folder as a table with their last modified time, sorted from most recent to oldest modification.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/examples.md#2025-04-19_snippet_3

LANGUAGE: sql
CODE:
```
TABLE file.mtime AS "Last Modified"
FROM "books"
SORT file.mtime DESC
```

----------------------------------------

TITLE: Creating Custom Column Names in Dataview Tables
DESCRIPTION: Shows how to create tables with custom column names by using the 'AS' keyword to rename fields in the output table.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_2

LANGUAGE: dataview
CODE:
```
TABLE file.day AS "Day", file.mtime AS "Last Modified" FROM "folder"
```

----------------------------------------

TITLE: Grouping Books by Genre and Displaying in Sorted Tables using Dataview
DESCRIPTION: This snippet demonstrates how to use Dataview's API to group books by genre and create separate tables for each genre with books sorted by rating in descending order. It leverages the groupBy method and iterates through the resulting groups to create headers and tables.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-examples.md#2025-04-19_snippet_0

LANGUAGE: javascript
CODE:
```
for (let group of dv.pages("#book").groupBy(p => p.genre)) {
	dv.header(3, group.key);
	dv.table(["Name", "Time Read", "Rating"],
		group.rows
			.sort(k => k.rating, 'desc')
			.map(k => [k.file.link, k["time-read"], k.rating]))
}
```

----------------------------------------

TITLE: DataviewJS Table Creation
DESCRIPTION: Example of creating a complex table with nested bullet points
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md#2025-04-19_snippet_4

LANGUAGE: javascript
CODE:
```
dv.table(
	["Col1", "Col2", "Col3"],
		[
			["Row1", "Dummy", "Dummy"],
			["Row2", 
				["Bullet1",
				 "Bullet2",
				 "Bullet3"],
			 "Dummy"],
			["Row3", "Dummy", "Dummy"]
		]
	);
```

----------------------------------------

TITLE: TABLE Query with FLATTEN for List Processing
DESCRIPTION: A TABLE query that flattens file lists into separate rows, filtering by author name and displaying list text with a custom column header.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_15

LANGUAGE: dataview
CODE:
```
```dataview
TABLE L.text AS "My lists"
FROM "dailys"
FLATTEN file.lists AS L
WHERE contains(L.author, "Surname")
```
```

----------------------------------------

TITLE: Querying Tasks Completed on a Specific Date with Dataview
DESCRIPTION: This Dataview query returns all tasks from the 'tasks' folder that were completed on August 6, 2021. It uses the 'completion' field to filter tasks by their completion date.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/tasks/Tasks Completed on specific Date.md#2025-04-19_snippet_0

LANGUAGE: dataview
CODE:
```
task from "tasks" where
completion = date(2021-08-06)
```

----------------------------------------

TITLE: Grouping Query Results in Dataview
DESCRIPTION: Shows how to organize results into groups using the GROUP BY clause, which creates hierarchical groupings based on specified fields.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_7

LANGUAGE: dataview
CODE:
```
TABLE file.name FROM "folder" GROUP BY file.folder
```

----------------------------------------

TITLE: Embedding Date Calculations with Inline DQL
DESCRIPTION: A practical example showing how to embed date calculations within text using inline DQL queries. This demonstrates displaying the current date and calculating time until a deadline.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/dql-js-inline.md#2025-04-19_snippet_2

LANGUAGE: markdown
CODE:
```
Today is `= date(today)` - `= [[exams]].deadline - date(today)` until exams!
```

----------------------------------------

TITLE: Filtering Games by Tags Using LIST
DESCRIPTION: A query that lists games belonging to either the 'mobas' or 'crpg' game tags, demonstrating the use of the OR operator for filtering by multiple tags.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/examples.md#2025-04-19_snippet_1

LANGUAGE: sql
CODE:
```
LIST FROM #games/mobas OR #games/crpg
```

----------------------------------------

TITLE: YAML Frontmatter Example with Nested Objects
DESCRIPTION: A YAML frontmatter example demonstrating how nested object structures are defined in Obsidian, which can later be accessed using object notation in Dataview queries.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md#2025-04-19_snippet_6

LANGUAGE: yaml
CODE:
```
---
aliases:
  - "ABC"
current_episode: "S01E03"
episode_metadata:
  previous: "S01E02"
  next: "S01E04"
---
```

----------------------------------------

TITLE: Grouped TASK Query by File in Dataview
DESCRIPTION: A TASK query that groups incomplete tasks by their source file, showing how to organize tasks based on where they appear in the vault. The numbers in parentheses indicate task counts per group.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_17

LANGUAGE: dataview
CODE:
```
```dataview
TASK
WHERE !completed
GROUP BY file.link
```
```

----------------------------------------

TITLE: Filter Function for Array Filtering
DESCRIPTION: The filter function filters elements in an array according to a predicate function, returning a new list of the elements that matched the condition.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_16

LANGUAGE: javascript
CODE:
```
filter([1, 2, 3], (x) => x >= 2) = [2, 3]
filter(["yes", "no", "yas"], (x) => startswith(x, "y")) = ["yes", "yas"]
```

----------------------------------------

TITLE: Querying Games with Dataview Markdown
DESCRIPTION: Example of using Dataview query language to create a table of games with metadata, sorted by rating.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/README.md#2025-04-19_snippet_0

LANGUAGE: markdown
CODE:
```
```dataview
table time-played, length, rating
from "games"
sort rating desc
```
```

----------------------------------------

TITLE: TABLE Query with Folder Filtering and Multiple Fields
DESCRIPTION: A TABLE query for pages in a specific protocol folder, displaying creation time, appointment details, and follow-ups, filtered and sorted.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_14

LANGUAGE: dataview
CODE:
```
```dataview
TABLE file.ctime, appointment.type, appointment.time, follow-ups
FROM "30 Protocols/32 Management"
WHERE follow-ups
SORT appointment.time
```
```

----------------------------------------

TITLE: Exact Contains Function for Strings, Lists, and Objects
DESCRIPTION: The econtains function checks if an exact match is found in a string, list, or object. It's case sensitive and behaves differently depending on the input type.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_4

LANGUAGE: javascript
CODE:
```
econtains("Hello", "Lo") = false
econtains("Hello", "lo") = true
```

LANGUAGE: javascript
CODE:
```
econtains(["These", "are", "words"], "word") = false
econtains(["These", "are", "words"], "words") = true
```

LANGUAGE: javascript
CODE:
```
econtains({key:"value", pairs:"here"}, "here") = false
econtains({key:"value", pairs:"here"}, "key") = true
econtains({key:"value", recur:{recurkey: "val"}}, "value") = false
econtains({key:"value", recur:{recurkey: "val"}}, "Recur") = false
econtains({key:"value", recur:{recurkey: "val"}}, "recurkey") = false
```

----------------------------------------

TITLE: Querying Uncompleted Tasks with Dataview in Obsidian
DESCRIPTION: This Dataview query displays all uncompleted tasks from all folders except the 'recipes' folder. It uses the 'task' keyword to indicate it should retrieve task items and filters them using the '!completed' condition to show only those that remain uncompleted.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/tasks/Uncompleted Tasks.md#2025-04-19_snippet_0

LANGUAGE: dataview
CODE:
```
task from -"recipes"
WHERE !completed
```

----------------------------------------

TITLE: Extracting Tasks from Projects
DESCRIPTION: A query that extracts all tasks from files in the 'dataview' folder, showing both completed and uncompleted tasks with their hierarchical structure.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/examples.md#2025-04-19_snippet_2

LANGUAGE: sql
CODE:
```
TASK FROM "dataview"
```

----------------------------------------

TITLE: Using Lambdas with Map Function in Dataview
DESCRIPTION: An example of using lambdas with the map function in a CALENDAR query to check if all tasks are completed and flatten the results.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md#2025-04-19_snippet_9

LANGUAGE: dataview
CODE:
```
```dataview
CALENDAR file.day
FLATTEN all(map(file.tasks, (x) => x.completed)) AS "allCompleted"
WHERE !allCompleted
```
```

----------------------------------------

TITLE: Unique Function for Removing Duplicates
DESCRIPTION: The unique function creates a new array with only unique values, removing any duplicates from the original array.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_17

LANGUAGE: javascript
CODE:
```
unique([1, 3, 7, 3, 1]) => [1, 3, 7]
```

----------------------------------------

TITLE: Displaying Query Results as Calendar in Dataview
DESCRIPTION: Demonstrates how to create a calendar view of query results using the CALENDAR command and a date field.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_6

LANGUAGE: dataview
CODE:
```
CALENDAR file.day FROM "folder"
```

----------------------------------------

TITLE: Basic TASK Query in Dataview
DESCRIPTION: A simple TASK query that displays all tasks in the vault as an interactive list. Users can check/uncheck tasks directly in the results, which will update the original files.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_15

LANGUAGE: dataview
CODE:
```
```dataview
TASK
```
```

----------------------------------------

TITLE: LIST Query with Computed Values in Dataview
DESCRIPTION: A LIST query that displays computed values combining multiple fields for each result from a specific folder.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_3

LANGUAGE: dataview
CODE:
```
```dataview
LIST "File Path: " + file.folder + " _(created: " + file.cday + ")_"
FROM "Games"
```
```

----------------------------------------

TITLE: Filtered TASK Query with Tag Condition in Dataview
DESCRIPTION: A TASK query that filters for incomplete tasks containing a specific tag (#shopping). This demonstrates how to combine the WHERE clause with task properties to create targeted task lists.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md#2025-04-19_snippet_16

LANGUAGE: dataview
CODE:
```
```dataview
TASK
WHERE !completed AND contains(tags, "#shopping")
```
```

----------------------------------------

TITLE: Limiting Query Results in Dataview
DESCRIPTION: Shows how to limit the number of returned results using the LIMIT clause, which is useful for displaying only the most relevant items.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_9

LANGUAGE: dataview
CODE:
```
LIST FROM "folder" LIMIT 10
```

----------------------------------------

TITLE: Displaying Query Results as Tasks in Dataview
DESCRIPTION: Shows how to display query results in a task view format using the TASK command, which renders results with checkbox indicators.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_5

LANGUAGE: dataview
CODE:
```
TASK FROM #project
```

----------------------------------------

TITLE: Finding All Directly and Indirectly Linked Pages with Depth-First Search
DESCRIPTION: This code implements a depth-first search algorithm to find all pages that are linked (directly or indirectly) to a specified page. It uses a stack to track pages to process and a Set to prevent duplicate processing, collecting both inlinks and outlinks for each page.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-examples.md#2025-04-19_snippet_1

LANGUAGE: javascript
CODE:
```
let page = dv.current().file.path;
let pages = new Set();

let stack = [page];
while (stack.length > 0) {
	let elem = stack.pop();
	let meta = dv.page(elem);
	if (!meta) continue;

	for (let inlink of meta.file.inlinks.concat(meta.file.outlinks).array()) {
		console.log(inlink);
		if (pages.has(inlink.path)) continue;
		pages.add(inlink.path);
		stack.push(inlink.path);
	}
}

// Data is now the file metadata for every page that directly OR indirectly links to the current page.
let data = dv.array(Array.from(pages)).map(p => dv.page(p));
```

----------------------------------------

TITLE: Querying Incomplete Tasks in Dataview
DESCRIPTION: A Dataview TASK query that filters for tasks that are not fully completed, accessing the implicit 'fullyCompleted' field directly in TASK queries.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-tasks.md#2025-04-19_snippet_4

LANGUAGE: markdown
CODE:
```
```dataview
TASK
WHERE !fullyCompleted
```
```

----------------------------------------

TITLE: LIST Query with Tag Source Filtering
DESCRIPTION: A LIST query that filters pages to only include those with either #status/open or #status/wip tags.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_6

LANGUAGE: dataview
CODE:
```
```dataview
LIST
FROM #status/open OR #status/wip
```
```

----------------------------------------

TITLE: Executing Dataview Queries with dv.query in JavaScript
DESCRIPTION: The asynchronous dv.query function executes a Dataview query and returns the results as a structured object. The return type varies by query type but always includes a 'type' field and success status.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md#2025-04-19_snippet_13

LANGUAGE: javascript
CODE:
```
await dv.query("LIST FROM #tag") =>
    { successful: true, value: { type: "list", values: [value1, value2, ...] } }

await dv.query(`TABLE WITHOUT ID file.name, value FROM "path"`) =>
    { successful: true, value: { type: "table", headers: ["file.name", "value"], values: [["A", 1], ["B", 2]] } }

await dv.query("TASK WHERE due") =>
    { successful: true, value: { type: "task", values: [task1, task2, ...] } }
```

----------------------------------------

TITLE: Filtering Recent Files with WHERE Command
DESCRIPTION: Query to find files modified within the last 24 hours using the WHERE command
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/data-commands.md#2025-04-19_snippet_0

LANGUAGE: sql
CODE:
```
LIST WHERE file.mtime >= date(today) - dur(1 day)
```

----------------------------------------

TITLE: TASK Query with Multiple Data Commands
DESCRIPTION: A complex TASK query filtering incomplete tasks, sorting by creation date, limiting results, grouping by file, and sorting groups by file creation time.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md#2025-04-19_snippet_10

LANGUAGE: dataview
CODE:
```
```dataview
TASK
WHERE !completed
SORT created ASC
LIMIT 10
GROUP BY file.link
SORT rows.file.ctime ASC
```
```

----------------------------------------

TITLE: Displaying Query Results as Tables in Dataview
DESCRIPTION: Demonstrates how to format query results as a table using the TABLE command, showing how to specify columns to display specific file metadata or properties.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_1

LANGUAGE: dataview
CODE:
```
TABLE file.day, file.mtime FROM "folder"
```

----------------------------------------

TITLE: Regextest Function for Pattern Testing
DESCRIPTION: The regextest function checks if a regex pattern can be found in a string using the JavaScript regex engine. It returns true if any part of the string matches the pattern.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md#2025-04-19_snippet_21

LANGUAGE: javascript
CODE:
```
regextest("\w+", "hello") = true
regextest(".", "a") = true
regextest("yes|no", "maybe") = false
regextest("what", "what's up dog?") = true
```

----------------------------------------

TITLE: Querying by Links in Dataview
DESCRIPTION: Two Dataview queries demonstrating how to use link-based sources. The first shows how to query files linking to the current file, and the second shows how to query outgoing links from a specific file.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/sources.md#2025-04-19_snippet_3

LANGUAGE: markdown
CODE:
```
```dataview
LIST
FROM [[]]
```

```dataview
LIST
FROM outgoing([[Dashboard]])
```
```

----------------------------------------

TITLE: Inline DQL for Saving Calculations in Metadata Fields
DESCRIPTION: Shows how to use Inline DQL to calculate and store values in metadata fields, useful for reusing calculations in queries.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/faq.md#2025-04-19_snippet_2

LANGUAGE: markdown
CODE:
```
start:: 07h00m
end:: 18h00m
pause:: 01h30m
duration:: `= this.end - this.start - this.pause`
```

----------------------------------------

TITLE: Sorting Query Results in Dataview
DESCRIPTION: Demonstrates how to sort query results using the SORT clause, with options for ascending or descending order.
SOURCE: https://github.com/blacksmithgu/obsidian-dataview/blob/master/test-vault/blog/2021-08-08-a-post.md#2025-04-19_snippet_8

LANGUAGE: dataview
CODE:
```
LIST FROM "folder" SORT file.name ASC
```