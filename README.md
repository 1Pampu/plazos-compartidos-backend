# Fixed-Term Shared Deposits

## Description

Fixed-Term Shared Deposits is a comprehensive backend system designed to manage fixed-term deposit accounts. It provides a robust API for creating, updating, and retrieving deposit information, calculating daily interest rates, and handling user authentication and authorization.

The system is built using Django REST Framework for the backend logic and API, MySQL for database management, Docker for deployment, and GitHub Actions for continuous integration and deployment. Daily interest calculations are automated using Supercronic, ensuring accurate and timely updates to deposit accounts.

## API Reference

### Authentication

#### Usage
To access the API, you need to include a header with the name "Authorization" in each request with a Bearer token.

| Header       | Type     | Description                |
| :----------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Bearer token for authentication. |

#### Register
```http
  POST /api/register
```

| Parameter   | Type     | Description                |
| :--------   | :------- | :------------------------- |
| `username`  | `string` | **Required**.  User's username. |
| `email`     | `string` | **Required**. User's email address. |
| `password`  | `string` | **Required**. User's password.  |
| `password2` | `string` | **Required**. Confirmation of password. |

#### Login

```http
  POST /api/login
```

| Parameter | Type     | Description                         |
| :-------- | :------- | :-------------------------          |
| `email`   | `string` | **Required**. User's email address. |
| `password`| `string` | **Required**. User's password.      |

### Plazos

#### Create Plazo

```http
  POST /api/plazos
```

| Parameter  | Type     | Description                                             |
| :--------- | :------- | :------------------------------------------------------ |
| `interes`  | `float`  | **Required**. Daily interest rate percentage given.     |
| `titulo`   | `string` | **Required**. Identifier.                               |
| `dia`      | `integer`| **Required**. The day of the month the term starts.     |

#### Modify Plazo

```http
  PATCH /api/plazos/${plazo_id}
```

| Parameter  | Type     | Description                                             |
| :--------- | :------- | :------------------------------------------------------ |
| `interes`  | `float`  | **Optional**. Daily interest rate percentage given.     |
| `titulo`   | `string` | **Optional**. Identifier.                               |
| `dia`      | `integer`| **Optional**. The day of the month the term starts.     |

#### Get All Plazos

```http
  GET /api/plazos
```

#### Get Plazo

```http
  GET /api/plazos/${plazo_id}
```

#### Delete Plazo

```http
  DELETE /api/plazos/${plazo_id}
```

### Entidades

#### Create Entidad

```http
  POST /api/plazos/${plazo_id}/entidades
```

| Parameter  | Type     | Description                                             |
| :--------- | :------- | :------------------------------------------------------ |
| `nombre`   | `string` | **Required**. Name of the entity or participant.        |


#### Modify Entidad

```http
  PATCH /api/plazos/${plazo_id}/entidades/${entidad_id}
```

| Parameter  | Type     | Description                                             |
| :--------- | :------- | :------------------------------------------------------ |
| `nombre`   | `string` | **Required**. Name of the entity or participant.        |

#### Get All Entidades

```http
  GET /api/plazos/${plazo_id}/entidades
```

#### Get Entidad

```http
  GET /api/plazos/${plazo_id}/entidades/${entidad_id}
```

#### Delete Entidad

```http
  DELETE /api/plazos/${plazo_id}/entidades/${entidad_id}
```

### Transactions

#### Create Transactions

```http
  POST /api/plazos/${plazo_id}/operaciones
```
| Parameter | Type     | Description                                                                                              |
| :-------- | :------- | :------------------------------------------------------------------------------------------------------- |
| `fecha`   | `date`   | **Required**. Date of the transaction. Cannot be earlier than an existing transaction date or in the future. |
| `monto`   | `float`  | **Required**. Amount of the transaction.                                                                 |
| `tipo`    | `string` | **Required**. Type of the transaction: either "Deposito" or "Retiro".                                    |

#### Get All Transactions
```http
  GET /api/plazos/${plazo_id}/operaciones
```

#### Get Entity's Transactions
```http
  GET /api/plazos/${plazo_id}/operaciones/${entidad_id}
```

## Technologies used:

* **Django REST Framework**: Used for the entire backend, including the application logic and the API.
* **MySQL**: Relational database management system used for storing and managing data.
* **Docker**: Used for deployment, ensuring the application runs consistently across different environments.
* **GitHub Actions**: Automation platform used to automatically deploy the application on an Ubuntu server in a Docker container and upload the Dockerfile.
* **Supercronic**: Used to schedule daily interest calculations at midnight.


## Demo

API URL: https://server-martin.duckdns.org:8888

Working App with a Visual Interface: [Live Preview](https://1pampu.github.io/plazos-compartidos-frontend/index.html)

Repository of the FrontEnd: [Repository](https://github.com/1Pampu/plazos-compartidos-frontend)


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://1pampu.github.io/my-portfolio/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/martin-piampiani/)
