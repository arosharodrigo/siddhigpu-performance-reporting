
1. GPU profiling

1.1 nvprof

nvprof --print-api-trace --print-gpu-trace --output-profile logs/prof.out --log-file logs/prof.log ${APP}
nvprof --import-profile prof.out #- Summarized report will generate

sample usage of nvprof:

APP="${JVM} ${JOPT} -jar ${JAR} --enable-async true --enable-gpu true --usecase ${u} --execplan ${p} --execplan-count ${x} --usecase-count ${c} --ringbuffer-size ${r} --threadpool-size ${t} --events-per-tblock ${b} --batch-max-size ${Z} --batch-min-size ${z} --strict-batch-scheduling ${s} --work-size ${w} --selector-workers ${l} --use-multidevice false --device-count 0 --input-file ${DEBS_FILE}"
nvprof --print-api-trace --print-gpu-trace --output-profile logs/prof.out --log-file logs/prof.log ${APP}

sample output:

arosha@arosha-PC:8192-8192-batch-size-x-1-c-1$ nvprof --import-profile prof.out
======== Profiling result:
Time(%)      Time     Calls       Avg       Min       Max  Name
 42.43%  344.635s      6051  56.955ms  48.152ms  122.55ms  SiddhiGpu::ProcessEventsJoinRightTriggerCurrentOn(SiddhiGpu::JoinKernelParameters*, int, int, int)
 42.38%  344.224s      6045  56.944ms  2.0441ms  67.209ms  SiddhiGpu::ProcessEventsJoinLeftTriggerCurrentOn(SiddhiGpu::JoinKernelParameters*, int, int, int)
 14.57%  118.337s     24198  4.8903ms  4.2560us  34.518ms  [CUDA memcpy DtoH]
  0.19%  1.56574s     12102  129.38us  2.1120us  871.08us  SiddhiGpu::ResultSorter(char*, int*, int*, int, int, int, char*)
  0.18%  1.46920s     12102  121.40us  94.084us  195.21us  SiddhiGpu::ProcessEventsFilterKernelFirstV2(SiddhiGpu::KernelParametersFilterStandalone*, int)
  0.17%  1.40539s     12128  115.88us     576ns  1.2789ms  [CUDA memcpy HtoD]
  0.05%  385.12ms     12096  31.838us  29.505us  51.202us  SiddhiGpu::JoinSetWindowState(char*, int, char*, int, int, int, int, int)
  0.01%  91.906ms     12102  7.5940us  4.4480us  8.7360us  void cub::ScanRegionKernel<cub::DeviceScanDispatch<int*, int*, cub::Sum, int, int>::PtxScanRegionPolicy, int*, int*, cub::ScanTileState<int, bool=1>, cub::Sum, int, int>(int*, cub::Sum, int, int, cub::DeviceScanDispatch<int*, int*, cub::Sum, int, int>::PtxScanRegionPolicy, int*, cub::GridQueue<int>)
  0.00%  40.011ms     12098  3.3070us  2.5280us  1.1224ms  [CUDA memcpy DtoD]
  0.00%  20.454ms     12102  1.6900us     928ns  2.5290us  void cub::ScanInitKernel<int, cub::ScanTileState<int, bool=1>>(cub::GridQueue<int>, int, int)

======== API calls:
Time(%)      Time     Calls       Avg       Min       Max  Name
 99.36%    1e+03s     24214  50.737ms  3.0090us  154.88ms  cudaThreadSynchronize
  0.33%  4.11744s     48396  85.078us  3.7650us  206.69ms  cudaMemcpyAsync
  0.19%  2.40930s     72600  33.185us  3.4150us  762.25ms  cudaLaunch
  0.06%  782.56ms     12102  64.663us     281ns  381.06ms  cudaGetDevice
  0.02%  265.78ms        12  22.149ms  77.555us  236.86ms  cudaHostRegister
  0.01%  140.45ms     24204  5.8020us  1.4570us  22.226ms  cudaFuncGetAttributes
  0.01%  77.619ms    375090     206ns     100ns  11.941ms  cudaSetupArgument
  0.00%  28.465ms     36306     784ns     183ns  289.01us  cudaDeviceGetAttribute
  0.00%  26.929ms     72600     370ns     103ns  160.84us  cudaConfigureCall
  0.00%  12.786ms     48418     264ns     112ns  274.04us  cudaPeekAtLastError
  0.00%  969.34us        40  24.233us  3.6970us  158.29us  cudaMalloc
  0.00%  320.45us        83  3.8600us      93ns  183.27us  cuDeviceGetAttribute
  0.00%  227.52us        28  8.1250us  3.4290us  23.268us  cudaMemcpy
  0.00%  32.713us         1  32.713us  32.713us  32.713us  cuDeviceTotalMem
  0.00%  27.856us         1  27.856us  27.856us  27.856us  cuDeviceGetName
  0.00%  15.381us         6  2.5630us     964ns  6.5140us  cudaSetDevice
  0.00%  13.169us         6  2.1940us     263ns  5.3210us  cudaGetLastError
  0.00%  7.1920us         6  1.1980us     165ns  3.9080us  cudaGetDeviceCount
  0.00%     822ns         2     411ns     158ns     664ns  cuDeviceGetCount
  0.00%     282ns         2     141ns     120ns     162ns  cuDeviceGet
arosha@arosha-PC:8192-8192-batch-size-x-1-c-1$


2. CPU profiling

2.1 nmon

Please download the NMON prebuilt executables from either [1] or [2]. Extract it on the VM and run NMON as follows.

nmon_x86_64_ubuntu1104 -f -s 15 -c 200 -F test.nmon

In this case we are requesting NMON to collect performance information in every 15 seconds for 200 times and dump those information to a file called test.nmon. That means altogether NMON will run for 3000 seconds (i.e., 5 minutes). Likewise you need to set the appropriate rate of collection of performance information and the duration for which NMON should run.

Once you have collected the performance profile (e.g., test.nmon file) use the following command to generate the HTML charts and observe system behavior during the experiment. NMON charts tool is on [3].

./nmonchart test.nmon /tmp/hostname_date_time.html

[1] http://sourceforge.net/projects/nmon/files/nmon16d_x86.tar.gz

[2] https://sourceforge.net/projects/nmon/files/nmon_x86_64_ubuntu1104/download

[3] https://sourceforge.net/projects/nmon/files/nmonchart30.tar/download

sample usage:

./nmon_x86_64_ubuntu1104 -f -s 15 -c 200 -F /home/arosha/install/nmon/nmon-data-files/2016-09-23-Join.nmon
./nmonchart /home/arosha/install/nmon/nmon-data-files/2016-09-23-Join.nmon /home/arosha/install/nmon/nmon-data-files/2016-09-23-Join.html

3. Other links

https://devblogs.nvidia.com/parallelforall/cuda-pro-tip-nvprof-your-handy-universal-gpu-profiler/
http://gamedev.stackexchange.com/questions/87860/how-to-profile-cpu-and-gpu-performance-if-i-have-a-monster-pc
