# Verilog File Generation Script

This repository contains a Python script that automates the generation of Verilog files for hardware design. The script allows users to define module headers, input and output ports, internal wires, parameters, and logic for both combinational and sequential circuits. It also generates corresponding testbench files for simulation.

## Features

- **Module Header Creation**: Define the module name, input ports, output ports, and internal wires. 
- **Parameter Management**: Specify parameters to be included in the Verilog file.
- **Logic Generation**: Automatically generates combinational and sequential logic structures based on user input.
- **Testbench Creation**: Generates a testbench for the designed module, including clock generation and initial conditions.

## Functions

1. **`create_module_header_ports_strings(module_name, input_ports, output_ports, internal_wires)`**: Creates the module header and port declarations.
2. **`create_paramters_strings(parameters)`**: Converts parameter specifications into a Verilog-compatible format.
3. **`create_my_logic_comb_strings(comb_logic_dict)`**: Generates combinational logic based on provided conditions.
4. **`create_my_logic_seq_strings(seq_logic_dict)`**: Generates sequential logic based on clock and reset conditions.
5. **`create_logic_strings(my_logic)`**: Combines the logic strings for both combinational and sequential logic.
6. **`create_my_main_file(module_name_input, my_ports_wires_header, parameters, my_logic, path)`**: Writes the main Verilog file with the specified components.
7. **`create_test_bnech_file(module_name_input, my_ports_wires_header, parameters, clk_name, my_test_bench_info, path)`**: Generates a testbench file for simulation.
8. **`run()`**: The main function that executes the script, collects user inputs, and generates the Verilog and testbench files.

## Usage

To use the script:

1. Run the script to start the interactive command-line interface.
2. Follow the prompts to enter the module name, parameters, input and output ports, and internal wires.
3. Specify the logic for the module, including both combinational and sequential logic.
4. The script will generate the Verilog files and testbench files in the specified directory.

