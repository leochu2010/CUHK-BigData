#!/usr/bin/python
import math

current_time=0
#max window size 
N=1000
#max bucket size
max_bucket_num=int(round(math.log(N,2)))
max_bucket_size=int(math.pow(2, max_bucket_num))
#max number of buckets of a size
max_buckets_per_size=2

steamInput = open("cmsc5741_stream_data.txt","r")
output = open("output.txt", "w")

#round(math.log(N,2))
buckets_by_size_dict = {}

#init
for log2_size in range(0,max_bucket_num):
    size = int(math.pow(2,log2_size))
    buckets_by_size_dict[size]=[]

#def count_one():
    
def count_one():
    num_of_one=0
    
    for log2_size in range(0,max_bucket_num):
        size = int(math.pow(2,log2_size))
        buckets = buckets_by_size_dict[size]
        for bucket in buckets:
            if bucket["timestamp"]+bucket["size"] > N:
                num_of_one+=bucket["size"]/2
            else:
                num_of_one+=bucket["size"]
                
    print "number of 1s=",num_of_one
    output.write(", number of 1s: "+str(num_of_one)+"\n")
    
def print_buckets():
    print "Buckets:"
    output.write("Buckets:")
    id=0  
    for log2_size in range(0,max_bucket_num):
        size = int(math.pow(2,log2_size))
        buckets = buckets_by_size_dict[size]        
        if len(buckets) > 0:
            for bucket in buckets:   
                id+=1             
                print id,": Size=",bucket["size"],", timestamp=",bucket["timestamp"],", create time=",bucket["create_time"]
                output.write("("+str(id)+": Size="+str(bucket["size"])+", timestamp="+str(bucket["timestamp"])+", create time="+str(bucket["create_time"])+")")
                

def maintain_buckets():
    for log2_size in range(0,max_bucket_num):
        size = int(math.pow(2,log2_size))
        
        buckets = buckets_by_size_dict[size]
        if len(buckets)>max_buckets_per_size:
                        
            #remove first 2 and put into next size buckets
            first_bucket = buckets[0]
            del buckets[:max_buckets_per_size]
            
            #double the bucket size
            first_bucket["size"]=size*2
            #put it into next size list
            if size*2 < max_bucket_size:
                buckets_by_size_dict[size*2].append(first_bucket)                            
            
    for log2_size in reversed(range(0,max_bucket_num)):
        size = int(math.pow(2,log2_size))        
        buckets = buckets_by_size_dict[size]
        
        for bucket in reversed(buckets):
            if bucket["create_time"] <= current_time - N:
                buckets.remove(bucket)
            else:
                break
        
                
if ( __name__ == "__main__"):

    #get into the while loop
    one_bit="0"
    while one_bit=="0" or one_bit=="1":
        #read a bit
        one_bit=steamInput.read(1)
        current_time+=1
        create_time=current_time
        timestamp=create_time%N
        
        #if 0 read another bit
        if one_bit != "0" and one_bit !="1":
            continue        
        elif one_bit == "1":
            #create size 1 bucket
            bucket = {"size":1, "create_time":create_time, "timestamp":timestamp}
                        
            #put the new bucket size 1 buckets                      
            buckets_by_size_dict[1].append(bucket)
        
        print "@",current_time
        output.write("@"+str(current_time)+":")
         
        maintain_buckets()
        print_buckets()
        count_one()
    
    output.close()
        
    