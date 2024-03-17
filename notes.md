
# hackmud scripting environment

    - raw es6, synchronous plus some preprocessor directives for hackmud things
    - all scripts are stored as source code in DB
    - a preprocessor runs on them the expand game commands (like script calls, #D, #db, etc)
    - dependencies are fetched recursively until all the code is found and preprocessed
    - it's all stuck together along with some game-provided boilerplate
    - checked for sanity with Esprima and then handed off to v8

# limiting factors:
    
    - no eval or anything that would be an eval-like
    - no this (but you can emulate it a little bit and it might actually be safe to re-enable)
    - no Proxy or Reflect
    - 256mb memory cap (you wont hit this generally unless some recursion shenanigans or t3 shenanigans are afoot)
    - 5000ms runtime limit from your top-level script run 
    - 3000ms time to parse the script and any scripts you are subscripting
    - no web bollocks (though you can hackjob webassembly into it lol)
    - no console.log; you return outputs

# character counts:

    - does not count whitespace and // comments
    - all other comments are counted
    - ignores // by removing // to end of line
    - parser doesn't know that // inside a str isn't a comment
    - hackmud will truncate `var x="http://google.com"` to `var x="http:` which will cause a syntax error. 
    - easiest fix is to use /\/ anywhere you want // to appear.
