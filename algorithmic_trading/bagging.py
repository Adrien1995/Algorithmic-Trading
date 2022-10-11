# -*- coding: utf-8 -*-
"""

@author: AdrienAntoinette
"""

import numpy as np 

import random 

class BagLearner(object):
    
    def __init__(self, learner, kwargs = {}, bags = 10, boost = False, verbose=False):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   	
        #self.leaf_size = leaf_size
        self.verbose = verbose
        #self.learner =  
        self.bags = bags
        self.learners = []  
        #kwargs = {"k":10}  
        
        for i in range(0,self.bags):  
            self.learners.append(learner(**kwargs)) 		  		    	 		 		   		 		  
        pass  # move along, these aren't the drones you're looking for  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    
    
    ######sample selection with replacement and training each learner in our bags 
    def add_evidence(self, data_x, data_y):
        mods = []
        
        #shuffle_x = np.take(ftrain,np.random.permutation(ftrain.shape[0]),axis=0)
        for i in self.learners:
            #perm = np.arange(data_x.shape[0])
            #perm2 = np.random.shuffle(perm)
            
            perm_ind = np.random.choice(data_x.shape[0], size=data_x.shape[0],replace=True)
            newx = data_x[perm_ind,:]
            newy = data_y[perm_ind]
            
            b = i.add_evidence(newx, newy)
            mods.append(b)
        return np.array(mods)
            #####querying each learner in our bags and taking the mean of their predicitons
    def query(self, xtest):
        ensemble = []
        for i in self.learners:
            a = i.query(xtest)
            ensemble.append(a)
        ensemble = np.mean(ensemble, axis=0)
        return np.array(ensemble)
        
                
            
            
        
        
    
    
    