#!/usr/bin/python

import sys

if len(sys.argv) != 4:
    print "USAGE: comp_gf_hmmer_acc.py <labels_file> <gf_classify_file> <hmmer3_tbl_file>"
    sys.exit(1)

labels = dict()
hmmer_labels = dict()
gf_labels = dict()

for line in open(sys.argv[1]):
    lexemes = line.strip().split()
    if len(lexemes) != 2:
        continue

    labels[lexemes[0]] = lexemes[1].lower()

if len(labels) == 0:
    unlabeled = True
else:
    unlabeled = False

for line in open(sys.argv[2]):
    lexemes = line.strip().split()
    if len(lexemes) < 4:
        continue

    gf_labels[lexemes[0]] = lexemes[-1]

    if unlabeled:
        labels[lexemes[0]] = "whoknows"

for line in open(sys.argv[3]):
    if line[0] == "#":
        continue

    lexemes = line.strip().split()

    if len(lexemes) != 19:
        continue

    if lexemes[2] not in hmmer_labels:  #Top reported hit is always the highest scoring hit in hmmscan tbl output
        hmmer_labels[lexemes[2]] = lexemes[0]

gf_corr = 0
hmm_corr = 0

hmm_counts = dict()
gf_counts = dict()

classes = set()

for seqid in labels:
    label = labels[seqid]
    if seqid not in gf_labels:
        print >>sys.stderr, "sequence %s was not in gfclassify results file" % seqid
        gf_label = "(unknown)"
    else:
        gf_label = gf_labels[seqid].lower()

    if seqid not in hmmer_labels:
        hmmer_label = "bg"
    else:
        hmmer_label = hmmer_labels[seqid].lower()

    if not unlabeled and (gf_label != label or hmmer_label != label):
        print "%s\t%s\t%s\t%s" % (seqid, gf_label, hmmer_label, label)

    if not unlabeled and gf_label == label:
        gf_corr += 1.0
    if hmmer_label == label:
        hmm_corr += 1.0

    if hmmer_label not in hmm_counts:
        hmm_counts[hmmer_label] = dict()
    hmm_counts[hmmer_label][label] = hmm_counts[hmmer_label].get(label, 0) + 1
    if gf_label not in gf_counts:
        gf_counts[gf_label] = dict()
    gf_counts[gf_label][label] = gf_counts[gf_label].get(label, 0) + 1

    classes.add(label)
    classes.add(hmmer_label)
    classes.add(gf_label)

seq_tot = len(labels)

classes = sorted(classes)


print
for label in classes:
    print label, [gf_counts.get(label, dict()).get(x, 0) for x in classes], sum([gf_counts.get(label, dict()).get(x, 0) for x in classes])
print
for label in classes:
    print label, [hmm_counts.get(label, dict()).get(x, 0) for x in classes], sum([hmm_counts.get(label, dict()).get(x, 0) for x in classes])

print
print "Total sequences: %s, gf error rate: %s, hmm error rate: %s" % (seq_tot, (seq_tot - gf_corr) / seq_tot, (seq_tot - hmm_corr) / seq_tot)
