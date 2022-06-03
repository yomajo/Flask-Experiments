# Flask Isolated Experiments
Flask App with different experiments on different routes

*Tailored for PostgreSQL*. Login credentials in personal `.env`

Currently in menu:

### Products CRUD

`/products` - basic GET, POST, PUT, DELETE



### Products CRUD

`/users` - flask-login, to register, login users and based on `clearance` level allow / disallow to access certain routes.

See `required_clearance` decorator for role-based access control.


