import argparse
from calico import parseToCalicoPolicy
from cilium import parseToCiliumPolicy

parser = argparse.ArgumentParser(description='file name to parse')
parser.add_argument('file', type=str, help='relative file path')
parser.add_argument('cni', type=str, help='calico or cilium')
args = parser.parse_args()

if args.cni == 'calico':
    parseToCalicoPolicy(args.file)
elif args.cni == 'cilium':
    parseToCiliumPolicy(args.file)



