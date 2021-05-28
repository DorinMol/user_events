# User Events App

![](https://img.shields.io/badge/fastAPI-python-red)

In order to play around with python and fastAPI, i made this small rest api application. The functionality behind is as usual... user crud, events crud and user authentication. Also added another layer of privilegees using roles (admin & user)

---

**Ussage**

- Clone the project
- Use **pip** to install **pipenv**
- Inside the root of the project run **pipenv install** ( this will read the **Pipfile** and create an environment, install dependencies)
- Duplicate **.env.example** file and add your database and other app configs
- To start ( outside of environment - **pipenv run uvicorn main:app --reload**)
- I think that's all

---

Inside the repo there is a **.http** file where you can check all crud operations that i've used for tests.

As for the database layer i've used **postgres**.

---

### Alembic for managing migrations

[Alembic docs](https://alembic.sqlalchemy.org/)

[Also very helpfull tutorial here](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)
