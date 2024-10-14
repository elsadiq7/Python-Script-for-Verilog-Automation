## importing
#built in lib
import string
import os
## don't worry my code if you don't have , it will have any error iI handle it
##  pip install pandas  /   pip install numpy # in your cmd to install them  don't numpy
import pandas as pd
import numpy as np

global used_key_words
global seq_inputs
global flag_comb
flag_comb=[]
used_key_words = []
seq_inputs = {}
space_cap = "    "
space_small = "  "


#*********************************************************************##
def word_unique_characters(value):
    '''

    :param value: input value as string
    :return: True or false depend on if the word is allowed as variable in verilog
    '''
    string_ascii = list(string.ascii_letters)  #load a-z,A-Z
    #adding alowed chars and numbers inn verilog variables
    string_ascii.append('_')
    string_ascii.extend([str(i) for i in range(10)])  # Extend with numeric characters as strings
    char_unique = set(value)  # convert input value to set to get unique char in it
    allowed_as_charonly = all(char in string_ascii for char in char_unique)  # check that evert char is allowed or not
    allowed_start = (value[0] in string.ascii_letters or value[0] == "_")  #check begging by a-z,A-Z or_

    allowed = allowed_as_charonly and allowed_start
    return allowed


#*********************************************************************##
def read_key_words(path="keywords.csv"):
    '''
    :param path: path to csv file
    :return: Array of reversed word in verilog
    '''
    try:
        df = pd.read_csv(path)
        keywords = np.array(df['Keywords'])
    except Exception as e:
        return [
            "always", "and", "assign", "automatic", "begin", "buf", "bufif0", "bufif1",
            "case", "casex", "casez", "cell", "cmos", "config", "deassign", "default",
            "defparam", "design", "disable", "edge", "else", "end", "endcase",
            "endconfig", "endfunction", "endgenerate", "endmodule", "endprimitive",
            "endspecify", "endtable", "endtask", "event", "for", "force", "forever",
            "fork", "function", "generate", "genvar", "highz0", "highz1", "if",
            "ifnone", "incdir", "include", "initial", "inout", "input", "instance",
            "integer", "join", "large", "liblist", "library", "localparam", "macromodule",
            "medium", "module", "nand", "negedge", "nmos", "nor", "noshowcancelled",
            "not", "notif0", "notif1", "or", "output", "parameter", "pmos", "posedge",
            "primitive", "pull0", "pull1", "pulldown", "pullup", "pulsestyle_ondetect",
            "pulsestyle_onevent", "rcmos", "reg", "release", "repeat", "rnmos",
            "rpmos", "rtran", "rtranif0", "rtranif1", "scalared", "showcancelled",
            "signed", "small", "specify", "specparam", "strong0", "strong1", "supply0",
            "supply1", "table", "task", "tran", "tranif0", "tranif1", "tri", "tri0",
            "tri1", "triand", "trior", "trireg", "unsigned", "use", "uwire", "vectored",
            "wait", "wand", "weak0", "weak1", "while", "wire", "wor", "xnor", "xor"]

    return keywords


#*********************************************************************##
def handle_error(value, number=False, keywords=None, range=None):
    '''
    :param value: input value as string
    :param number: check it is number or not
    :param keywords: keywords of verilog
    :param range: range in which number are allowed to be in
    :return: True or false based it correct input ot not
    '''
    correct_input = -1
    # check string
    if not number:
        if value not in keywords and value not in used_key_words:
            correct_input = 1 if word_unique_characters(value) and value.strip() != "" else -1
    #check number
    elif number:
        num_value = int(value)
        if range is not None and min(range) <= num_value <= max(range):
            correct_input = 1

    return correct_input


#*********************************************************************##
def take_input(message, number=False, keywords=None, range=None):
    '''
    :param message: input message
    :param number: check it is number or not
    :param keywords: keywords of verilog
    :param range: range in which number are allowed to be in
    :return: correct input allowed to be used in verilog
    '''
    while True:
        print("******************************************************")
        try:
            if number:
                value = int(input(message))
            else:
                value = input(message)

            correct_input = handle_error(value, number, keywords, range)
            if correct_input == 1:
                used_key_words.append(value)
                return value
            else:
                raise Exception

        except Exception as e:
            print("Invalid Input! Please try again.")


#*********************************************************************##
def take_parameters(keywords):
    print("******************************************************")

    print("Define you parameters to make a generic design \U0001F600: ")
    parameter_num = take_input(message="How many parameters do you have 0 to .... ?,Note:zero meaning you have any:",
                               number=True, keywords=None, range=[0, float("inf")])
    our_dec = dict()
    count = 0
    for i in range(parameter_num):
        print("******************************************************")
        count += 1
        parameter_name = take_input(f"Enter Parameter #{str(i + 1)} name:",
                                    number=False, keywords=keywords, range=None)
        parameter_size = take_input(message=f"Enter Parameter #{str(i + 1)} size:",
                                    number=True, keywords=None, range=[1, float("inf")])
        our_dec[parameter_name] = parameter_size
    if count == 0:
        print("\nyou don't make your design a generic one ")
    return our_dec


#*********************************************************************##

def choose_parameter_ports(message, parameter_dict):
    '''

    :param message: input message (port type)
    :param parameter_dict: parameters you have entered
    :return: return port size depend on parameter  or size if user don't want to use it
    '''
    print("******************************************************")

    yes_param = take_input(message=f"does you want your {message[0]} port to have a parameter\n1-yes\n2-no:\n",
                           number=True, keywords=None, range=[1, 2])
    if yes_param == 1:
        print(f"choose your from parameter ")
        for (key, value) in enumerate(parameter_dict.items()):
            print(f"{key + 1}-{value[0]}")
        port_param_num = take_input(message=f"enter your parameter num:",
                                    number=True, keywords=None, range=[1, len(parameter_dict)])
        port_size = list(parameter_dict.keys())[port_param_num - 1]
    else:
        port_size = take_input(message=f"Enter you {message[0]} #{str(message[1])} size:",
                               number=True, keywords=None, range=[1, float("inf")])
    return port_size


#*********************************************************************##
def take_ports(message, keywords, parameter_dict, range_nums):
    types = ["reg", "wire"]
    ports_num = take_input(message=f"Enter you {message}  number \U0001F600:",
                           number=True, keywords=None, range=range_nums)
    port_dict = dict()
    count = 0
    for i in range(ports_num):
        count += 1
        port_name = take_input(f"Enter {message} #{str(i + 1)} name:",
                               number=False, keywords=keywords, range=None)
        print(f"choose your {message} type: ")
        print("1-reg")
        print("2-wire")
        choose_type = take_input(message=f"Enter you {message}  type \U0001F600:",
                                 number=True, keywords=None, range=[1, 2])

        if parameter_dict == {}:
            port_size = take_input(message=f"Enter {message}  #{str(i + 1)} size:",
                                   number=True, keywords=None, range=[1, float("inf")])
        else:
            port_size = choose_parameter_ports([message, str(i + 1)], parameter_dict)

        port_dict[port_name] = [port_size, types[choose_type - 1]]

    if count == 0:
        print(f"you make don't enter any {message} ")
    return port_dict


#*********************************************************************##
def create_if_case(message):
    '''

    :param message: input message if or case
    :return: return for you if case num and have a default  value or not
    '''

    have_if_case = take_input(message=f"do you have {message} statement (1-yes 2-no):"
                              , number=True, keywords=None, range=[1, 2])
    if have_if_case == 1:
        if_num_case = take_input(message=f"how many cases you have:"
                                 , number=True, keywords=None, range=[1, float("inf")])
        default_else_case = take_input(message="Do you have default case or if:1-yes-- 2-no:"
                                       , number=True, keywords=None, range=[1, 2])

        return [if_num_case, default_else_case == 1]
    else:
        return [None, None]


#*********************************************************************##
def create_comb_logic():
    '''

    :return: shape of case and if in comb logic
    '''
    print("welcome to no clock area, Area Make huge delay  \U0001F602.")
    my_comb_logic = dict()
    my_comb_logic["if"] = create_if_case("if")
    my_comb_logic["case"] = create_if_case("case")
    return my_comb_logic


#*********************************************************************##
def create_seq_logic(keywords):
    '''

    :param keywords: reversed kewords for verliog
    :return: shape of sequential logic
    '''
    sysn = ["Syn", "ASyn"]
    edge = ["pos", "neg"]
    print("welcome to ....?")
    print("for sure clocked area, That  make your STA Fall \U0001F602")
    clk_name = take_input(message=f"Enter your clock name:"
                          , number=False, keywords=keywords, range=None)
    clk_edge = take_input(message=f"your clock (1-posedge,2-negedge):"
                          , number=True, keywords=None, range=[1, 2])
    seq_inputs[clk_name] = [1, "wire"]
    do_you_have_reset = take_input(message=f"Do you have reset signal:1-yes 2-no:",
                                   number=True, keywords=None, range=[1, 2])
    reset_type = None
    reset_name = None
    reset_edge = None
    if do_you_have_reset == 1:
        reset_name = take_input(message=f"Enter your reset Name:"
                                , number=False, keywords=keywords, range=None)
        reset_edge = take_input(message=f"your reset: (1-posedge,2-negedge):"
                                , number=True, keywords=None, range=[1, 2])
        seq_inputs[reset_name] = [1, "wire"]
        reset_type = take_input(
            message=f"your reset is Synchronous or ASynchronous (1-Synchronous -- 2-ASynchronous):"
            , number=True, keywords=None, range=[1, 2])

    # to avoid None-1 error
    try:

        return {"clk_name": clk_name, "clk_edge": edge[clk_edge - 1], "reset_name": reset_name,
                "reset_edge": edge[reset_edge - 1], "reset_type": sysn[reset_type - 1]}
    except:
        return {"clk_name": clk_name, "clk_edge": edge[clk_edge - 1], "reset_name": None,
                "reset_edge": None, "reset_type": None}


#*********************************************************************##
def create_my_logic(keywords):
    print("******************************************************")
    print("You know what next?")
    print("it is logic time.")
    logic_dict = {"comb": {}, "seq": {}}
    logic_type = take_input(message=f"Choose your logic type: \n 1-combinational\n 2-sequential \n 3-mix\n"
                            , number=True, keywords=None, range=[1, 3])

    if logic_type == 1:
        flag_comb.append(1)
        logic_dict["comb"] = create_comb_logic()
        logic_dict["seq"] = {"clk_name": None, "clk_edge": None, "reset_name": None, "reset_edge": None,
                             "reset_type": None}
    elif logic_type == 2:
        flag_comb.append(0)
        logic_dict["comb"] = {"if": [None, None], "case": [None, None]}
        logic_dict["seq"] = create_seq_logic(keywords)

    elif logic_type == 3:
        flag_comb.append(1)
        logic_dict["comb"] = create_comb_logic()
        logic_dict["seq"] = create_seq_logic(keywords)

    return logic_dict


#*********************************************************************##
def create_test_bench_info():
    '''

    :return: return clk period for testbench and number of cases for you
    '''
    clk_period = None
    if len(seq_inputs) > 0:
        clk_period = take_input(message=f"enter your clock period:"
                                , number=True, keywords=None, range=[1, float("inf")])
    cases_num = take_input(message=f"number of test cases:"
                           , number=True, keywords=None, range=[1, float("inf")])
    return {"clk_period": clk_period, "cases_num": cases_num}


#*********************************************************************##

def create_ports_strings(your_ports, type):
    '''

    :param your_ports: your entered ports
    :param type: type of ports  input or output or ""  for internal
    :return: ports to be used directly in verilog , return ports names only to be used in header
    '''
    ports = []
    ports_names = []
    for (key, value) in your_ports.items():
        ports_names.append(key)
        if (value[0] != 1):
            ports.append(f"{type}{str(value[1])}   [{str(value[0])}{str("-1")}:0]  {key};\n")
        else:
            ports.append(f"{type}{str(value[1])} {key};\n")

    return ports, ports_names


#*********************************************************************##

def create_module_header_ports_strings(module_name, input_ports, output_ports, internal_wires):
    '''

    :param module_name: take module name to use it in module header
    :param input_ports: input ports with its specs
    :param output_ports: output ports with its specs
    :param internal_wires: internal wire with its specs
    :return: dict of all in out internal header file to used in verliog
    '''
    ports = []
    input_ports_op = None
    output_ports_op = None
    internal_wires_op = None

    # if used to check if you have input or output or internal
    if input_ports != None:
        input_ports_op, input_names = create_ports_strings(input_ports, "input ")
        ports.extend(input_names)
    if output_ports != None:
        output_ports_op, output_names = create_ports_strings(output_ports, "output ")
        ports.extend(output_names)
    if internal_wires != None:
        internal_wires_op, internal_wires_names = create_ports_strings(internal_wires, "")

    if (len(ports) == 0):
        module_header = f"module {module_name} ;\n"
    else:
        module_header = f"module {module_name} ( {",".join(ports)} ) ;\n"
    return {"input_ports": input_ports_op, "internal_wires": internal_wires_op, "output_ports": output_ports_op,
            "module_header": module_header}


#*********************************************************************##
def create_paramters_strings(parameters):
    '''

    :param parameters: parameters with your specs
    :return: array of parameters to used in verilog directly
    '''
    parameters_ARRAY = []
    for (key, value) in parameters.items():
        parameters_ARRAY.append(f"parameter {key}={value};\n")
    return parameters_ARRAY


#*********************************************************************##
def create_my_logic_comb_strings(comb_logic_dict):
    '''

    :param comb_logic_dict: comb logic info
    :return: array of lines to be used in always@(*)  (comb logic
    '''
    my_comb_strings = []

    if_info = comb_logic_dict["if"]
    case_info = comb_logic_dict["case"]

    #check that you have if
    if if_info[0] is not None:
        my_comb_strings.extend([
            f"{space_cap}{space_small}if (your_case#1)\n",
            f"{space_cap}{space_small * 2}begin\n",
            f"{space_cap}{space_small * 2}// statements for condition 1\n",
            f"{space_cap}{space_small * 2}end\n\n"
        ])
        # print  number of else if  to be used in comb logic
        for i in range(if_info[0] - 1):
            my_comb_strings.extend([
                f"{space_cap}{space_small}else if (case#{i + 2})\n",
                f"{space_cap}{space_small * 2}begin\n",
                f"{space_cap}{space_small * 2}// statements for condition {i + 2}\n",
                f"{space_cap}{space_small * 2}end\n\n"
            ])
            # print  number if  (if stat)  have default else
        if if_info[1] == True:
            my_comb_strings.extend([
                f"{space_cap}{space_small}else\n",
                f"{space_cap}{space_small * 2}begin\n",
                f"{space_cap}{space_small * 2}// statements for default condition\n",
                f"{space_cap}{space_small * 2}end\n\n"
            ])
        my_comb_strings.append("\n\n")
    # check that you have case
    if case_info[0] is not None:
        my_comb_strings.extend([
            f"{space_cap}{space_small}case (your_test)\n"
        ])
        # print  number of  (cases)  to be used in comb logic
        for i in range(case_info[0]):
            my_comb_strings.extend([
                f"{space_cap}{space_small * 2}{i}: begin\n",
                f"{space_cap}{space_small * 2}// statements for your case# {i + 1}\n",
                f"{space_cap}{space_small * 2}end\n\n"
            ])
            # print  number if  (case stat)  have default case
        if case_info[1] == True:
            my_comb_strings.extend([
                f"{space_cap}{space_small * 2}default: begin\n",
                f"{space_cap}{space_small * 2}// statements for default case\n",
                f"{space_cap}{space_small * 2}end\n\n"
            ])
        my_comb_strings.append(f"{space_cap}{space_small}endcase\n")
    # to check that you have comb logic
    if (len(my_comb_strings) != 0 or flag_comb[0]==1):
        my_comb_strings.insert(0,
                               f"// comb logic\nalways @(*) begin\n{space_cap}//////////Enter your logic here//////////\n")
        my_comb_strings.append("\n\n")
        my_comb_strings.append("\nend\n\n")
    return my_comb_strings


#*********************************************************************##
def create_my_logic_seq_strings(seq_logic_dict):
    '''

    :param seq_logic_dict: seq logic info
    :return: array of lines to be used in seq logic
    '''
    # {"clk_name": None, "clk_edge": None, "reset_name": None, "reset_edge": None, "reset_type": None}
    my_seq_strings = []
    space_cap = "    "  # Standard indentation for nested logic
    space_small = "        "  # Extra indentation for deeper nested logic

    if seq_logic_dict['clk_name'] is not None:
        my_seq_strings.append(f"always @({seq_logic_dict['clk_edge']}edge {seq_logic_dict['clk_name']}")

        if seq_logic_dict['reset_name'] is not None and seq_logic_dict['reset_type'] != "Syn":
            my_seq_strings[-1] += f" or {seq_logic_dict['reset_edge']}edge {seq_logic_dict['reset_name']}"

        my_seq_strings[-1] += ") begin\n"

        if seq_logic_dict['reset_name'] is not None:
            if seq_logic_dict['reset_edge'] == "pos":
                my_seq_strings.append(f"{space_cap}if ({seq_logic_dict['reset_name']}) begin\n"
                                      f"{space_small}// your reset logic here\n"
                                      f"{space_cap}end\n\n")
            else:
                my_seq_strings.append(f"{space_cap}if (~{seq_logic_dict['reset_name']}) begin\n"
                                      f"{space_small}// your reset logic here\n"
                                      f"{space_cap}end\n\n")

            my_seq_strings.append(f"{space_cap}else begin\n"
                                  f"{space_small}// your logic here\n"
                                  f"{space_cap}end\n\n")
        else:
            my_seq_strings.append(f"{space_cap}// your logic here\n")
        my_seq_strings.insert(0, "\n//seq logic\n")
        my_seq_strings.append("end\n\n")

    return my_seq_strings


#*********************************************************************##
def create_logic_strings(my_logic):
    return create_my_logic_comb_strings(my_logic["comb"]) + create_my_logic_seq_strings(my_logic["seq"])


##########################################################################
def create_my_main_file(module_name_input, my_ports_wires_header, parameters, my_logic,path=""):
    if path == "":
        my_path = f"{module_name_input}.v"
    else:
        my_path = f"{path}/{module_name_input}.v"
    with open(f"{my_path}", "w") as f:
        f.writelines(f"{my_ports_wires_header["module_header"]}")
        f.write("\n")

        if parameters != []:
            f.write("////parameters\n")
            f.writelines(parameters)
        f.write("\n")

        if my_ports_wires_header["input_ports"] != []:
            f.write("//// input ports\n")
            f.writelines(my_ports_wires_header["input_ports"])
        f.write("\n")

        if my_ports_wires_header["output_ports"] != []:
            f.write("//// output ports\n")
            f.writelines(my_ports_wires_header["output_ports"])
        f.write("\n")
        if my_ports_wires_header["internal_wires"] != []:
            f.write("//// internal_wires\n")
            f.writelines(my_ports_wires_header["internal_wires"])
        f.write("\n")
        f.write("\n")
        f.writelines(my_logic)
        f.write("\nendmodule")


def create_test_bnech_file( module_name_input, my_ports_wires_header, parameters, clk_name, my_test_bench_info,path=""):
    if path == "":
        my_path = f"{module_name_input}_tb.v"
    else:
        my_path = f"{path}/{module_name_input}_tb.v"
    with open(f"{my_path}", "w") as f:
        f.writelines(f"module {module_name_input}_tb;\n")
        f.write("\n")
        if (parameters != None):
            f.write("////parameters\n")
            f.writelines(parameters)
        f.write("\n")
        #**********************************************************************
        if (my_ports_wires_header["input_ports"] != None):
            f.write("//// input ports\n")
            for i in my_ports_wires_header["input_ports"]:
                i = i.replace("input", "")
                i = i.replace("wire", "reg")
                f.writelines(i)
        f.write("\n")

        if (my_ports_wires_header["output_ports"] != None):
            f.write("//// output ports\n")
            for i in my_ports_wires_header["output_ports"]:
                i = i.replace("output", "")
                i = i.replace("reg", "wire")
                f.write(i)
        f.write("\n")
        # **********************************************************************

        module_name = module_name_input
        module_header = my_ports_wires_header["module_header"]
        module_par = module_header.split("(")[1]
        module_par = module_par.split(")")[0]
        module_par = module_par.split(",")
        module_par = [param.strip() for param in module_par]
        module_par = [f".{param}({param})" for param in module_par]
        module_par = ",\n".join(module_par)
        module_init = f"\n//module initialization\n {module_name} {module_name}_tb ( {module_par} ) ;"
        f.write(module_init)
        f.write("\n")
        # **********************************************************************

        f.write(f"\n//your cases\n")
        f.write("initial begin \n")
        for i in range(my_test_bench_info["cases_num"]):
            f.write(f"\n{space_cap}//case#{i}\n")
        f.write("end\n")
        clk_per = my_test_bench_info["clk_period"]
        if (clk_per != None):
            clock = f"\n//clock\nalways #{int(int(my_test_bench_info["clk_period"]) / 2)} {clk_name}=~{clk_name}\n"
            f.write(f"{clock};\n")

        f.write("\n")

        f.write("\nendmodule")


def run():
    # path = "D:/Way to  create brain/ITI\Verliog/Labs/lab3"
    print("Welcome to Python scripting for creating verilog \U0001F600 \U0001F600 ")
    keywords = read_key_words()
    final_input_ports = {}
    if keywords is None:
        print("Invalid path for Keywords CSV file.")
    else:
        try:
           path=input("Enter your path for creating Files:")
           path=path.replace("\\","/")
           if os.path.exists(path):
               print("The path exists.")
           else:
               raise Exception
           module_name_input = take_input("Please enter a module name: ", number=False, keywords=keywords, range=None)
           parameters = take_parameters(keywords=keywords)
           print("Ports time!")
           print("Please don't enter your clock and rst if you have any,wait unital logic to be entered in detail")
           input_ports = take_ports("inputs port", keywords, parameters, [1, float("inf")])
           output_ports = take_ports("outputs port", keywords, parameters, [1, float("inf")])
           internal_wires = take_ports("internal port", keywords, parameters, [0, float("inf")])
           my_logic = create_my_logic(keywords)

           print("Test bench time!")
           my_test_bench_info = create_test_bench_info()
           print(my_test_bench_info)
           if (len(seq_inputs) > 0):
               final_input_ports.update(seq_inputs)
               final_input_ports.update(input_ports)
           else:
               final_input_ports.update(input_ports)
           parameters = create_paramters_strings(parameters)
           my_ports_wires_header = create_module_header_ports_strings(module_name_input, final_input_ports,
                                                                      output_ports,
                                                                      internal_wires)
           my_logic_strings = create_logic_strings(my_logic)

           create_my_main_file(module_name_input, my_ports_wires_header, parameters, my_logic_strings, path)
           create_test_bnech_file(module_name_input, my_ports_wires_header, parameters, my_logic["seq"]["clk_name"],
                                  my_test_bench_info, path)
           used_key_words.clear()
           seq_inputs.clear()
           flag_comb.clear()
        except Exception as e:
               print("please enter a valid path")

