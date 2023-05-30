# This script takes the contents of a .clf file via STDIN as input and returns a flattened version via STDOUT.
# Sample usage: cat [input_clf_file] | python3 flatten_clause_notation.py > [output_clf_file]

import sys
import copy

heading=[]
comments=[]


# Rule1
def rule1(drs,comment):
    # Apply rule 1 until there no change
    while True:
        original = copy.deepcopy(drs)

        # Find x PRESUPPOSITION y and y PRESUPPOSITION z
        for i in range(len(drs)):
            if drs[i][1]=="PRESUPPOSITION":
                # x PRESUPPOSITION y
                x=drs[i][0]
                y=drs[i][2]
                z=""
                # now trying to find y PRESUPPOSITION z
                for j in range(len(drs)):
                    if drs[j][1] == "PRESUPPOSITION" and drs[j][0] == y and drs[j][0] !=x :
                        z = drs[j][2]

                # if we have x, y and z
                if z!="":
                    drs,comment = remove_statement_from_drs(drs,[x, "PRESUPPOSITION", y],comment)
                    drs = replace_in_drs(drs, x, y)
                    break

        if is_equal(original, drs):
            break
    return drs,comment

# Rule2
def rule2(drs,comment):
   # Apply rule 2 until there no change
    while True:
        original = copy.deepcopy(drs)

        # Find x PRESUPPOSITION y and z PRESUPPOSITION y
        for i in range(len(drs)):
            if drs[i][1]=="PRESUPPOSITION":
                # x PRESUPPOSITION y
                x=drs[i][0]
                y=drs[i][2]
                z=""
                # now trying to find z PRESUPPOSITION y
                for j in range(len(drs)):
                    if drs[j][1] == "PRESUPPOSITION" and drs[j][2] == y and not drs[j][0]==x:
                        z = drs[j][0]
                # if we have x, y and z
                if z!="":
                    drs,comment = remove_statement_from_drs(drs,[z, "PRESUPPOSITION", y],comment)
                    drs = replace_in_drs(drs, z, x)
                    break
        if is_equal(original, drs):
            break
    return drs,comment


# Rule3
def rule3(drs,comment):
   # Apply rule 3
   while True:
       original = copy.deepcopy(drs)
       for i in range(len(drs)):
           if drs[i][1] in {"CONTINUATION", "CONTRAST", "ELABORATION", "EXPLANATION"}:
                x = drs[i][0]
                y = drs[i][2]
                stmt = drs[i][1]
                drs,comment = remove_statement_from_drs(drs,[x,stmt, y],comment)
                drs = replace_in_drs(drs, x, y)
                break
       if is_equal(original, drs):
           break
   return drs,comment


# Checks if two DRSs are equal
def is_equal(drs1,drs2):
    if len(drs1)!=len(drs2):
        return False

    drs1=set([str(i) for i in drs1])
    drs2=set([str(i) for i in drs2])
    return drs1==drs2

# Replaces x with y
def replace_in_drs(drs,x,y):
    for i in range(len (drs)):
        for j in range(len(drs[i])):
            if drs[i][j] == x:
                drs[i][j]=y
    return drs

# This removes the given statement from the DRS
def remove_statement_from_drs(drs, statement,comment):
    for i in range(len(drs)-1,-1, -1 ):
        if len(drs[i])==len(statement):
            found=True
            for j in range(len(statement)):
                if statement[j]!=drs[i][j]:
                    found=False
                    break
            if found:
                del drs[i]
                del comment[i]
    return drs,comment

# This will search for bx PRESUPPOSITION by and bx CONTINUATION by and remove bx CONTINUATION by when found
def remove_continuation_if_presupposition_exists(drs,comment):
    # Apply until there is no change
    while True:
        original = copy.deepcopy(drs)

        # Find x PRESUPPOSITION y and x PRESUPPOSITION y
        for i in range(len(drs)):
            if drs[i][1]=="PRESUPPOSITION":
                # x PRESUPPOSITION y
                x=drs[i][0]
                y=drs[i][2]
                z=False
                # now trying to find x CONTINUATION y
                for j in range(len(drs)):
                    if drs[j][1] == "CONTINUATION" and drs[j][0] == x and drs[j][2] == y:
                        z=True
                        break

                # if we have find it then we remove it
                if z:
                    drs,comment = remove_statement_from_drs(drs,[x, "CONTINUATION", y],comment)
                    break

        if is_equal(original, drs):
            break
    return drs,comment

all_drses= sys.stdin.read()


all_drses=[i.strip(" ") for i in all_drses.split("\n\n") if i.strip()!=""]
all_drses=[i.split("\n") for i in all_drses]
all_drses=[[i for i in j if not i.strip(" ").startswith("%") or i.startswith("%%%")] for j in all_drses]
headings=[[i for i in j if i.startswith("%")] for j in all_drses]
comments=[[("%" + i).rsplit("%",1)[1].strip(" ") for i in j if not i.startswith("%") and not i=="" and i.find("%")!=-1 ] for j in all_drses]
#comments=[ [i[0], ""] if i[0]==i[1] else i for i in comments]
all_drses=[ [j.rsplit("%")[0].strip(" ") for j in i ] for i in all_drses]
all_drses=[ "\n".join([ j for j in i if j!=""]) for i in all_drses]
for indice in range(len(all_drses)):
    DRS_clause=all_drses[indice]
    comment=comments[indice]
    heading=headings[indice]
    DRS_clause = [c.strip(" ") for c in DRS_clause.split("\n") if c!=""]
    # Remove the same lines if any
    unique_content=[]
    new_comment=[]
    for i in range(len(DRS_clause)):
        if DRS_clause[i] not in unique_content:
            unique_content.append(DRS_clause[i])
            new_comment.append("" if comment==[] else comment[i])
    comment=new_comment
    DRS_clause=[i.split(" ") for i in unique_content]
    del unique_content
    DRS_clause,comment = remove_continuation_if_presupposition_exists(DRS_clause,comment)
    DRS_clause,comment = rule3(DRS_clause,comment)
    DRS_clause,comment = rule1(DRS_clause,comment)
    DRS_clause,comment = rule2(DRS_clause,comment)
    DRS_clause =  [ " ".join(i) for i in DRS_clause]
    max_length=-1
    for i in DRS_clause:
        if len(i)>max_length:
            max_length=len(i)
    max_length+=1
    DRS_clause=[i + " "*(max_length-len(i)) for i in DRS_clause]
    for i in range(len(DRS_clause)):
        DRS_clause[i]+= ("% "+comment[i] if comment[i].strip(" ")!=DRS_clause[i].strip(" ") and comment[i].strip()!="" else "")
    DRS_clause="\n".join(DRS_clause) + "\n"
    heading="\n".join([ "".join(i) for i in heading])

    print(heading)
    print(DRS_clause)
