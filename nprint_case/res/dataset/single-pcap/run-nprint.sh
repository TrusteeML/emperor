nprintml \
  --tcp \
  --ipv4 \
  --aggregator index \
  --label-file labels.txt \
  --nprint-filter "ipv4_src_[0-9]+|ipv4_dst_[0-9]+|tcp_sprt_[0-9]+|tcp_dprt_[0-9]+|tcp_seq_[0-9]+|tcp_ackn_[0-9]+" \
  --pcap-file test.pcap \
  --save-nprint \
  --output nprintml


