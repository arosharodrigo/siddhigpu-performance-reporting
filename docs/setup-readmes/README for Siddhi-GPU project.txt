README for Siddhi-GPU project
=============================

1. Project locations:

Siddhi GPU (<siddhi>)	- https://github.com/prabodha007/siddhi/tree/gpu-filters-3.0.0.1-allop
Performanc Samples 	- https://github.com/prabodha007/siddhigpu-performance-test

2. Environment

Java version	: 1.6.0_29
Maven version	: Apache Maven 3.1.1

OS 			- Ubuntu 16.04.1 LTS
Kernal 			- 4.4.0-34-generic
gcc/g++ 		- 5.4.0
CUDA Driver Version 	- 8.0
CUDA Runtime Version 	- 7.5
Nvidia Card/Driver	- GeForce GTX 960/nvidia-364

3. Enable debug logs on GPU

Uncomment following properties under maven-antrun-plugin in <siddhi>/modules/siddhi-gpu/modules/cudac-lib/pom.xml.

<arg value="GPU_DEBUG=5" />

4. If you are using only single GPU make sure to set 'cuda.device' as '0' in all siddhi queries.
This may endup with java core dump when you try to run the samples.

5. Download cub-1.3.2.zip (http://nvlabs.github.io/cub/) and place it in desired location, and set path in <siddhi>/modules/siddhi-gpu/modules/cudac-lib/src/jni/Makefile
CUB_LIB_PATH

6. Set CPPBUILD path

7. Set PLATFORM (linux-x86_64)

8. When compiling 'CUDA-C Library' module there may be an error come related to 'mem_cpy' as follows:

[exec] /usr/include/string.h: In function ‘void* __mempcpy_inline(void*, const void*, size_t)’:
[exec] /usr/include/string.h:652:42: error: ‘memcpy’ was not declared in this scope
[exec]    return (char *) memcpy (__dest, __src, __n) + __n;

This is due to gcc version and can do a workaround by adding following flag to when compile.
-D_FORCE_INLINES

For ex: 
NVCCFLAGS += -D_FORCE_INLINES -g -G --ptxas-options=-v -maxrregcount=${MAXREGCOUNT} -lineinfo

9. Set respective CUDA compute capability in 'CUDA_ARCH' field, according to GeForce GPU device.

For ex: GTX960 compute capabilty is 5.0

CUDA_ARCH := -gencode arch=compute_20,code=sm_20 \
-gencode arch=compute_20,code=sm_21 \
-gencode arch=compute_30,code=sm_30 \
-gencode arch=compute_35,code=sm_35 \
-gencode arch=compute_50,code=sm_50 \
-gencode arch=compute_50,code=compute_50
GENCODE_FLAGS   := $(CUDA_ARCH)


