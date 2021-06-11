# CS172_final

## Team member 1 - Xianghu Wang
## Team member 2 - Chengyue Lin  


How to run our code: we use Python 3.9 version. 


The crawler is done by Xianghu Wang. The elasticsearch part is done by Chengyue Lin.    
And both of us work together to finish the extension part.
            

Part 1:    
First, we define a search linkQuence. It contains two list store visited and unvisited sites list respectively.   
Then we use BFS search strategy to crawl the sites from the URL seed.    
The following step is: 
1. we pop out one URL from unvisited sites list.   
2. use beautifulsoup to get hyperlink and content from the step 1 URL link     
3. Put the URL into the URL that has been accessed   
4. push the hyperlink from step 2 into the unvisited list 
5. repeat step 1 to 4 until get the number of sites you want. 

Part 2:   

For the elasticsearch part, we use the local machine to run it. We create and set up the index.  
And we put the data (.json) file into the elasticsearch. User can input what query they want to search inside our index.  
We just write a match function to find which URL is match with query.   

Part 3:   
For the extension part, we implement the multi-threaded crawler. We create a thread for writing the data into function.    
Specifically, we write a function writeData to listen the data queue. Once there is a data write into data queue, it will write to the local file (data.json).    
Then we create threading pool for the main crawler function.

