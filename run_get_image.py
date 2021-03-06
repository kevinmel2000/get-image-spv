#!/usr/bin/python
import sys
import subprocess

VULKAN_SDK_PATH = "/home/dan/VulkanSDK/1.0.46.0/x86_64/"
VERTEX_SHADER = "./shaders/shader_base.vert"


def system_call(command):
    """
    Execute the command
    """
    print command
    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return p.stdout.read(),p.stderr.read()


def check_output(s_out, s_err):
    """
    Just to check if the system calls were succesful
    """
    if (s_out):
        print s_out
    if (s_err):
        print "Error:" + s_err


def compile_code():
    """
    Compile get_image_spv by invoking the Makefile
    """
    s_out,s_err = system_call("make")
    check_output(s_out, s_err)
        
        
def compile_shaders(vertex_file, fragment_file):
    """
    Compile the fragment shader
    """
    s_out,s_err = system_call(VULKAN_SDK_PATH + "bin/glslangValidator " + "-V " + vertex_file )
    check_output(s_out, s_err)
    s_out,s_err = system_call( "mv vert.spv shaders/ " )
    check_output(s_out, s_err)
    s_out,s_err = system_call(VULKAN_SDK_PATH + "bin/glslangValidator " + "-V " + fragment_file )
    check_output(s_out, s_err)
    s_out,s_err = system_call( "mv frag.spv shaders/ " )
    check_output(s_out, s_err)
    
    
def run_get_image(json_file):
    """
    Run get image
    """
    s_out,s_err = system_call("LD_LIBRARY_PATH=" + VULKAN_SDK_PATH + "lib/" + " ./get_image_spv" + " --json " + json_file + " --fragment shaders/frag.spv"  )
    check_output(s_out, s_err)
    
    
    
if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print "USAGE: " + sys.argv[0] + " <fragment_shader>.frag " + "<fragment_shader>.json"
        exit(1)
        
    compile_code()
    compile_shaders(VERTEX_SHADER, sys.argv[1])
    run_get_image(sys.argv[2])
