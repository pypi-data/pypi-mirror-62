# String-routing

Connect strings to functions. Best usage with input commands.

## Usage

``` python
import route

sr = route.StringRouter()  # Construct the string router

@sr.route("login")
def login():
    print("Running login...")
```

To run the __login__ function with the command:

``` python
command = input("Command: ") # Input command for example
sr.trigger(command) # <- will run the command if it has a link
```

```
Command: login

Running login...
```
Typing: 
``` python
print(sr)
```
Will ouput:
```
{'login': <function login at 0xPOINTER>}
```
For each of the links connected