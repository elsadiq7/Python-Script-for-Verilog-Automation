from main import run, take_input

while True:
    input_clk = take_input(message=f"do you want to create verilog files? (1-yes,2-no):  "
                           , number=True, keywords=None, range=[1, 2])
    if input_clk==1:
       run()
       print("the files are written at your path ")
       print("*" * 60)
       print("#" * 60)
    elif input_clk==2:
       print("thanks for using our service")
       break





























# def make_init(module_name_input,header):
#         module_name = module_name_input
#         module_header =header
#         module_par = module_header.split("(")[1]
#         module_par = module_par.split(")")[0]
#         module_par = module_par.split(",")
#         module_par = [param.strip() for param in module_par]
#         module_par = [f".{param}({param})" for param in module_par]
#         module_par = ",\n".join(module_par)
#         module_init = f"\n//module initialization\n {module_name} {module_name}_1 ( {module_par} ) ;"
#         print(module_init)
#
# make_init("FIFO","FIFO ( w_clk,w_rst,w_data,write,w_ptr,r_clk,r_rst,read,r_ptr,r_data ) ;")
# make_init("create_full_single","create_full_single ( w_clk,w_rst,w_ptr,r_ptr_gray,write_en,full,w_ptr_gray,write) ;")
# make_init("create_empty_single","module create_empty_single ( r_clk,r_rst,r_ptr,w_ptr_gray,read_en,empty,r_ptr_gray,read ) ;")
#
#


# import os
#
#
# def get_f_files(directory):
#     # Get list of files in the directory
#     files = os.listdir(directory)
#
#     # Filter files ending with .f
#     f_files = [file for file in files if file.endswith('.v')]
#
#     return f_files
#
#
# # Example usage
# directory = 'D:\Way to  create brain\ITI\Verliog\Labs\lab3'
# directory=directory.replace("\\","/")# Replace with your directory path
# f_files = get_f_files(directory)
#
# print(" ".join(f_files))



for i in range(16):
    print(f"wire [32-1:0] block_{i}=block_data[{i}*32-1:{i-1}*32];")
























