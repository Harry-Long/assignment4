Can't locate local/lib.pm in @INC (you may need to install the local::lib module) (@INC contains: /nics/b/home/hzhan101/perl5/lib/perl5 /opt/moab/lib/perl5 /opt/moab/lib/perl5 /nics/e/sw/cs400_centos7.3_acfsoftware/anaconda3/4.4.0/centos7.3_gnu6.3.0/anaconda3-4.4.0/lib/site_perl/5.26.2/x86_64-linux-thread-multi /nics/e/sw/cs400_centos7.3_acfsoftware/anaconda3/4.4.0/centos7.3_gnu6.3.0/anaconda3-4.4.0/lib/site_perl/5.26.2 /nics/e/sw/cs400_centos7.3_acfsoftware/anaconda3/4.4.0/centos7.3_gnu6.3.0/anaconda3-4.4.0/lib/5.26.2/x86_64-linux-thread-multi /nics/e/sw/cs400_centos7.3_acfsoftware/anaconda3/4.4.0/centos7.3_gnu6.3.0/anaconda3-4.4.0/lib/5.26.2 .).
BEGIN failed--compilation aborted.
Traceback (most recent call last):
  File "/lustre/haven/proj/UTK0150/hzhan101/assignment4/train_mnist.py", line 172, in <module>
    dist.init_process_group('gloo',
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 500, in init_process_group
    store, rank, world_size = next(rendezvous_iterator)
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/rendezvous.py", line 190, in _env_rendezvous_handler
Traceback (most recent call last):
  File "/lustre/haven/proj/UTK0150/hzhan101/assignment4/train_mnist.py", line 172, in <module>
Traceback (most recent call last):
  File "/lustre/haven/proj/UTK0150/hzhan101/assignment4/train_mnist.py", line 172, in <module>
Traceback (most recent call last):
  File "/lustre/haven/proj/UTK0150/hzhan101/assignment4/train_mnist.py", line 172, in <module>
    store = TCPStore(master_addr, master_port, world_size, start_daemon, timeout)
RuntimeError: Address already in use
    dist.init_process_group('gloo',
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 503, in init_process_group
    dist.init_process_group('gloo',
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 503, in init_process_group
    _update_default_pg(_new_process_group_helper(
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 588, in _new_process_group_helper
    dist.init_process_group('gloo',
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 503, in init_process_group
    _update_default_pg(_new_process_group_helper(
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 588, in _new_process_group_helper
    pg = ProcessGroupGloo(
RuntimeError: [enforce fail at ../third_party/gloo/gloo/transport/tcp/address.cc:30] sizeof(impl_) == bytes.size(). 136 vs 45
    _update_default_pg(_new_process_group_helper(
  File "/lustre/haven/proj/UTK0150/envs/pytorch181/lib/python3.9/site-packages/torch/distributed/distributed_c10d.py", line 588, in _new_process_group_helper
    pg = ProcessGroupGloo(
RuntimeError: [enforce fail at ../third_party/gloo/gloo/transport/tcp/address.cc:30] sizeof(impl_) == bytes.size(). 136 vs 45
    pg = ProcessGroupGloo(
RuntimeError: [enforce fail at ../third_party/gloo/gloo/transport/tcp/address.cc:30] sizeof(impl_) == bytes.size(). 136 vs 45
--------------------------------------------------------------------------
Primary job  terminated normally, but 1 process returned
a non-zero exit code. Per user-direction, the job has been aborted.
--------------------------------------------------------------------------
--------------------------------------------------------------------------
mpirun detected that one or more processes exited with non-zero status, thus causing
the job to be terminated. The first process to do so was:

  Process name: [[5657,1],1]
  Exit code:    1
--------------------------------------------------------------------------
