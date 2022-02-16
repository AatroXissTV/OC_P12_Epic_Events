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

- id (primary key / int)
- first_name (varchar(25))
- last_name (varchar(25))
- email (varchar(100))
- phone (varchar(20))
- mobile (varchar(20))
- company_name (varchar(250))
- date_created (DateTime)
- date_updated (DateTime)
- sales_contact (ForeignKey(team) / int)

### contract

- id (primary key / int)
- sales_contact (ForeignKey(team) / int)
- customer (ForeignKey(customer) / int)
- date_created (DateTime)
- date_updated (DateTime)
- status (boolean)
- amount (Float)
- payment_due (DateTime)

### event

- id (primary key / int)
- customer (ForeignKey(customer) / int)
- date_created (DateTime)
- date_updated (DateTime)
- support_contact (ForeignKey(team) / int)
- event_status (ForeignKey(event) / int)
- attendees (int)
- event_date (DateTime)
- notes (varchar(1000))

# team

- id (primary key / int)
- first_name (varchar(25))
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