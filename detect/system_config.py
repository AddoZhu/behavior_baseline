########################################################
#
#                   Artifacts path
#
########################################################

### CADETS

topic = 'e3-cadets-2-test'

alert_path = '/behavior_baseline/detect/apt_alert/fasttext_mlp_2_test.log'

attack_nodes_dict = {
'e3-cadets-1-test': [
        '81.49.200.166',
        'nginx',
        '/tmp/vUgefal',
        'vUgefal',
        '/var/log/devc',
        '61.167.39.128'
    ],
    'e3-cadets-2-test': [
        '25.159.96.207',
        'nginx',
        '/tmp/tmux-1002',
        '/tmp/minions',
        '/tmp/font',
        'minions',
        '/tmp/XIM',
        'XIM',
        '53.158.101.118',
        'sshd',
        '/var/log/netlog',
        '/var/log/sendmail',
        '/tmp/main',
        'main',
        '/tmp/test',
        'test',
        '192.113.144.28'
    ],
    'e3-cadets-3-test': [
        '25.159.96.207',
        'nginx',
        '/tmp/pEja72mA',
        '/tmp/eWq10bVcx',
        'pEja72mA',
        '53.158.101.118',
        '/tmp/memhelp.so',
        '/tmp/eraseme',
        '/tmp/done.so',
        '198.115.236.119'
    ],
}

### THEIA
# topic = 'e3-theia-1-test'

# alert_path = '/behavior_baseline/detect/apt_alert/fasttext_mlp_1_test.log'

# attack_nodes_dict = {
#     'e3-theia-1-test': [
#         '64189C2B-0000-0000-0000-000000000020',
#         '0100D00F-44C5-0600-0000-00006E15B00E',
#         '80370C6E-42AD-9299-4497-500000000040',
#         '6818A92B-0000-0000-0000-000000000020',
#         '80370C6E-AAB0-A174-5848-500000000040',
        
#         'F71F9730-0000-0000-0000-000000000020',
#         '0100D00F-5EC5-0600-0000-0000697C471C',
#         '80370C6E-7BAD-9299-4497-500000000040',
#         'FB1F9E30-0000-0000-0000-000000000020',
#         '80370C6E-64B2-A174-5848-500000000040',

#         '0100D00F-1D12-1E00-0000-00009F8F0C12'
#     ],
#     'e3-theia-2-test': [
#         '223838BC-0200-0000-0000-000000000020',
#         '0100D00F-A84B-1E00-0000-00008C1CB31C',
#         '283847BC-0200-0000-0000-000000000020',
#         '80370C6E-D2AA-9534-C617-500000000040',
#         '80370C6E-D2AA-9534-C617-500000000040',

#         '0100D00F-A84B-1E00-0000-000049134A16',
#     ],
# }

###TRACE
# topic = 'e3-trace-2-test'

# alert_path = '/behavior_baseline/detect/apt_alert/fasttext_mlp_2_test.log'

# attack_nodes_dict = {
#     'e3-trace-1-test': [
#         'D435C452-F2A4-DD84-72D6-502060FB35FA',
#         'B0E6DFED-CDD0-92B7-017B-A6DAD83054A0',
#         '41BED274-6761-FF93-4254-9A966671956F',
#         'E0466B29-83E5-1AAE-71BD-CFE146134699',
#         'C9FE6BB4-870D-D742-8179-55B42F423770',
#         'E4F95CAA-E071-00FA-E4F7-0141EF9ED9E8',
#         'F85DD396-C3A1-8055-4872-930F80AB41FA',
#         '190A4CE3-955A-E051-E3D1-5FE0AC85E95C',
#     ],
#     'e3-trace-2-test': [
#         'A494D8CF-50ED-5620-1FBE-07A0EE363991',
#         '59169A99-4C73-E5E0-1E25-DB232BA80F32',
#         '1F52B45B-9618-A060-215D-7BD61ECCAE05',
#         '96FE4223-D38F-9D49-C00F-D51954FA7DD4',
#         'D64910E4-454E-156D-BF13-BC7AD66F7A6A',
#         '7E6F9A12-EDFA-C87E-B4D5-DB6C782DC6DC',
#         '9736A2A7-D8A8-498F-A633-743D7AEAAEDF', 
#         '66C31C14-7518-0945-62A9-A7BE2735B99A',
#         '9821EF8B-BDFE-AFC2-EDC8-E2AFC528D66C',
#         '2A25D735-8DD9-0026-DE60-544F311757AE',
#     ],
# }
