TITLE: Aggregating List Values with `reduce` and `math sum` (NuShell)
DESCRIPTION: Shows different ways to aggregate values in a list. It uses `reduce` to calculate the sum and product, demonstrating the `--fold` flag for an initial accumulator value. It also shows using `math sum` as a simpler alternative for summation and `enumerate` with `reduce` to access both index and item.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/working_with_lists.md#_snippet_12

LANGUAGE: NuShell
CODE:
```
let scores = [3 8 4]
$"total = ($scores | reduce { |elt, acc| $acc + $elt })" # total = 15

$"total = ($scores | math sum)" # easier approach, same result

$"product = ($scores | reduce --fold 1 { |elt, acc| $acc * $elt })" # product = 96

$scores | enumerate | reduce --fold 0 { |elt, acc| $acc + $elt.index * $elt.item } # 0*3 + 1*8 + 2*4 = 16
```

----------------------------------------

TITLE: Illustrating Nushell Type Signatures
DESCRIPTION: This snippet demonstrates various places where type signatures can be applied in Nushell, including variable declarations, parameters in custom commands and closures, and input/return type declarations for custom commands.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/lang-guide/chapters/types/type_signatures.md#_snippet_0

LANGUAGE: nu
CODE:
```
# Variable declaration
let x: int = 9

# Parameter declaration in custom commands
def my-command [x: int, y: string] { }

# Parameter declaration in closures
do {|nums : list<int>| $nums | describe} [ 1 2 3 ]

# Input and Return type declaration on a custom command
def my-filter []: nothing -> list { }

# Multiple Input/Return type signatures on a custom command
def my-filter []: [
  nothing -> list
  range -> list
] { }
```

----------------------------------------

TITLE: Search for all files excluding target and .git directories in Nushell
DESCRIPTION: Searches for all files and directories recursively (`**/*`) while excluding paths containing `target` or `.git` directories, and also excluding the root directory itself (`*/`).
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/glob.md#_snippet_10

LANGUAGE: nu
CODE:
```
> glob **/* --exclude [**/target/** **/.git/** */]
```

----------------------------------------

TITLE: Filtering ls output by modification date in Nushell
DESCRIPTION: This example filters the output of the `ls` command to list only entries that were modified within the last two weeks.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/where.md#_snippet_5

LANGUAGE: nu
CODE:
```
ls | where modified >= (date now) - 2wk
```

----------------------------------------

TITLE: Define and Run a Simple Command (Nu)
DESCRIPTION: This example demonstrates how to define a basic custom command named `say-hi` that simply prints 'hi' and then immediately calls it.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/def.md#_snippet_0

LANGUAGE: Nu
CODE:
```
def say-hi [] { echo 'hi' }; say-hi
```

----------------------------------------

TITLE: Nushell Script with Shebang and Stdin Flag
DESCRIPTION: An example script using a shebang (`#!/usr/bin/env -S nu --stdin`) to tell the OS to execute it with `nu --stdin`. This allows the script's `main` function to access standard input via the `$in` variable.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/scripts.md#_snippet_21

LANGUAGE: Nushell
CODE:
```
#!/usr/bin/env -S nu --stdin
def main [] {
  echo $"stdin: ($in)"
}
```

----------------------------------------

TITLE: List old directories by name in home directory (Nushell)
DESCRIPTION: This command lists all items (including hidden ones) in the home directory, shows only their names, filters for directories, and further filters for those modified more than 7 days ago.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/ls.md#_snippet_6

LANGUAGE: nu
CODE:
```
> ls -as ~ | where type == dir and modified < ((date now) - 7day)
```

----------------------------------------

TITLE: Creating a Simple Nushell Command
DESCRIPTION: Defines a basic custom command named `greet` that accepts one positional argument, `name`. The command block uses string interpolation to construct a greeting message.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/custom_commands.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
def greet [name] {
  $"Hello, ($name)!"
}
```

----------------------------------------

TITLE: Defining a simple Nushell function for export
DESCRIPTION: Defines a function `increment` that takes an integer input (`$in`) and returns the input plus one. This function is marked with `export` to make it available when the module is imported.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/modules/creating_modules.md#_snippet_0

LANGUAGE: nu
CODE:
```
export def increment []: int -> int  {
    $in + 1
}
```

----------------------------------------

TITLE: Fetching Data with HTTP GET in Nushell
DESCRIPTION: This snippet demonstrates how to use the `http get` command in Nushell to fetch data from a web API and then access a specific field from the returned JSON object.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/cookbook/README.md#_snippet_0

LANGUAGE: nu
CODE:
```
(http get https://api.chucknorris.io/jokes/random).value
```

----------------------------------------

TITLE: Creating Directory Bash and Nu
DESCRIPTION: Creates a new directory at the specified path.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/coming_from_bash.md#_snippet_11

LANGUAGE: Bash
CODE:
```
mkdir <path>
```

LANGUAGE: Nu
CODE:
```
mkdir <path>
```

----------------------------------------

TITLE: Copy Files (CMD vs Nu)
DESCRIPTION: Commands to copy files from a source location to a destination.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/coming_from_cmd.md#_snippet_7

LANGUAGE: cmd
CODE:
```
COPY <source> <destination>
```

LANGUAGE: nushell
CODE:
```
cp <source> <destination>
```

----------------------------------------

TITLE: Crawling Paginated API (Loop) in Nushell
DESCRIPTION: An example of how to fetch data from a paginated API endpoint (like GitHub issues) using a traditional loop in Nushell. It iteratively makes HTTP GET requests, appends responses to a list, and breaks the loop when a page contains fewer items than the page size.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2023-10-17-nushell_0_86.md#_snippet_9

LANGUAGE: nushell
CODE:
```
mut pages = []
for page in 1.. {
  let resp = http get (
    {
      scheme: https,
      host: "api.github.com",
      path: "/repos/nushell/nushell/issues",
      params: { page: $page, per_page: $PAGE_SIZE }
    } | url join)

  $pages = ($pages | append $resp)

  if ($resp | length) < $PAGE_SIZE {
    break
  }
}
$pages
```

----------------------------------------

TITLE: Install Nushell via APT on Debian/Ubuntu
DESCRIPTION: This script adds the official Nushell APT repository, updates the package list, and installs the Nushell package on Debian or Ubuntu systems. It requires `curl` and `sudo`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/installation.md#_snippet_0

LANGUAGE: sh
CODE:
```
curl -fsSL https://apt.fury.io/nushell/gpg.key | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/fury-nushell.gpg
echo "deb https://apt.fury.io/nushell/ /" | sudo tee /etc/apt/sources.list.d/fury.list
sudo apt update
sudo apt install nushell
```

----------------------------------------

TITLE: Changing to Parent Directory using cd (Nushell)
DESCRIPTION: Uses the `..` shortcut with the `cd` command to navigate up one level to the parent directory.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/moving_around.md#_snippet_13

LANGUAGE: Nushell
CODE:
```
cd ..
```

----------------------------------------

TITLE: Change Directory (CMD vs Nu)
DESCRIPTION: Commands to change the current working directory to a specified path.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/coming_from_cmd.md#_snippet_3

LANGUAGE: cmd
CODE:
```
CD <directory>
```

LANGUAGE: nushell
CODE:
```
cd <directory>
```

----------------------------------------

TITLE: Sorting Git Log by Date in Reverse (Nushell)
DESCRIPTION: This snippet executes a `git log` command to get commit details, pipes the output line by line, splits each line into columns based on a delimiter, converts the date column to a datetime type, sorts the table by date, and finally reverses the order to display the newest commits first. It requires Git installed and being run inside a Git repository.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/cookbook/parsing_git_log.md#_snippet_9

LANGUAGE: Nushell
CODE:
```
git log --pretty=%h»¦«%s»¦«%aN»¦«%aE»¦«%aD -n 25 | lines | split column "»¦«" commit subject name email date | upsert date {|d| $d.date | into datetime} | sort-by date | reverse
```

----------------------------------------

TITLE: Creating Table with Table-literal Syntax (Nushell)
DESCRIPTION: Demonstrates creating a table using the table-literal syntax. This syntax requires specifying column headers followed by a semicolon, and then listing rows as separate lists.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/lang-guide/chapters/types/basic_types/table.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
[[column1, column2]; [Value1, Value2] [Value3, Value4]]
# => ╭───┬─────────┬─────────╮
# => │ # │ column1 │ column2 │
# => ├───┼─────────┼─────────┤
# => │ 0 │ Value1  │ Value2  │
# => │ 1 │ Value3  │ Value4  │
# => ╰───┴─────────┴─────────╯
```

----------------------------------------

TITLE: Delete Merged Git Branches (Nu)
DESCRIPTION: This Nushell command deletes local Git branches that have been merged into either 'master' or 'main'. It first lists merged branches, filters out the current branch if it's master or main, and then iteratively deletes each remaining branch using `git branch -D`. Be aware this is a hard deletion.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/cookbook/git.md#_snippet_0

LANGUAGE: nu
CODE:
```
git branch --merged | lines | where ($it != "* master" and $it != "* main") | each {|br| git branch -D ($br | str trim) } | str trim
```

----------------------------------------

TITLE: String to Integer Conversion Change
DESCRIPTION: Converting a string to an integer changed from using the `str to-int` command to using the `into int` command.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2022-03-22-nushell_0_60.md#_snippet_49

LANGUAGE: Nushell
CODE:
```
str to-int
```

LANGUAGE: Nushell
CODE:
```
into int
```

----------------------------------------

TITLE: Updating a Record Field in Nushell
DESCRIPTION: Demonstrates updating the value of a field within a record using the `update` command. Note that variables in Nushell are immutable, so the command outputs the modified record without changing the original variable.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/working_with_records.md#_snippet_0

LANGUAGE: nu
CODE:
```
let my_record = {
 name: "Sam"
 age: 30
 }
$my_record | update age { $in + 1 }
```

----------------------------------------

TITLE: Listing Directory Contents (Nushell)
DESCRIPTION: Uses the `ls` command to list the contents of the current directory. Nushell returns the output as a structured table.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/moving_around.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
ls
```

----------------------------------------

TITLE: Using the 'like' String Operator in Nushell
DESCRIPTION: Demonstrates the new `like` operator for pattern matching strings. It checks if the string on the left matches the glob pattern on the right.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-11-12-nushell_0_100_0.md#_snippet_2

LANGUAGE: Nushell
CODE:
```
"hello world" like "hello*"
```

----------------------------------------

TITLE: Chaining Nushell `if-else if-else` Statements
DESCRIPTION: This snippet demonstrates chaining multiple conditional checks using `if-else if-else` in Nushell. Conditions are evaluated sequentially, and the first true condition's block is executed. If all conditions are false, the final `else` block runs.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/if.md#_snippet_2

LANGUAGE: Nushell
CODE:
```
if 5 < 3 { 'yes!' } else if 4 < 5 { 'no!' } else { 'okay!' }
```

----------------------------------------

TITLE: Loop with condition and break in Nushell
DESCRIPTION: This example demonstrates using the `loop` command in Nushell to repeatedly execute a block of code. It initializes a mutable variable `x`, enters a loop, checks if `x` is greater than 10, breaks the loop if the condition is true, and increments `x` otherwise. Finally, it outputs the final value of `x`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/loop.md#_snippet_0

LANGUAGE: nu
CODE:
```
mut x = 0; loop { if $x > 10 { break }; $x = $x + 1 }; $x
```

----------------------------------------

TITLE: Creating Directory with Multi-stage Pipeline using $in in NuShell
DESCRIPTION: This multi-stage pipeline demonstrates creating a directory with tomorrow's date in its name, leveraging the `$in` variable. Each step processes the output of the previous one: getting today's date, adding one day, formatting, constructing the name, and finally creating the directory.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/pipelines.md#_snippet_5

LANGUAGE: nu
CODE:
```
date now                    # 1: today
| $in + 1day                # 2: tomorrow
| format date '%F'          # 3: Format as YYYY-MM-DD
| $'($in) Report'           # 4: Format the directory name
| mkdir $in                 # 5: Create the directory
```

----------------------------------------

TITLE: Catching Errors and Accessing Error Record in Nushell
DESCRIPTION: Illustrates the use of the `try...catch` block to handle errors. The `catch` block now receives an error record (`$err`) providing structured information about the error.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-11-12-nushell_0_100_0.md#_snippet_9

LANGUAGE: Nushell
CODE:
```
try { error "oh no!" } catch { |err| $err }
```

----------------------------------------

TITLE: Define Custom Command with cd in Nushell
DESCRIPTION: Illustrates how to define a custom command `gohome` that changes the directory to home. Note that `def --env` is required for the directory change to persist in the current environment.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/cd.md#_snippet_2

LANGUAGE: nu
CODE:
```
def --env gohome [] { cd ~ }
```

----------------------------------------

TITLE: Attaching Custom Completions to Nushell `extern` Commands
DESCRIPTION: This example demonstrates how to apply custom completions to known external (`extern`) commands in Nushell. It shows `git push` being augmented with completers for `remote` and `refspec` arguments, using `string@"nu-complete git remotes"` and `string@"nu-complete git branches"` respectively. This allows Nushell to provide intelligent suggestions for external command arguments.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/custom_completions.md#_snippet_5

LANGUAGE: nu
CODE:
```
export extern "git push" [
    remote?: string@"nu-complete git remotes",  # the name of the remote
    refspec?: string@"nu-complete git branches" # the branch / refspec
    ...
]
```

----------------------------------------

TITLE: Interpolating Arguments for External Commands in Nushell
DESCRIPTION: This snippet illustrates different methods for interpolating values into arguments for external commands using Nushell. It shows how bare word interpolation with `=(...)` or string interpolation with `$("(...)")` evaluates expressions, while literal strings are passed as-is. It also demonstrates interpolation in comma-separated bare words.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-06-25-nushell_0_95_0.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
^echo --foo=(2 + 2) # prints --foo=4
^echo -foo=$"(2 + 2)" # prints -foo=4
^echo foo="(2 + 2)" # prints (no interpolation!) foo=(2 + 2)
^echo foo,(2 + 2),bar # prints foo,4,bar
```

----------------------------------------

TITLE: String Concatenation (Replacing `build-string`)
DESCRIPTION: Provides examples of the recommended ways to concatenate strings after the removal of the `build-string` command, using the `+` operator, string interpolation, or `str join`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2022-11-29-nushell-0.72.md#_snippet_17

LANGUAGE: Nushell
CODE:
```
"hello" + " " + "world"
$"hello world"
["hello", "world"] | str join " "
```

----------------------------------------

TITLE: Sorting Data by Named Column in Nushell
DESCRIPTION: Opens a text file, processes it by splitting lines into named columns ('first_name', 'last_name', 'job') and trimming whitespace, and then sorts the entire table based on the values in the 'first_name' column.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/loading_data.md#_snippet_10

LANGUAGE: Nushell
CODE:
```
open people.txt | lines | split column "|" first_name last_name job | str trim | sort-by first_name
```

----------------------------------------

TITLE: Iterating Over Nushell List with each
DESCRIPTION: Demonstrates using the `each` command with a block to iterate over each item in a list and perform an action.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/working_with_lists.md#_snippet_8

LANGUAGE: nu
CODE:
```
let names = [Mark Tami Amanda Jeremy]
$names | each { |elt| $"Hello, ($elt)!" }
# Outputs "Hello, Mark!" and three more similar lines.
```

----------------------------------------

TITLE: Shorthand Filtering with `$it` in Nushell
DESCRIPTION: This Nushell snippet presents another shorthand for filtering data with the `where` command. It uses the `$it` variable to refer to the current row's properties, allowing direct comparison of `$it.size` to `10kb` without an explicit block or math mode.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2020-04-21-nushell_0_13_0.md#_snippet_14

LANGUAGE: Nushell
CODE:
```
> ls | where $it.size > 10kb
```

----------------------------------------

TITLE: Conditional Output with Nushell `if-else`
DESCRIPTION: This example illustrates the `if-else` construct in Nushell. If the initial condition is true, the `then` block is executed; otherwise, the `else` block is executed, providing an alternative output.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/if.md#_snippet_1

LANGUAGE: Nushell
CODE:
```
if 5 < 3 { 'yes!' } else { 'no!' }
```

----------------------------------------

TITLE: Using Custom Command Output in a Pipeline in Nushell
DESCRIPTION: Shows that the output of a custom command (`my-ls`) can be seamlessly used as input for the next command in a pipeline (`get name`), just like built-in commands.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/custom_commands.md#_snippet_11

LANGUAGE: Nushell
CODE:
```
my-ls | get name
```

----------------------------------------

TITLE: Install Nushell via Cargo (Dataframe Feature)
DESCRIPTION: Instructions for installing Nushell with the optional dataframe functionality enabled, using the Rust package manager, Cargo. This requires Rust to be installed and includes the necessary feature flag.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-04-30-nushell_0_93_0.md#_snippet_1

LANGUAGE: Shell
CODE:
```
cargo install nu --features=dataframe
```

----------------------------------------

TITLE: Set environment variables by key-value record in Nushell
DESCRIPTION: This snippet demonstrates how to use `with-env` to temporarily set multiple environment variables using a record (key-value pair) and then access them within the provided block.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/with-env.md#_snippet_0

LANGUAGE: nu
CODE:
```
with-env {X: "Y", W: "Z"} { [$env.X $env.W] }
╭───┬───╮
│ 0 │ Y │
│ 1 │ Z │
╰───┴───╯
```

----------------------------------------

TITLE: New Nushell `mut` and Assignment Operator Parsing with Pipelines
DESCRIPTION: Illustrates the updated parsing where both `mut` and the assignment operator (=) now absorb the pipeline, allowing command output to be assigned directly to variables, including when piping lists to commands like `math sum`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-08-20-nushell_0_97_1.md#_snippet_2

LANGUAGE: Nushell
CODE:
```
mut x = 2
# $x will be set to a random integer
$x = random int
# $x will be set to 6
# previously `math sum` would have received nothing input
$x = [1 2 3] | math sum
```

----------------------------------------

TITLE: Loading a Registered Plugin (Nushell)
DESCRIPTION: Use the `plugin use` command to load a specific plugin, like 'gstat', from the new `plugin.msgpackz` registry file into the current Nushell session. This replaces the deprecated `source` command for loading plugins.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-04-30-nushell_0_93_0.md#_snippet_10

LANGUAGE: Nushell
CODE:
```
> plugin use gstat
```

----------------------------------------

TITLE: Upcasing a string using pipe
DESCRIPTION: Demonstrates how to use the `str upcase` command to convert a string literal to uppercase by piping the string into the command.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/str_upcase.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
> 'nu' | str upcase
NU
```

----------------------------------------

TITLE: Echoing multiple values in Nushell
DESCRIPTION: This example demonstrates how the `echo` command returns multiple arguments as a list. It shows the structured output format of Nushell for a list of numbers [1, 2, 3].
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/echo.md#_snippet_0

LANGUAGE: nu
CODE:
```
echo 1 2 3
╭───┬───╮
│ 0 │ 1 │
│ 1 │ 2 │
│ 2 │ 3 │
╰───┴───╯
```

----------------------------------------

TITLE: Piping Stdout Nushell
DESCRIPTION: Executes the `demo.nu` script and pipes its standard output (`foo`) to the `str upcase` command, capturing the result ("FOO") in the `$result` variable. Standard error (`barbar`) is printed directly to the terminal.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/lang-guide/chapters/pipelines.md#_snippet_1

LANGUAGE: nu
CODE:
```
let result = nu demo.nu | str upcase
```

----------------------------------------

TITLE: New If/Else If/Else Syntax in Nushell (0.60+)
DESCRIPTION: Shows how the new if/else syntax in Nushell 0.60 can be chained together using else if for handling multiple conditions. Requires variable x.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2022-03-22-nushell_0_60.md#_snippet_12

LANGUAGE: Nushell
CODE:
```
if $x < 3 {
  echo "less than three"
} else if $x < 10 {
  echo "less than ten
} else {
  echo "something else!"
}
```

----------------------------------------

TITLE: Compute cumulative sum over partition in Nushell
DESCRIPTION: This example demonstrates how to use `polars over` to compute a cumulative sum within partitions defined by column 'a'. It first creates a table, converts it to a lazy DataFrame, selects column 'a' and a new column 'cum_b' which is the cumulative sum of 'b' partitioned by 'a', and finally collects the result.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/polars_over.md#_snippet_0

LANGUAGE: nu
CODE:
```
[[a b]; [x 2] [x 4] [y 6] [y 4]]
        | polars into-lazy
        | polars select a (polars col b | polars cumulative sum | polars over a | polars as cum_b)
        | polars collect
```

----------------------------------------

TITLE: Using Spread Operator in Nushell Record Literals
DESCRIPTION: Illustrates the use of the spread operator (`...`) within a record literal to unpack fields from existing record variables, record literals, and command outputs that produce records, allowing for easy merging and creation of new records in Nushell.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/operators.md#_snippet_9

LANGUAGE: Nushell
CODE:
```
{
  ...$config,
  users: [alice bob],
  ...{ url: example.com },
  ...(sys mem)
}
```

----------------------------------------

TITLE: Natural Sort with Mixed Types in Nushell
DESCRIPTION: Shows how the `--natural` (`-n`) flag sorts mixed integer and string values numerically based on their string representation, rather than by type then value.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-10-15-nushell_0_99_0.md#_snippet_6

LANGUAGE: nushell
CODE:
```
[1 "4" 3 "2"] | sort --natural
```

----------------------------------------

TITLE: Explain a command pipeline within a closure (Nushell)
DESCRIPTION: This example demonstrates using the `explain` command to inspect a closure that contains a typical Nushell command pipeline. The closure lists files (`ls`), sorts them by name and type ignoring case (`sort-by`), and then extracts the 'name' column (`get name`). The output of `explain` is then piped to the `table --expand` command for a formatted and readable display.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/explain.md#_snippet_0

LANGUAGE: nu
CODE:
```
explain {|| ls | sort-by name type --ignore-case | get name } | table --expand
```

----------------------------------------

TITLE: Example Usage of Nushell Polars Plugin
DESCRIPTION: Demonstrates a basic use case of the Polars plugin in Nushell. It pipes the output of the `ls` command into the `polars into-df` command to create a DataFrame, then uses `describe` to show its structure.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/plugins.md#_snippet_5

LANGUAGE: nu
CODE:
```
ls | polars into-df | describe
```

----------------------------------------

TITLE: Regex Match Comparison in Nushell
DESCRIPTION: Illustrates using the `=~` operator to check if a string matches a given regular expression.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/working_with_strings.md#_snippet_38

LANGUAGE: nu
CODE:
```
'APL' =~ '^\w{0,3}$'
```

----------------------------------------

TITLE: Counting Files in Subdirectories using par-each (Nushell)
DESCRIPTION: This snippet shows the parallel version of counting files in subdirectories by replacing `each` with `par-each`. It performs the same operation but processes the directories concurrently, potentially leading to significant performance improvements on multi-core systems.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/parallelism.md#_snippet_1

LANGUAGE: nu
CODE:
```
ls | where type == dir | par-each { |row|
    { name: $row.name, len: (ls $row.name | length) }
}
```

----------------------------------------

TITLE: Creating a Table from Records in Nushell
DESCRIPTION: Demonstrates how to construct a table by piping a stream of values (generated by seq) into an each command that transforms each value into a record. This shows a new way to define tables using lists of records.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2022-03-22-nushell_0_60.md#_snippet_5

LANGUAGE: Nushell
CODE:
```
> seq 3 | each { |x| { name: Bob, x: $x } }
  #   name   x
────────────────
  0   Bob    1
  1   Bob    2
  2   Bob    3
```

----------------------------------------

TITLE: Print the square of each integer using `for` in Nushell
DESCRIPTION: This Nushell snippet demonstrates how to iterate over a list of integers using the `for` command and print the square of each element.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/for.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
for x in [1 2 3] { print ($x * $x) }
```

----------------------------------------

TITLE: If with Else If and Else Nushell
DESCRIPTION: Illustrates chaining multiple conditions using `else if` and a final `else` branch. Conditions are evaluated sequentially. The first condition that evaluates to true executes its corresponding block. If no `if` or `else if` condition is true, the `else` block is executed.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/control_flow.md#_snippet_3

LANGUAGE: nu
CODE:
```
if $x > 0 { 'positive' } else if $x == 0 { 'zero' } else { "negative" }
```

----------------------------------------

TITLE: Conditional Syntax Change
DESCRIPTION: The syntax for conditional statements changed from requiring two blocks after `if` to using `if { ... } else { ... }`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2022-03-22-nushell_0_60.md#_snippet_38

LANGUAGE: Nushell
CODE:
```
if { } { }
```

LANGUAGE: Nushell
CODE:
```
if { } else { }
```

----------------------------------------

TITLE: Renaming Files with Zip Nushell
DESCRIPTION: This practical example demonstrates using `zip` to pair a list of existing .ogg files (obtained via `glob`) with a list of desired new filenames, then using `each` and `mv` to rename each file based on the zipped pairs.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/zip.md#_snippet_3

LANGUAGE: nu
CODE:
```
glob *.ogg | zip ['bang.ogg', 'fanfare.ogg', 'laser.ogg'] | each {|| mv $in.0 $in.1 }
```

----------------------------------------

TITLE: Install Nushell with Homebrew (Shell)
DESCRIPTION: Installs the Nushell package using the Homebrew package manager on macOS or Linux.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/README.md#_snippet_0

LANGUAGE: shell
CODE:
```
$ brew install nushell
```

----------------------------------------

TITLE: Join two tables using the 'a' column in Nushell
DESCRIPTION: This example demonstrates performing an inner join between two simple tables. It uses the `join` command to combine rows where the value in the 'a' column matches in both the left table (`[{a: 1 b: 2}]`) and the right table (`[{a: 1 c: 3}]`). The result includes columns from both tables for the matching rows.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/join.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
[{a: 1 b: 2}] | join [{a: 1 c: 3}] a
```

----------------------------------------

TITLE: Installing Nushell via Winget (User Scope) - CMD
DESCRIPTION: This command installs Nushell for the current user using the winget package manager. This is the default installation scope for Nushell via winget, requiring no additional flags.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2025-05-23-nushell_0_104_1.md#_snippet_0

LANGUAGE: cmd
CODE:
```
winget install Nushell.Nushell
```

----------------------------------------

TITLE: Basic If Condition Nushell
DESCRIPTION: Shows the basic usage of the `if` command in Nushell. It evaluates a condition (`$x > 0`) and executes the block `{ 'positive' }` if the condition is true, returning the block's result. If false, it returns `null`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/control_flow.md#_snippet_1

LANGUAGE: nu
CODE:
```
if $x > 0 { 'positive' }
```

----------------------------------------

TITLE: Parsing Delimited File with Pattern - Nushell
DESCRIPTION: Opens a text file (`bands.txt`), reads lines, parses each line using a pattern `{Band}:{Album}:{Year}` to extract fields, skips the header row, and sorts the resulting table by the 'Year' column.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/cookbook/files.md#_snippet_4

LANGUAGE: nu
CODE:
```
open bands.txt | lines | parse "{Band}:{Album}:{Year}" | skip 1 | sort-by Year
```

----------------------------------------

TITLE: Creating a Nushell List with Commas
DESCRIPTION: Demonstrates the literal syntax for creating a list in Nushell using commas to separate values.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/lang-guide/chapters/types/basic_types/list.md#_snippet_0

LANGUAGE: nu
CODE:
```
[ foo, bar, baz ]
```

----------------------------------------

TITLE: 定义简单的包装命令
DESCRIPTION: 让我们把[`ls`](/commands/docs/ls.md)移到我们编写的命令中：
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/zh-CN/book/custom_commands.md#_snippet_2

LANGUAGE: Nushell
CODE:
```
def my-ls [] { ls }
```

----------------------------------------

TITLE: Define Command to Change Directory (--env) (Nu)
DESCRIPTION: This example defines a command `gohome` that changes the current directory to the user's home directory using `cd ~`. The `--env` flag is crucial here to make the directory change affect the caller's environment. The snippet then asserts that the current working directory (`$env.PWD`) is indeed the expanded home path.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/def.md#_snippet_3

LANGUAGE: Nu
CODE:
```
def --env gohome [] { cd ~ }; gohome; $env.PWD == ('~' | path expand)
```

----------------------------------------

TITLE: Conditional Output with Nushell `if`
DESCRIPTION: This snippet demonstrates the basic usage of the `if` command in Nushell. It evaluates a condition and, if true, executes the provided block, outputting its result. If the condition is false, nothing is returned.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/if.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
if 2 < 3 { 'yes!' }
```

----------------------------------------

TITLE: Fetch Nushell Blog Contributors (Shell)
DESCRIPTION: Fetches the list of contributors for the Nushell blog repository from the GitHub API, extracts author information, sorts the results by login name, and displays only the login names.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2019-12-31-happy-nu-year-2020.md#_snippet_4

LANGUAGE: shell
CODE:
```
fetch https://api.github.com/repos/nushell/blog/stats/contributors | get author | sort-by login | get login
```

----------------------------------------

TITLE: Recursive Directory Traversal with Globs (Bash/Nushell)
DESCRIPTION: Compares the traditional Bash approach using `find` and `xargs` for recursive file operations with the more idiomatic Nushell method utilizing the `**` glob pattern for traversing directory trees.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/lang-guide/chapters/types/basic_types/glob.md#_snippet_5

LANGUAGE: bash
CODE:
```
find -iname *.txt | xargs -I {} echo {} | tr "[:lower:]" "[:upper:]"
```

LANGUAGE: nu
CODE:
```
# Nostalgic for the Good Ole DOS days?
ls **/*.txt | get name | str upcase
```

----------------------------------------

TITLE: Check if string contains substring (Nushell)
DESCRIPTION: Uses `str contains` to check if the input string `'my_library.rb'` contains the substring `'.rb'`. Expected output is `true`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/commands/docs/str_contains.md#_snippet_0

LANGUAGE: nu
CODE:
```
'my_library.rb' | str contains '.rb'
true
```

----------------------------------------

TITLE: Defining Custom Command in Nushell
DESCRIPTION: Demonstrates how to define a simple custom command `add` that takes two arguments and returns their sum. Shows basic usage of the defined command.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2021-01-05-nushell_0_25.md#_snippet_0

LANGUAGE: Nushell
CODE:
```
def add [x, y] {
    = $x + $y
}

add 1 5
```

----------------------------------------

TITLE: Modifying Mutable Variable with For Loop in Nushell
DESCRIPTION: Illustrates a key advantage of `for` loops: their ability to modify mutable variables declared in the outer scope. This example shows how a `for` loop can append elements to a mutable list `result`, which is not possible with closures used by commands like `each`.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/control_flow.md#_snippet_9

LANGUAGE: Nushell
CODE:
```
mut result = []
for $it in [1 2 3] { $result = ($result | append ($it + 1)) }
$result
# => ╭───┬───╮
# => │ 0 │ 2 │
# => │ 1 │ 3 │
# => │ 2 │ 4 │
# => ╰───┴───╯
```

----------------------------------------

TITLE: Handling Empty Input with `last` in Nushell
DESCRIPTION: This snippet demonstrates how to use a `try` block to prevent the `last` command from erroring when it receives empty input. It wraps the `last` command within `try { ... }`, allowing the pipeline to continue and return null instead of failing.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/blog/2024-04-30-nushell_0_93_0.md#_snippet_31

LANGUAGE: nushell
CODE:
```
[] | try { last }
```

----------------------------------------

TITLE: Changing Directory using cd (Nushell)
DESCRIPTION: Basic usage of the `cd` command to change the current working directory to a specified path.
SOURCE: https://github.com/nushell/nushell.github.io/blob/main/book/moving_around.md#_snippet_11

LANGUAGE: Nushell
CODE:
```
cd cookbook
```