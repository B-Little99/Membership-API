from passlib.hash import pbkdf2_sha256

class PasswordHashing():
    # This function hashes the password based on the SHA-256 algorithm
    def hashPassword(password):
        password = str(password)
        newPassword = pbkdf2_sha256.hash(password)
        return newPassword

    # This function verifies the hashed password with the input password
    def verifyHash(hashedPassword, inputPassword):
        verification = pbkdf2_sha256.verify(inputPassword, hashedPassword)
        return verification