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

- id
- first_name
- last_name
- email
- phone
- mobile
- company_name
- date_created
- date_updated
- sales_contact

### contract

- id
- sales_contact
- customer
- date_created
- date_updated
- status
- amount
- payment_due

### event

- id
- customer
- date_created
- date_updated
- support_contact
- event_status
- attendees
- event_date
- notes

# team

- id
- first_name
- last_name
- email
- password
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