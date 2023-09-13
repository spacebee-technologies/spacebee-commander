# commander
Client application to send commands to Rovertito.

## Telecommands
In the 'Telecommands' folder, when adding a new telecommand, make sure to define these attributes in its constructor:

        *   name[string] Name of the telecommand
        *   help[string] Description and usage for the telecommand
        *   help_input[string] Description for the inptus arguments
        *   operation[16 bits] Unique identifier for a given telemetry or telecommand
        *   area_version[16 bits] Protocol version
        *   num_inputs[int] Number of input arguments for this command	

And define the following functions:

*   ```
    def loadInputArguments(self,arg):
        "Load input arguments into the body formated in bytes and calculate the body length."
    arg is a string. 
    Raise ValueError to prevent invalid inputs.
    Need to define:
    1.  body_length
    2.  body
*   ```
    def parseOutputArguments(self,response):
    "Parse the output argument, where the response is a byte sequence, and return a dictionary."

    ```
    Need to return a dictonary.