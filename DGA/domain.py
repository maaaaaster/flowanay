from publicsuffix import PublicSuffixList
import codecs
psl_file = codecs.open('/home/OpenCode/FlowAnay/Cluster/suffix.dat', encoding='utf8')
psl = PublicSuffixList(psl_file)


def loadWhiteMap():
    whiteSet = set()
    for line in open('/home/OpenCode/FlowAnay/DGA/prank.top.1m.20180322').readlines():
        domain = line.split('\t')[0]
        whiteSet.add(psl.get_public_suffix(domain))
    for line in open('/home/OpenCode/FlowAnay/DGA/top-1m.csv').readlines():
        domain = line.split(',')[1]
        whiteSet.add(psl.get_public_suffix(domain))
    print ("loaded %d white Domains"%len(whiteSet))
    return whiteSet


if __name__=='__main__':
    loadWhiteMap()
