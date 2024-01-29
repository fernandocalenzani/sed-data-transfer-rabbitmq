import * as crypto from 'crypto';

function encrypt(message, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cfb', Buffer.from(key), iv);

    const encrypted = Buffer.concat([iv, cipher.update(message, 'utf-8'), cipher.final()]);

    return encrypted.toString('base64');
}

function decrypt(ciphertext, key) {
    const encryptedText = Buffer.from(ciphertext, 'base64');
    const iv = encryptedText.slice(0, 16);
    const decipher = crypto.createDecipheriv('aes-256-cfb', Buffer.from(key), iv);

    const decrypted = Buffer.concat([decipher.update(encryptedText.slice(16)), decipher.final()]);

    return decrypted.toString('utf-8');
}

// Exemplo de uso
const key = "chave-secreta";
const textoOriginal = "Hello, World!";

const textoCifrado = encrypt(textoOriginal, key);
console.log("Texto cifrado:", textoCifrado);

const textoDecifrado = decrypt(textoCifrado, key);
console.log("Texto decifrado:", textoDecifrado);
