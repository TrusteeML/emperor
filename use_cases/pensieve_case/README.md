# IoT Use Case

Trustee application to the Pensieve RL model [[1]](#references) for adaptive bit-rate prediction, <br>and comparison to related work Metis [[2]](#references).

> The code inside this use case was mostly adapted from the original Pensieve and Metis repositories.
> Pansieve: https://github.com/hongzimao/pensieve
> Metis: https://github.com/transys-project/metis

## Reproducibility steps

The comparison with Metis can be run in a regular Ubuntu 20.04, using Python 3.7, and can be found inside the `metis/` directory.
Meanwhile, the Pensieve experimental setup evaluation can be executed inside a VM, with [Vagrant](https://www.vagrantup.com/docs/vagrantfile), using the provided Vagrantfile.

## References

[1] H. Mao, R. Netravali, and M. Alizadeh. Neural Adaptive Video Streaming with Pensieve. In Proceedings of the Conference of the ACM Special Interest Group on Data Communication, SIGCOMM ’17, page 197–210, New York, NY, USA, 2017. Association for Computing Machinery. Code available at GitHub repository at https: //github.com/hongzimao/pensieve.<br>
[2] Z. Meng, M. Wang, J. Bai, M. Xu, H. Mao, and H. Hu. Interpreting Deep Learning-Based Networking Systems. In Proceedings of the Annual Conference of the ACM SIGCOMM, SIGCOMM ’20, page 154–171, New York, NY, USA, 2020. Association for Computing Machinery.<br>