# Use Cases

A brief description of each use case can be found below.
 

## Folder structure

| Use Case           | Description                                                                                                                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `heartbleed_case/` | Trustee application to a Random Forest Classifier for an Intrustion Detection System, <br>trained with CIC-IDS-2017 dataset pre-computed features [[1]](#references).                                                    |
| `kitsune_case/`    | Trustee application to Kitsune [[11]](#references) model for anomaly detection in network traffic, <br>trained with features extracted from Kitsune's Mirai attack trace  [[1]](#references).                            |
| `iot_case/`        | Trustee application to Random Forest Classifier to distguish IoT devices [[2]](#references), <br>trained with features extracted from the pcaps from the UNSW IoT Dataset [[3]](#references)                             |
| `moon_star_case/`  | Trustee application to Neural Network Moon and Stars Shortcut learning toy example from [[4]](#references)                                                                                                               |
| `nprint_ids_case/` | Trustee application to the nPrintML [[5]](#references) AutoGluon Tabular Predictor [[9]](#references) <br>for an Intrustion Detection System, also trained using pcaps from the  CIC-IDS-2017 dataset [[1]](#references) |
| `nprint_ids_case/` | Trustee application to the nPrintML [[5]](#references) AutoGluon Tabular Predictor [[9]](#references) <br>for OS Fingerprinting, also trained using with pcaps from the CIC-IDS-2017 dataset [[1]](#references)          |
| `pensieve_case/`   | Trustee application to the Pensieve RL model [[6]](#references) for adaptive bit-rate prediction, <br>and comparison to related work Metis [[7]](#references).                                                           |
| `vpn_case/`        | Trustee application the 1D-CNN trained to detect VPN traffic from [[8]](#references),<br> trained with the ISCX VPN-nonVPN dataset [[10]](#references)                                                                   |

## References 

[1] I. Sharafaldin., A. H. Lashkari., and A. A. Ghorbani. Toward Gener- ating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. In Proceedings of the 4th International Conference on Information Systems Security and Privacy - ICISSP, pages 108–116. INSTICC, SciTePress, 2018. <br>
[2] Z. Xiong and N. Zilberman. Do Switches Dream of Machine Learning? Toward In-Network Classification. In Proceedings of the 18th ACM Workshop on Hot Topics in Networks, HotNets ’19, page 25–33, New York, NY, USA, 2019. Association for Computing Machinery.<br>
[3] A. Sivanathan, H. H. Gharakheili, F. Loi, A. Radford, C. Wijenayake, A. Vishwanath, and V. Sivaraman. Classifying IoT Devices in Smart Environments Using Network Traffic Characteristics. IEEE Transactions on Mobile Computing, 18(8):1745–1759, 2019. <br>
[4] R. Geirhos, J. Jacobsen, C. Michaelis, R. Zemel, W. Brendel, M. Bethge, and F. A. Wichmann. Shortcut learning in deep neural networks. Nature Machine Intelligence, 2(11):665–673, Nov 2020.<br>
[5] J. Holland, P. Schmitt, N. Feamster, and P. Mittal. New Directions in Automated Traffic Analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, CCS ’21, page 3366–3383, New York, NY, USA, 2021. Association for Computing Machinery.<br>
[6] H. Mao, R. Netravali, and M. Alizadeh. Neural Adaptive Video Streaming with Pensieve. In Proceedings of the Conference of the ACM Special Interest Group on Data Communication, SIGCOMM ’17, page 197–210, New York, NY, USA, 2017. Association for Computing Machinery. Code available at GitHub repository at https: //github.com/hongzimao/pensieve.<br>
[7] Z. Meng, M. Wang, J. Bai, M. Xu, H. Mao, and H. Hu. Interpreting Deep Learning-Based Networking Systems. In Proceedings of the Annual Conference of the ACM SIGCOMM, SIGCOMM ’20, page 154–171, New York, NY, USA, 2020. Association for Computing Machinery.<br>
[8] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang. End-to-end encrypted traffic classification with one-dimensional convolution neural networks. In 2017 IEEE International Conference on Intelligence and Security Informatics (ISI), pages 43–48, 2017. Code available at GitHub repository https://github.com/echowei/DeepTraffic.<br>
[9] N. Erickson, J. Mueller, A. Shirkov, H. Zhang, P. Larroy, M. Li, and A. Smola. AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data, 2020.
[10] G. Draper-Gil., A. H. Lashkari., M. S. I. Mamun, and A. A. Ghorbani. Characterization of Encrypted and VPN Traffic using Time-related Features. In Proceedings of the 2nd International Conference on Information Systems Security and Privacy - ICISSP,, pages 407–414. INSTICC, SciTePress, 2016.<br>
[11] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, "Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection", Network and Distributed System Security Symposium 2018 (NDSS'18)<br>