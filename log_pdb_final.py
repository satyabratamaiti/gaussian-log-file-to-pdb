#!/usr/bin/env python
# coding: utf-8

# In[46]:
# python3.5 log_pdb_final.py hadded-BLCChsT.log  [templated pdb should be in same directory]

import re
import argparse

# In[47]:
#
parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

filename=args.echo
filename_pdb= args.echo[:-4]+".pdb"
opt_pdb=filename_pdb[:-4]+"_opt.pdb"
fp=open(filename,'r')




# In[48]:


params_found= False
orientation_found= False
ready_to_operation = False
passed_count = 0
x=[]
y=[]
z=[]
for line in fp:
    if ready_to_operation ==  True :
        if (re.search("----" ,line ) != None) :
            ready_to_operation = False
        else :
            x_="{0:.3f}".format(float(line.strip().split()[3]))
            y_="{0:.3f}".format(float(line.strip().split()[4]))
            z_="{0:.3f}".format(float(line.strip().split()[5]))
            x.append(x_)
            y.append(y_)
            z.append(z_)
    else :
        if (re.search("Optimized Parameters" ,line ) != None) :
            params_found = True
        elif ( (params_found == True ) and ( re.search("Standard orientation:" ,line ) != None )):
            orientation_found = True
        elif ( params_found == True and   orientation_found == True) :
            passed_count = passed_count + 1
            if (  passed_count == 4 ):
                ready_to_operation = True
            

pdb_data=[]
fp1=open(filename_pdb,'r')
for line1 in fp1:
    if line1[:4]=="ATOM":
        pdb_data.append(line1[:26])
        
#print(len(pdb_data))

final_data=[]


#print(len(final_data))
for i in range(0,len(x)):
    #print(i)
    p_data=pdb_data[i]
    #print(p_data)
    xx=x[i]
    #print(xx)
    yy=y[i]
    zz=z[i]
 #   data_row = p_data + " :: " + xx + " :: " + yy + " :: " + zz
    data_row = '%-30s%8.3f%8.3f%8.3f' % (p_data,float(xx),float(yy),float(zz))
    #print(data_row)
    final_data.append(data_row)
    #print(type(data_row))
#print(final_data)
fw=open(opt_pdb,'w')
for sen in final_data:
    fw.write(sen + "\n")
fw.write("END" + "\n")
    

