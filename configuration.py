import socket
local_ip_addr = socket.gethostbyname(socket.gethostname())
wait_time = 10
tcp_port = 2112
team_name = 'RedHatYossi\n'
standard_buffer_size = 1024
udp_port = 12000
broadcast_addr = "255.255.255.255"
broadcast_port = 13117
broadcast_pack_unpack_format = '>IbH'
broadcast_magic_cookie_identifier = 'feedbeef'
broadcast_message_type = '2'
udp_receiver_buffer_size = 7
hex_basis = 16
broadcast_message_delay = 1