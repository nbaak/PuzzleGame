# creates and maintains secrets
import uuid
import os


def create_secret(file:str) -> str:
    secret = str(uuid.uuid4())

    with open(file, 'w') as f:
        f.write(secret)

    return secret


def get_secret(file:str) -> str:
    if not os.path.exists(file):
        return create_secret(file)
    else:
        with open(file, 'r') as f:
            return f.read()


def verify(possible_secret:str, file:str) -> bool:
    return possible_secret == get_secret(file)


def test():
    secret = get_secret('./secret')
    print(secret)
    print(verify(secret, './secret'))
    print(verify('secret', './secret'))


if __name__ == "__main__":
    test()
