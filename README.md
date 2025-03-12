# software-architecture-lab3

### Step: 1
After running all services, we send 10 messages using HTTP POST requests to the facade-service.
<img src="images/1.png">

### Step: 2
The messages are distributed randomly among the available logging-service instances.
<img src="images/2.png">

### Step: 3
In the Management Center, we can see that all messages are distributed across three different Hazelcast maps.
<img src="images/3.png">

### Step: 4
If we terminate one logging-service instance, the system rebalance the map, ensuring no data loss.
<img src="images/4.png">

### Step: 5
Next, we terminate two logging-service instances at once.
<img src="images/5.png">

### Step: 6
As a result, we can observe visible data loss.
<img src="images/6.png">