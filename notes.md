### Description of global variables
#### On Leader Node
1. nextIndex[followerId] - Index of the log on the followerId node for which leader will be sending the data
2. matchIndex[followerId] - Logs on the followerId node and leader completely match till matchIndex[followerId]. Note matchIndex[followerId] = nextIndex[followerId-1]
3. mayBeNeedToCommit - A follower just entered some entries into its log. So some log entries may now be present in majority of nodes. Check if this is the case and commit the entries that got majority.

#### On All Nodes
1. commitIndex - Logs from index 0 to commitIndex - 1 are committed, i.e., they are present in majority of the nodes.
2. 

### Function Definitions
1. replyAppendEntries(term, followerId, entriesToAppend, success)
	entriesToAppend - If success is True, it is the number of entries appended by the followerId node else it is the rightmost entry which is known to be a mismatch.
2.


### Function Preconditions
1. 




### Pointers
1. For starting election timeout, use electionTimeCall = False, shift = True

2. 



### Properties
1. Time is divided into terms. Term is divided into election and normal execution period. Election results in atmost one node to be elected leader. All requests goes through leader. The leader log is the truth. Every other node's log should match leader's log. 
2. Since leader's log is the truth, ensure that the future leaders contains the committed entries by the leader otherwise the current leaders committed entries will be lost. As soon as a entry is committed, it is passed to the state machine, and result from state machine is returned to the client. Hence client will get the wrong result if this property is not satisfied.
3. A entry will present in the log only because of a leader. Leader is identified by a term. Leader writes only one entry at a index. Therefore if (term, index) matches the entry should match across nodes.
4. A follower accepts the entry from leader only if the entry prior to proposed entry matches to that of leader node. This is a induction step and ensures that follower log matches entirely with the leader log. A entry is in majority only if majority of the nodes has the same log data till that entry.
5. 


### Rules
#### Commitment Rules 
* [!Raft Video](https://www.youtube.com/watch?v=YbZ3zDzDnrw) at 36:01
For a leader to decide an entry is committed:
* Must be stored on a majority of servers
* At least one new entry fro leader's term ust also be stored on majority of servers

### Doubts
1. 



