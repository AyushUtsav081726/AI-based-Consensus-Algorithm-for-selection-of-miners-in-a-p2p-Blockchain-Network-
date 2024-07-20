# Python Blockchain Code

## Requirments :

- Windows 8 or Higher
- Python Version 3.6 or Higher
- pipenv installed

## How to setup :

1. Open Terminal
2. Install pipenv [ Optional: Only if pipenv doesnt exist ]

```
pip install pipenv
```

3. Installing all Required Dependencies
```
pipenv install
```

4. Setup is done

## Executing the Software:

The Project works basically on api interface only hence **POSTMAN** is required to execute POST and GET request

### List of API Endpoints:

- Here **port** is depending on the selected **port** to run the server by default is set to **5000**

### GET

```
1. http://127.0.0.1:{port}/validate
2. http://127.0.0.1:{port}/chain
3. http://127.0.0.1:{port}/nodes/staker
4. http://127.0.0.1:{port}/stakerdetails
4. http://127.0.0.1:{port}/savetocsv
```

### POST [ NEED TO USE POSTMAN FOR THIS ]
### Optional [ Data for each Transaction is set as Default ]
```
1. http://127.0.0.1:{port}/transactions/new JSON-data-input : { sender, recipent, amount }
```

### TUTORIAL ON EXECUTION

**Disclaimer:** *The code is not optimized properly and errors are prone to occur time to time. To excute error free do follow the below steps carefully. To restart the system just turn off all the Terminal Servers that are executing* **Crtl+C** 

- All servers that are running in each terminal must be of different **ports**
- Each **port** also automatically acts as a **Staker**
- This simulation uses TEST data for transactions and doesnt track the BALANCE of any user 

### STEPS:

### Step 1: ( Starting with 1 Server )

- Switching on the Server on the Terminal
- Open a terminal and run the below command to begin 
```
python blockchain.py
```

- By default it will start a **localhost** server at **port 5000**
```
https://127.0.0.1:5000
```
- The above URL is the where the server is running, the above URL has no output response when opened [ Yet to Build ]

### Step 2: ( Running more Servers/Stakers )

- Type below each of these in different Terminals:
```
python blockchain.py --port 5002
python blockchain.py --port 5003
python blockchain.py --port 5004
python blockchain.py --port 5005
```

- Now we are running multiple servers as to have more stakers 
```
https://127.0.0.1:5002
https://127.0.0.1:5003
https://127.0.0.1:5004
https://127.0.0.1:5005
```

-*Warning:* *Due to some unoptimal code **port: 5001** and **port: 6001** have issues and please avoide using these ports for now*

- Now we have almost 5 Servers running as stakers

### Step 3: ( Check the chain for respective Stakers/Servers )

### Try this in postman or browser

### PORT: 5000
```
http://127.0.0.1:5000/chain
```
```
{
    "chain": [
        {
            "index": 1,
            "previous_hash": "1",
            "proof": 100,
            "timestamp": 1622716895.7398086,
            "transactions": []
        }
    ],
    "length": 1
}
```

### PORT: 5002
```
http://127.0.0.1:5002/chain
```
```
{
    "chain": [
        {
            "index": 1,
            "previous_hash": "1",
            "proof": 100,
            "timestamp": 1622716895.7398086,
            "transactions": []
        }
    ],
    "length": 1
}
```
- Both chains will be same size but different as they havent compared with each other yet

### Step 4: ( Finding the Validator )

- Now we have to find a validator to execute the transaction
- Right now POS is running where a Staker is randomly picked for first 50 Blocks
- Then on only the early Stakers who joined before 50 blocks will be added to Kmeans Algorithm to continue finding new Stakers
- Data of total number of blocks validated is saved in the blockchain 

- To execute the validation process follow the below code in same terminal
- Important to note the **port:5000** as thats where the transaction occured

```
http://127.0.0.1:5000/validate
```

- This will search for the validator and allow them to validate the transaction to the respective Block Number

```
{
    "index": 2,
    "message": "New Block Forged",
    "previous_hash": "9f0d2919fde6fe2f0bd1e67063a84dafd68bbf73c4aa5ad6d11b12bb8f116c5c",
    "proof": 24536,
    "transactions": [
            {
            "amount": 1,
            "recipient": "ccbb1563ab2b45c294f63012b2c05f22",
            "sender": "0"
            }
        ],
    "validator": "127.0.0.1:5000"
}
```

- The above details would be different since its genrated randomly
- In the above example **Validator is port:5000**

### Step 5: ( Checking chains of stakers/servers )

- Now we will check the blockchain of selected servers

```
http://127.0.0.1:5002/chain
http://127.0.0.1:5000/chain
```

- Here **port:5002** chain is longer than **port:5000**
- Hence the consenses will have to roleout the longer blockchain to others in network

### Step 6: ( Storing Blockchain Data as a CSV file )

```
http://127.0.0.1:5000/savetocsv
```

- In the Folder you will see a new file called "Blockchain_Dataset.csv" which will contain all Stakers details from the Blockchain system


## Any issues do contact me on whatsapp or email 
