# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""
import numpy as np
import random
from scipy import stats

class RTLearner(object):  		  	   		   	 		  		  		    	 		 		   		 		  
   	  	   		   	 		  		  		    	 		 		   		 		  
     		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size = 5, verbose=False):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   	
        self.leaf_size = leaf_size
        self.verbose = verbose		  		  		    	 		 		   		 		  
        pass  	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(self, data_x, data_y):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		   	 		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		   	 		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """  
        
        #####Taking care of cases that lead to leaf formation 
        
        if data_x.shape[0] <= self.leaf_size:
            #return np.array([-1,np.mean(data_y),-1,-1])
            return np.array([-1,stats.mode(data_y)[0],-1,-1])
        
        elif np.all(data_y ==data_y[0]):
            return np.array([-1,data_y[0],-1,-1])
        
        elif np.all(data_x== data_x[0,:]):
             return np.array([-1,data_y[0],-1,-1])
          			 		  		  		    	 		 		   		 		  
                
        
        else:
              ####using correlation to find splitfeature and value      
            
            cols = data_x.shape[1]-1
            
            splitfeature = random.randint(0,cols)
            
            splitval = np.median(data_x[:,splitfeature])
            if np.all(data_x[:,splitfeature]<=splitval) ==True or np.all(data_x[:,splitfeature]>splitval) ==True:
                #return np.array([-1,np.mean(data_y),-1,-1])
                return np.array([-1,stats.mode(data_y)[0],-1,-1])
            else:
                   ####building decision tree         
        
                lefttree = self.add_evidence(data_x[data_x[:,splitfeature] <= splitval],data_y[data_x[:,splitfeature]<= splitval])
                righttree = self.add_evidence(data_x[data_x[:,splitfeature] > splitval],data_y[data_x[:,splitfeature] > splitval])
                
                if lefttree.shape[0] == lefttree.size:    
                    root = [splitfeature, splitval, 1, 2]
                else:
                    root = [splitfeature, splitval, 1, lefttree.shape[0]+1]
                    
                self.tree = np.vstack((root,lefttree,righttree))
                return self.tree
            
     #####going down the tree recursively for each point in xtest to find prediction     
    def query(self, xtest):
        self.ytest = np.empty((xtest.shape[0]))
        for i in range(0,len(xtest)):
            dat = xtest[i]
            self.ytest[i] = self.query_datapt(dat,0)
           
        return self.ytest    
    
    def query_datapt(self, dat, row=0):
                
        node = self.tree[row,0]
        node = int(node)
        splitval = self.tree[row,1]
        
        if node == -1:
            return splitval
        
        elif dat[node] <= splitval:
            return self.query_datapt(dat, row + int(self.tree[row,2]))
        
        else:
            return self.query_datapt(dat, row + int(self.tree[row,3]))
    