# Step 1: Let's do a Conceptual Data Model (CDM)

## Looking for 'concepts'

- customers
- contracts
- events
- team

## Looking for 'associations'

- a contract is SIGNED with a customer
- an event is CREATED when a contract is SIGNED
- a team member is ASSOCIATED to an event when the event is CREATED
 ES

## UML

### customer

- id: (primary key - autoincrement)
- first_name: (CharField(max_length=25))
- last_name: (CharField(max_length=25))
- email: (EmailField(max_length=254))
- phone: (CharField(max_length=20))
- mobile: (CharField(max_length=20))
- company_name: (CharField(max_length=100))
- date_created: (DateTimeField(auto_now_add=True))
- date_updated: (DateTimeField(auto_now=True))

FK: Team -> sales_contact_id
- sales_contact: (ForeignKey(team) / int)


### contract

- id: (primary key - autoincrement)
- project_name: (CharField(max_length=100))
- signed: (BooleanField(default=False))
- amount: (DecimalField(max_digits=10, decimal_places=2))
- payment_due_date: (DateField())
- date_created: (DateTimeField(auto_now_add=True))
- date_updated: (DateTimeField(auto_now=True))

FK customer -> customer_id
- customer: (ForeignKey(customer) / int)
- sales_contact: (ForeignKey(team) / int)


### event

- id (primary key - autoincrement)
- event_name: (CharField(max_length=100))
- event_date: (DateField())
- attendees: (IntegerField())
- notes: (TextField())  
- date_created: (DateTimeField(auto_now_add=True))
- date_updated: (DateTimeField(auto_now=True))

FK customer -> customer_id
- customer: (ForeignKey(customer) / int)
- support_contact: (ForeignKey(team) / int)
- event_status: (ForeignKey(event) / int)

# team

- id (primary key / int)
- username (CharField(max_length=50))
- first_name (CharField(max_length=25))
- last_name (varchar(25))
- email (varchar(100))
- password (varchar(100))
- role
    * sales = read_only(customers, contracts, events)
        * CRU on customers and contracts
        * C on events
        * modify/access to customers they are responsible of + contracts & events
    * support = read_only(customers, contracts, events)
        * CRU on his events
        * R on customers associated to the event
        * modify/access to events they are responsible of
    * management = CRUD on team, customers, contracts, events
        * add a team in support to manage an event
